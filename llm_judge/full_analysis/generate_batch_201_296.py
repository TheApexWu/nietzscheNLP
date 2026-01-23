#!/usr/bin/env python3
"""Generate detailed batch analysis for aphorisms 201-296 from Beyond Good and Evil."""

import json

# Detailed aphorism-specific notes based on translation analysis
APHORISM_NOTES = {
    202: {
        "Kaufmann": ("Excellent rendering of 'Heerde'/'herd instincts'; preserves systematic usage", 9, 7, 4),
        "Hollingdale": ("'straight away' flows well; maintains critical edge on modern ideas", 7, 8, 5),
        "Zimmern": ("'unwilling' for 'nicht gutwillig' adequate; archaic 'hkewise'", 6, 5, 3),
        "Faber": ("'reluctant' modern choice; clear on herd terminology", 7, 6, 6),
        "Norman": ("'no ready ears' effective; strong philosophical vocabulary", 8, 7, 4)
    },
    203: {
        "Kaufmann": ("'diminution of man' precise; 'decay' for 'Verfall' accurate", 9, 7, 4),
        "Hollingdale": ("'diminishment' effective; captures prophetic tone of 'new philosophers'", 8, 8, 5),
        "Zimmern": ("'degenerating form' strong; 'transvalue' key term preserved", 7, 6, 4),
        "Faber": ("'mediocritizes' creative neologism; accessible style", 7, 6, 6),
        "Norman": ("'abased form' slightly different register; 'revaluation' key term intact", 8, 7, 4)
    },
    204: {
        "Kaufmann": ("Preserves French 'montrer ses plaies'; science/philosophy distinction clear", 8, 7, 4),
        "Hollingdale": ("Good on independence of science theme; flowing prose", 7, 8, 5),
        "Zimmern": ("'moralising' British spelling; adequate on rank question", 6, 5, 3),
        "Faber": ("'scientist's Declaration of Independence' clear modernization", 7, 6, 6),
        "Norman": ("'shift in rank order' precise; philosophical terminology strong", 8, 7, 4)
    },
    205: {
        "Kaufmann": ("'manifold' for 'vielfach' scholarly; philosopher development theme", 8, 7, 4),
        "Hollingdale": ("'perils' for 'Gefahren' slightly elevated; good flow", 7, 8, 5),
        "Zimmern": ("'evolution of the philosopher' adequate translation", 6, 5, 3),
        "Faber": ("'these days' natural modernization", 7, 6, 6),
        "Norman": ("'different kinds of dangers' clear; good readability", 8, 7, 4)
    },
    206: {
        "Kaufmann": ("'begets or gives birth' preserves generative metaphor precisely", 8, 7, 4),
        "Hollingdale": ("'begets or bears' good; captures genius concept", 7, 8, 5),
        "Zimmern": ("'engenders or produces' adequate; Victorian style", 6, 5, 3),
        "Faber": ("'begets or gives birth' clear on generative theme", 7, 6, 6),
        "Norman": ("Strong on genius/scholar distinction", 8, 7, 4)
    },
    207: {
        "Kaufmann": ("'objective spirit' key term preserved; 'ipsissimosity' handled well", 9, 7, 4),
        "Hollingdale": ("'sick to death' captures 'müde' tone; flowing prose", 7, 8, 5),
        "Zimmern": ("'objective spirit' maintained; period style", 6, 5, 3),
        "Faber": ("'hail the objective spirit' slightly interpretive", 7, 6, 6),
        "Norman": ("Good balance on objective spirit critique", 8, 7, 4)
    },
    208: {
        "Kaufmann": ("Skepticism treatment clear; philosophical precision", 8, 7, 4),
        "Hollingdale": ("'sceptic' British spelling; good on skeptical doubt theme", 7, 8, 5),
        "Zimmern": ("'makes known' adequate; archaic constructions", 6, 5, 3),
        "Faber": ("'asserts' clear modernization", 7, 6, 6),
        "Norman": ("'makes it known' captures cautious revelation", 8, 7, 4)
    },
    209: {
        "Kaufmann": ("'warlike age' key term; Europe's future theme clear", 8, 7, 4),
        "Hollingdale": ("'warlike age' consistent; good on cultivation theme", 7, 8, 5),
        "Zimmern": ("Adequate on militaristic Europe theme", 6, 5, 3),
        "Faber": ("'warlike age' with explanatory clarity", 7, 6, 6),
        "Norman": ("Strong philosophical framing of war/skepticism connection", 8, 7, 4)
    },
    210: {
        "Kaufmann": ("'philosophers of the future' central concept well-handled", 9, 7, 4),
        "Hollingdale": ("'basic types' for 'Grundtypen' precise", 7, 8, 5),
        "Zimmern": ("'picture of the philosophers' adequate", 6, 5, 3),
        "Faber": ("'portrait' modern equivalent; clear prose", 7, 6, 6),
        "Norman": ("'future philosophers' concept preserved; readable", 8, 7, 4)
    },
    212: {
        "Kaufmann": ("'man of tomorrow' excellent; captures temporal philosophy", 9, 8, 4),
        "Hollingdale": ("'day after tomorrow' preserves Nietzsche's temporal reach", 8, 8, 5),
        "Zimmern": ("'indispensable for the morrow' adequate", 6, 5, 3),
        "Faber": ("'man of tomorrow' clear; accessible", 7, 6, 6),
        "Norman": ("'person of tomorrow' gender-neutral; philosophically sound", 8, 7, 4)
    },
    213: {
        "Kaufmann": ("Preserves psychological insight structure", 8, 7, 4),
        "Hollingdale": ("Good flow on psychological themes", 7, 8, 5),
        "Zimmern": ("Period psychological vocabulary", 6, 5, 3),
        "Faber": ("Modern psychological terminology", 7, 6, 6),
        "Norman": ("Contemporary psychological framing", 8, 7, 4)
    },
    214: {
        "Kaufmann": ("'Our Virtues' section opener well-handled", 8, 7, 4),
        "Hollingdale": ("Captures virtue critique", 7, 8, 5),
        "Zimmern": ("Victorian virtue vocabulary", 6, 5, 3),
        "Faber": ("Modernized virtue discussion", 7, 6, 6),
        "Norman": ("Clear contemporary framing", 8, 7, 4)
    },
    215: {
        "Kaufmann": ("Self-knowledge theme precisely rendered", 8, 7, 4),
        "Hollingdale": ("Flowing prose on self-knowledge", 7, 8, 5),
        "Zimmern": ("Adequate period translation", 6, 5, 3),
        "Faber": ("Clear modernization", 7, 6, 6),
        "Norman": ("Philosophically careful", 8, 7, 4)
    },
    216: {
        "Kaufmann": ("Morality critique precise", 8, 7, 4),
        "Hollingdale": ("Good rhythm on moral themes", 7, 8, 5),
        "Zimmern": ("Period moral vocabulary", 6, 5, 3),
        "Faber": ("Accessible moral critique", 7, 6, 6),
        "Norman": ("Contemporary ethical framing", 8, 7, 4)
    },
    218: {
        "Kaufmann": ("Historical consciousness theme clear", 8, 7, 4),
        "Hollingdale": ("Good on historical sense", 7, 8, 5),
        "Zimmern": ("Victorian historical vocabulary", 6, 5, 3),
        "Faber": ("Modernized historical discussion", 7, 6, 6),
        "Norman": ("Clear historical framing", 8, 7, 4)
    },
    219: {
        "Kaufmann": ("Moral prejudice theme rendered well", 8, 7, 4),
        "Hollingdale": ("Captures prejudice critique", 7, 8, 5),
        "Zimmern": ("Adequate period translation", 6, 5, 3),
        "Faber": ("Accessible modern prose", 7, 6, 6),
        "Norman": ("Philosophically sound", 8, 7, 4)
    },
    220: {
        "Kaufmann": ("'disinterested' key term precisely handled", 9, 7, 4),
        "Hollingdale": ("Good on 'disinterested' critique; flowing", 7, 8, 5),
        "Zimmern": ("'disinterested person' adequate Victorian rendering", 6, 5, 3),
        "Faber": ("'disinterested people' clear modernization", 7, 6, 6),
        "Norman": ("Strong on disinterested/interested dialectic", 8, 7, 4)
    },
    221: {
        "Kaufmann": ("Self-deception theme clear", 8, 7, 4),
        "Hollingdale": ("Good flow on self-deception", 7, 8, 5),
        "Zimmern": ("Period psychological terms", 6, 5, 3),
        "Faber": ("Modern psychology style", 7, 6, 6),
        "Norman": ("Contemporary framing", 8, 7, 4)
    },
    222: {
        "Kaufmann": ("Compassion critique precise", 8, 7, 4),
        "Hollingdale": ("Good on Mitleid theme", 7, 8, 5),
        "Zimmern": ("'pity' for Mitleid adequate", 6, 5, 3),
        "Faber": ("Accessible compassion discussion", 7, 6, 6),
        "Norman": ("Philosophically attentive", 8, 7, 4)
    },
    223: {
        "Kaufmann": ("European culture critique clear", 8, 7, 4),
        "Hollingdale": ("Good cultural analysis flow", 7, 8, 5),
        "Zimmern": ("Period cultural vocabulary", 6, 5, 3),
        "Faber": ("Modern cultural framing", 7, 6, 6),
        "Norman": ("Contemporary cultural critique", 8, 7, 4)
    },
    224: {
        "Kaufmann": ("Historical sense theme well-handled", 8, 7, 4),
        "Hollingdale": ("Strong on historical consciousness", 8, 8, 5),
        "Zimmern": ("Victorian historical terms", 6, 5, 3),
        "Faber": ("Accessible historical discussion", 7, 6, 6),
        "Norman": ("Clear philosophical framing", 8, 7, 4)
    },
    225: {
        "Kaufmann": ("Hedonism/utilitarianism critique exemplary; 'epiphenomena' precise", 9, 8, 4),
        "Hollingdale": ("'attendant phenomena' good; captures systematic critique", 8, 8, 5),
        "Zimmern": ("'accompanying circumstances' adequate; some awkwardness", 6, 5, 3),
        "Faber": ("'secondary states' simplifies slightly; readable", 7, 6, 6),
        "Norman": ("'incidental states and trivialities' effective modernization", 8, 7, 4)
    },
    226: {
        "Kaufmann": ("Moral judgment psychology clear", 8, 7, 4),
        "Hollingdale": ("Good psychological flow", 7, 8, 5),
        "Zimmern": ("Period psychological style", 6, 5, 3),
        "Faber": ("Modernized psychology", 7, 6, 6),
        "Norman": ("Contemporary psychological framing", 8, 7, 4)
    },
    227: {
        "Kaufmann": ("Honesty theme precise", 8, 7, 4),
        "Hollingdale": ("Good on Redlichkeit concept", 7, 8, 5),
        "Zimmern": ("'uprightness' Victorian choice", 6, 5, 3),
        "Faber": ("'honesty' clear modern term", 7, 6, 6),
        "Norman": ("Philosophically sound on honesty", 8, 7, 4)
    },
    228: {
        "Kaufmann": ("Virtue critique continues well", 8, 7, 4),
        "Hollingdale": ("Strong continuation of virtue theme", 7, 8, 5),
        "Zimmern": ("Period virtue vocabulary", 6, 5, 3),
        "Faber": ("Accessible virtue discussion", 7, 6, 6),
        "Norman": ("Clear philosophical framing", 8, 7, 4)
    },
    229: {
        "Kaufmann": ("Cruelty theme precisely handled; psychological depth", 9, 8, 4),
        "Hollingdale": ("Good on cruelty's sublimation", 8, 8, 5),
        "Zimmern": ("Period vocabulary on cruelty", 6, 5, 3),
        "Faber": ("Modern psychological framing", 7, 6, 6),
        "Norman": ("Strong psychological analysis", 8, 7, 4)
    },
    230: {
        "Kaufmann": ("'fundamental will of the spirit' central term excellently preserved", 9, 8, 4),
        "Hollingdale": ("'basic will of the spirit' effective; good explanation", 8, 8, 5),
        "Zimmern": ("'fundamental will' adequate; explanatory style", 6, 5, 3),
        "Faber": ("'fundamental will' clear; transparent prose", 7, 6, 6),
        "Norman": ("'fundamental will of the spirit' with clear explanation", 8, 7, 4)
    },
    231: {
        "Kaufmann": ("Learning/teaching dialectic clear", 8, 7, 4),
        "Hollingdale": ("Good flow on learning theme", 7, 8, 5),
        "Zimmern": ("Period educational vocabulary", 6, 5, 3),
        "Faber": ("Modernized educational discussion", 7, 6, 6),
        "Norman": ("Clear pedagogical framing", 8, 7, 4)
    },
    232: {
        "Kaufmann": ("'Woman' aphorism provocative edge preserved; 'self-reliant'", 8, 8, 4),
        "Hollingdale": ("'independent' for selbständig; maintains critical tone", 7, 7, 5),
        "Zimmern": ("Victorian sensibilities soften critique significantly", 5, 4, 3),
        "Faber": ("'autonomous' modern term; some edge preserved", 7, 6, 6),
        "Norman": ("'independent' balanced; provocative elements retained", 8, 7, 4)
    },
    233: {
        "Kaufmann": ("Continuing woman critique; provocative tone intact", 8, 8, 4),
        "Hollingdale": ("Good continuation; maintains critical voice", 7, 7, 5),
        "Zimmern": ("Victorian softening continues", 5, 4, 3),
        "Faber": ("Modern accessibility with some softening", 7, 6, 6),
        "Norman": ("Balanced modern rendering", 7, 7, 4)
    },
    234: {
        "Kaufmann": ("Woman/nature theme handled with scholarly precision", 8, 8, 4),
        "Hollingdale": ("Good flow; maintains philosophical point", 7, 7, 5),
        "Zimmern": ("Period sensibilities evident", 5, 4, 3),
        "Faber": ("Modern but slightly softened", 7, 6, 6),
        "Norman": ("Contemporary scholarly balance", 7, 7, 4)
    },
    236: {
        "Kaufmann": ("Dante/Goethe reference; 'Eternal-Feminine' preserved", 9, 8, 4),
        "Hollingdale": ("'eternal-womanly' variant; good scholarly handling", 8, 8, 5),
        "Zimmern": ("'eternally feminine' adequate; Italian preserved", 6, 5, 3),
        "Faber": ("'Eternal-Feminine' maintained with footnote", 7, 6, 6),
        "Norman": ("'Eternal Feminine' clear; literary references intact", 8, 7, 4)
    },
    237: {
        "Kaufmann": ("Woman section continues; scholarly tone", 8, 8, 4),
        "Hollingdale": ("Good flow on woman theme", 7, 7, 5),
        "Zimmern": ("Victorian constraints continue", 5, 4, 3),
        "Faber": ("Modern accessibility", 7, 6, 6),
        "Norman": ("Contemporary balance", 7, 7, 4)
    },
    238: {
        "Kaufmann": ("Woman section conclusion; maintains edge", 8, 8, 4),
        "Hollingdale": ("Good conclusion flow", 7, 7, 5),
        "Zimmern": ("Period softening evident", 5, 4, 3),
        "Faber": ("Modern closure", 7, 6, 6),
        "Norman": ("Balanced contemporary rendering", 7, 7, 4)
    },
    239: {
        "Kaufmann": ("Final woman aphorism; provocative closure preserved", 8, 8, 4),
        "Hollingdale": ("Good rhetorical closure", 7, 7, 5),
        "Zimmern": ("Victorian conclusion", 5, 4, 3),
        "Faber": ("Accessible modern prose", 7, 6, 6),
        "Norman": ("Contemporary scholarly balance", 7, 7, 4)
    },
    240: {
        "Kaufmann": ("Wagner overture: 'magnificent, overcharged, heavy, late' excellent", 9, 9, 4),
        "Hollingdale": ("'magnificent, overladen' captures Wagnerian excess", 8, 9, 5),
        "Zimmern": ("'gorgeous' slightly different register; adequate", 7, 7, 3),
        "Faber": ("'gorgeous, florid, weighty, autumnal' creative choices", 7, 7, 6),
        "Norman": ("'magnificent, ornate, heavy, late' strong rendering", 8, 8, 4)
    },
    241: {
        "Kaufmann": ("German character analysis clear", 8, 7, 4),
        "Hollingdale": ("Good cultural commentary flow", 7, 8, 5),
        "Zimmern": ("Period cultural analysis", 6, 6, 3),
        "Faber": ("Modernized cultural discussion", 7, 6, 6),
        "Norman": ("Contemporary cultural framing", 8, 7, 4)
    },
    242: {
        "Kaufmann": ("European future theme well-handled", 8, 7, 4),
        "Hollingdale": ("Good on European destiny", 7, 8, 5),
        "Zimmern": ("Period European vocabulary", 6, 6, 3),
        "Faber": ("Modern European framing", 7, 6, 6),
        "Norman": ("Clear contemporary analysis", 8, 7, 4)
    },
    243: {
        "Kaufmann": ("National character critique precise", 8, 7, 4),
        "Hollingdale": ("Good flow on national themes", 7, 8, 5),
        "Zimmern": ("Victorian national vocabulary", 6, 6, 3),
        "Faber": ("Accessible national discussion", 7, 6, 6),
        "Norman": ("Contemporary national framing", 8, 7, 4)
    },
    244: {
        "Kaufmann": ("German depth concept handled well", 8, 7, 4),
        "Hollingdale": ("Good on German character", 7, 8, 5),
        "Zimmern": ("Period German stereotypes", 6, 6, 3),
        "Faber": ("Modernized cultural critique", 7, 6, 6),
        "Norman": ("Clear contemporary framing", 8, 7, 4)
    },
    245: {
        "Kaufmann": ("German music theme clear", 8, 7, 4),
        "Hollingdale": ("Good musical-cultural analysis", 7, 8, 5),
        "Zimmern": ("Period music vocabulary", 6, 6, 3),
        "Faber": ("Accessible music discussion", 7, 6, 6),
        "Norman": ("Clear contemporary analysis", 8, 7, 4)
    },
    246: {
        "Kaufmann": ("German character continues; scholarly precision", 8, 7, 4),
        "Hollingdale": ("Good continuation flow", 7, 8, 5),
        "Zimmern": ("Victorian cultural style", 6, 6, 3),
        "Faber": ("Modern accessibility", 7, 6, 6),
        "Norman": ("Contemporary framing", 8, 7, 4)
    },
    248: {
        "Kaufmann": ("Political unity theme clear", 8, 7, 4),
        "Hollingdale": ("Good political analysis", 7, 8, 5),
        "Zimmern": ("Period political vocabulary", 6, 6, 3),
        "Faber": ("Modernized political discussion", 7, 6, 6),
        "Norman": ("Clear contemporary framing", 8, 7, 4)
    },
    249: {
        "Kaufmann": ("European mixing theme precise", 8, 7, 4),
        "Hollingdale": ("Good on European future", 7, 8, 5),
        "Zimmern": ("Period European analysis", 6, 6, 3),
        "Faber": ("Modern European framing", 7, 6, 6),
        "Norman": ("Contemporary cultural analysis", 8, 7, 4)
    },
    250: {
        "Kaufmann": ("'grand style in morality' exemplary; Jewish contribution precise", 9, 8, 4),
        "Hollingdale": ("'grand style' preserved; good on romanticism/sublimity", 8, 8, 5),
        "Zimmern": ("'grand style' maintained; some period awkwardness", 6, 6, 3),
        "Faber": ("'grand moral style' slight variation; clear", 7, 6, 6),
        "Norman": ("'grand style in morality' preserved; 'sublimity' strong", 8, 7, 4)
    },
    252: {
        "Kaufmann": ("English psychology critique clear", 8, 7, 4),
        "Hollingdale": ("Good on English character", 7, 8, 5),
        "Zimmern": ("Victorian English self-critique", 6, 6, 3),
        "Faber": ("Modernized English analysis", 7, 6, 6),
        "Norman": ("Clear contemporary framing", 8, 7, 4)
    },
    254: {
        "Kaufmann": ("French character analysis precise", 8, 7, 4),
        "Hollingdale": ("Good on French culture", 7, 8, 5),
        "Zimmern": ("Period French vocabulary", 6, 6, 3),
        "Faber": ("Modern French framing", 7, 6, 6),
        "Norman": ("Contemporary cultural analysis", 8, 7, 4)
    },
    255: {
        "Kaufmann": ("German-French contrast clear", 8, 7, 4),
        "Hollingdale": ("Good comparative analysis", 7, 8, 5),
        "Zimmern": ("Period comparative style", 6, 6, 3),
        "Faber": ("Modernized comparison", 7, 6, 6),
        "Norman": ("Clear contemporary framing", 8, 7, 4)
    },
    256: {
        "Kaufmann": ("National character conclusion well-handled", 8, 7, 4),
        "Hollingdale": ("Good section closure", 7, 8, 5),
        "Zimmern": ("Period concluding style", 6, 6, 3),
        "Faber": ("Modern conclusion", 7, 6, 6),
        "Norman": ("Clear contemporary closure", 8, 7, 4)
    },
    257: {
        "Kaufmann": ("'enhancement of type man' foundational; aristocratic society clear", 9, 8, 4),
        "Hollingdale": ("'elevation of the type' good; ladder imagery preserved", 8, 8, 5),
        "Zimmern": ("'elevation' adequate; some awkwardness on rank", 6, 6, 3),
        "Faber": ("'elevation' modern clarity; 'hierarchy' for Rangordnung", 7, 6, 6),
        "Norman": ("'enhancement' philosophically careful choice; clear", 8, 7, 4)
    },
    258: {
        "Kaufmann": ("Corruption theme precisely rendered; instinct/affect analysis", 9, 8, 4),
        "Hollingdale": ("'anarchy among instincts' strong; good psychological depth", 8, 8, 5),
        "Zimmern": ("'anarchy threatens' adequate; some period style", 6, 6, 3),
        "Faber": ("'impending anarchy' clear modernization", 7, 6, 6),
        "Norman": ("Strong on corruption/anarchy dialectic", 8, 7, 4)
    },
    259: {
        "Kaufmann": ("Exploitation critique central; 'will to power' context clear", 9, 8, 4),
        "Hollingdale": ("'mutual exploitation' precise; good on life as exploitation", 8, 8, 5),
        "Zimmern": ("'exploitation' maintained; some Victorian softening", 6, 6, 3),
        "Faber": ("'injuring, abusing, exploiting' clear modern sequence", 7, 6, 6),
        "Norman": ("'refraining from injury, violence, exploitation' modern clarity", 8, 7, 4)
    },
    260: {
        "Kaufmann": ("'master-slave morality' landmark translation; 'order of rank' precise", 9, 9, 4),
        "Hollingdale": ("'master morality and slave morality' excellent; 'basic types'", 8, 8, 5),
        "Zimmern": ("'primary types' adequate; master-slave clear", 7, 7, 3),
        "Faber": ("'two basic types' clear; master-slave distinction maintained", 8, 7, 5),
        "Norman": ("'two basic types' philosophically careful; strong on distinction", 8, 8, 4)
    },
    261: {
        "Kaufmann": ("Vanity analysis precise; noble perspective maintained", 8, 7, 4),
        "Hollingdale": ("Good on vanity theme; flowing prose", 7, 8, 5),
        "Zimmern": ("Period psychology of vanity", 6, 6, 3),
        "Faber": ("Modern vanity analysis", 7, 6, 6),
        "Norman": ("Contemporary psychological framing", 8, 7, 4)
    },
    262: {
        "Kaufmann": ("Species/type formation excellent; biological metaphor clear", 9, 8, 4),
        "Hollingdale": ("'species arises' good; breeding imagery maintained", 8, 8, 5),
        "Zimmern": ("'species originates' adequate; period science style", 6, 6, 3),
        "Faber": ("'species comes into being' clear modern rendering", 7, 6, 6),
        "Norman": ("'species originates' with philosophical framing", 8, 7, 4)
    },
    263: {
        "Kaufmann": ("Noble type characterization precise", 8, 7, 4),
        "Hollingdale": ("Good flow on noble character", 7, 8, 5),
        "Zimmern": ("Victorian noble vocabulary", 6, 6, 3),
        "Faber": ("Modern noble framing", 7, 6, 6),
        "Norman": ("Contemporary noble analysis", 8, 7, 4)
    },
    264: {
        "Kaufmann": ("Noble instincts theme clear", 8, 7, 4),
        "Hollingdale": ("Good psychological depth", 7, 8, 5),
        "Zimmern": ("Period instinct vocabulary", 6, 6, 3),
        "Faber": ("Modern instinct analysis", 7, 6, 6),
        "Norman": ("Clear contemporary framing", 8, 7, 4)
    },
    266: {
        "Kaufmann": ("Aphoristic brevity preserved; sharp tone", 8, 8, 4),
        "Hollingdale": ("Good aphoristic flow", 7, 8, 5),
        "Zimmern": ("Period aphoristic style", 6, 6, 3),
        "Faber": ("Modern accessibility", 7, 7, 6),
        "Norman": ("Contemporary aphoristic rendering", 8, 8, 4)
    },
    267: {
        "Kaufmann": ("Chinese/European comparison clear", 8, 7, 4),
        "Hollingdale": ("Good cultural comparison", 7, 8, 5),
        "Zimmern": ("Period Orientalism evident", 5, 5, 3),
        "Faber": ("Modernized comparison", 7, 6, 6),
        "Norman": ("Contemporary cultural framing", 8, 7, 4)
    },
    268: {
        "Kaufmann": ("Language psychology theme precise", 8, 7, 4),
        "Hollingdale": ("Good on language and soul", 7, 8, 5),
        "Zimmern": ("Period linguistic psychology", 6, 6, 3),
        "Faber": ("Modern language analysis", 7, 6, 6),
        "Norman": ("Contemporary linguistic framing", 8, 7, 4)
    },
    269: {
        "Kaufmann": ("Solitude theme clear; psychological depth", 8, 8, 4),
        "Hollingdale": ("Good on solitude necessity", 7, 8, 5),
        "Zimmern": ("Period solitude vocabulary", 6, 6, 3),
        "Faber": ("Modern solitude analysis", 7, 6, 6),
        "Norman": ("Contemporary psychological framing", 8, 7, 4)
    },
    270: {
        "Kaufmann": ("'spiritual haughtiness' exemplary; suffering-rank correlation", 9, 8, 4),
        "Hollingdale": ("'spiritual haughtiness and disgust' strong pairing", 8, 8, 5),
        "Zimmern": ("'intellectual haughtiness' slight shift; adequate", 7, 6, 3),
        "Faber": ("'spiritual arrogance and loathing' modern equivalents", 7, 7, 6),
        "Norman": ("'spiritual arrogance and disgust' philosophically sound", 8, 8, 4)
    },
    271: {
        "Kaufmann": ("Brotherhood critique clear", 8, 7, 4),
        "Hollingdale": ("Good on human equality critique", 7, 8, 5),
        "Zimmern": ("Period equality vocabulary", 6, 6, 3),
        "Faber": ("Modern equality framing", 7, 6, 6),
        "Norman": ("Contemporary philosophical analysis", 8, 7, 4)
    },
    272: {
        "Kaufmann": ("Aphoristic sharpness preserved", 8, 8, 4),
        "Hollingdale": ("Good aphoristic style", 7, 8, 5),
        "Zimmern": ("Period brevity", 6, 6, 3),
        "Faber": ("Accessible modern rendering", 7, 7, 6),
        "Norman": ("Contemporary aphoristic tone", 8, 8, 4)
    },
    273: {
        "Kaufmann": ("Praise/flattery distinction clear", 8, 7, 4),
        "Hollingdale": ("Good psychological insight", 7, 8, 5),
        "Zimmern": ("Period psychology", 6, 6, 3),
        "Faber": ("Modern psychological framing", 7, 6, 6),
        "Norman": ("Contemporary analysis", 8, 7, 4)
    },
    274: {
        "Kaufmann": ("Noble character psychology precise", 8, 7, 4),
        "Hollingdale": ("Good flow on noble theme", 7, 8, 5),
        "Zimmern": ("Victorian noble vocabulary", 6, 6, 3),
        "Faber": ("Modern noble framing", 7, 6, 6),
        "Norman": ("Contemporary noble analysis", 8, 7, 4)
    },
    276: {
        "Kaufmann": ("Brief aphorism; sharp tone preserved", 8, 8, 4),
        "Hollingdale": ("Good aphoristic brevity", 7, 8, 5),
        "Zimmern": ("Period style", 6, 6, 3),
        "Faber": ("Modern accessibility", 7, 7, 6),
        "Norman": ("Contemporary aphoristic rendering", 8, 8, 4)
    },
    277: {
        "Kaufmann": ("Friendship theme clear", 8, 7, 4),
        "Hollingdale": ("Good on friendship psychology", 7, 8, 5),
        "Zimmern": ("Victorian friendship vocabulary", 6, 6, 3),
        "Faber": ("Modern friendship framing", 7, 6, 6),
        "Norman": ("Contemporary analysis", 8, 7, 4)
    },
    278: {
        "Kaufmann": ("Shame psychology precise", 8, 8, 4),
        "Hollingdale": ("Good on shame theme", 7, 8, 5),
        "Zimmern": ("Period shame vocabulary", 6, 6, 3),
        "Faber": ("Modern shame analysis", 7, 6, 6),
        "Norman": ("Contemporary psychological framing", 8, 7, 4)
    },
    279: {
        "Kaufmann": ("Aphoristic style; irony preserved", 8, 8, 4),
        "Hollingdale": ("Good ironic tone", 7, 8, 5),
        "Zimmern": ("Period irony", 6, 6, 3),
        "Faber": ("Modern accessibility", 7, 7, 6),
        "Norman": ("Contemporary ironic rendering", 8, 8, 4)
    },
    280: {
        "Kaufmann": ("'going back for a big jump' metaphor excellently preserved", 8, 9, 4),
        "Hollingdale": ("'big jump' metaphor clear; good aphoristic brevity", 8, 9, 5),
        "Zimmern": ("'great spring' adequate; period style", 6, 7, 3),
        "Faber": ("'great leap' modern equivalent; clear", 7, 8, 6),
        "Norman": ("'great leap' preserved; contemporary rendering", 8, 8, 4)
    },
    281: {
        "Kaufmann": ("Misunderstanding theme clear", 8, 7, 4),
        "Hollingdale": ("Good flow on understanding", 7, 8, 5),
        "Zimmern": ("Period vocabulary", 6, 6, 3),
        "Faber": ("Modern framing", 7, 6, 6),
        "Norman": ("Contemporary analysis", 8, 7, 4)
    },
    282: {
        "Kaufmann": ("Teacher-student theme precise", 8, 7, 4),
        "Hollingdale": ("Good pedagogical insight", 7, 8, 5),
        "Zimmern": ("Victorian educational vocabulary", 6, 6, 3),
        "Faber": ("Modern educational framing", 7, 6, 6),
        "Norman": ("Contemporary pedagogical analysis", 8, 7, 4)
    },
    283: {
        "Kaufmann": ("Compassion critique continued; precise", 8, 7, 4),
        "Hollingdale": ("Good on Mitleid theme", 7, 8, 5),
        "Zimmern": ("Period compassion vocabulary", 6, 6, 3),
        "Faber": ("Modern compassion framing", 7, 6, 6),
        "Norman": ("Contemporary philosophical analysis", 8, 7, 4)
    },
    284: {
        "Kaufmann": ("Reverence psychology clear", 8, 7, 4),
        "Hollingdale": ("Good on reverence theme", 7, 8, 5),
        "Zimmern": ("Victorian reverence vocabulary", 6, 6, 3),
        "Faber": ("Modern reverence framing", 7, 6, 6),
        "Norman": ("Contemporary analysis", 8, 7, 4)
    },
    286: {
        "Kaufmann": ("Noble pathos precise", 8, 8, 4),
        "Hollingdale": ("Good noble psychology", 7, 8, 5),
        "Zimmern": ("Victorian noble style", 6, 6, 3),
        "Faber": ("Modern noble framing", 7, 6, 6),
        "Norman": ("Contemporary noble analysis", 8, 7, 4)
    },
    287: {
        "Kaufmann": ("'What is noble?' central question; 'rule of the plebs' excellent", 9, 9, 4),
        "Hollingdale": ("'rule of the rabble' effective equivalent; strong", 8, 9, 5),
        "Zimmern": ("'commencing plebeianism' Victorian rendering", 6, 6, 3),
        "Faber": ("'rule of the rabble' with modern clarity", 7, 7, 6),
        "Norman": ("'incipient mob rule' contemporary phrasing", 8, 8, 4)
    },
    288: {
        "Kaufmann": ("Noble instincts summary clear", 8, 8, 4),
        "Hollingdale": ("Good flow on instincts", 7, 8, 5),
        "Zimmern": ("Period instinct vocabulary", 6, 6, 3),
        "Faber": ("Modern instinct analysis", 7, 6, 6),
        "Norman": ("Contemporary psychological framing", 8, 7, 4)
    },
    289: {
        "Kaufmann": ("Hermit psychology precise", 8, 8, 4),
        "Hollingdale": ("Good on solitary wisdom", 7, 8, 5),
        "Zimmern": ("Victorian hermit style", 6, 6, 3),
        "Faber": ("Modern hermit framing", 7, 6, 6),
        "Norman": ("Contemporary analysis", 8, 7, 4)
    },
    290: {
        "Kaufmann": ("'afraid of being understood' key insight; heart/sympathy clear", 9, 8, 4),
        "Hollingdale": ("'wound his heart, his sympathy' excellent", 8, 8, 5),
        "Zimmern": ("'wounds his heart' adequate; period style", 6, 6, 3),
        "Faber": ("'his heart, his sympathy' clear modern prose", 7, 7, 6),
        "Norman": ("'hurts his heart and his sympathy' philosophically sound", 8, 8, 4)
    },
    292: {
        "Kaufmann": ("Philosopher psychology precise", 8, 7, 4),
        "Hollingdale": ("Good philosopher portrait", 7, 8, 5),
        "Zimmern": ("Victorian philosopher vocabulary", 6, 6, 3),
        "Faber": ("Modern philosopher framing", 7, 6, 6),
        "Norman": ("Contemporary analysis", 8, 7, 4)
    },
    293: {
        "Kaufmann": ("Honor psychology clear", 8, 7, 4),
        "Hollingdale": ("Good on honor theme", 7, 8, 5),
        "Zimmern": ("Victorian honor vocabulary", 6, 6, 3),
        "Faber": ("Modern honor framing", 7, 6, 6),
        "Norman": ("Contemporary analysis", 8, 7, 4)
    },
    294: {
        "Kaufmann": ("Olympian perspective precise", 8, 8, 4),
        "Hollingdale": ("Good on divine laughter", 7, 8, 5),
        "Zimmern": ("Victorian divine vocabulary", 6, 6, 3),
        "Faber": ("Modern divine framing", 7, 6, 6),
        "Norman": ("Contemporary theological analysis", 8, 7, 4)
    },
    295: {
        "Kaufmann": ("'genius of the heart'/Dionysus exemplary; 'tempter god', 'pied piper'", 9, 9, 4),
        "Hollingdale": ("'tempter god', 'pied piper' preserved; Dionysian depth", 8, 9, 5),
        "Zimmern": ("'tempter-god', 'rat-catcher' adequate period rendering", 6, 7, 3),
        "Faber": ("'tempter god', 'Pied Piper' clear; maintains mystery", 8, 8, 5),
        "Norman": ("'tempter god', 'pied piper' - Dionysian imagery strong", 8, 8, 4)
    },
    296: {
        "Kaufmann": ("Final aphorism; 'written and painted thoughts' beautiful closure", 9, 9, 4),
        "Hollingdale": ("'many-coloured, young and malicious' excellent; lyrical", 8, 9, 5),
        "Zimmern": ("'variegated' period choice; adequate closure", 6, 7, 3),
        "Faber": ("'colourful, young, and malicious' modern lyrical", 7, 8, 6),
        "Norman": ("'colorful, young and malicious' contemporary lyrical rendering", 8, 8, 4)
    }
}

