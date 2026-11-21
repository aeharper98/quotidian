# Quotidian — learn freestyle rap and new words (Version 1)

*Quotidian (adj.): everyday, daily. A daily freestyle habit that grows your vocabulary.*

## The idea

A black screen with one huge word. The beat drops. You rap. Tap anywhere and the next word appears, and it **rhymes with the last one**, the British way (accent rhymes, slant rhymes, multis). Tap the word itself to see what it means without stopping the beat. Words you had to look up come back in later sessions until you know them.

## App Store listing

- **Name:** Quotidian: Freestyle Rap
- **Subtitle:** Learn rhymes & new words daily
- **Keywords:** freestyle,rap,rhyme,vocabulary,words,beats,lyrics,grime,battle,hiphop,spit,bars,flow,dictionary,learn
- **Category:** Music (secondary: Education)

## What's in the bundle (already made, in `Resources/`)

- `Beats/beats.json` plus **6 beats**. Each one is an **intro** (2 filtered bars and a riser, played once) and a **48-bar arranged loop** (`.mp3`, 80–130 s). All audio is synthesised from code, so we own 100% of it.
  - **Eski**: grime, 140 BPM (free)
  - **Dusty**: boom bap, 90 BPM, the beginner beat (free)
  - **Midnight**: UK drill, 142 BPM (free)
  - **Brass**: soul boom bap with horns, choir and bass guitar, 92 BPM (Pro later; free during beta)
  - **Afterglow**: emotional UK garage with chopped vocals and piano, 132 BPM (Pro later)
  - **Foundry**: sparse left-field hip-hop with metal percussion and dissonant chords, 100 BPM (Pro later)
- Every loop follows the same arrangement, listed in `sections` in `beats.json`: **A (8 bars) → A2 (8) → BREAK (4) → BUILD (4, ending in a one-beat silent gap) → DROP (8) → SWITCH (8) → STRIP (4) → A2 (4)**, then back to A. There are volume moves, fills every 4 and 8 bars, and crashes on the drops.
- `words.json`: 40 rhyme chains and 374 words. Each chain has a `sound`, a rhyme `type` (perfect / accent / slant / multi / dialect / cheap) and a one-line `note` explaining why the words rhyme. Each word has a `level` (1 simple, 2 mid, 3 advanced), part of speech and definition. Level 3 words also have an example bar (`ex`).

## Screens

### 1. Home
- Big "Today's Cypher" button showing the streak flame and a count, e.g. "🔥 6".
- Beat picker: 6 cards (name, style, BPM), sorted easiest first, that preview on tap, plus a **Your own music** card.
- "Free play" button.
- Small links to Word Bank and Settings.

### 2. Cypher (the main screen)
- Full-bleed black. One word in the centre, **huge** (as big as fits on one line, heavy rounded font, auto-shrink for long words).
- On start: the **intro** plays (filtered) with a "3 · 2 · 1" countdown on its last bar, then **the drop**: the loop starts and the first word slams in.
- **Tap anywhere except the word:** go to the next word, with a quick scale-in animation and a light haptic.
- **Tap the word:** a definition card slides up from the bottom (word, part of speech, definition, example bar if present). It fades after 4 seconds or on the next tap. **The beat never stops.** Tapping also saves the word to the Word Bank.
- **Pulse:** the word gently scales (1.0 → 1.04) on every beat, with a bigger pulse on bar 1, synced to the beat clock.
- **New chain:** when the chain changes, a small chip at the top shows the rhyme type (e.g. "ACCENT RHYME") with the chain's `note` underneath in small text for 3 seconds. This is how the app teaches British rhyme without a tutorial.
- **Next-word preview (setting, on by default):** the upcoming word shows faintly at 25% opacity under the main word, so you can plan a bar ahead.
- Top bar, small and low-contrast: ✕ to end, timer, record toggle (●).
- End of session: summary screen with words seen, words looked up (tap to review), time, streak, and recording playback if you recorded.

### 3. Word Bank
- Every word you tapped, newest first, with its definition and the chain it came from.
- Status: **Learning** (tapped) or **Known**. A word becomes Known once you've seen it 3 times in later sessions without tapping it.
- Tap a word to hear the example bar read with text-to-speech.

### 4. Settings
- **Vocabulary:** a 3-stop slider, **Simple / Mixed / Advanced** (default Mixed). Controls how often advanced words come up.
- **Rhyme style:** Strict (perfect and multi chains only) or **UK loose** (everything, the default).
- **Word change:** Tap (default) / Every bar / Every 2 bars. Auto modes change the word exactly on the downbeat.
- **Next-word preview:** on/off.
- **Haptic on beat:** on/off.
- Daily reminder notification time (default 7pm).

## How words are picked

1. A session is a sequence of **chains**. Within a chain the words rhyme, and when the chain ends you move to a new chain (a new rhyme sound), like a verse changing scheme.
2. Each chain shows **4–6 words**, then switches.
3. **The first word of each chain is always level 1**, so you hear the sound clearly before the hard words arrive.
4. After that, pick levels by the vocabulary setting:
   - Simple: 80% L1, 20% L2, 0% L3
   - Mixed: 45% L1, 30% L2, 25% L3
   - Advanced: 20% L1, 30% L2, 50% L3
   (If a chain has no word at the chosen level, use the nearest level.)
