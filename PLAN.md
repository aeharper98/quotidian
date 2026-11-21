# Quotidian — learn freestyle rap and new words (Version 1)

*Quotidian (adj.): everyday, daily. A daily freestyle habit that grows your vocabulary.*

## The idea

A black screen with one huge word. The beat drops. You rap. Tap anywhere and the next word appears, and it **rhymes with the last one** by sound, not spelling (sound rhymes, slant rhymes, multis). Tap the word itself to see what it means without stopping the beat. Words you had to look up come back in later sessions until you know them.

## App Store listing

- **Name:** Quotidian: Freestyle Rap
- **Subtitle:** Learn rhymes & new words daily
- **Keywords:** freestyle,rap,rhyme,vocabulary,words,beats,lyrics,grime,battle,hiphop,spit,bars,flow,dictionary,learn
- **Category:** Music (secondary: Education)

## What's in the bundle (already made, in `Resources/`)

- `Beats/beats.json` plus **6 beats**. Each one is an **intro** (2 filtered bars and a riser, played once) and a **48-bar arranged loop** (`.mp3`, 80–130 s). All audio is synthesised from code, so we own 100% of it.
  - **Eski**: grime, 140 BPM (free)
  - **Dusty**: boom bap, 90 BPM, the beginner beat (free)
  - **Midnight**: drill, 142 BPM (free)
  - **Brass**: soul boom bap with horns, choir and bass guitar, 92 BPM (Pro later; free during beta)
  - **Afterglow**: emotional garage with chopped vocals and piano, 132 BPM (Pro later)
  - **Foundry**: sparse left-field hip-hop with metal percussion and dissonant chords, 100 BPM (Pro later)
- Every loop follows the same arrangement, listed in `sections` in `beats.json`: **A (8 bars) → A2 (8) → BREAK (4) → BUILD (4, ending in a one-beat silent gap) → DROP (8) → SWITCH (8) → STRIP (4) → A2 (4)**, then back to A. There are volume moves, fills every 4 and 8 bars, and crashes on the drops.
- `words.json`: 40 rhyme chains and 374 words. Each chain has a `sound`, a rhyme `type` (perfect / accent / slant / multi / dialect / cheap) and a one-line `note` explaining why the words rhyme. Each word has a `level` (1 simple, 2 mid, 3 advanced), part of speech and definition. Level 3 words also have an example bar (`ex`).

## Screens

### 0. First-launch walkthrough (4 steps, skippable, reopen from "How it works")
1. **"One word. One beat. You rap."** What the app is, in two sentences.
2. **"Tap anywhere for the next rhyme."** A practice pad you actually tap: drama → karma → farmer → armour. Then it explains that out loud the r goes quiet, which is why they rhyme.
3. **"Tap the word to learn it."** Tap *quotidian* to see its meaning: "saved to your word bank".
4. **"How hard?"** Pick Simple, Mixed or Advanced, each with example words. A tip to turn the volume up and the silent switch off. The **"Drop the beat"** button starts the first session on Dusty, the slowest beat.

Next only unlocks once you've done the step's tap, so nobody reaches a session without knowing the two gestures.

### 1. Home
- **Word of the Day card** at the top: the word, part of speech, its rhyme sound, definition, example bar, and a **"Freestyle with it"** button. That button starts a normal session on your chosen beat, opening on today's word (chip: "WORD OF THE DAY").
  - Picking the word: every level-3 word in a fixed shuffled order, one per local calendar day, so it's the same for everyone and neighbouring days use different rhyme sounds. 108 advanced words is about 3.5 months before it repeats, and new word packs extend it.
  - Free play is untouched. Word of the Day is an option, never forced.
- Big "Today's Cypher" button showing the streak flame and a count, e.g. "🔥 6".
- Beat picker: 6 cards (name, style, BPM), sorted easiest first, that preview on tap, plus a **Your own music** card.
- "Free play" button.
- Small links to Word Bank and Settings.

### 2. Cypher (the main screen)
- Full-bleed black. One word in the centre, **huge** (as big as fits on one line, heavy rounded font, auto-shrink for long words).
- **First-word reveal:** before any sound plays, the first word is already on screen with its definition card open. A chip reads "YOUR FIRST WORD · Multi chain · ED-uh-bul", and the hint "tap anywhere to drop the beat" pulses below. You get as long as you like to think of an opening line.
- **Tap to drop:** the filtered intro plays with the word still up, and the hint counts down ("drop in 4… 3… 2… 1"). On the drop the screen flashes, the haptic hits, and the next-word preview appears. The first word stays, because it's the one you prepared for.
- **Tap anywhere except the word:** go to the next word, with a quick scale-in animation and a light haptic.
- **Tap the word:** a definition card slides up from the bottom (word, part of speech, definition, example bar if present). It fades after 4 seconds or on the next tap. **The beat never stops.** Tapping also saves the word to the Word Bank.
- **Pulse:** the word gently scales (1.0 → 1.04) on every beat, with a bigger pulse on bar 1, synced to the beat clock.
- **New chain:** when the chain changes, a small chip at the top shows the rhyme type (e.g. "SOUND RHYME") with the chain's `note` underneath in small text for 3 seconds. This is how the app teaches rhyme without a tutorial.
- **Next-word preview (setting, on by default):** the upcoming word shows faintly at 25% opacity under the main word, so you can plan a bar ahead.
- Top bar, small and low-contrast: ✕ to end, timer, record toggle (●).
- **End of session:** a summary with time, words seen and words looked up, then **every word from the session** in order, each with its definition and example bar. Words you looked up are tagged, and each row has a **☆ favourite** button. If you recorded, the recording plays at the top.