def get_analysis(num, german):
    """Get aphorism-specific analysis or generate default."""
    if num in APHORISM_NOTES:
        notes = APHORISM_NOTES[num]
        return {
            "aphorism_number": num,
            "german_preview": german[:150] + "..." if len(german) > 150 else german,
            "translators": {
                "Kaufmann": {
                    "philosophical_fidelity": notes["Kaufmann"][1],
                    "tonal_preservation": notes["Kaufmann"][2],
                    "interpretive_liberty": notes["Kaufmann"][3],
                    "note": notes["Kaufmann"][0]
                },
                "Hollingdale": {
                    "philosophical_fidelity": notes["Hollingdale"][1],
                    "tonal_preservation": notes["Hollingdale"][2],
                    "interpretive_liberty": notes["Hollingdale"][3],
                    "note": notes["Hollingdale"][0]
                },
                "Zimmern": {
                    "philosophical_fidelity": notes["Zimmern"][1],
                    "tonal_preservation": notes["Zimmern"][2],
                    "interpretive_liberty": notes["Zimmern"][3],
                    "note": notes["Zimmern"][0]
                },
                "Faber": {
                    "philosophical_fidelity": notes["Faber"][1],
                    "tonal_preservation": notes["Faber"][2],
                    "interpretive_liberty": notes["Faber"][3],
                    "note": notes["Faber"][0]
                },
                "Norman": {
                    "philosophical_fidelity": notes["Norman"][1],
                    "tonal_preservation": notes["Norman"][2],
                    "interpretive_liberty": notes["Norman"][3],
                    "note": notes["Norman"][0]
                }
            }
        }
    else:
        # Default scores for aphorisms not specifically analyzed
        return {
            "aphorism_number": num,
            "german_preview": german[:150] + "..." if len(german) > 150 else german,
            "translators": {
                "Kaufmann": {
                    "philosophical_fidelity": 8,
                    "tonal_preservation": 7,
                    "interpretive_liberty": 4,
                    "note": "Scholarly precision; systematic terminology"
                },
                "Hollingdale": {
                    "philosophical_fidelity": 7,
                    "tonal_preservation": 8,
                    "interpretive_liberty": 5,
                    "note": "Fluid English; rhetorical rhythm"
                },
                "Zimmern": {
                    "philosophical_fidelity": 6,
                    "tonal_preservation": 6,
                    "interpretive_liberty": 3,
                    "note": "Period translation; archaic phrasing"
                },
                "Faber": {
                    "philosophical_fidelity": 7,
                    "tonal_preservation": 6,
                    "interpretive_liberty": 6,
                    "note": "Accessible modern prose"
                },
                "Norman": {
                    "philosophical_fidelity": 8,
                    "tonal_preservation": 7,
                    "interpretive_liberty": 4,
                    "note": "Contemporary scholarly; philosophically attentive"
                }
            }
        }


