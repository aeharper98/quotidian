"""Synthesise Quotidian's beats from scratch (no samples, so we own 100% of the audio).

Every beat is a full ARRANGEMENT that loops seamlessly (tails and reverb wrap around):
  A (8) > A2 (8) > BREAK (4) > BUILD (4, ends in a one-beat gap) > DROP (8) > SWITCH (8) > STRIP (4) > A2 (4)
with section volume moves, fills every 4 and 8 bars, crashes on the drops.

Each beat renders:
  <id>_intro.mp3  - 2 filtered bars + riser, played once before the first drop
  <id>_loop.mp3   - the 48-bar arrangement, padded 1 s each side; loop frames [loopStartFrame, +loopFrames)
  previews/<id>_preview.mp3 - intro + loop once, for listening
beats.json carries bpm/bar length and the section map so the app can react to drops.
"""
import json
import os
import subprocess
import sys

import numpy as np

SR = 44100
OUT = sys.argv[1] if len(sys.argv) > 1 else "beats"
PREV = sys.argv[2] if len(sys.argv) > 2 else "previews"
ONLY = sys.argv[3].split(",") if len(sys.argv) > 3 else None
rng = np.random.default_rng(7)

SECTIONS = [("A", 0, 8), ("A2", 8, 8), ("BREAK", 16, 4), ("BUILD", 20, 4),
            ("DROP", 24, 8), ("SWITCH", 32, 8), ("STRIP", 40, 4), ("A2", 44, 4)]
TOTAL = 48
LOOP_PAD = SR  # 1 second of wrap-around padding either side of the encoded loop


def section(b):
    for name, s, n in SECTIONS:
        if s <= b < s + n:
            return name, b - s, n
    raise ValueError(b)


# ---------------------------------------------------------------- dsp helpers
def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(dur):
    return np.arange(max(1, int(dur * SR))) / SR


def spectral(x, lo=0.0, hi=SR / 2, order=4):
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    m = np.ones_like(f)
    if lo > 0:
        m *= 1 / (1 + (lo / np.maximum(f, 1)) ** order)
    if hi < SR / 2:
        m *= 1 / (1 + (f / hi) ** order)
    return np.fft.irfft(X * m, n)


def noise(dur):
    return rng.uniform(-1, 1, max(1, int(dur * SR)))


def fade_tail(x, ms=8):
    k = min(len(x), int(SR * ms / 1000))
    if k > 0:
        x[-k:] *= np.linspace(1, 0, k)
    return x


def env_ar(t, a, dur, rel):
    e = np.minimum(t / max(a, 1e-4), 1)
    return e * np.where(t > dur, np.exp(-(t - dur) * rel), 1.0)


# ---------------------------------------------------------------- buses
class Bus:
    def __init__(self, n, wrap):
        self.n, self.wrap = n, wrap
        self.buf = np.zeros((2, n))

    def add(self, sig, at, gain=1.0, pan=0.0):
        if gain <= 0:
            return
        s = int(round(at * SR)) % self.n if self.wrap else int(round(at * SR))
        L = gain * np.sqrt(0.5 * (1 - pan))
        R = gain * np.sqrt(0.5 * (1 + pan))
        sig = sig[: self.n]
        first = min(len(sig), self.n - s)
        if first > 0:
            self.buf[0, s:s + first] += sig[:first] * L
            self.buf[1, s:s + first] += sig[:first] * R
        rest = len(sig) - max(first, 0)
        if self.wrap and rest > 0:
            self.buf[0, :rest] += sig[first:] * L
            self.buf[1, :rest] += sig[first:] * R


class Mix:
    """dry, wet (reverb send), filt (low-passed, for breakdowns/builds), pump (side-chained to kicks)."""

    def __init__(self, seconds, wrap, sidechain=0.0):
        n = int(round(seconds * SR))
        self.n, self.wrap, self.sc = n, wrap, sidechain
        self.dry, self.wet, self.filt, self.pump = (Bus(n, wrap) for _ in range(4))
        self.kicks = []

    def music(self, sec, i, n, pump=False):
        """Router for melodic parts: filtered in BREAK, filter opening across BUILD."""
        main = self.pump if pump else self.dry

        def add(sig, at, gain=1.0, pan=0.0, send=0.0):
            if sec == "BREAK":
                self.filt.add(sig, at, gain, pan)
            elif sec == "BUILD":
                p = (i + 1) / (n + 1)
                self.filt.add(sig, at, gain * (1 - p), pan)
                main.add(sig, at, gain * p, pan)
            else:
                main.add(sig, at, gain, pan)
            if send:
                self.wet.add(sig, at, gain * send, pan)
        return add

    def kick(self, sig, at, gain=1.0):
        self.dry.add(sig, at, gain)
        self.kicks.append(at)

    def render(self, filt_hz=700):
        out = self.dry.buf.copy()
        out += np.vstack([spectral(self.filt.buf[c], 0, filt_hz) for c in range(2)])
        if self.sc > 0 and self.kicks:
            curve = np.ones(self.n)
            win = tt(0.35)
            duck = 1 - self.sc * np.exp(-win / 0.09)
            for k in self.kicks:
                s = int(k * SR) % self.n
                e = min(self.n, s + len(win))
                curve[s:e] = np.minimum(curve[s:e], duck[: e - s])
                if self.wrap and s + len(win) > self.n:
                    r = s + len(win) - self.n
                    curve[:r] = np.minimum(curve[:r], duck[len(win) - r:])
            out += self.pump.buf * curve
        else:
            out += self.pump.buf
        out += reverb(self.wet.buf, self.wrap)
        return out


def reverb(buf, wrap, seconds=1.8, damp=4500):
    n = buf.shape[1]
    out = np.zeros_like(buf)
    for ch in range(2):
        ir = noise(seconds) * np.exp(-tt(seconds) * 4.0)
        ir = spectral(ir, 250, damp)
        ir /= np.sqrt(np.sum(ir ** 2)) * 6
        if wrap:
            irp = np.zeros(n)
            irp[: min(len(ir), n)] = ir[:n]
            out[ch] = np.fft.irfft(np.fft.rfft(buf[ch]) * np.fft.rfft(irp), n)
        else:
            L = n + len(ir)
            out[ch] = np.fft.irfft(np.fft.rfft(buf[ch], L) * np.fft.rfft(ir, L), L)[:n]
    return out


