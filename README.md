# Quotidian

Learn freestyle rap and new words, one tap at a time. See [PLAN.md](PLAN.md) for the V1 build plan.

- `Resources/Beats/`: 6 beats (intro and a 48-bar arranged loop, padded for seamless looping) plus `beats.json` metadata and the section map
- `Resources/words.json`: 40 British-aware rhyme chains, 374 words with definitions
- `web/index.html`: playable web prototype of the mechanics (same beats and words)
- `previews/`: mp3s to listen to each beat (intro → drop → loop ×2)
- `tools/`: scripts that generate the above
  - `python3 tools/make_beats.py Resources/Beats previews` re-synthesises all beats (needs numpy and ffmpeg with libmp3lame, about 2 minutes)
  - `python3 tools/build_words.py tools Resources/words.json` validates `tools/chains.py` and rebuilds the word data