5. **Learning words** from the Word Bank get 3× weight whenever their chain comes up.
6. Don't repeat a chain until every eligible chain has been used. Never show the same word twice in one session.
7. **Daily Cypher:** the random seed is the date, so everyone gets the same chains and beat on a given day. It's 3 minutes long, the beat rotates daily, and finishing at least 2 minutes extends the streak. Start the Daily Cypher so its first DROP lands in the first 30 seconds.

## Audio

- Use `AVAudioEngine` with an `AVAudioPlayerNode`.
- **Loop files are padded:** each loop `.mp3` has 1 second of extra audio before and after the loop. Read **exactly** `loopFrames` frames starting at `loopStartFrame` (both in `beats.json`) into one `AVAudioPCMBuffer`, and loop that buffer with `.loops`. That region is seamless by construction, so the loop has no click or gap.
- Schedule the intro buffer, then the loop buffer immediately after it, so it plays sample-accurately with no gap.
- Beat clock: `barSeconds` and `bpm`, with beat 0 = the first frame of the loop region. The clock drives the pulse, haptics, auto word-change and the section events below.
- **React to the arrangement** (section map in `beats.json`):
  - **BREAK:** the word dims to 60% and the chip says "BREAKDOWN · slow it down".
  - **BUILD:** the pulse gets stronger each bar, and the screen goes black on the silent gap beat.
  - **DROP:** start a new rhyme chain exactly on the drop. The word slams in with a flash in the beat's accent colour and a heavy haptic.
  - **SWITCH:** start a new chain, and the chip says "SWITCH-UP".
- Audio session: `.playAndRecord` with `.defaultToSpeaker` and `.allowBluetoothA2DP`, so the beat keeps playing with the mute switch on.
- Use the `free` flag in `beats.json` to lock premium beats later. Everything is unlocked during beta.

## Your own music

- A seventh option in the beat picker is **"Your own music"**. You start Spotify, Apple Music or YouTube first, then open Quotidian, and your music keeps playing.
- In this mode the app plays nothing and uses audio session category `.ambient` (or `.playback` with `.mixWithOthers`), so iOS never pauses or ducks the other app.
- Set the tempo with **tap tempo** or ± buttons (60–180 BPM). It drives the pulse and auto word-change. There are no sections, so chains change every 4–6 words as usual.
- **Recording in this mode** uses `.playAndRecord` with `.mixWithOthers`, `.defaultToSpeaker` and `.allowBluetoothA2DP`. The mic hears the music from the speaker, so the recording includes it. With headphones you get the voice only. Apps aren't allowed to capture another app's audio directly, so we don't try.
- Streaming apps don't give us the song's BPM, so tap tempo is the only way to get it.

## Recording (simple version for V1)

- The record toggle on the Cypher screen records the **mic only** (a separate file, `.m4a`) while the beat plays.
- Show a one-time tip: "Use headphones for a cleaner recording."
- Playback on the summary screen plays the voice and beat together, starting in sync. Save the start offset (seconds into the loop when recording began).
- Keep the last 10 recordings, with a share sheet to export a mixed file.

## Design

- Black background (#000) and white text. Each beat has an accent colour: **Eski** acid green #B6FF3B, **Dusty** warm amber #FFB547, **Midnight** electric blue #4DA3FF, **Brass** gold #F2C14E, **Afterglow** sunset pink #FF6FA3, **Foundry** steel #A8B3BD.
- Word font: SF Pro Rounded Heavy (or a bold condensed face), all lowercase, huge.
- Hardly any UI on the Cypher screen. The word is the whole app.
- Haptics: light tap on next word, soft tick on each downbeat if enabled.

## How we build it

- **No Rork.** Claude writes the native SwiftUI app directly in this repo.
  - The Xcode project is generated from `project.yml` (XcodeGen), so it stays readable and easy to diff.
  - The code lives in `App/`, and the bundled data lives in `Resources/`.
- Builds run on **GitHub Actions macOS runners**. Every push compiles the app, and a manual "Ship to TestFlight" workflow signs it and uploads it with an App Store Connect API key stored as repo secrets.
- The whole loop works from a phone: Claude pushes code, Actions builds it, you install from TestFlight, and you send feedback in chat.
- The web prototype (`web/index.html`) is for testing the mechanics. It shares the same `words.json` and beats.

## Data and storage

- Everything is stored on the device for V1 (SwiftData): Word Bank entries, streak, sessions and settings. No account or backend yet.

## Not in V1 (planned)

- Transcription and an AI coach that scores your bars and suggests changes. This will be a Pro subscription.
- More beats and themed word packs (Pro).
- An in-app beat generator.
- Leaderboards for the Daily Cypher.

## After it's built

Run a full build and check that:
- the intro → loop transition and the loop wrap-around have no gap or click,
- a new chain starts on each DROP,
- tapping the word doesn't advance,
- definitions don't pause audio,
- the Word Bank fills from taps,
- the streak counts.
