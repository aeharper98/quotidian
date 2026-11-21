"""Synthesise Quotidian's starter beats from scratch (no samples, so we own 100% of the audio).

Each beat renders two files:
  <id>_intro.wav  - 2 filtered bars + riser, played once before "the drop"
  <id>_loop.wav   - 16 bars that loop seamlessly (tails and reverb wrap around)
plus a preview mp3 (intro + loop x2) for listening.
"""
import json
import os
import subprocess
import sys

import numpy as np

SR = 44100
rng = np.random.default_rng(7)
OUT = sys.argv[1] if len(sys.argv) > 1 else "beats"


# ---------------------------------------------------------------- helpers
def mtof(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def tt(dur):
    return np.arange(int(dur * SR)) / SR


def spectral(x, lo=0.0, hi=SR / 2, soft=0.15):
    """Band-pass by FFT with soft edges (fine for short one-shots)."""
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    m = np.ones_like(f)
    if lo > 0:
        m *= 1 / (1 + (lo / np.maximum(f, 1)) ** (4 / soft * 0.15))
    if hi < SR / 2:
        m *= 1 / (1 + (f / hi) ** (4 / soft * 0.15))
    return np.fft.irfft(X * m, n)


def noise(dur):
    return rng.uniform(-1, 1, int(dur * SR))


def fade_tail(x, ms=8):
    k = min(len(x), int(SR * ms / 1000))
    if k > 0:
        x[-k:] *= np.linspace(1, 0, k)
    return x


class Bus:
    """Stereo buffer. wrap=True makes anything past the end wrap to the start (seamless loops)."""

    def __init__(self, seconds, wrap):
        self.n = int(round(seconds * SR))
        self.buf = np.zeros((2, self.n))
        self.wrap = wrap

    def add(self, sig, at, gain=1.0, pan=0.0):
        s = int(round(at * SR))
        L = gain * np.sqrt(0.5 * (1 - pan))
        R = gain * np.sqrt(0.5 * (1 + pan))
        idx = np.arange(s, s + len(sig))
        if self.wrap:
            idx %= self.n
        else:
            keep = idx < self.n
            idx, sig = idx[keep], sig[keep]
        np.add.at(self.buf[0], idx, sig * L)
        np.add.at(self.buf[1], idx, sig * R)


def reverb(buf, wrap, seconds=1.6, damp=4000):
    n = buf.shape[1]
    ir_len = int(seconds * SR)
    out = np.zeros_like(buf)
    for ch in range(2):
        ir = noise(seconds) * np.exp(-tt(seconds) * 4.5)
        ir = spectral(ir, 200, damp)
        ir /= np.sqrt(np.sum(ir ** 2)) * 6
        if wrap:  # circular convolution => tail wraps into the loop start
            L = n
            irp = np.zeros(L)
            irp[: min(ir_len, L)] = ir[:L]
            out[ch] = np.fft.irfft(np.fft.rfft(buf[ch]) * np.fft.rfft(irp), L)
        else:
            L = n + ir_len
            y = np.fft.irfft(np.fft.rfft(buf[ch], L) * np.fft.rfft(ir, L), L)
            out[ch] = y[:n]
    return out


# ---------------------------------------------------------------- instruments
def kick(f0=150, f1=48, decay=6.0, dur=0.6, drive=1.6):
    t = tt(dur)
    f = f1 + (f0 - f1) * np.exp(-t * 32)
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * decay)
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
    x = spectral(noise(dur), 7000, 16000) * np.exp(-t * (9 if open_ else 70))
    return fade_tail(x * vel * 0.55)


def sub808(segs, step, dur_total):
    """segs: list of (start_step, midi, len_steps, slide_from_midi or None). Returns one continuous signal."""
    out = np.zeros(int(dur_total * SR) + SR)
    for start, m, ln, slide in segs:
        d = ln * step + 0.05
        t = tt(d)
        f_to = mtof(m)
        if slide is not None:
            f_from = mtof(slide)
            f = f_to + (f_from - f_to) * np.exp(-t * 28)
        else:
            f = np.full_like(t, f_to)
        ph = 2 * np.pi * np.cumsum(f) / SR
        amp = np.minimum(t / 0.004, 1) * np.exp(-t * 0.9)
        # saturation adds harmonics so the bass is audible on a phone speaker
        sig = np.tanh(np.sin(ph) * 2.6) * amp * 0.8
        sig = fade_tail(sig, 15)
        s = int(start * step * SR)
        out[s : s + len(sig)] += sig
    return out


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
    x = additive(mtof(m), dur + 0.05, "square", cutoff)
    env = np.minimum(t / 0.003, 1) * np.exp(-t * 7)
    return fade_tail(x * env * 0.35)


