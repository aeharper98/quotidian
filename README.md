# Quotidian

Learn freestyle rap and new words, one tap at a time. See [PLAN.md](PLAN.md) for the V1 build plan.

- `Resources/Beats/`: 3 starter beats (intro and seamless 16-bar loop) plus `beats.json` metadata
- `Resources/words.json`: 40 British-aware rhyme chains, 374 words with definitions
- `previews/`: mp3s to listen to each beat (intro → drop → loop ×2)
- `tools/`: scripts that generate the above
  - `python3 tools/make_beats.py <outdir>` re-synthesises the beats (needs numpy and ffmpeg)
  - `python3 tools/build_words.py tools Resources/words.json` validates `tools/chains.py` and rebuilds the word data
