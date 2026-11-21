# App Store listing and review answers

Copy these into App Store Connect. Character limits were checked by script (see the bottom of this file).

## Name, subtitle, category
- **Name (30):** Quotidian: Freestyle Rap
- **Subtitle (30):** Learn rhymes & new words daily
- **Primary category:** Music · **Secondary:** Education
- **Bundle ID:** _to decide_
- **Price:** Free. No in-app purchases in V1.

## Promotional text (170)
A word appears. The beat drops. You rap. Freestyle practice that rhymes the British way and teaches you a new word every day.

## Keywords (100)
freestyle,rap,rhyme,vocabulary,words,beats,lyrics,grime,battle,hiphop,bars,flow,dictionary,learn,uk

## Description (4000)
A word appears. The beat drops. You rap.

Quotidian is a daily freestyle trainer. You get one big word on a black screen and an original beat. Rap a line that lands on the word, then tap anywhere for the next one. It rhymes with the last, so your bars rhyme too.

RHYMES THE BRITISH WAY
Quotidian rhymes by sound, the way UK MCs do. In a British accent "karma", "farmer" and "armour" all rhyme, and so do "caught" and "court". You'll learn slant rhymes, multis and accent rhymes as you go, with a one-line note each time the rhyme sound changes.

LEARN A WORD WHILE YOU RAP
Tap the word to see what it means. The beat keeps going. Words you look up go into your word bank and come back in later sessions until you know them. Pick Simple, Mixed or Advanced vocabulary. Advanced brings in words like obsidian, rigmarole and quotidian.

A NEW WORD EVERY DAY
Every day there's a Word of the Day. Start a freestyle with it, or take on the 3-minute Daily Cypher, which opens on it, to keep your streak.

SIX ORIGINAL BEATS
Grime, boom bap, UK drill, soul, UK garage and left-field hip-hop. Each one is a full arrangement with breakdowns, build-ups and drops, and the rhyme sound switches right on the drop.

OR YOUR OWN MUSIC
Play Spotify or Apple Music in the background and set the tempo. Quotidian stays silent and keeps your music playing.

DRIVE MODE
Hear each word spoken over the beat and skip with your steering-wheel controls.

RECORD YOURSELF
Turn on recording to hear your freestyle back over the beat.

No account. No ads. No tracking. Everything stays on your phone.

## What's New (first release)
First release. Drop a beat, get a word, start rapping.

## URLs
- **Support URL:** _hosted docs/support.html_
- **Privacy Policy URL:** _hosted docs/privacy.html_
- **Marketing URL (optional):** none

## App Privacy ("nutrition label")
- **Data collection:** "No, we do not collect data from this app."
- Reason: all data (word bank, settings, streak, recordings) stays on the device. No analytics SDKs and no third-party SDKs.

## Age rating questionnaire (answers)
- Cartoon or fantasy violence: **None**
- Realistic violence: **None.** A few vocabulary words *describe* violence (e.g. slaughter, assail, onslaught) in dictionary definitions. There are no depictions.
- Profanity or crude humour: **None**
- Mature or suggestive themes: **None**
- Horror or fear themes: **None**
- Medical or treatment information: **None**
- Alcohol, tobacco, drugs: **None**
- Sexual content or nudity: **None**
- Gambling, contests: **None**
- Unrestricted web access: **No**
- User-generated content shared with others: **No** (recordings stay on device; sharing goes through the iOS share sheet)
- Messaging or chat: **No** · Advertising: **No** · Parental controls: **No** · Age assurance: **No**
- **Expected rating: 4+.** We're happy to set 9+ manually if we want to be cautious about the battle-rap tone of a few example bars.

## Permission prompts (Info.plist)
- **NSMicrophoneUsageDescription:** "Quotidian records your freestyle so you can play it back over the beat. Recordings stay on your phone."
- **Notifications** (requested from Settings, not at launch). Pre-prompt in the app: "Get a daily reminder with your Word of the Day?"

## Daily reminder copy (rotates)
- "Today's word: **{word}**. Drop a bar on it."
- "{word}: {short definition}. You've got 3 minutes."
- "Your {n}-day streak is waiting. Today's word is {word}."

## Notes for App Review
Quotidian is a freestyle rap practice app. Tap Free play (or finish the 4-step walkthrough) to start. The first word appears with its definition, and you tap anywhere to start the beat. Tap anywhere for the next rhyme, and tap the word itself for its definition. All beats are original audio synthesised by the developer. There are no accounts, logins or in-app purchases. "Your own music" mode deliberately mixes with other apps' audio, and the microphone is used only when the user turns on recording.

## CarPlay
Drive mode uses the standard Now Playing screen and remote commands (next and previous track). A separate request for the **CarPlay audio** entitlement is filed at developer.apple.com/contact/carplay once the app record exists.