def bass_square(m, dur, cutoff=700):
    t = tt(dur)
    x = additive(mtof(m), dur, "square", cutoff)
    env = np.minimum(t / 0.005, 1) * np.exp(-t * 1.5)
    return fade_tail(np.tanh(x * 1.5) * env * 0.6, 12)


def rhodes(m, dur):
    f = mtof(m)
    t = tt(dur + 0.6)
    x = (
        np.sin(2 * np.pi * f * t)
        + 0.35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 4)
        + 0.12 * np.sin(2 * np.pi * 7.1 * f * t) * np.exp(-t * 18)
    )
    env = np.minimum(t / 0.006, 1) * np.exp(-t * 1.3)
    rel = np.where(t > dur, np.exp(-(t - dur) * 9), 1.0)
    return fade_tail(x * env * rel * 0.22)


def bell(m, dur):
    f = mtof(m)
    t = tt(dur + 1.0)
    idx = 2.2 * np.exp(-t * 5)
    x = np.sin(2 * np.pi * f * t + idx * np.sin(2 * np.pi * 3.5 * f * t))
    x += 0.3 * np.sin(2 * np.pi * f * 0.5 * t)
    env = np.minimum(t / 0.002, 1) * np.exp(-t * 2.2)
    return fade_tail(x * env * 0.28)


def pad(ms, dur, cutoff=1400):
    t = tt(dur + 0.5)
    x = np.zeros_like(t)
    for m in ms:
        for det in (-0.08, 0.0, 0.08):
            x += additive(mtof(m + det), dur + 0.5, "saw", cutoff)
    env = np.minimum(t / 0.35, 1)
    env *= np.where(t > dur, np.exp(-(t - dur) * 5), 1.0)
    return fade_tail(x * env * 0.035 / max(1, len(ms) / 3))


def riser(dur):
    t = tt(dur)
    x = noise(dur)
    # crude sweep: blend progressively brighter band-limited versions
    lo = spectral(x, 300, 1500)
    hi = spectral(x, 3000, 14000)
    p = (t / dur) ** 2
    return fade_tail((lo * (1 - p) + hi * p) * p * 0.6, 3)


def crackle(seconds):
    n = int(seconds * SR)
    x = spectral(rng.normal(0, 1, n), 500, 6000) * 0.006
    pops = rng.random(n) < 0.00035
    x[pops] += rng.uniform(-0.08, 0.08, pops.sum())
    return x


# ---------------------------------------------------------------- render
def finish(dry, wet, wrap, drive=1.4):
    mix = dry.buf + reverb(wet.buf, wrap)
    mix = np.tanh(mix * drive) / np.tanh(drive)
    return mix


def master(loop, intro, target_db=-11.0):
    """Match loudness across beats (loop RMS ~ target), soft-limit, then peak-normalise."""
    rms = np.sqrt(np.mean(loop ** 2))
    g = 10 ** (target_db / 20) / rms
    loop, intro = np.tanh(loop * g * 1.2) / 1.2, np.tanh(intro * g * 1.2) / 1.2
    peak = max(np.abs(loop).max(), np.abs(intro).max())
    return loop * 0.89 / peak, intro * 0.89 / peak


