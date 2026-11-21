"""Validate chains.py and emit words.json for the app bundle."""
import json, sys, collections
sys.path.insert(0, sys.argv[1]); from chains import CHAINS

TYPES = {
 "perfect": ("Perfect rhyme", "Everything from the stressed vowel onwards matches exactly."),
 "accent":  ("Sound rhyme", "Rhymes out loud even if the spelling says no: the r after a vowel goes quiet."),
 "slant":   ("Slant rhyme", "The vowels match and the consonants are close. Most great flows run on these."),
 "multi":   ("Multi", "Two or more syllables rhyme in a row. This is what makes a crowd react."),
 "dialect": ("Slang rhyme", "Rhymes on how people actually talk, like 'thing' said as 'ting'."),
 "cheap":   ("Cheap rhyme", "Easy and predictable. Good for warming up, but go for something rarer."),
}
errs, out, seen = [], [], collections.Counter()
for c in CHAINS:
    ws = []
    for line in c["words"].strip().splitlines():
        p = [x.strip() for x in line.split("|")]
        if len(p) not in (4, 5): errs.append(f"{c['id']}: bad line {line!r}"); continue
        w = {"w": p[0], "level": int(p[1]), "pos": p[2], "def": p[3]}
        if len(p) == 5: w["ex"] = p[4]
        if w["level"] == 3 and "ex" not in w: errs.append(f"{c['id']}: {p[0]} level 3 needs example")
        if not w["def"].endswith("."): errs.append(f"{c['id']}: {p[0]} def needs full stop")
        seen[p[0].lower()] += 1; ws.append(w)
    if c["type"] not in TYPES: errs.append(f"{c['id']}: unknown type")
    if sum(w["level"] == 1 for w in ws) < 2: errs.append(f"{c['id']}: needs >=2 simple words")
    out.append({k: c[k] for k in ("id", "sound", "type", "note")} | {"words": ws})
errs += [f"duplicate word {w}" for w, n in seen.items() if n > 1]
if errs: print("\n".join(errs)); sys.exit(1)
data = {"version": 1, "rhymeTypes": {k: {"label": a, "explain": b} for k, (a, b) in TYPES.items()}, "chains": out}
json.dump(data, open(sys.argv[2], "w"), indent=1, ensure_ascii=False)
lv = collections.Counter(w["level"] for c in out for w in c["words"])
print(f"{len(out)} chains, {sum(lv.values())} words, by level {dict(sorted(lv.items()))}")