# target level of each section relative to A, in dB (the arrangement's dynamics)
TARGET_DB = {"A": 0.0, "A2": 1.0, "BREAK": -8.0, "BUILD": -2.0, "DROP": 2.0, "SWITCH": 0.0, "STRIP": -2.0}


def gain_curve(x, bar):
    """Measure each section, then set it to its target level. BUILD ramps up and its last beat is cut (the gap)."""
    n = x.shape[1]
    lvl = {}
    for name, s0, ln in SECTIONS:
        seg = x[:, int(s0 * bar * SR):int((s0 + ln) * bar * SR)]
        lvl.setdefault(name, []).append(np.sqrt(np.mean(seg ** 2)) + 1e-9)
    ref = np.mean(lvl["A"])
    g = np.ones(n)
    for b in range(TOTAL):
        sec, i, ln = section(b)
        want = ref * 10 ** (TARGET_DB[sec] / 20)
        base = float(np.clip(want / np.mean(lvl[sec]), 0.4, 4.0))
        s, e = int(b * bar * SR), min(n, int((b + 1) * bar * SR))
        if sec == "BUILD":
            g[s:e] = base * np.linspace(0.7 + 0.3 * i / ln, 0.7 + 0.3 * (i + 1) / ln, e - s)
            if i == ln - 1:
                g[s + int(0.75 * bar * SR):e] = 0.06
        else:
            g[s:e] = base
    k = int(0.03 * SR)  # 30 ms smoothing, circular
    c = np.concatenate([g[-k:], g, g[:k]])
    cs = np.cumsum(np.insert(c, 0, 0))
    return (cs[2 * k:] - cs[:-2 * k])[:n] / (2 * k)


# ---------------------------------------------------------------- drums
def kick(f0=150, f1=48, decay=6.0, dur=0.6, drive=1.6):
    t = tt(dur)
    f = f1 + (f0 - f1) * np.exp(-t * 32)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay)
    click = spectral(noise(dur), 1500, 9000) * np.exp(-t * 300) * 0.5
    return fade_tail(np.tanh((body + click) * drive) * 0.9)


def snare(tone=185, dur=0.35, bright=7000):
    t = tt(dur)
    body = np.sin(2 * np.pi * tone * t) * np.exp(-t * 22) * 0.55
    rattle = spectral(noise(dur), 1200, bright) * np.exp(-t * 15) * 1.1
    return fade_tail(np.tanh((body + rattle) * 1.3))


def clap(dur=0.4):
    t = tt(dur)
    env = np.exp(-t * 16)
    for off in (0.0, 0.011, 0.022):
        env += np.exp(-np.maximum(t - off, 0) * 180) * (t >= off) * 0.8
    return fade_tail(spectral(noise(dur), 900, 6000) * env * 0.9)


def hat(open_=False, vel=1.0):
    dur = 0.35 if open_ else 0.06
    t = tt(dur)
    return fade_tail(spectral(noise(dur), 7000, 16000) * np.exp(-t * (9 if open_ else 70)) * vel * 0.55)


def rim():
    t = tt(0.08)
    x = (np.sin(2 * np.pi * 1700 * t) * 0.6 + np.sin(2 * np.pi * 520 * t)) * np.exp(-t * 60)
    return fade_tail((x + spectral(noise(0.08), 2000, 9000) * np.exp(-t * 120) * 0.5) * 0.5)


def shaker(vel=1.0):
    t = tt(0.09)
    e = np.minimum(t / 0.012, 1) * np.exp(-t * 35)
    return fade_tail(spectral(noise(0.09), 5000, 13000) * e * vel * 0.35)


def crash():
    t = tt(2.2)
    x = spectral(noise(2.2), 4000, 15000) * np.exp(-t * 2.0)
    for r in (1, 1.41, 1.83, 2.37, 2.91):
        x += 0.05 * np.sin(2 * np.pi * 3200 * r * t) * np.exp(-t * 3)
    return fade_tail(x * 0.45, 50)


def ride(vel=1.0):
    t = tt(1.0)
    x = spectral(noise(1.0), 6000, 14000) * np.exp(-t * 6) * 0.4
    for r in (1, 1.34, 1.67, 2.13, 2.5):
        x += 0.12 * np.sin(2 * np.pi * 2900 * r * t) * np.exp(-t * 4)
    return fade_tail(x * vel * 0.35, 30)


def metal(base, decay=8.0, vel=1.0):
    """Struck-metal foley: inharmonic modes plus a clank."""
    t = tt(0.6)
    x = np.zeros_like(t)
    for r, a in ((1, 1), (2.76, 0.6), (5.40, 0.4), (8.93, 0.25), (13.34, 0.12)):
        if base * r < 16000:
            x += a * np.sin(2 * np.pi * base * r * t + rng.uniform(0, 6)) * np.exp(-t * decay * (1 + r * 0.15))
    x += spectral(noise(0.6), 1500, 7000) * np.exp(-t * 90) * 0.8
    return fade_tail(x * vel * 0.22, 20)


# ---------------------------------------------------------------- tonal
def additive(freq, dur, kind="square", cutoff=3000):
    t = tt(dur)
    x = np.zeros_like(t)
    n = 1
    while n * freq < min(cutoff, SR / 2 - 500):
        if kind == "square" and n % 2 == 1:
            x += np.sin(2 * np.pi * n * freq * t) / n
        elif kind == "saw":
            x += np.sin(2 * np.pi * n * freq * t) / n * (-1) ** (n + 1)
        n += 1
    return x


def pluck_square(m, dur, cutoff=2600):
    t = tt(dur + 0.05)
    return fade_tail(additive(mtof(m), dur + 0.05, "square", cutoff) * np.minimum(t / 0.003, 1) * np.exp(-t * 7) * 0.35)


def bass_square(m, dur, cutoff=700):
    t = tt(dur)
    x = additive(mtof(m), dur, "square", cutoff)
    return fade_tail(np.tanh(x * 1.5) * np.minimum(t / 0.005, 1) * np.exp(-t * 1.5) * 0.6, 12)