def write_wav(path, x):
    pcm = (np.clip(x.T, -1, 1) * 32767).astype("<i2")
    import wave

    with wave.open(path, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


def render(beat):
    bpm = beat["bpm"]
    step = 60 / bpm / 4
    bar = step * 16
    loop_dry, loop_wet = Bus(bar * 16, True), Bus(bar * 16, True)
    intro_dry, intro_wet = Bus(bar * 2, False), Bus(bar * 2, False)
    beat["build"](loop_dry, loop_wet, step, bar, intro=False)
    beat["build"](intro_dry, intro_wet, step, bar, intro=True)
    loop = finish(loop_dry, loop_wet, True)
    intro = finish(intro_dry, intro_wet, False)
    # filtered intro (the "before the drop" feel), riser stays bright
    intro = np.vstack([spectral(intro[c], 0, beat.get("intro_lp", 1100)) for c in range(2)])
    r = riser(bar)
    s = int(bar * SR)
    intro[:, s : s + len(r)] += r[: intro.shape[1] - s] * 0.5
    intro *= 1.8
    intro[:, -int(0.02 * SR) :] *= np.linspace(1, 0, int(0.02 * SR))
    loop, intro = master(loop, intro)
    return loop, intro, bar


def swing_t(i, step, amt):
    return i * step + (step * amt if i % 2 == 1 else 0)


# ---------------------------------------------------------------- beat 1: grime
def build_grime(dry, wet, step, bar, intro):
    riff = [(0, 77), (3, 77), (6, 75), (8, 72), (11, 72), (14, 70),
            (16, 68), (19, 68), (22, 70), (24, 72), (27, 75), (30, 72)]
    bass = [(0, 29, 3), (3, 29, 2), (6, 41, 1), (8, 29, 4), (14, 32, 2),
            (16, 25, 3), (19, 25, 2), (22, 37, 1), (24, 27, 4), (30, 27, 2)]
    chords = {0: [53, 56, 60], 1: [49, 53, 56], 1.5: [51, 55, 58]}
    bars = 2 if intro else 16
    for b in range(bars):
        t0 = b * bar
        half = b % 2
        for s, m in riff:
            if s // 16 == half:
                n = pluck_square(m, step * 1.5)
                dry.add(n, t0 + (s % 16) * step, 1.4, 0.25)
                wet.add(n, t0 + (s % 16) * step, 0.25)
        if intro or b >= 8:
            for key, ms in chords.items():
                if (half == 0 and key == 0) or (half == 1 and key in (1, 1.5)):
                    at = t0 + (8 * step if key == 1.5 else 0)
                    p = pad(ms, bar / 2 if half else bar)
                    dry.add(p, at, 0.8, -0.2)
                    wet.add(p, at, 0.4)
        if intro:
            continue
        for s, m, ln in bass:
            if s // 16 == half:
                dry.add(bass_square(m, ln * step), t0 + (s % 16) * step, 0.75)
        kicks = [0, 10] if b % 4 != 3 else [0, 7, 10]
        if b == 15:
            kicks = [0]
        for s in kicks:
            dry.add(kick(), t0 + s * step, 0.8)
        dry.add(clap(), t0 + 8 * step, 0.8)
        dry.add(snare(), t0 + 8 * step, 0.5)
        wet.add(clap(), t0 + 8 * step, 0.3)
        for s in range(0, 16, 2):
            dry.add(hat(vel=1.0 if s % 4 == 0 else 0.6), t0 + s * step, 0.8, 0.3)
        if b % 2 == 1:
            dry.add(hat(vel=0.5), t0 + 15 * step, 0.8, 0.3)
        if b in (7, 15):
            for i, s in enumerate((12, 13, 14, 15)):
                dry.add(snare(), t0 + s * step, 0.25 + 0.12 * i)


# ---------------------------------------------------------------- beat 2: boom bap
def build_boombap(dry, wet, step, bar, intro):
    prog = [  # (bass midi, chord voicing) each held 2 bars
        (38, [53, 57, 60, 64]),  # Dm9
        (34, [57, 60, 62, 65]),  # Bbmaj9
        (31, [58, 62, 65, 69]),  # Gm9
        (33, [55, 58, 61, 64]),  # A7b9
    ]
    sw = 0.17
    bars = 2 if intro else 16
    for b in range(bars):
        t0 = b * bar
        root, ch = prog[(b // 2) % 4] if not intro else prog[0]
        hits = [(0, 1.6), (10, 0.6)] if b % 2 == 0 else [(0, 1.0), (6, 0.5), (11, 1.2)]
        for s, beats in hits:
            for m in ch:
                r = rhodes(m, beats * 4 * step)
                at = t0 + swing_t(s, step, sw)
                dry.add(r, at, 1.4, 0.15 * (m % 3 - 1))
                wet.add(r, at, 0.35)
        if intro:
            continue
        for s, m, ln in [(0, root, 6), (7, root, 2), (10, root + 7, 3), (14, root + 12, 2)]:
            dry.add(bass_square(m, ln * step, 500), t0 + swing_t(s, step, sw), 0.65)
        kicks = [0, 7, 10] if b % 2 == 0 else [0, 10, 13]
        if b == 15:
            kicks = [0, 7]
        for s in kicks:
            dry.add(kick(f0=120, f1=52, decay=8, drive=2.0), t0 + swing_t(s, step, sw), 0.8)
        for s in (4, 12):
            dry.add(snare(tone=200, bright=6000), t0 + s * step, 0.9)
            wet.add(snare(), t0 + s * step, 0.15)
        for s in range(0, 16, 2):
            dry.add(hat(vel=0.9 if s % 4 == 0 else 0.55), t0 + swing_t(s, step, sw), 0.8, -0.3)
        for s in (3, 11):
            dry.add(hat(vel=0.3), t0 + swing_t(s, step, sw), 0.8, -0.3)
        if b % 4 == 3:
            dry.add(snare(tone=200, bright=5000), t0 + swing_t(15, step, sw), 0.25)
    cr = crackle(dry.n / SR)
    dry.buf += cr * 1.0


# ---------------------------------------------------------------- beat 3: UK drill
def build_drill(dry, wet, step, bar, intro):
    motif = [(0, 78), (3, 81), (6, 85), (10, 79), (12, 78),
             (16, 76), (19, 81), (22, 83), (26, 79), (28, 78)]
    b808 = [(0, 30, 6, None), (6, 30, 3, None), (10, 33, 4, 30), (14, 37, 2, 33),
            (16, 30, 6, 37), (22, 26, 4, 30), (26, 28, 3, None), (29, 30, 3, 28)]
    chords = [[54, 57, 61], [50, 54, 57]]  # F#m, D
    bars = 2 if intro else 16
    for b in range(bars):
        t0 = b * bar
        half = b % 2
        for s, m in motif:
            if s // 16 == half:
                n = bell(m + (12 if (b >= 8 and b % 4 >= 2) else 0), step * 2)
                dry.add(n, t0 + (s % 16) * step, 1.2, -0.3)
                wet.add(n, t0 + (s % 16) * step, 0.45)
        if intro or b >= 8:
            p = pad(chords[half], bar, cutoff=900)
            dry.add(p, t0, 0.9, 0.2)
            wet.add(p, t0, 0.4)
        if intro:
            continue
        if half == 0:
            segs = [(s, m, ln, sl) for s, m, ln, sl in b808]
            sig = sub808(segs, step, bar * 2)
            dry.add(sig[: int(bar * 2 * SR)], t0, 0.7)
        for s in ([0] if half == 0 else [0, 6]):
            dry.add(kick(f0=170, f1=60, decay=14, dur=0.25), t0 + s * step, 0.7)
        dry.add(snare(tone=210, bright=9000), t0 + 8 * step, 0.85)
        wet.add(snare(), t0 + 8 * step, 0.2)
        if half == 1 and b != 15:
            dry.add(snare(tone=210, bright=9000), t0 + 14 * step, 0.55)
        hats = [0, 3, 6, 8, 10, 12, 14]
        roll = b % 4 == 3
        for s in hats:
            if roll and s >= 12:
                continue
            dry.add(hat(vel=0.8 if s in (0, 8) else 0.55), t0 + s * step, 0.75, 0.35)
        if roll:  # triplet roll across the last beat
            for i in range(6):
                dry.add(hat(vel=0.35 + 0.08 * i), t0 + 12 * step + i * (4 * step / 6), 0.75, 0.35)
        if b in (7, 15):
            for i in range(8):
                dry.add(hat(vel=0.3 + 0.06 * i), t0 + 14 * step + i * step / 4, 0.7, 0.35)


BEATS = [
    dict(id="eski", name="Eski", style="Grime", bpm=140, key="F minor", build=build_grime,
         blurb="Square-wave grime riff, half-time clap. Fast and bouncy."),
    dict(id="dusty", name="Dusty", style="Boom bap", bpm=90, key="D minor", build=build_boombap,
         intro_lp=900, blurb="Swung drums, warm keys, vinyl crackle. Slow and roomy, best for beginners."),
    dict(id="midnight", name="Midnight", style="UK drill", bpm=142, key="F# minor", build=build_drill,
         blurb="Sliding 808s, skippy hats, dark bells. Hardest to ride."),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    meta = []
    for beat in BEATS:
        loop, intro, bar = render(beat)
        lw, iw = f"{OUT}/{beat['id']}_loop.wav", f"{OUT}/{beat['id']}_intro.wav"
        write_wav(lw, loop)
        write_wav(iw, intro)
        for src in (lw, iw):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-c:a", "aac", "-b:a", "192k",
                            src.replace(".wav", ".m4a")], check=True)
        prev = np.concatenate([intro, loop, loop], axis=1)
        pw = f"{OUT}/{beat['id']}_preview.wav"
        write_wav(pw, prev)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", pw, "-b:a", "192k",
                        pw.replace(".wav", ".mp3")], check=True)
        os.remove(pw)
        meta.append({k: beat[k] for k in ("id", "name", "style", "bpm", "key", "blurb")} | {
            "beatsPerBar": 4, "loopBars": 16, "introBars": 2,
            "loopFile": f"{beat['id']}_loop.m4a", "introFile": f"{beat['id']}_intro.m4a",
            "barSeconds": round(bar, 6), "free": True,
        })
        print(beat["id"], "ok", round(loop.shape[1] / SR, 2), "s loop")
    with open(f"{OUT}/beats.json", "w") as f:
        json.dump({"beats": meta}, f, indent=2)