### 3. Word Bank
- Two tabs: **★ Favourites** and **Looked up**.
- **Favourites:** any word you star (from the summary, the Word of the Day card or the bank). Favourites get 3× weight in normal sessions. **Practise favourites** starts a session where each new chain opens on one of your favourites, so you relearn them in rhyme.
- Every word you tapped, newest first, with its definition and the chain it came from.
- Status: **Learning** (tapped) or **Known**. A word becomes Known once you've seen it 3 times in later sessions without tapping it.
- Tap a word to hear the example bar read with text-to-speech.

### 4. Settings
- **Vocabulary:** a 3-stop slider, **Simple / Mixed / Advanced** (default Mixed). Controls how often advanced words come up.
- **Rhyme style:** Strict (perfect and multi chains only) or **Loose** (everything, the default).
- **Word change:** Tap (default) / Every bar / Every 2 bars. Auto modes change the word exactly on the downbeat.
- **Next-word preview:** on/off.
- **Haptic on beat:** on/off.
- **Daily reminder:** off by default. The app offers it after your first finished session. You pick the time (default 7pm), and the notification shows today's word, e.g. "Today's word: obsidian. Drop a bar on it."
- **Reset progress:** clears the word bank, streak and history, with an in-app confirm step.
- **How it works:** replays the walkthrough.

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
7. **Daily Cypher:** it always opens on the **Word of the Day**. The random seed is the date, so everyone gets the same chains and beat on a given day. It's 3 minutes long, the beat rotates daily, and finishing at least 2 minutes extends the streak. Start the Daily Cypher so its first DROP lands in the first 30 seconds.

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

## Recording: audio or video, only on your phone

- **Record** in a session has three states: **Off / Audio / Video**. Video uses the selfie camera in a small corner preview, so the giant word stays the main thing on screen.
- **Audio:** an `AVAudioEngine` input tap writes the mic to `.m4a`. **Video:** `AVCaptureSession` (front camera + mic) writes `.mov`.
- We log the **exact loop position when recording starts** and a **timestamp for every word shown**. When you play back or export:
  - the beat is mixed under your voice, perfectly in time (offline render / `AVMutableComposition`),
  - for video, the words can appear on screen at the moments they came up (`AVVideoCompositionCoreAnimationTool`). That's the shareable clip.
- **Storage: on the device only.**
  - Files go in the app's `Application Support/Recordings` folder, marked `isExcludedFromBackup = true`, so they never go to iCloud backups either.
  - No uploads and no cloud features. Nothing leaves the phone unless you tap **Share** or **Save to Photos** yourself. (If iCloud Photos is on, Apple syncs Photos; we say this beside the button.)
- A **Recordings** screen lists every take with its date, beat, length and size, plus total storage used. Swipe to delete. Takes are kept until you delete them, with no automatic clean-up.
- Permissions are asked only when you first pick Audio (mic) or Video (camera + mic), never at launch.

## Recording: technical notes

- Show a one-time tip: "Use headphones for a cleaner recording."
- Record the voice (and camera) separately from the beat, then mix at playback or export. That way the beat stays clean and in sync without the speaker feeding back into the mic.
- In **own-music mode** we can't add the beat afterwards, so the mic captures whatever is playing out loud.

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

## Drive mode (CarPlay-safe)

- A toggle in a session ("Drive mode") and an automatic suggestion when CarPlay or car Bluetooth connects.
- Each word is **spoken** with `AVSpeechSynthesizer` half a bar before the downbeat, ducking the beat slightly. There's nothing to read.
- `MPRemoteCommandCenter`: **next track** = next word, **previous track** = say the word again and read its definition, **play/pause** = pause the beat.
- `MPNowPlayingInfoCenter`: the title is the current word, the artist is "Rhyming on AH-muh", the album is the beat name. Steering-wheel buttons and the CarPlay Now Playing screen work without a special entitlement.
- A full CarPlay app (its own icon and browsable beats) needs Apple's **CarPlay audio** entitlement. We'll request it once the app record exists and add a `CPTemplateApplicationSceneDelegate` with a beat list when it's granted.

## Data and storage

- Everything is stored on the device for V1 (SwiftData): Word Bank entries, streak, sessions and settings. No account or backend yet.

## Money: launch free

- **V1 is completely free:** no paywall, no ads, no account. Everything is unlocked, including all 6 beats.
- Why: the app only works if people come back every day. A paywall before anyone has a streak hurts retention and early reviews, and the beats cost us nothing to make.
- First get TestFlight and first-month numbers: day-7 retention, sessions per week, words looked up.
- The first paid feature will be the **AI coach**, the only feature that costs real money each time someone uses it. Possible extras alongside it: themed word packs and unlimited recording history.
- Ignore the `free` flag in `beats.json` for V1.

## Launch checklist

- [x] Privacy policy (`docs/privacy.html`) and support page (`docs/support.html`). They still need a contact email and public hosting.
- [x] App Store text, keywords, age rating answers, privacy label and review notes (`docs/app-store.md`)
- [x] App icon options (`design/icon/`). One needs choosing.
- [x] App Store screenshots at 6.9" (1320×2868) (`design/screenshots/`)
- [ ] Bundle ID, app record and API key secrets
- [ ] Native app, cloud build and TestFlight
- [ ] CarPlay audio entitlement request

## Copy rule

Never frame the app as "British" or "UK" rap, and don't tag words as British or London slang. Explain *why* words rhyme (the r goes quiet, the vowels match, how people actually say it), not *where* the rhyme comes from. Genre names drop the UK prefix: Drill, Garage.

## Not in V1 (planned)

- **Share a clip:** a 15-second vertical video of your recording with the words animating on screen, for TikTok, Reels or Stories. This is how the app spreads, and it should be the first post-launch feature.

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