def sub808(segs, step, dur_total):
    out = np.zeros(int(dur_total * SR) + SR)
    for start, m, ln, slide in segs:
        t = tt(ln * step + 0.05)
        f_to = mtof(m)
        f = f_to + (mtof(slide) - f_to) * np.exp(-t * 28) if slide is not None else np.full_like(t, f_to)
        sig = np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * 2.6) * np.minimum(t / 0.004, 1) * np.exp(-t * 0.9) * 0.8
        sig = fade_tail(sig, 15)
        s = int(start * step * SR)
        out[s:s + len(sig)] += sig
    return out


def sub(m, dur):
    f = mtof(m)
    t = tt(dur)
    x = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(4 * np.pi * f * t)  # 2nd harmonic: audible on phones
    return fade_tail(np.tanh(x * 1.3) * np.minimum(t / 0.005, 1) * 0.6, 20)


def bass_guitar(m, dur, vel=1.0):
    f = mtof(m)
    t = tt(dur + 0.08)
    x = np.zeros_like(t)
    for n in range(1, 14):
        if n * f > 4000:
            break
        x += np.sin(2 * np.pi * n * f * t) / n ** 1.3 * np.exp(-t * (1.5 + n * 1.2))
    thump = np.zeros_like(t)
    k = min(len(t), int(0.015 * SR))
    thump[:k] = spectral(noise(0.015), 200, 2000)[:k] * np.linspace(1, 0, k) * 0.4
    x = np.tanh((x + thump) * 1.4) * env_ar(t, 0.003, dur, 25)
    return fade_tail(x * vel * 0.5, 10)


def rhodes(m, dur, vel=1.0):
    f = mtof(m)
    t = tt(dur + 0.6)
    x = (np.sin(2 * np.pi * f * t) + 0.35 * np.sin(4 * np.pi * f * t) * np.exp(-t * 4)
         + 0.12 * np.sin(2 * np.pi * 7.1 * f * t) * np.exp(-t * 18))
    return fade_tail(x * np.minimum(t / 0.006, 1) * np.exp(-t * 1.3) * env_ar(t, 1e-4, dur, 9) * 0.22 * vel)


def piano(m, dur, vel=1.0):
    f = mtof(m)
    t = tt(dur + 1.2)
    x = np.zeros_like(t)
    for n in range(1, 14):
        fn = n * f * np.sqrt(1 + 0.0004 * n * n)
        if fn > 11000:
            break
        x += (vel ** (0.3 * n)) / n ** 1.1 * np.sin(2 * np.pi * fn * t) * np.exp(-t * (0.9 + 0.5 * n))
    k = min(len(t), int(0.03 * SR))
    x[:k] += spectral(noise(0.03), 800, 5000)[:k] * np.exp(-tt(0.03)[:k] * 120) * 0.15 * vel
    return fade_tail(x * env_ar(t, 0.002, dur, 7) * 0.2 * vel, 30)


def bell(m, dur):
    f = mtof(m)
    t = tt(dur + 1.0)
    x = np.sin(2 * np.pi * f * t + 2.2 * np.exp(-t * 5) * np.sin(2 * np.pi * 3.5 * f * t)) + 0.3 * np.sin(np.pi * f * t)
    return fade_tail(x * np.minimum(t / 0.002, 1) * np.exp(-t * 2.2) * 0.28)


def pad(ms, dur, cutoff=1400):
    t = tt(dur + 0.5)
    x = np.zeros_like(t)
    for m in ms:
        for det in (-0.08, 0.0, 0.08):
            x += additive(mtof(m + det), dur + 0.5, "saw", cutoff)
    return fade_tail(x * env_ar(t, 0.35, dur, 5) * 0.035 / max(1, len(ms) / 3))


def brass(m, dur, swell=False, vel=1.0):
    """Horn-section voice: brightness opens with the attack like a real brass player."""
    f = mtof(m)
    t = tt(dur + 0.12)
    if swell:
        bright = 1.5 + 9 * np.minimum(t / max(dur, 0.1), 1) ** 1.5
        amp = np.minimum(t / max(dur * 0.8, 0.05), 1) ** 2
    else:
        bright = 2.5 + 10 * np.minimum(t / 0.03, 1) * np.exp(-t * 5)
        amp = np.minimum(t / 0.015, 1)
    vib = 0.004 * np.sin(2 * np.pi * 5.5 * t) * np.minimum(t / 0.3, 1)
    x = np.zeros_like(t)
    for det in (-0.06, 0.07):
        ph = 2 * np.pi * np.cumsum(f * 2 ** (det / 12) * (1 + vib)) / SR
        for n in range(1, 30):
            if n * f > 7000:
                break
            x += np.exp(-n / bright) / n * np.sin(n * ph)
    x = np.tanh(x * 1.2)
    return fade_tail(x * amp * env_ar(t, 1e-4, dur, 30) * 0.22 * vel, 15)


FORMANTS = {
    "a": [(800, 1.0), (1150, 0.5), (2900, 0.25)],
    "o": [(450, 1.0), (800, 0.45), (2830, 0.1)],
    "u": [(325, 1.0), (700, 0.3), (2530, 0.06)],
    "e": [(400, 1.0), (2000, 0.45), (2550, 0.3)],
    "i": [(290, 1.0), (2250, 0.35), (2900, 0.28)],
}


def voice(m, dur, vowel="a", attack=0.02, bend=0.0, breath=0.05, vib_depth=0.005):
    """Additive formant voice (no samples): harmonics weighted by vowel resonances."""
    f = mtof(m)
    t = tt(dur + 0.1)
    vib = vib_depth * np.sin(2 * np.pi * 5.2 * t) * np.minimum(t / 0.25, 1)
    fi = f * (1 - bend * np.exp(-t * 25)) * (1 + vib)
    ph = 2 * np.pi * np.cumsum(fi) / SR
    x = np.zeros_like(t)
    for n in range(1, 60):
        fn = n * f
        if fn > 5000:
            break
        w = sum(g * np.exp(-((fn - F) / (F * 0.18 + 60)) ** 2) for F, g in FORMANTS[vowel]) + 0.01
        x += w * np.sin(n * ph) / np.sqrt(n)
    x += spectral(noise(dur + 0.1), 1500, 6000)[: len(t)] * breath
    return fade_tail(x * env_ar(t, attack, dur, 40) * 0.25, 6)


