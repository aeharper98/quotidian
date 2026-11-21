# Quotidian rhyme chains (hand-curated; rhymes by how words sound out loud, not spelling).
# Line format:  word | level (1 simple, 2 mid, 3 advanced) | part of speech | definition | example bar (level 3)
# type: perfect, accent ("sound rhyme": works out loud because the r after a vowel goes quiet), slant (vowel match),
#       multi (2+ syllables rhyme), dialect (how people actually talk, e.g. ting), cheap (easy rhyme - use sparingly)

CHAINS = [
dict(id="ah-muh", sound="AH-muh", type="accent",
     note="Say them out loud: the r in 'farmer' and 'armour' goes quiet, so they land right on 'drama'.",
     words="""
drama|1|noun|Exciting, emotional events, or a play for stage or screen.
karma|1|noun|The idea that what you put out comes back to you.
farmer|1|noun|Someone who runs a farm.
armour|1|noun|Protective metal covering worn in battle.
charmer|1|noun|Someone who wins people over easily.
llama|1|noun|A long-necked South American animal, related to the camel.
pyjamas|1|noun|Loose clothes you sleep in.
melodrama|2|noun|Over-the-top emotion, like a soap opera.
panorama|3|noun|A wide, unbroken view of a whole area.|Top floor of the block, I'm taking in the panorama
dharma|3|noun|In Hindu and Buddhist thought, your true duty or path in life.|Stay on my dharma, I don't need the drama
"""),
dict(id="aw-duh", sound="AW-duh", type="accent",
     note="Out loud, 'order' sounds like 'aw-duh', a near-perfect match for 'water'. The t and d are close enough.",
     words="""
water|1|noun|The clear liquid that falls as rain and fills rivers and seas.
order|1|noun|A request for something, or things arranged neatly.
border|1|noun|The line where one country or area ends and another begins.
daughter|1|noun|Someone's female child.
quarter|1|noun|One of four equal parts.
recorder|1|noun|A device that records sound, or a simple wooden flute.
supporter|1|noun|A fan, or someone who backs you.
slaughter|2|verb|To kill brutally, or to beat someone heavily.
mortar|2|noun|The paste that holds bricks together.
hoarder|2|noun|Someone who stores up far more than they need.
marauder|3|noun|A raider who roams around looking for things to steal.|Roll through the ends like a marauder, no order
"""),
dict(id="id-ee-un", sound="ID-ee-un", type="multi",
     note="A multi: three syllables rhyme in a row (ID-ee-un). Long words like these sound clever because the whole tail of the word matches.",
     words="""
video|1|noun|Recorded moving pictures.
idiot|1|noun|A very foolish person.
hideous|1|adjective|Extremely ugly.
idiom|2|noun|A phrase whose meaning isn't literal, like 'spill the tea'.
quotidian|3|adjective|Everyday, ordinary, part of daily life.|Bars are quotidian, I spit 'em like it's every day, see
obsidian|3|noun|Shiny black glass formed when lava cools fast.|Cold heart, black ice, mind sharp like obsidian
meridian|3|noun|An imaginary line from pole to pole; also the peak of something.|Greenwich meridian, I'm the line that the time's on
insidious|3|adjective|Harmful in a slow, sneaky way you don't notice at first.|Doubt is insidious, creeps in like it's hideous
perfidious|3|adjective|Disloyal; ready to betray people.|Perfidious man, you'd sell your mates for a video
fastidious|3|adjective|Very fussy about details and doing things properly.|Fastidious with the flow, every syllable placed
invidious|3|adjective|Unfair, and likely to cause resentment.|Comparing me to them? That's invidious, bro
viridian|3|noun|A deep blue-green colour.|Viridian waves when the beat goes oceanic
"""),
dict(id="an-dum", sound="AN-dum", type="slant",
     note="Assonance: the vowels match (AN-uh) and the consonants just sit close. It's about sound, not spelling, and it's what most great flows run on.",
     words="""
random|1|adjective|Happening without a plan or pattern.
anthem|1|noun|A song people sing together with pride.
handsome|1|adjective|Good-looking.
panda|1|noun|A black-and-white bear from China.
mandem|1|slang|A group of guys; your friends (slang).
ransom|2|noun|Money demanded to free someone held captive.
phantom|2|noun|A ghost, or something that isn't really there.
tandem|2|noun|Two things working together, side by side.
fandom|2|noun|All the fans of something, as a community.
propaganda|2|noun|Biased information spread to push a point of view.
candour|3|noun|Being open, honest and frank.|Speak with candour, no propaganda
memorandum|3|noun|A written note, often an official record or agreement.|Sign the memorandum, me and the mandem
"""),
dict(id="ing", sound="ING", type="dialect",
     note="Said casually, 'thing' becomes 'ting'. Freestylers rhyme on how they actually talk, not how it's written.",
     words="""
thing|1|noun|An object, or a matter or situation.
ting|1|slang|Slang for 'thing'.
ring|1|noun|A circle, often jewellery worn on a finger.
king|1|noun|A male ruler of a country.
sting|1|verb|To cause a sharp pain.
string|1|noun|Thin cord or thread.
spring|1|noun|The season after winter, or a coiled bit of metal.
plaything|1|noun|A toy, or someone treated like one.
offspring|2|noun|A person's or animal's children.
wellspring|3|noun|A rich, never-ending source of something.|My mind's a wellspring, every bar's a new ting
underling|3|noun|Someone low-ranking who takes orders.|You're an underling, I'm the one that crowned the king
"""),
dict(id="ay-shun", sound="AY-shun", type="cheap",
     note="The easiest rhyme in English. Fine for warming up, but crowds hear '-ation' coming. Try landing a rarer word instead.",
     words="""
nation|1|noun|A country and its people.
station|1|noun|A place where trains or buses stop.
patience|1|noun|Being able to wait calmly.
vacation|1|noun|A holiday.
frustration|1|noun|Feeling annoyed because you can't do something.
imagination|1|noun|The ability to picture things in your mind.
procrastination|2|noun|Putting off things you should do now.
trepidation|3|noun|Nervous fear about something coming up.|Step to the mic with no trepidation
veneration|3|noun|Deep respect, almost worship.|Give the OGs veneration
conflagration|3|noun|A huge, destructive fire.|Bars spread like a conflagration
abnegation|3|noun|Giving up something you want, often for others.|Self-abnegation, I give it all to the station
equivocation|3|noun|Being deliberately vague to avoid committing.|Straight talk, no equivocation
"""),
dict(id="ed-uh-bul", sound="ED-uh-bul", type="multi",
     note="Match the stressed vowel (ED), then let '-uh-bul' carry the rest. 'Impeccable' still works because 'EK' is close to 'ED'.",
     words="""
incredible|1|adjective|Amazing, hard to believe.
edible|1|adjective|Safe to eat.
medical|1|adjective|To do with medicine and health.
unforgettable|1|adjective|So memorable you can't forget it.
credible|2|adjective|Believable, trustworthy.
regrettable|2|adjective|Unfortunate; something you'd wish hadn't happened.
indelible|3|adjective|Impossible to remove or forget.|Ink on the page is indelible
ineffable|3|adjective|Too great or intense to put into words.|The feeling's ineffable, flow's incredible
impeccable|3|adjective|Flawless.|Timing's impeccable, every bar's edible
"""),
dict(id="ish-un", sound="ISH-un", type="perfect",
     note="A clean perfect rhyme, but the advanced words are where the points are. 'Erudition' beats 'mission' every time.",
     words="""
mission|1|noun|An important task or goal.
vision|1|noun|Sight, or a clear idea of the future.
decision|1|noun|A choice you've made.
ambition|1|noun|A strong desire to succeed.
position|1|noun|Where someone or something is.
tradition|1|noun|A custom passed down through generations.
superstition|2|noun|A belief in luck or magic without evidence.
acquisition|2|noun|Something you've gained or bought.
erudition|3|noun|Deep knowledge from lots of study.|Pure erudition, I study the vision
attrition|3|noun|Wearing something down gradually.|War of attrition, I outlast the competition
sedition|3|noun|Speech or action stirring up rebellion against the state.|They call it sedition, I call it my mission
premonition|3|noun|A feeling that something's about to happen.|Had a premonition I'd win this position
"""),
dict(id="ee-ree-us", sound="EER-ee-us", type="multi",
     note="Three syllables to match: the stressed vowel, then 'ee-us'. 'Curious' and 'serious' have slightly different vowels but ride together fine.",
     words="""
serious|1|adjective|Not joking; important.
curious|1|adjective|Wanting to know or learn things.
furious|1|adjective|Extremely angry.
mysterious|1|adjective|Strange and hard to explain.
delirious|2|adjective|Confused and wild, from illness or excitement.
luxurious|2|adjective|Very comfortable and expensive.
imperious|3|adjective|Bossy and arrogant, acting like a ruler.|Imperious, I rule the room, I'm serious
spurious|3|adjective|Fake, or based on bad reasoning.|Your claims are spurious, that's why I'm furious
penurious|3|adjective|Extremely poor, or very stingy.|Penurious past but the future's luxurious
injurious|3|adjective|Causing harm or damage.|Bars injurious, keep it curious
"""),
dict(id="op-ik", sound="OP-ik", type="slant",
     note="'Pocket' and 'topic' don't match on paper, but say them quickly and they're close. Mosaic rhymes like 'stop it' use two words to match one.",
     words="""
topic|1|noun|The subject being talked about.
pocket|1|noun|A small pouch sewn into clothes.
rocket|1|noun|A vehicle that flies into space.
stop it|1|phrase|Quit doing that.
drop it|1|phrase|Let it fall, or release something new.
tropic|2|noun|The hot region either side of the equator.
microscopic|2|adjective|Too small to see without a microscope.
myopic|3|adjective|Short-sighted, literally or in thinking.|Your view's myopic, I see past the topic
philanthropic|3|adjective|Generous; giving to good causes.|Philanthropic with the bars, take one for your pocket
misanthropic|3|adjective|Disliking people in general.|Misanthropic mood, so I'm leaving in a rocket
kaleidoscopic|3|adjective|Colourful and constantly changing.|Flow's kaleidoscopic, every bar a new topic
"""),
dict(id="en-tul", sound="EN-tul", type="perfect",
     note="Perfect rhyme on 'EN-tul'. Long words ending in '-mental' let you stack three or four syllables of rhyme.",
     words="""
mental|1|adjective|To do with the mind; also slang for crazy.
rental|1|noun|Something you pay to use for a while.
dental|1|adjective|To do with teeth.
gentle|1|adjective|Kind and soft.
central|1|adjective|In the middle; most important.
instrumental|2|noun|A track with no vocals.
sentimental|2|adjective|Driven by feelings and nostalgia.
monumental|2|adjective|Huge, very important.
detrimental|3|adjective|Causing harm.|Doubting me's detrimental, my flow's monumental
transcendental|3|adjective|Beyond normal experience; spiritual.|Transcendental on the instrumental
incidental|3|adjective|Happening alongside something bigger; minor.|Fame's incidental, the bars are fundamental
"""),
dict(id="ish-us", sound="ISH-us", type="perfect",
     note="A goldmine of advanced vocab. Every one of these ends in 'ISH-us', so once you find the vowel the rhyme is free.",
     words="""
vicious|1|adjective|Cruel or violent.
delicious|1|adjective|Tastes really good.
ambitious|1|adjective|Determined to succeed.
suspicious|1|adjective|Not trusting; or seeming dodgy.
nutritious|1|adjective|Good for your body.
malicious|2|adjective|Meaning to cause harm.
fictitious|2|adjective|Made up, not real.
auspicious|3|adjective|A good sign that things will go well.|Auspicious start, the beat's delicious
capricious|3|adjective|Changing mood or mind suddenly.|Capricious crowd, so my flow stays vicious
avaricious|3|adjective|Greedy for money.|Avaricious? Nah, I'm just ambitious
expeditious|3|adjective|Quick and efficient.|Expeditious with the bars, no time to be suspicious
surreptitious|3|adjective|Done secretly so no one notices.|Surreptitious, slid in quiet, now I'm vicious
"""),
dict(id="air-ee-us", sound="AIR-ee-us", type="multi",
     note="Three-syllable multi. Get the 'AIR' sound right and four words in a row will sound planned.",
     words="""
hilarious|1|adjective|Extremely funny.
various|1|adjective|Several different kinds.
Aquarius|2|noun|A star sign, the water carrier.
nefarious|3|adjective|Wicked, criminal.|Nefarious plans, but the bars are hilarious
precarious|3|adjective|Shaky; likely to collapse.|Your position's precarious
gregarious|3|adjective|Sociable; loves being around people.|Gregarious, I'm with the mandem in various
vicarious|3|adjective|Felt through someone else's experience.|Live vicarious through my bars, it's hilarious
"""),
dict(id="uh-ul", sound="UH-ul", type="slant",
     note="Mixing 'subtle', 'trouble' and 'struggle' works because the vowel (UH) is identical. The middle consonant can change.",
     words="""
trouble|1|noun|Difficulty or problems.
double|1|adjective|Twice as much.
bubble|1|noun|A ball of air in liquid.
struggle|1|noun|A hard effort against difficulty.
juggle|1|verb|To handle several things at once.
cuddle|1|verb|To hug lovingly.
puddle|1|noun|A small pool of rainwater.
subtle|2|adjective|Delicate, not obvious.
rubble|2|noun|Broken stone from a ruined building.
kerfuffle|2|noun|A fuss or commotion.
rebuttal|3|noun|An argument that disproves another.|Here's my rebuttal, it's subtle but it's trouble
befuddle|3|verb|To confuse completely.|Wordplay to befuddle, leave 'em in a muddle
"""),
dict(id="ime", sound="IME", type="perfect",
     note="One-syllable perfect rhymes are easy to hit, so use them to land the end of a line hard.",
     words="""
time|1|noun|What clocks measure.
rhyme|1|noun|Words that end with the same sound.
crime|1|noun|An illegal act.
climb|1|verb|To go up.
prime|1|adjective|The best; at your peak.
sublime|2|adjective|So excellent it's almost spiritual.
pantomime|2|noun|A comic Christmas stage show where the audience shouts along.
paradigm|3|noun|A model or way of seeing things.|Shift the paradigm every time I rhyme
maritime|3|adjective|To do with the sea and ships.|Maritime flow, I'm sailing through time
"""),
dict(id="al-uh-ree", sound="AL-uh-ree", type="multi",
     note="Three syllables, stress on the first. 'Battery' and 'flattery' swap AL for AT, and the ear still accepts it.",
     words="""
salary|1|noun|Pay you get for a job.
gallery|1|noun|A place that shows art.
calorie|1|noun|A unit of energy in food.
galaxy|1|noun|A huge system of stars.
battery|1|noun|Stores power for devices.
flattery|2|noun|Over-the-top praise.
cavalry|2|noun|Soldiers on horseback; help arriving.
fallacy|3|noun|A mistaken belief or faulty argument.|Your flow's a fallacy, mine's from a galaxy
alchemy|3|noun|A magical-seeming transformation.|Turn words into gold, call it alchemy
"""),
dict(id="ok-ruh-see", sound="OK-ruh-see", type="multi",
     note="Four syllables matching (OK-ruh-see). 'Philosophy' only partly fits, but the rhythm sells it.",
     words="""
democracy|1|noun|Government chosen by the people.
Socrates|1|noun|An ancient Greek philosopher.
monopoly|1|noun|Total control of a market; also a board game.
hypocrisy|2|noun|Saying one thing, doing another.
philosophy|2|noun|The study of big questions about life.
bureaucracy|3|noun|A system weighed down by officials and rules.|Cut the bureaucracy, skip the hypocrisy
autocracy|3|noun|Rule by one person with total power.|Mic's my autocracy, no democracy
aristocracy|3|noun|The highest social class; nobles.|Not born in the aristocracy
meritocracy|3|noun|A system where people rise by ability.|Freestyle's a meritocracy
theocracy|3|noun|A state ruled by religious leaders.|Mic is my church, call it theocracy
"""),
dict(id="ort", sound="ORT / AWT", type="accent",
     note="Out loud, 'caught' and 'court' can sound identical, because the r goes quiet. Spelling hides rhymes like this.",
     words="""
short|1|adjective|Not long or tall.
sport|1|noun|A competitive game or activity.
caught|1|verb|Grabbed, or found doing something.
taught|1|verb|Showed someone how to do something.
thought|1|noun|An idea in your head.
court|1|noun|Where trials happen, or where you play tennis.
astronaut|1|noun|Someone who travels to space.
fraught|3|adjective|Full of tension or worry.|Fraught with nerves but I'm never caught short
distraught|3|adjective|Extremely upset.|Left 'em distraught with a single thought
juggernaut|3|noun|A huge, unstoppable force; also a big lorry.|Juggernaut flow, can't be stopped or caught
onslaught|3|noun|A fierce, overwhelming attack.|Bar onslaught, every line's taught
"""),
dict(id="aw", sound="AW", type="accent",
     note="'Saw', 'sore' and 'soar' can all sound the same out loud. That opens up hundreds of extra rhymes.",
     words="""
more|1|adjective|A greater amount.
floor|1|noun|What you stand on.
war|1|noun|Armed conflict.
saw|1|verb|Looked at; or a cutting tool.
raw|1|adjective|Uncooked; or real and unpolished.
core|1|noun|The central part.
encore|2|noun|An extra performance because the crowd wants more.
folklore|2|noun|Traditional stories and beliefs.
carnivore|2|noun|A meat-eater.
rapport|3|noun|A close, easy connection with people.|Got rapport with the crowd, they're screaming for more
abhor|3|verb|To hate intensely.|Fake MCs I abhor, keep it raw
"""),
dict(id="ah", sound="AH", type="accent",
     note="'Star', 'spa' and 'memoir' all end on the same open 'ah', so French borrowings fit right in.",
     words="""
star|1|noun|A burning sun far away; or a famous person.
car|1|noun|A vehicle with four wheels.
bar|1|noun|A line of rap; or a place to drink.
far|1|adjective|A long way away.
spa|1|noun|A place for relaxing treatments.
avatar|2|noun|An icon or character that represents you.
bazaar|2|noun|A market with lots of stalls.
memoir|3|noun|A book of someone's own memories.|Every bar's a page of my memoir
repertoire|3|noun|The full range of things someone can perform.|Deep repertoire, I'm a star
faux pas|3|noun|An embarrassing social slip.|Biting my flow? That's a faux pas
"""),
dict(id="oo-shun", sound="OO-shun", type="perfect",
     note="Perfect rhyme. Advanced words add weight, because 'retribution' hits harder than 'solution'.",
     words="""
solution|1|noun|The answer to a problem.
pollution|1|noun|Dirt and poison in the environment.
revolution|1|noun|A big change or uprising.
evolution|2|noun|Gradual development over time.
constitution|2|noun|A country's founding rules; or your health.
retribution|3|noun|Punishment as payback.|Bars are retribution
absolution|3|noun|Formal forgiveness.|No absolution, this is evolution
dissolution|3|noun|The breaking up or ending of something.|Dissolution of your crew, that's the solution
restitution|3|noun|Paying back for something lost or stolen.|Want restitution for the bars you took
"""),
dict(id="ip-tik", sound="IP-tik", type="slant",
     note="Mosaic rhyme: 'flipped it' (two words) rhymes with 'cryptic' (one word). Splitting a rhyme across words is a key freestyle skill.",
     words="""
flipped it|1|phrase|Turned it over; changed it up.
ripped it|1|phrase|Tore it; or performed brilliantly.
script it|1|phrase|Plan it out in advance.
cryptic|2|adjective|Mysterious, hidden meaning.
elliptical|2|adjective|Oval-shaped; or leaving words out.
apocalyptic|3|adjective|Like the end of the world.|Apocalyptic flow, I didn't script it
triptych|3|noun|An artwork in three panels.|Three bars, a triptych, cryptic
"""),
dict(id="ess-iv", sound="ESS-iv", type="perfect",
     note="Perfect rhyme. All adjectives, so you can describe yourself or your opponent in a chain.",
     words="""
aggressive|1|adjective|Ready to attack.
impressive|1|adjective|Deserving admiration.
excessive|1|adjective|Too much.
obsessive|2|adjective|Can't stop thinking about something.
progressive|2|adjective|Favouring change and new ideas.
possessive|2|adjective|Wanting to own or control.
oppressive|3|adjective|Harsh and controlling; or heavy and stifling.|Heat's oppressive, flow's impressive
transgressive|3|adjective|Breaking social or moral rules.|Transgressive bars, a bit aggressive
"""),
dict(id="en-shun", sound="EN-shun", type="perfect",
     note="'Pretentious' adds 'us' but keeps the EN-shun core. A slightly longer word still counts.",
     words="""
tension|1|noun|Stress or tightness.
mention|1|verb|To say something briefly.
attention|1|noun|Focus or notice.
invention|1|noun|Something newly created.
dimension|2|noun|A measurement; or a whole other world.
pretentious|2|adjective|Trying to seem more important than you are.
contentious|3|adjective|Likely to cause an argument.|Contentious bars, I get attention
apprehension|3|noun|Worry about what might happen.|Apprehension, you can feel the tension
condescension|3|noun|Talking down to people.|Your condescension, I don't even mention
"""),
dict(id="ark", sound="ARK", type="perfect",
     note="Single-syllable punch. Words like 'matriarch' put the rhyme on a syllable that isn't stressed, which gives a cool off-beat feel.",
     words="""
dark|1|adjective|Without light.
park|1|noun|A green public space.
mark|1|noun|A sign, score or stain.
spark|1|noun|A tiny flash of fire.
shark|1|noun|A big predatory fish.
lark|2|noun|A bit of fun; also a songbird.
monarch|2|noun|A king or queen.
embark|2|verb|To begin a journey.
matriarch|3|noun|A woman who heads a family or group.|Nan's the matriarch, she lit the spark
patriarch|3|noun|A man who heads a family or group.|Patriarch talk, but you're a lark
oligarch|3|noun|One of a small group of rich, powerful people.|Flow like an oligarch, money in the dark
"""),
dict(id="ail", sound="AIL", type="perfect",
     note="Perfect rhyme. Advanced verbs like 'curtail' and 'regale' make your bars sound deliberate.",
     words="""
fail|1|verb|To not succeed.
mail|1|noun|Letters and parcels.
scale|1|noun|Size or level; or a fish's skin plate.
tale|1|noun|A story.
jail|1|noun|Prison.
inhale|1|verb|To breathe in.
prevail|2|verb|To win in the end.
regale|3|verb|To entertain someone with stories.|I regale 'em with a tale
curtail|3|verb|To cut short or limit.|Try to curtail me, I prevail
assail|3|verb|To attack fiercely.|Assail the mic, I never fail
"""),
dict(id="ite", sound="ITE", type="perfect",
     note="Hugely common rhyme sound. Reach for 'erudite' or 'contrite' to stand out.",
     words="""
night|1|noun|The dark hours.
light|1|noun|Brightness that lets you see.
fight|1|verb|To battle.
write|1|verb|To put words down.
dynamite|1|noun|An explosive.
despite|2|preposition|Even though.
parasite|2|noun|Something that lives off another.
erudite|3|adjective|Very learned and well-read.|Erudite, I read all night
contrite|3|adjective|Truly sorry for doing wrong.|Not contrite, I'm right
trite|3|adjective|Overused and unoriginal.|Your bars are trite, mine are dynamite
"""),
dict(id="ay-shus", sound="AY-shus", type="multi",
     note="'Contagious' and 'tenacious' differ on one consonant (j vs sh), which is close enough. A crowd hears the vowel.",
     words="""
gracious|1|adjective|Kind and polite.
spacious|1|adjective|Roomy.
contagious|1|adjective|Spreads from person to person.
outrageous|1|adjective|Shocking.
courageous|1|adjective|Brave.
audacious|3|adjective|Boldly daring; cheeky.|Audacious, contagious, flow's outrageous
tenacious|3|adjective|Determined; never lets go.|Tenacious, I'm courageous
loquacious|3|adjective|Very talkative.|Loquacious, I talk 'til the room's spacious
vivacious|3|adjective|Lively and full of energy.|Vivacious crowd, the energy's contagious
sagacious|3|adjective|Wise, with good judgement.|Sagacious with the bars, gracious
advantageous|3|adjective|Giving you an edge.|Home crowd's advantageous
"""),
dict(id="ar-kee", sound="AR-kee", type="accent",
     note="Say 'khaki' as 'KAH-kee' and it lands on 'snarky'. How you pronounce a word can unlock a rhyme.",
     words="""
khaki|1|noun|A dull yellow-brown colour.
snarky|1|adjective|Sarcastic and rude.
sparky|1|slang|An electrician (UK); or lively.
anarchy|2|noun|No government or rules; chaos.
monarchy|2|noun|Rule by a king or queen.
hierarchy|2|noun|A ranking from top to bottom.
malarkey|3|noun|Nonsense.|None of that malarkey, khaki
oligarchy|3|noun|Rule by a small, powerful group.|Break the oligarchy, bring anarchy
"""),
dict(id="ust", sound="UST", type="perfect",
     note="Perfect rhyme. Note 'august' (an adjective with stress on the second syllable) versus 'August' the month.",
     words="""
trust|1|noun|Belief in someone's honesty.
dust|1|noun|Fine dirt.
must|1|verb|Have to.
rust|1|noun|Orange decay on metal.
disgust|1|noun|Strong dislike.
robust|2|adjective|Strong and sturdy.
unjust|2|adjective|Unfair.
august|3|adjective|Respected and impressive (stress on 'GUST').|August company, I earned their trust
wanderlust|3|noun|A strong desire to travel.|Wanderlust, leave the haters in the dust
"""),
dict(id="ole", sound="OLE", type="perfect",
     note="Perfect rhyme with some brilliant vocab. 'Rigmarole' is a great word to drop.",
     words="""
soul|1|noun|Your inner self.
goal|1|noun|An aim; or scoring in football.
roll|1|verb|To turn over and over.
control|1|noun|Power over something.
hole|1|noun|A gap or opening.
parole|2|noun|Early release from prison.
cajole|3|verb|To persuade by flattery.|Cajole the crowd, take control
rigmarole|3|noun|A long, pointless, complicated process.|Skip the rigmarole, straight to the goal
"""),
dict(id="az-um", sound="AZ-um", type="slant",
     note="Two syllables, stress on the first. Pairs with mosaic rhymes like 'has 'em' and 'smash 'em'.",
     words="""
sarcasm|1|noun|Saying the opposite of what you mean to mock.
enthusiasm|1|noun|Eager excitement.
spasm|2|noun|A sudden, uncontrolled muscle movement.
chasm|2|noun|A deep crack in the ground; a huge gap.
phantasm|3|noun|An illusion or ghostly image.|Phantasm flow, I vanish, no sarcasm
"""),
dict(id="ack", sound="ACK", type="perfect",
     note="Short and punchy. Long words ending in '-iac' put the rhyme at the very end, which makes a strong closer.",
     words="""
back|1|noun|The rear; or support.
track|1|noun|A song; or a path.
black|1|adjective|The darkest colour.
crack|1|verb|To break slightly.
attack|1|verb|To go after.
knack|2|noun|A natural skill.
maniac|2|noun|A wild person.
cul-de-sac|2|noun|A dead-end street.
almanac|3|noun|A yearly book of facts and dates.|Write my name in the almanac
hypochondriac|3|noun|Someone always worried they're ill.|Bars so sick, I'm a hypochondriac
"""),
dict(id="oh-shun", sound="OH-shun", type="perfect",
     note="Perfect rhyme. 'Explosion' and 'erosion' swap sh for zh, which is still close.",
     words="""
ocean|1|noun|A huge body of saltwater.
motion|1|noun|Movement.
potion|1|noun|A magic drink.
emotion|1|noun|A feeling.
lotion|1|noun|Cream for your skin.
devotion|2|noun|Deep commitment.
commotion|2|noun|A noisy disturbance.
erosion|2|noun|Slow wearing away.
locomotion|3|noun|The ability to move from place to place.|Pure locomotion, my flow's an ocean
"""),
dict(id="ink", sound="INK", type="perfect",
     note="One syllable. 'Hoodwink' gives you a two-syllable word that still lands on the rhyme.",
     words="""
think|1|verb|To use your mind.
drink|1|noun|Something to swallow.
link|1|noun|A connection.
pink|1|adjective|A light red colour.
wink|1|verb|To close one eye quickly.
brink|2|noun|The very edge.
extinct|2|adjective|No longer existing.
hoodwink|3|verb|To trick or deceive.|Can't hoodwink me, I think
"""),
dict(id="in-ing", sound="IN-ing", type="perfect",
     note="Two syllables, stress on IN. 'Underpinning' rhymes on its last two syllables, which is a quiet flex.",
     words="""
winning|1|verb|Coming first.
spinning|1|verb|Turning round and round.
beginning|1|noun|The start.
grinning|1|verb|Smiling widely.
pinning|1|verb|Fixing in place.
underpinning|3|noun|The foundation that holds something up.|Faith is the underpinning, that's why I'm winning
"""),
dict(id="own", sound="OWN (as in crown)", type="perfect",
     note="Perfect rhyme. Compound words like 'showdown' are easy multis.",
     words="""
town|1|noun|A small city.
down|1|adverb|Towards the ground.
crown|1|noun|What a king wears.
frown|1|noun|An unhappy face.
clown|1|noun|A comic performer.
showdown|2|noun|A final confrontation.
renown|3|noun|Fame and respect.|Renown in the town, I wear the crown
"""),
dict(id="ead", sound="ED", type="perfect",
     note="One syllable, perfect rhyme. 'Figurehead' rhymes only its final syllable, which still works on the beat.",
     words="""
head|1|noun|The top of your body.
bread|1|noun|A baked food; also slang for money.
said|1|verb|Spoke.
red|1|adjective|The colour of blood.
instead|1|adverb|As an alternative.
widespread|2|adjective|Found everywhere.
thoroughbred|2|noun|A pure-bred horse; or a top-quality person.
figurehead|3|noun|A leader in name only, with no real power.|You're a figurehead, I'm the one that's said
"""),
dict(id="ee-zun", sound="EE-zun", type="perfect",
     note="Two syllables. 'Freezing' and 'squeezing' swap n for ng, and they ride along fine.",
     words="""
reason|1|noun|A cause or explanation.
season|1|noun|A time of year.
freezing|1|adjective|Very cold.
pleasing|1|adjective|Satisfying.
treason|2|noun|Betraying your own country.
"""),
dict(id="em-uh-rul", sound="EM-uh-rul", type="slant",
     note="A soft multi: three syllables with a matching vowel. 'General' and 'several' fit even though spelling differs.",
     words="""
general|1|adjective|Broad, not specific; or an army leader.
several|1|adjective|More than two but not many.
federal|2|adjective|To do with a central government.
ephemeral|3|adjective|Lasting a very short time.|Fame's ephemeral, bars are general
"""),
]