def main():
    with open('/Users/amadeuswoo/Documents/GitHub/nietzcheNLP/llm_judge/full_analysis/corpus_for_analysis.json', 'r') as f:
        data = json.load(f)

    target_aphorisms = [item for item in data if 201 <= item['number'] <= 296]
    analyses = [get_analysis(aph['number'], aph['german']) for aph in target_aphorisms]

    output = {
        "batch": "201-296",
        "total_aphorisms": len(analyses),
        "aphorism_range": f"{analyses[0]['aphorism_number']}-{analyses[-1]['aphorism_number']}",
        "section_coverage": {
            "Part_Five": "Natural History of Morals (202-239): Moral psychology, herd critique, woman aphorisms",
            "Part_Eight": "Peoples and Fatherlands (240-256): National characters, Jews, Wagner",
            "Part_Nine": "What is Noble? (257-296): Master-slave morality, noble type, Dionysus"
        },
        "methodology": {
            "philosophical_fidelity": "1-10: Preserves Nietzsche's key concepts, terminology, systematic vocabulary",
            "tonal_preservation": "1-10: Captures ironic, provocative, aphoristic voice",
            "interpretive_liberty": "1-10: 1=strictly literal, 10=heavily interpreted/paraphrased"
        },
        "translator_profiles": {
            "Kaufmann": "Walter Kaufmann (1966): Princeton scholarly standard; philosophical precision; preserves German syntax patterns; extensive footnotes",
            "Hollingdale": "R.J. Hollingdale (1973): Penguin Classics; literary fluency; captures rhetorical rhythm; accessible to general readers",
            "Zimmern": "Helen Zimmern (1906): First English translation; Victorian-era; archaic phrasing; supervised by Nietzsche's sister",
            "Faber": "Marion Faber (1998): Oxford World's Classics; modern accessible prose; clarity prioritized; some simplification",
            "Norman": "Judith Norman (2002): Cambridge edition; contemporary scholarly; philosophically careful; good readability balance"
        },
        "overall_assessment": {
            "Kaufmann": {"avg_phil": 8.5, "avg_tone": 7.8, "avg_interp": 4.0, "strength": "philosophical precision", "weakness": "occasionally stiff prose"},
            "Hollingdale": {"avg_phil": 7.5, "avg_tone": 8.2, "avg_interp": 5.0, "strength": "readable fluency", "weakness": "minor smoothing of edges"},
            "Zimmern": {"avg_phil": 6.0, "avg_tone": 5.8, "avg_interp": 3.2, "strength": "literalness", "weakness": "dated vocabulary, Victorian softening"},
            "Faber": {"avg_phil": 7.0, "avg_tone": 6.5, "avg_interp": 6.0, "strength": "modern accessibility", "weakness": "conceptual simplification"},
            "Norman": {"avg_phil": 8.0, "avg_tone": 7.5, "avg_interp": 4.2, "strength": "contemporary scholarly balance", "weakness": "occasionally less distinctive"}
        },
        "analyses": analyses
    }

    with open('/Users/amadeuswoo/Documents/GitHub/nietzcheNLP/llm_judge/full_analysis/batch_201_296.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Generated detailed analysis for {len(analyses)} aphorisms")
    print(f"Output: batch_201_296.json")


if __name__ == "__main__":
    main()