def choir(ms, dur, vowel="u"):
    t_len = int((dur + 0.6) * SR)
    x = np.zeros(t_len)
    for m in ms:
        for det in (-0.1, 0.1):
            v = voice(m + det, dur + 0.5, vowel, attack=0.4, breath=0.02, vib_depth=0.007)
            x[: len(v)] += v[:t_len]
    t = tt(dur + 0.6)
    return fade_tail(x * env_ar(t, 0.4, dur, 3)[: len(x)] * 0.5 / len(ms), 40)


def riser(dur):
    t = tt(dur)
    x = noise(dur)
    p = (t / dur) ** 2
    return fade_tail((spectral(x, 300, 1500) * (1 - p) + spectral(x, 3000, 14000) * p) * p * 0.6, 3)


def crackle(seconds):
    n = int(seconds * SR)
    x = spectral(rng.normal(0, 1, n), 500, 6000) * 0.006
    pops = rng.random(n) < 0.00035
    x[pops] += rng.uniform(-0.08, 0.08, pops.sum())
    return x


def swing_t(i, step, amt):
    return i * step + (step * amt if i % 2 == 1 else 0)


def human(sd=0.006):
    return float(rng.normal(0, sd))


def snare_roll(mx, t0, step, from_step, to_step, per_step=1, gain=0.5, fn=snare):
    k = 0
    total = (to_step - from_step) * per_step
    for s in range(from_step, to_step):
        for j in range(per_step):
            mx.dry.add(fn(), t0 + (s + j / per_step) * step, gain * (0.4 + 0.6 * k / max(1, total)))
            k += 1


def common_build(mx, sec, i, n, t0, step, bar, kick_fn, snare_fn=snare):
    """Shared build-up: kicks on every beat, then 8ths, then a 16th snare roll, then the gap."""
    if i < n - 1:
        for s in range(0, 16, 4 if i < n - 2 else 2):
            mx.kick(kick_fn(), t0 + s * step, 0.55 + 0.1 * i)
    if i >= n - 2:
        per = 1 if i == n - 2 else 2
        snare_roll(mx, t0, step, 0, 12 if i == n - 1 else 16, per, 0.55, snare_fn)
    if i == n - 1:
        mx.dry.add(riser(bar * 0.75), t0, 0.5)


# ================================================================ beats
def build_eski(mx, step, bar, intro):
    riff = [(0, 77), (3, 77), (6, 75), (8, 72), (11, 72), (14, 70),
            (16, 68), (19, 68), (22, 70), (24, 72), (27, 75), (30, 72)]
    bassA = [(0, 29, 3), (3, 29, 2), (6, 41, 1), (8, 29, 4), (14, 32, 2),
             (16, 25, 3), (19, 25, 2), (22, 37, 1), (24, 27, 4), (30, 27, 2)]
    bassB = [(0, 29, 2), (2, 41, 1), (4, 29, 2), (8, 44, 1), (10, 41, 2), (13, 29, 3),
             (16, 25, 2), (18, 37, 1), (20, 25, 2), (24, 39, 1), (26, 27, 2), (29, 39, 3)]
    for b in range(2 if intro else TOTAL):
        sec, i, n = ("INTRO", b, 2) if intro else section(b)
        t0, half = b * bar, b % 2
        M = mx.music(sec, i, n)
        if sec != "STRIP" and not (sec == "SWITCH" and half == 1):
            up = 12 if sec == "DROP" and b % 4 >= 2 else 0
            for s, m in riff:
                if s // 16 == half:
                    M(pluck_square(m + up, step * 1.5), t0 + (s % 16) * step, 1.4, 0.25, 0.25)
        if sec in ("INTRO", "A2", "BREAK", "BUILD", "DROP"):
            chords = [([53, 56, 60], 0, bar)] if half == 0 else [([49, 53, 56], 0, bar / 2), ([51, 55, 58], 8, bar / 2)]
            for ms, s, d in chords:
                M(pad(ms, d), t0 + s * step, 0.8, -0.2, 0.4)
        if intro:
            continue
        if sec in ("A", "A2", "DROP", "SWITCH", "STRIP") or (sec == "BUILD" and i >= 2):
            for s, m, ln in (bassB if sec == "SWITCH" else bassA):
                if s // 16 == half:
                    M(bass_square(m, ln * step), t0 + (s % 16) * step, 0.75)
        if sec == "BREAK":
            continue
        if sec == "BUILD":
            common_build(mx, sec, i, n, t0, step, bar, kick)
            continue
        if i == 0 and sec in ("DROP", "SWITCH"):
            mx.dry.add(crash(), t0, 0.7)
        if sec == "SWITCH":
            kicks, claps = [0, 3, 6, 10], [4, 12]
        else:
            kicks, claps = ([0, 10] if b % 4 != 3 else [0, 7, 10]), [8]
        for s in kicks:
            mx.kick(kick(), t0 + s * step, 0.8)
        for s in claps:
            mx.dry.add(clap(), t0 + s * step, 0.8)
            mx.dry.add(snare(), t0 + s * step, 0.5)
            mx.wet.add(clap(), t0 + s * step, 0.3)
        hats = range(0, 16, 1 if sec == "DROP" else 2)
        for s in hats:
            mx.dry.add(hat(vel=1.0 if s % 4 == 0 else 0.6 if s % 2 == 0 else 0.35), t0 + s * step, 0.8, 0.3)
        if sec == "DROP" and half == 1:
            mx.dry.add(hat(True, 0.6), t0 + 14 * step, 0.7, 0.3)
        if (b + 1) % 8 == 0:
            snare_roll(mx, t0, step, 12, 16, 1, 0.6)
        elif (b + 1) % 4 == 0:
            for s in (13, 15):
                mx.dry.add(hat(vel=0.5), t0 + s * step, 0.8, 0.3)


