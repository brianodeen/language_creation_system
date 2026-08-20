#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mraow Organic Lexicon & Valence Compounding Engine (mraow_lexicon_engine.py)

Generates and compiles the single-source vocabulary database (data/vocabulary.json)
for the Mraow feline-derived human language.
Features:
- Dual-dialect generation (Classical Trill & Accessible Ruh)
- Multi-sound valence matrix (Purr/Positive, Hiss/Negative, Growl/Territory, Meow/Neutral, Chatter/Focus)
- Derivational compounding and affixes
- Leipzig interlinear glossed example sentences
"""

import json
import os
import re
import sys

# Ensure script directory is in sys.path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from mraow_transcribe_ipa import transcribe_to_ipa, convert_trill_to_ruh

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

BASE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")
VOCAB_OUTPUT = os.path.join(DATA_DIR, "vocabulary.json")
TEMPLATE_OUTPUT = os.path.join(DATA_DIR, "vocabulary_starter_template.json")

# Master Curated Feline Vocabulary Database
CORE_VOCABULARY = [
    # -------------------------------------------------------------------------
    # Chapter 1: Core Vocalizations, Tones, & Dialects
    # -------------------------------------------------------------------------
    {
        "word": "mrāow",
        "pos": "interjection / noun",
        "valence": "neutral",
        "grammar": "Class 4 (Meow-Neutral)",
        "en": "hello; standard greeting; entity; baseline reality",
        "etymology": "[feline open vocalization + Level Tone 1]",
        "literal": "I am here / it exists",
        "example_target": "Mrāow, ī shā-trr.",
        "example_gloss": "hello, 1SG greet-HORT",
        "example_en": "Hello, I greet you warmly.",
        "chapter": 1,
        "notes": "The primary neutral greeting and name of the language.",
        "manufactured": False
    },
    {
        "word": "mráow",
        "pos": "particle / interjection",
        "valence": "neutral",
        "grammar": "Interrogative particle (Tone 2 Rising)",
        "en": "what?; who?; may I enter?; inquiry",
        "etymology": "[mrāow + Rising Tone 2]",
        "literal": "who/what is there?",
        "example_target": "Mráow? Tū tā-trr?",
        "example_gloss": "inquiry? 2SG enter-HORT",
        "example_en": "Who is there? Would you like to enter?",
        "chapter": 1,
        "notes": "Polite entry request or questioning particle.",
        "manufactured": False
    },
    {
        "word": "mràow",
        "pos": "particle / interjection",
        "valence": "neutral / assertive",
        "grammar": "Imperative / Finality marker (Tone 3 Falling)",
        "en": "halt!; enough!; it is settled; done",
        "etymology": "[mrāow + Falling Tone 3]",
        "literal": "it is finished / stop",
        "example_target": "Mràow! Nyā-kē shō.",
        "example_gloss": "halt! claw-PL retract",
        "example_en": "Halt! Sheathe your claws.",
        "chapter": 1,
        "notes": "Decisive conversational closure or commanding halt.",
        "manufactured": False
    },
    {
        "word": "prrr",
        "pos": "interjection / verb",
        "valence": "positive",
        "grammar": "Class 1 (Purr-Beneficial root)",
        "en": "yes; deeply content; in harmony; safe",
        "etymology": "[feline continuous laryngeal vibration]",
        "literal": "purr / deep safety",
        "example_target": "Ī prrr, prōm nō.",
        "example_gloss": "1SG purr, den.BEN TOP",
        "example_en": "I am deeply content in this safe den.",
        "chapter": 1,
        "notes": "The core positive affirmation; 'yes' in Mraow.",
        "manufactured": False
    },
    {
        "word": "trrrt",
        "pos": "interjection / verb",
        "valence": "positive",
        "grammar": "Class 1 (Chirp-Greeting root)",
        "en": "welcome!; come join; delighted discovery",
        "etymology": "[feline ascending chirp trill]",
        "literal": "chirp / joyful invitation",
        "example_target": "Trrrt! Tū shē-mī-trr.",
        "example_gloss": "welcome! 2SG walk-together-HORT",
        "example_en": "Welcome! Come walk with us.",
        "chapter": 1,
        "notes": "Friendly approach signal between bonded companions.",
        "manufactured": False
    },
    {
        "word": "mrrr",
        "pos": "noun / verb",
        "valence": "positive",
        "grammar": "Class 1 (Churr-Affection root)",
        "en": "maternal care; affection; soothing touch; reassurance",
        "etymology": "[feline low-frequency churr murmur]",
        "literal": "gentle rumble / affection",
        "example_target": "Mā-mrrr mīr-a sā-mrr.",
        "example_gloss": "mother-churr child-ACC soothe-BEN",
        "example_en": "The mother gently soothes the young kitten.",
        "chapter": 1,
        "notes": "Used for familial and intimate comfort.",
        "manufactured": False
    },
    {
        "word": "h’m",
        "pos": "particle / noun",
        "valence": "positive",
        "grammar": "Class 1 (Silent Breath / Esoteric)",
        "en": "devotion; silent trust; sacred secret; pure faith",
        "etymology": "[feline mouthed breath / silent meow]",
        "literal": "silent breath",
        "example_target": "H’m nō, ī vī-shā.",
        "example_gloss": "sacred_silence TOP, 1SG perceive-CONT",
        "example_en": "In sacred silence, I contemplate.",
        "chapter": 1,
        "notes": "Spoken with soft aspiration; represents total vulnerability.",
        "manufactured": False
    },
    {
        "word": "hss",
        "pos": "interjection / verb",
        "valence": "negative",
        "grammar": "Class 2 (Hiss-Hazardous root)",
        "en": "no; stay back!; refusal; dangerous boundary",
        "etymology": "[feline pulmonary alveolar fricative]",
        "literal": "hiss / veto",
        "example_target": "Hss! Tū tā-hss.",
        "example_gloss": "no! 2SG enter-PROH",
        "example_en": "No! Do not enter!",
        "chapter": 1,
        "notes": "The sacred covenant of refusal; immediately respected by law.",
        "manufactured": False
    },
    {
        "word": "pft",
        "pos": "interjection / verb",
        "valence": "negative",
        "grammar": "Class 2 (Spit-Reflex root)",
        "en": "danger!; abort immediately!; venomous shock",
        "etymology": "[feline explosive spit puff]",
        "literal": "spit / emergency abort",
        "example_target": "Pft! Hsīna lō!",
        "example_gloss": "abort! poison drop!",
        "example_en": "Drop it! That is poison!",
        "chapter": 1,
        "notes": "Immediate reflex command to avert fatal hazard.",
        "manufactured": False
    },
    {
        "word": "grrr",
        "pos": "noun / verb",
        "valence": "negative / territorial",
        "grammar": "Class 3 (Growl-Territory root)",
        "en": "territorial law; boundary warning; heavy stone; power",
        "etymology": "[feline epiglottic rumbling growl]",
        "literal": "growl / territorial weight",
        "example_target": "Grrr nō, grāow kwā-grr.",
        "example_gloss": "territory TOP, border guard-IMP",
        "example_en": "By territorial law, guard this border!",
        "chapter": 1,
        "notes": "Represents bedrock, legal decrees, and boundary dominance.",
        "manufactured": False
    },
    {
        "word": "skrēe",
        "pos": "noun / interjection",
        "valence": "negative",
        "grammar": "Class 2 (Shriek / Crisis)",
        "en": "catastrophe; severe battle cry; agony; emergency",
        "etymology": "[feline high-tension shriek]",
        "literal": "shriek / mortal crisis",
        "example_target": "Skrēe nō, klān fō-trā.",
        "example_gloss": "alarm TOP, clan assemble-URG",
        "example_en": "At the sound of crisis, the clan mobilizes.",
        "chapter": 1,
        "notes": "Emergency alert call across settlements.",
        "manufactured": False
    },
    {
        "word": "k-k-k",
        "pos": "noun / verb",
        "valence": "focused",
        "grammar": "Class 4 (Chatter / Analytical)",
        "en": "hunting calculation; intense focus; desire; precision measurement",
        "etymology": "[feline predatory jaw-chatter clicks]",
        "literal": "chatter / calculation",
        "example_target": "Ī k-k-k, tār-vī nō.",
        "example_gloss": "1SG calculate, bird-target TOP",
        "example_en": "I calculate the trajectory of the flying prey.",
        "chapter": 1,
        "notes": "Used for engineering, math, and hunting focus.",
        "manufactured": False
    },
    {
        "word": "yāowl",
        "pos": "noun / verb",
        "valence": "neutral / high-intensity",
        "grammar": "Class 4 (Yowl / Broadcast)",
        "en": "long-distance broadcast; era; cosmological time; horizon song",
        "etymology": "[feline sustained loud caterwaul]",
        "literal": "yowl / horizon call",
        "example_target": "Yāowl nō, kōr-lā shō.",
        "example_gloss": "night-call TOP, stars shine",
        "example_en": "During the horizon song, the stars shine brightly.",
        "chapter": 1,
        "notes": "Used for history, astronomy, and long-range messages.",
        "manufactured": False
    },

    # -------------------------------------------------------------------------
    # Chapter 2: The Valence System & Noun Classes
    # -------------------------------------------------------------------------
    {
        "word": "praow",
        "pos": "noun",
        "valence": "positive",
        "grammar": "Class 1 (Purr-Beneficial)",
        "en": "sunbeam; warm basking day; good weather; fortune",
        "etymology": "[pr- \"purr-beneficial\"] + [aow \"atmosphere\"]",
        "literal": "good-warm-sky",
        "example_target": "Praow nō, ī prā-lā.",
        "example_gloss": "sunbeam TOP, 1SG bask-HAB",
        "example_en": "In the warm sunbeam, I bask happily.",
        "chapter": 2,
        "notes": "The quintessential feline expression of peace.",
        "manufactured": True
    },
    {
        "word": "hsaow",
        "pos": "noun",
        "valence": "negative",
        "grammar": "Class 2 (Hiss-Hazardous)",
        "en": "violent storm; freezing hail; blizzard; foul weather",
        "etymology": "[hs- \"hiss-hazardous\"] + [aow \"atmosphere\"]",
        "literal": "hostile-bad-sky",
        "example_target": "Hsaow nō, prōm tā-trr.",
        "example_gloss": "storm TOP, den enter-HORT",
        "example_en": "Because of the storm, let us enter the safe den.",
        "chapter": 2,
        "notes": "Opposite valence of praow.",
        "manufactured": True
    },
    {
        "word": "graow",
        "pos": "noun",
        "valence": "territorial",
        "grammar": "Class 3 (Growl-Territorial)",
        "en": "mountain gale; boundary wind; territorial landmark",
        "etymology": "[gr- \"growl-heavy\"] + [aow \"atmosphere\"]",
        "literal": "heavy-mountain-wind",
        "example_target": "Graow nō, bōr-kōr vī-shā.",
        "example_gloss": "mountain-gale TOP, peak reveal",
        "example_en": "Through the mountain gale, the high peak is revealed.",
        "chapter": 2,
        "notes": "Class 3 heavy meteorological phenomenon.",
        "manufactured": True
    },
    {
        "word": "prīna",
        "pos": "noun",
        "valence": "positive",
        "grammar": "Class 1 (Purr-Beneficial)",
        "en": "wholesome food; fresh prey; feast; nourishing meal",
        "etymology": "[pr- \"purr-beneficial\"] + [īna \"sustenance\"]",
        "literal": "blessed-food",
        "example_target": "Prīna nō, klān nā-prr.",
        "example_gloss": "feast TOP, clan eat-BEN",
        "example_en": "The clan happily feasts on fresh nourishment.",
        "chapter": 2,
        "notes": "Food that is pure, fresh, and restorative.",
        "manufactured": True
    },
    {
        "word": "hsīna",
        "pos": "noun",
        "valence": "negative",
        "grammar": "Class 2 (Hiss-Hazardous)",
        "en": "poison; spoiled food; toxic substance; trap bait",
        "etymology": "[hs- \"hiss-hazardous\"] + [īna \"sustenance\"]",
        "literal": "poisonous-food",
        "example_target": "Hsīna nō, nī nā-hss.",
        "example_gloss": "poison TOP, NEG eat-PROH",
        "example_en": "That is poison; do not eat it!",
        "chapter": 2,
        "notes": "Strictly marked with Class 2 hiss prefix.",
        "manufactured": True
    },
    {
        "word": "prōm",
        "pos": "noun",
        "valence": "positive",
        "grammar": "Class 1 (Purr-Beneficial)",
        "en": "safe den; hearth; warm bedroom; secure sanctuary",
        "etymology": "[pr- \"purr-beneficial\"] + [ōm \"shelter\"]",
        "literal": "safe-warm-den",
        "example_target": "Prōm nō, shē-lā prrr.",
        "example_gloss": "den TOP, sleep-HAB purr",
        "example_en": "In the safe den, we sleep in deep peace.",
        "chapter": 2,
        "notes": "Sanctuary where claws are always sheathed.",
        "manufactured": True
    },
    {
        "word": "hsōm",
        "pos": "noun",
        "valence": "negative",
        "grammar": "Class 2 (Hiss-Hazardous)",
        "en": "cage; trap; dungeon; hostile enclosure; prison",
        "etymology": "[hs- \"hiss-hazardous\"] + [ōm \"shelter\"]",
        "literal": "hostile-cage-trap",
        "example_target": "Hsōm nō, fō-lē-pō.",
        "example_gloss": "cage TOP, escape-PFV",
        "example_en": "We have escaped from the cage.",
        "chapter": 2,
        "notes": "Enclosed space designed to trap or harm.",
        "manufactured": True
    },
    {
        "word": "grōm",
        "pos": "noun",
        "valence": "territorial",
        "grammar": "Class 3 (Growl-Territorial)",
        "en": "fortress; citadel; clan hall; stone redoubt",
        "etymology": "[gr- \"growl-heavy\"] + [ōm \"shelter\"]",
        "literal": "stone-fortress-hall",
        "example_target": "Grōm nō, klān kwā-grr.",
        "example_gloss": "citadel TOP, clan defend-IMP",
        "example_en": "The clan defends the stone fortress.",
        "chapter": 2,
        "notes": "Large public or martial structure.",
        "manufactured": True
    },
    {
        "word": "prēl",
        "pos": "noun",
        "valence": "positive",
        "grammar": "Class 1 (Purr-Beneficial)",
        "en": "fresh spring water; sweet clean drink",
        "etymology": "[pr- \"purr-beneficial\"] + [ēl \"liquid\"]",
        "literal": "clean-sweet-water",
        "example_target": "Prēl nō, ī lēp-prr.",
        "example_gloss": "fresh_water TOP, 1SG lap-BEN",
        "example_en": "I happily drink the fresh spring water.",
        "chapter": 2,
        "notes": "Safe running water for drinking.",
        "manufactured": True
    },
    {
        "word": "hsēl",
        "pos": "noun",
        "valence": "negative",
        "grammar": "Class 2 (Hiss-Hazardous)",
        "en": "stagnant foul water; acid; toxic sludge",
        "etymology": "[hs- \"hiss-hazardous\"] + [ēl \"liquid\"]",
        "literal": "foul-stagnant-liquid",
        "example_target": "Hsēl nō, tū lēp-hss.",
        "example_gloss": "foul_water TOP, 2SG lap-PROH",
        "example_en": "Do not drink that foul water!",
        "chapter": 2,
        "notes": "Unclean or dangerous water source.",
        "manufactured": True
    },

    # -------------------------------------------------------------------------
    # Chapter 3: Verbs, Aspect, Mood Clitics, & Syntax
    # -------------------------------------------------------------------------
    {
        "word": "nā",
        "pos": "verb",
        "valence": "neutral",
        "grammar": "Transitive verb root",
        "en": "to eat; to ingest; to consume",
        "etymology": "[core semantic prime \"consume\"]",
        "literal": "eat",
        "example_target": "Ī prīna nā-prr.",
        "example_gloss": "1SG feast eat-BEN",
        "example_en": "I eat the feast with great pleasure.",
        "chapter": 3,
        "notes": "Standard verb for eating.",
        "manufactured": True
    },
    {
        "word": "lēp",
        "pos": "verb",
        "valence": "neutral",
        "grammar": "Transitive verb root",
        "en": "to drink; to lap liquid; to hydrate",
        "etymology": "[onomatopoeic felid lapping sound]",
        "literal": "lap drink",
        "example_target": "Tū prēl lēp-trr?",
        "example_gloss": "2SG water drink-HORT?",
        "example_en": "Would you like to drink some fresh water?",
        "chapter": 3,
        "notes": "Standard verb for drinking.",
        "manufactured": True
    },
    {
        "word": "shē",
        "pos": "verb",
        "valence": "positive",
        "grammar": "Intransitive verb root",
        "en": "to sleep; to rest; to recharge",
        "etymology": "[soft breath felid resting root]",
        "literal": "rest / sleep",
        "example_target": "Ī prōm shē-lā-prr.",
        "example_gloss": "1SG den rest-HAB-BEN",
        "example_en": "I regularly sleep peacefully in the warm den.",
        "chapter": 3,
        "notes": "Includes the connotations of safe vulnerability.",
        "manufactured": True
    },
    {
        "word": "chā",
        "pos": "verb / aspect clitic",
        "valence": "focused",
        "grammar": "Prowling Aspect (Imperfective / Progressive)",
        "en": "to stalk; to prowl; actively doing in progress",
        "etymology": "[felid stalking gait]",
        "literal": "stalk / currently occurring",
        "example_target": "Ī prīna chā-kkk.",
        "example_gloss": "1SG prey stalk-INT",
        "example_en": "I am calculating and stalking the prey.",
        "chapter": 3,
        "notes": "Used both as independent verb and progressive aspect marker.",
        "manufactured": True
    },
    {
        "word": "pō",
        "pos": "verb / aspect clitic",
        "valence": "neutral",
        "grammar": "Pouncing Aspect (Perfective / Completed)",
        "en": "to pounce; completed action; finished",
        "etymology": "[felid landing pounce]",
        "literal": "pounce / done",
        "example_target": "Klān fō-pō.",
        "example_gloss": "clan arrive-PFV",
        "example_en": "The clan has arrived cleanly.",
        "chapter": 3,
        "notes": "Marks clean, decisive completion of an action.",
        "manufactured": True
    },
    {
        "word": "vī-shā",
        "pos": "verb",
        "valence": "focused",
        "grammar": "Compound verb",
        "en": "to observe from a high perch; to contemplate; to survey",
        "etymology": "[vī \"high branch / perch\"] + [shā \"see / perceive\"]",
        "literal": "perch-see",
        "example_target": "Ī kōr vī-shā-lā.",
        "example_gloss": "1SG stars perch-observe-HAB",
        "example_en": "I observe the stars from the high perch.",
        "chapter": 3,
        "notes": "Higher philosophical and intellectual observation.",
        "manufactured": True
    },
    {
        "word": "nyā-kē",
        "pos": "noun",
        "valence": "neutral",
        "grammar": "Class 4 (Body part / Tool)",
        "en": "claws; fingernails; sharp instruments; defensive blades",
        "etymology": "[nyā \"paw\"] + [kē \"sharp edge\"]",
        "literal": "paw-sharpness",
        "example_target": "Nyā-kē shō nō, pēk prrr.",
        "example_gloss": "claws retract TOP, peace good",
        "example_en": "With claws retracted, peace is good.",
        "chapter": 3,
        "notes": "Central cultural symbol of peace (sheathed) or law (extended).",
        "manufactured": True
    },
    {
        "word": "klān",
        "pos": "noun",
        "valence": "positive",
        "grammar": "Class 1 (Purr-Beneficial)",
        "en": "clan; bonded group; family; trusted community",
        "etymology": "[purr-valenced social prime]",
        "literal": "bonded-cattery / clan",
        "example_target": "Klān nō, ī mrrr-sā.",
        "example_gloss": "clan TOP, 1SG love-care",
        "example_en": "As for the clan, I care for them with deep affection.",
        "chapter": 3,
        "notes": "The fundamental social unit in Mraow civilization.",
        "manufactured": True
    },
    {
        "word": "grāow",
        "pos": "noun",
        "valence": "territorial",
        "grammar": "Class 3 (Growl-Territorial)",
        "en": "territory; boundary marker; legal border; bedrock",
        "etymology": "[gr- \"growl-heavy\"] + [aow \"domain\"]",
        "literal": "territorial-domain",
        "example_target": "Grāow nō, nī tā-hss.",
        "example_gloss": "territory TOP, NEG cross-PROH",
        "example_en": "Do not cross this territorial boundary!",
        "chapter": 3,
        "notes": "Legally demarcated land or jurisdiction.",
        "manufactured": True
    },
    {
        "word": "kōr",
        "pos": "noun",
        "valence": "neutral",
        "grammar": "Class 4 (Cosmic / Ambient)",
        "en": "star; night sky; celestial beacon; navigation point",
        "etymology": "[celestial night root]",
        "literal": "night-spark",
        "example_target": "Kōr nō, mīlo vī-shā.",
        "example_gloss": "stars TOP, path reveal",
        "example_en": "The stars guide the path.",
        "chapter": 3,
        "notes": "Used for nighttime navigation and philosophy.",
        "manufactured": True
    }
]

def generate_vocabulary_database():
    """Compiles and writes vocabulary.json with dual-dialect lemmas and IPA transcriptions."""
    enriched_vocab = []
    
    for item in CORE_VOCABULARY:
        w_trill = item["word"]
        w_ruh = convert_trill_to_ruh(w_trill)
        ipa = transcribe_to_ipa(w_trill)
        
        # Dual-dialect example sentence conversion
        ex_target = item.get("example_target", "")
        ex_ruh = convert_trill_to_ruh(ex_target)
        
        entry = {
            "word": w_trill,
            "word_ruh": w_ruh,
            "ipa": ipa,
            "pos": item["pos"],
            "valence": item.get("valence", "neutral"),
            "grammar": item.get("grammar", ""),
            "en": item["en"],
            "etymology": item.get("etymology", ""),
            "literal": item.get("literal", ""),
            "example_target": ex_target,
            "example_ruh": ex_ruh,
            "example_gloss": item.get("example_gloss", ""),
            "example_en": item.get("example_en", ""),
            "chapter": item.get("chapter", 1),
            "notes": item.get("notes", ""),
            "manufactured": item.get("manufactured", False)
        }
        enriched_vocab.append(entry)
        
    os.makedirs(DATA_DIR, exist_ok=True)
    
    with open(VOCAB_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(enriched_vocab, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated {len(enriched_vocab)} dual-dialect vocabulary entries in '{VOCAB_OUTPUT}'.")
    
    # Also write starter schema template
    with open(TEMPLATE_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(enriched_vocab[:3], f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    generate_vocabulary_database()