def build_dusty(mx, step, bar, intro):
    prog = [(38, [53, 57, 60, 64]), (34, [57, 60, 62, 65]), (31, [58, 62, 65, 69]), (33, [55, 58, 61, 64])]
    sw = 0.17
    for b in range(2 if intro else TOTAL):
        sec, i, n = ("INTRO", b, 2) if intro else section(b)
        t0 = b * bar
        root, ch = prog[0] if intro else prog[(b // 2) % 4]
        M = mx.music(sec, i, n)
        if sec != "STRIP":
            if sec == "SWITCH":
                hits = [(0, 2.5)]
            else:
                hits = [(0, 1.6), (10, 0.6)] if b % 2 == 0 else [(0, 1.0), (6, 0.5), (11, 1.2)]
            for s, beats in hits:
                for m in ch:
                    M(rhodes(m, beats * 4 * step), t0 + swing_t(s, step, sw), 1.4, 0.15 * (m % 3 - 1), 0.35)
            if sec in ("A2", "DROP") and b % 2 == 1:
                for s, m in ((6, ch[-1] + 12), (14, ch[-2] + 12)):
                    M(rhodes(m, step * 3, 0.8), t0 + swing_t(s, step, sw), 1.0, 0.4, 0.5)
        if intro:
            continue
        if sec != "BREAK" or i >= 2:
            for s, m, ln in [(0, root, 6), (7, root, 2), (10, root + 7, 3), (14, root + 12, 2)]:
                M(bass_square(m, ln * step, 500), t0 + swing_t(s, step, sw), 0.65)
        bk = lambda: kick(f0=120, f1=52, decay=8, drive=2.0)
        if sec == "BREAK":
            for s in range(0, 16, 2):
                mx.dry.add(hat(vel=0.5), t0 + swing_t(s, step, sw), 0.6, -0.3)
            continue
        if sec == "BUILD":
            common_build(mx, sec, i, n, t0, step, bar, bk, lambda: snare(tone=200, bright=6000))
            continue
        if i == 0 and sec in ("DROP", "SWITCH"):
            mx.dry.add(crash(), t0, 0.55)
        kicks = ([0, 10] if sec == "SWITCH" else [0, 7, 10] if b % 2 == 0 else [0, 10, 13])
        for s in kicks:
            mx.kick(bk(), t0 + swing_t(s, step, sw), 0.8)
        for s in (4, 12):
            if sec == "SWITCH":
                mx.dry.add(rim(), t0 + s * step, 0.9)
            else:
                mx.dry.add(snare(tone=200, bright=6000), t0 + s * step, 0.9)
                mx.wet.add(snare(), t0 + s * step, 0.15)
        for s in range(0, 16, 2):
            mx.dry.add(hat(vel=0.9 if s % 4 == 0 else 0.55), t0 + swing_t(s, step, sw), 0.8, -0.3)
        for s in (3, 11):
            mx.dry.add(hat(vel=0.3), t0 + swing_t(s, step, sw), 0.8, -0.3)
        if sec == "DROP":
            for s in range(16):
                mx.dry.add(shaker(0.9 if s % 4 == 2 else 0.45), t0 + swing_t(s, step, sw), 0.8, 0.5)
        if (b + 1) % 8 == 0:
            snare_roll(mx, t0, step, 13, 16, 1, 0.5, lambda: snare(tone=200, bright=5000))
        elif (b + 1) % 4 == 0:
            mx.dry.add(snare(tone=200, bright=5000), t0 + swing_t(15, step, sw), 0.25)
    mx.dry.buf += crackle(mx.n / SR)


def build_midnight(mx, step, bar, intro):
    motif = [(0, 78), (3, 81), (6, 85), (10, 79), (12, 78), (16, 76), (19, 81), (22, 83), (26, 79), (28, 78)]
    motifB = [(0, 73), (3, 76), (6, 78), (8, 79), (12, 76), (16, 74), (19, 78), (22, 76), (24, 74), (28, 73)]
    b808A = [(0, 30, 6, None), (6, 30, 3, None), (10, 33, 4, 30), (14, 37, 2, 33),
             (16, 30, 6, 37), (22, 26, 4, 30), (26, 28, 3, None), (29, 30, 3, 28)]
    b808B = [(0, 30, 3, None), (3, 30, 3, None), (6, 25, 4, 30), (10, 28, 6, 25),
             (16, 30, 3, 28), (19, 33, 3, 30), (22, 35, 4, 33), (26, 30, 6, 35)]
    b808S = [(0, 30, 10, None), (16, 26, 8, None), (24, 28, 8, 26)]
    chords = [[54, 57, 61], [50, 54, 57]]
    for b in range(2 if intro else TOTAL):
        sec, i, n = ("INTRO", b, 2) if intro else section(b)
        t0, half = b * bar, b % 2
        M = mx.music(sec, i, n)
        if sec != "STRIP":
            mot = motifB if sec == "SWITCH" else motif
            for s, m in mot:
                if s // 16 == half:
                    up = 12 if (sec == "DROP" and b % 4 >= 2) else 0
                    M(bell(m + up, step * 2), t0 + (s % 16) * step, 1.2, -0.3, 0.45)
        if sec in ("INTRO", "A2", "BREAK", "BUILD", "DROP"):
            M(pad(chords[half], bar, cutoff=900), t0, 0.9, 0.2, 0.4)
        if intro:
            continue
        if half == 0 and (sec in ("A", "A2", "DROP", "SWITCH", "STRIP") or (sec == "BUILD" and i >= 1)):
            pat = b808B if sec == "SWITCH" else b808S if sec == "STRIP" else b808A
            M(sub808(pat, step, bar * 2)[: int(bar * 2 * SR)], t0, 0.7)
        if sec == "BREAK":
            continue
        if sec == "BUILD":
            for s in [0, 3, 6, 8, 10, 12, 14]:
                if not (i == n - 1 and s >= 12):
                    mx.dry.add(hat(vel=0.6), t0 + s * step, 0.75, 0.35)
            if i >= 2:
                mx.dry.add(snare(tone=210, bright=9000), t0 + 8 * step, 0.7)
            if i == n - 1:
                for j in range(12):
                    mx.dry.add(hat(vel=0.3 + 0.05 * j), t0 + 8 * step + j * (4 * step / 12) * 1.0, 0.75, 0.35)
                mx.dry.add(riser(bar * 0.75), t0, 0.5)
            continue
        if i == 0 and sec in ("DROP", "SWITCH"):
            mx.dry.add(crash(), t0, 0.6)
        for s in ([0] if half == 0 else [0, 6]):
            mx.kick(kick(f0=170, f1=60, decay=14, dur=0.25), t0 + s * step, 0.7)
        mx.dry.add(snare(tone=210, bright=9000), t0 + 8 * step, 0.85)
        mx.wet.add(snare(), t0 + 8 * step, 0.2)
        if half == 1 and (b + 1) % 8 != 0:
            mx.dry.add(snare(tone=210, bright=9000), t0 + 14 * step, 0.55)
        if sec == "SWITCH":  # triplet-feel hats
            for j in range(12):
                mx.dry.add(hat(vel=0.75 if j % 3 == 0 else 0.4), t0 + j * (16 * step / 12), 0.75, 0.35)
        else:
            roll = b % 4 == 3
            for s in [0, 3, 6, 8, 10, 12, 14]:
                if not (roll and s >= 12):
                    mx.dry.add(hat(vel=0.8 if s in (0, 8) else 0.55), t0 + s * step, 0.75, 0.35)
            if roll:
                for j in range(6):
                    mx.dry.add(hat(vel=0.35 + 0.08 * j), t0 + 12 * step + j * (4 * step / 6), 0.75, 0.35)
        if sec == "DROP":
            for s in (5, 13):
                mx.dry.add(rim(), t0 + s * step, 0.35, -0.4)
        if (b + 1) % 8 == 0:
            for j in range(8):
                mx.dry.add(hat(vel=0.3 + 0.06 * j), t0 + 14 * step + j * step / 4, 0.7, 0.35)


def build_brass(mx, step, bar, intro):
    """Soulful live-band boom bap: horn section, choir, bass guitar, loose human drums."""
    prog = [(31, [58, 62, 65], [55, 58, 62, 65]),   # Gm7
            (36, [58, 63, 67], [55, 58, 63, 67]),   # Cm7
            (39, [55, 58, 62], [51, 55, 58, 62]),   # Ebmaj7
            (38, [54, 60, 65], [54, 57, 60, 65])]   # D7#9
    bass_line = [(0, 0, 3), (3, 0, 1), (6, 12, 1), (7, 10, 1), (10, 7, 2), (13, 5, 1), (14, 3, 2)]
    hook = [(0, 74, 2), (2, 77, 2), (4, 79, 3), (7, 77, 1), (10, 74, 2), (12, 72, 4)]
    sw = 0.1
    for b in range(2 if intro else TOTAL):
        sec, i, n = ("INTRO", b, 2) if intro else section(b)
        t0, half = b * bar, b % 2
        root, horns, voicing = prog[0] if intro else prog[(b // 2) % 4]
        M = mx.music(sec, i, n)
        if sec in ("INTRO", "A2", "BREAK", "DROP"):
            if half == 0:
                M(choir([m + 12 for m in voicing[:3]], bar * 2 * 0.95, "u"), t0, 0.9, 0.0, 0.6)
        if sec in ("INTRO", "BUILD"):
            for m in horns:
                M(brass(m, bar * 0.9, swell=True), t0, 0.8, 0.1 * (m % 3 - 1), 0.4)
        if sec in ("A", "A2", "DROP") or (sec == "SWITCH" and half == 0):
            stabs = [(0, 2), (3, 1), (10, 2)] if half == 0 else [(6, 1), (8, 3), (14, 1)]
            for s, ln in stabs:
                for m in horns:
                    M(brass(m, ln * step, vel=0.9), t0 + swing_t(s, step, sw) + human(0.004), 0.9, 0.12 * (m % 3 - 1), 0.3)
        if sec == "DROP" and half == 1:
            for s, m, ln in hook:
                M(brass(m, ln * step), t0 + swing_t(s, step, sw), 1.0, -0.2, 0.35)
                M(brass(m - 12, ln * step), t0 + swing_t(s, step, sw), 0.6, 0.2, 0.2)
        if intro:
            continue
        if sec != "BREAK" or i >= 1:
            for s, iv, ln in bass_line:
                if sec == "STRIP" and s in (6, 7):
                    continue
                M(bass_guitar(root + iv, ln * step, 0.8 + 0.2 * (s == 0)), t0 + swing_t(s, step, sw) + human(0.003), 0.9)
        bk = lambda: kick(f0=110, f1=50, decay=9, drive=1.8)
        bs = lambda: snare(tone=220, bright=8000)
        if sec == "BREAK":
            continue
        if sec == "BUILD":
            common_build(mx, sec, i, n, t0, step, bar, bk, bs)
            continue
        if i == 0 and sec in ("DROP", "SWITCH"):
            mx.dry.add(crash(), t0, 0.55)
        kicks = [0, 7, 10] if half == 0 else [0, 3, 10]
        if sec == "SWITCH":
            kicks = [0, 6, 9, 11] if half == 0 else [0, 3, 8, 10]
        for s in kicks:
            mx.kick(bk(), t0 + swing_t(s, step, sw) + human(), 0.8 * rng.uniform(0.85, 1))
        for s in (4, 12):
            mx.dry.add(bs(), t0 + s * step + human(0.004), 0.85)
            mx.wet.add(bs(), t0 + s * step, 0.15)
        for s in (6, 9, 14) if sec != "STRIP" else (9,):
            if rng.random() < 0.6:
                mx.dry.add(bs(), t0 + swing_t(s, step, sw) + human(), 0.12)  # ghost notes
        if sec == "SWITCH":
            for s in range(0, 16, 2):
                mx.dry.add(ride(0.8 if s % 4 == 0 else 0.5), t0 + swing_t(s, step, sw) + human(), 0.6, 0.4)
        else:
            for s in range(16):
                v = (0.9 if s % 4 == 0 else 0.6 if s % 2 == 0 else 0.3) * rng.uniform(0.8, 1.1)
                mx.dry.add(hat(vel=v), t0 + swing_t(s, step, sw) + human(0.004), 0.75, -0.35)
        if sec == "DROP":
            mx.dry.add(hat(True, 0.5), t0 + swing_t(14, step, sw), 0.6, -0.35)
        if (b + 1) % 8 == 0:
            snare_roll(mx, t0, step, 12, 16, 2, 0.55, bs)
        elif (b + 1) % 4 == 0:
            mx.dry.add(bs(), t0 + swing_t(15, step, sw), 0.4)


def build_afterglow(mx, step, bar, intro):
    """Emotional UK-garage: side-chained piano, chopped formant vocals, 2-step drums, big build and drop."""
    prog = [(30, [57, 61, 64, 68]), (38, [54, 57, 61, 64]), (33, [52, 57, 61, 64]), (40, [52, 57, 59, 64])]
    chops = [(0, 73, 2, "a"), (3, 76, 1, "e"), (4, 76, 1, "e"), (6, 78, 2, "o"), (10, 76, 2, "a"), (14, 73, 2, "u"),
             (16, 71, 2, "a"), (19, 73, 1, "i"), (20, 73, 1, "i"), (22, 76, 3, "o"), (26, 73, 1, "e"), (27, 73, 1, "e"), (28, 69, 4, "a")]
    sw = 0.12
    for b in range(2 if intro else TOTAL):
        sec, i, n = ("INTRO", b, 2) if intro else section(b)
        t0, half = b * bar, b % 2
        root, ch = prog[0] if intro else prog[(b // 2) % 4]
        M = mx.music(sec, i, n, pump=True)
        if sec != "STRIP":
            hits = [(0, 6, 1.0), (6, 2, 0.6), (10, 5, 0.75)] if sec not in ("BREAK", "INTRO") else [(0, 15, 0.9)]
            for s, ln, v in hits:
                for m in ch:
                    M(piano(m, ln * step, v), t0 + swing_t(s, step, sw), 1.1, 0.15 * (m % 3 - 1), 0.35)
        if sec in ("INTRO", "A2", "BREAK", "DROP", "SWITCH", "STRIP"):
            for s, m, ln, v in chops:
                if s // 16 != half:
                    continue
                ss = s % 16
                if sec == "SWITCH" and ss in (3, 4, 19 % 16, 20 % 16, 10, 26 % 16):
                    for j in range(4):  # stutter
                        M(voice(m, step / 2 * 0.8, v, attack=0.003, bend=0.02), t0 + (ss + j / 2) * step, 0.9, 0.1, 0.3)
                else:
                    M(voice(m, ln * step * 0.85, v, attack=0.005, bend=0.03), t0 + swing_t(ss, step, sw), 1.0, 0.1, 0.4)
        if intro:
            continue
        if sec in ("A", "A2", "DROP", "SWITCH", "STRIP") or (sec == "BUILD" and i >= 2):
            for s, ln in ((0, 3), (6, 2), (10, 4)):
                mx.dry.add(sub(root + (12 if root < 33 else 0), ln * step), t0 + swing_t(s, step, sw), 0.7)
        gk = lambda: kick(f0=140, f1=50, decay=8, dur=0.4)
        if sec == "BREAK":
            continue
        if sec == "BUILD":
            common_build(mx, sec, i, n, t0, step, bar, gk, clap)
            continue
        if i == 0 and sec in ("DROP", "SWITCH"):
            mx.dry.add(crash(), t0, 0.6)
        if sec == "SWITCH":
            kicks = [0, 4, 8, 12]
        else:
            kicks = [0, 10] if half == 0 else [0, 7, 10]
        for s in kicks:
            mx.kick(gk(), t0 + swing_t(s, step, sw), 0.8)
        for s in (4, 12):
            mx.dry.add(clap(), t0 + s * step, 0.75)
            mx.wet.add(clap(), t0 + s * step, 0.3)
        for s in range(16):
            if s % 4 == 0 and sec != "SWITCH":
                continue
            v = 0.7 if s % 2 == 0 else 0.4
            mx.dry.add(hat(vel=v), t0 + swing_t(s, step, sw), 0.7, 0.3)
        if sec in ("DROP", "SWITCH"):
            for s in (2, 6, 10, 14):
                mx.dry.add(hat(True, 0.55), t0 + swing_t(s, step, sw), 0.6, -0.3)
        if (b + 1) % 8 == 0:
            snare_roll(mx, t0, step, 12, 16, 2, 0.5, clap)


def build_foundry(mx, step, bar, intro):
    """Sparse, uncluttered hip-hop/garage hybrid: dissonant cluster chords, struck-metal foley, short sub."""
    clusters = [[48, 51, 55, 59, 61], [44, 48, 51, 55, 62]]  # Cm(maj7,b9) / Abmaj7#11
    foley = [(3, 640, 0.7), (6, 1180, 0.5), (11, 410, 0.6), (14, 900, 0.4)]
    sw = 0.14
    for b in range(2 if intro else TOTAL):
        sec, i, n = ("INTRO", b, 2) if intro else section(b)
        t0, half = b * bar, b % 2
        M = mx.music(sec, i, n)
        ch = clusters[(b // 2) % 2]
        if sec not in ("STRIP",):
            if half == 0:
                for m in ch:
                    M(rhodes(m, bar * (1.2 if sec in ("BREAK", "INTRO") else 0.35), 0.9), t0, 1.9, 0.2 * (m % 3 - 1), 0.5)
            elif sec in ("A2", "DROP"):
                for m in ch[1:]:
                    M(rhodes(m + 12, step * 1.5, 0.7), t0 + swing_t(11, step, sw), 1.3, 0.3, 0.6)
        # foley runs everywhere: it's the texture of the beat
        for s, base, v in foley:
            if sec in ("BUILD",) and i == n - 1 and s >= 12:
                continue
            M(metal(base * (1.0 if half == 0 else 1.06), vel=v), t0 + swing_t(s, step, sw), 0.9, (s % 3 - 1) * 0.5, 0.5)
        if intro:
            continue
        if sec in ("A", "A2", "DROP", "SWITCH", "STRIP") or (sec == "BUILD" and i >= 1):
            root = 36 if (b // 2) % 2 == 0 else 32
            for s, iv, ln in ((0, 0, 3), (6, 0, 1), (11, -2, 2)):
                mx.dry.add(sub(root + iv, ln * step), t0 + swing_t(s, step, sw), 0.75)
        fk = lambda: kick(f0=130, f1=46, decay=10, dur=0.45, drive=2.2)

        def fsnare():
            return rim() * 0.8 + metal(2300, decay=25, vel=0.8)[: len(rim())]
        if sec == "BREAK":
            continue
        if sec == "BUILD":
            common_build(mx, sec, i, n, t0, step, bar, fk, fsnare)
            continue
        if i == 0 and sec in ("DROP", "SWITCH"):
            mx.dry.add(crash(), t0, 0.45)
        kicks = [0, 10] if sec == "SWITCH" else ([0, 7, 10] if half == 0 else [0, 10])
        for s in kicks:
            mx.kick(fk(), t0 + swing_t(s, step, sw), 0.85)
        for s in (4, 12):
            mx.dry.add(fsnare(), t0 + s * step, 1.0)
            mx.dry.add(snare(tone=240, bright=5000), t0 + s * step, 0.35)
            mx.wet.add(fsnare(), t0 + s * step, 0.3)
        if sec in ("A2", "DROP", "SWITCH"):
            hs = range(16) if sec == "SWITCH" else range(0, 16, 2)
            for s in hs:
                mx.dry.add(hat(vel=0.55 if s % 2 == 0 else 0.3), t0 + swing_t(s, step, sw), 0.7, 0.3)
        if (b + 1) % 8 == 0:
            for j, s in enumerate((13, 14, 15)):
                mx.dry.add(metal(700 + 200 * j, vel=0.8), t0 + swing_t(s, step, sw), 0.8)
    if True:  # low industrial hum, circular so it loops cleanly
        t = np.arange(mx.n) / SR
        hum = spectral(rng.normal(0, 1, mx.n), 60, 400) * 0.01 * (1 + 0.5 * np.sin(2 * np.pi * t / (bar * 2)))
        mx.dry.buf += hum


BEATS = [
    dict(id="eski", name="Eski", style="Grime", bpm=140, key="F minor", build=build_eski,
         blurb="Square-wave grime riff, half-time clap. Fast and bouncy."),
    dict(id="dusty", name="Dusty", style="Boom bap", bpm=90, key="D minor", build=build_dusty, intro_lp=900,
         blurb="Swung drums, warm keys, vinyl crackle. Slow and roomy, best for beginners."),
    dict(id="midnight", name="Midnight", style="UK drill", bpm=142, key="F# minor", build=build_midnight,
         blurb="Sliding 808s, skippy hats, dark bells. Hardest to ride."),
    dict(id="brass", name="Brass", style="Soul boom bap", bpm=92, key="G minor", build=build_brass,
         blurb="Live-band horns, choir and bass guitar over loose, human drums."),
    dict(id="afterglow", name="Afterglow", style="UK garage", bpm=132, key="F# minor", build=build_afterglow,
         sidechain=0.55, blurb="Emotional piano, chopped vocals, 2-step swing and a big drop."),
    dict(id="foundry", name="Foundry", style="Left-field hip-hop", bpm=100, key="C minor", build=build_foundry,
         blurb="Sparse and clanky: dissonant chords, metal percussion, lots of space."),
]


def render(beat):
    step = 60 / beat["bpm"] / 4
    bar = step * 16
    loop_mx = Mix(bar * TOTAL, True, beat.get("sidechain", 0.0))
    intro_mx = Mix(bar * 2, False, beat.get("sidechain", 0.0))
    beat["build"](loop_mx, step, bar, intro=False)
    beat["build"](intro_mx, step, bar, intro=True)
    loop = loop_mx.render()
    loop = loop * gain_curve(loop, bar)
    intro = intro_mx.render()
    intro = np.vstack([spectral(intro[c], 0, beat.get("intro_lp", 1100)) for c in range(2)]) * 1.8
    r = riser(bar)
    s = int(bar * SR)
    intro[:, s:s + len(r)] += r[: intro.shape[1] - s] * 0.5
    k = int(0.02 * SR)
    intro[:, -k:] *= np.linspace(1, 0, k)
    # loudness match across beats, soft-limit, peak-normalise
    # roll off above 15 kHz first: AAC cuts there anyway, and doing it ourselves stops encoder overshoot
    loop = np.vstack([spectral(loop[c], 0, 15000, order=8) for c in range(2)])
    intro = np.vstack([spectral(intro[c], 0, 15000, order=8) for c in range(2)])
    g = 10 ** (-11 / 20) / np.sqrt(np.mean(loop ** 2))
    loop, intro = np.tanh(loop * g * 1.2) / 1.2, np.tanh(intro * g * 1.2) / 1.2
    peak = max(np.abs(loop).max(), np.abs(intro).max())
    return loop * 0.82 / peak, intro * 0.82 / peak, bar


def write_wav(path, x):
    import wave
    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((np.clip(x.T, -1, 1) * 32767).astype("<i2").tobytes())


def encode(src, dst, args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, *args, dst], check=True)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PREV, exist_ok=True)
    meta, frames = [], {}
    for beat in BEATS:
        mpath = f"{OUT}/beats.json"
        if ONLY and beat["id"] not in ONLY:
            continue
        loop, intro, bar = render(beat)
        tmp = f"{OUT}/_tmp.wav"
        # pad with 1 s of the loop's own tail/head so the encoder never sees a cold start;
        # the app loops frames [LOOP_PAD, LOOP_PAD + loopFrames) which is seamless by construction
        write_wav(tmp, np.concatenate([loop[:, -LOOP_PAD:], loop, loop[:, :LOOP_PAD]], axis=1))
        encode(tmp, f"{OUT}/{beat['id']}_loop.mp3", ["-c:a", "libmp3lame", "-b:a", "192k"])
        frames[beat["id"]] = loop.shape[1]
        write_wav(tmp, intro)
        encode(tmp, f"{OUT}/{beat['id']}_intro.mp3", ["-c:a", "libmp3lame", "-b:a", "192k"])
        write_wav(tmp, np.concatenate([intro, loop], axis=1))
        encode(tmp, f"{PREV}/{beat['id']}_preview.mp3", ["-b:a", "160k"])
        os.remove(tmp)
        print(beat["id"], "ok", round(loop.shape[1] / SR, 1), "s", flush=True)
    for beat in BEATS:
        step = 60 / beat["bpm"] / 4
        meta.append({k: beat[k] for k in ("id", "name", "style", "bpm", "key", "blurb")} | {
            "beatsPerBar": 4, "loopBars": TOTAL, "introBars": 2,
            "loopFile": f"{beat['id']}_loop.mp3", "introFile": f"{beat['id']}_intro.mp3",
            "barSeconds": round(step * 16, 6),
            "sampleRate": SR, "loopStartFrame": LOOP_PAD,
            "loopFrames": frames.get(beat["id"], int(round(step * 16 * TOTAL * SR))),
            "sections": [{"name": s, "startBar": a, "bars": n} for s, a, n in SECTIONS],
            "free": beat["id"] in ("eski", "dusty", "midnight"),
        })
    with open(f"{OUT}/beats.json", "w") as f:
        json.dump({"beats": meta}, f, indent=2)
