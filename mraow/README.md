# Mraow Language System (Feline-Derived Human Language)

**Mraow** (`/mraʊ⁵⁵/`) is an efficient, expressive artificial language (conlang) engineered for human vocalization, adapted from natural feline acoustic biology, pitch/volume prosody, multi-sound valence morphosyntax, and dual-dialect accessibility.

---

## Key Features

1. **Human-Adapted Feline Phonetics**:
   - Spans 7 feline acoustic families: *Meows/Mraows*, *Purrs*, *Hisses*, *Growls*, *Yowls*, *Chatters*, and *Whispered/Silent Breaths*.
   - Uses a Romanized phonetic writing system with tone diacritics (`ā`, `á`, `à`, `ǎ`, `â`).

2. **Dual Dialect Architecture**:
   - **Mraow-Trill (Classical / Felid Register)**: Employs true alveolar and uvular trills (`prrr`, `trrrt`, `grrr`).
   - **Mraow-Ruh (Human-Accessible Register)**: Systematically replaces trilled *r* with the accessible vocalic syllable `"ruh"` / `"ru"` (`puruh`, `tùruht`, `gùruh`), enabling effortless pronunciation for speakers who cannot roll their Rs.

3. **Multi-Sound Valence (Axiology)**:
   - Feline sounds govern **both Noun Classes (Genders)** and **Verbal Moods**:
     - **Positive (Purr/Trill/Churr)**: Safety, comfort, nourishment, health, peace, cooperative endorsement (`-prr` / `-trr`).
     - **Negative (Hiss/Spit/Growl/Shriek)**: Danger, toxicity, conflict, prohibition, urgent warning (`-hss` / `-grr`).
     - **Neutral/Analytical (Meow/Chatter/Yowl)**: Objects, baseline facts, hunting focus, long-distance communication (`-kkk`).

4. **Efficient Grammar**:
   - Topic-Comment sentence structure with streamlined S-V-O subclauses.
   - High information density through tonal modulation and transparent agglutinative affixes.

---

## Directory Layout

```
mraow/
├── README.md                               # This file
├── data/
│   ├── vocabulary.json                     # Single-source database with dual-dialect lemmas
│   └── vocabulary_starter_template.json    # JSON schema template
├── docs/
│   ├── 01_PHONETICS_AND_DIALECTS.md        # Sound taxonomy, IPA, dual dialects, 5 tones
│   ├── 02_GRAMMAR_AND_VALENCE_SYSTEM.md    # Noun classes, verbal moods, topic-comment syntax
│   └── 03_CULTURAL_WORLDVIEW.md            # Sensory metaphors, perch elevation, scent borders
├── scripts/
│   ├── mraow_transcribe_ipa.py             # Rule-based IPA phonetic transcriber (Trill & Ruh)
│   ├── mraow_lexicon_engine.py             # Lexicon generation & valence compounding engine
│   └── build_mraow_books.py                # Dictionary compiler & chapter glossary injector
├── book_1_grammar/                         # Language lessons & grammatical curriculum
├── book_2_dictionary/                      # Compiled bidirectional dictionaries
└── book_3_phrasebook/                      # Thematic feline dialogues & conversation guides
```

---

## Quick Start

### 1. Transcribe Mraow Orthography to IPA (Both Dialects)
```bash
# Classical Trill Dialect
python scripts/mraow_transcribe_ipa.py "mrāow" "prr̂t" "hsìss" "chírr" "grr̄"

# Accessible Ruh Dialect
python scripts/mraow_transcribe_ipa.py "məráow" "púruht" "hsìss" "túruh" "gùruh"
```

### 2. Generate or Update Vocabulary
```bash
python scripts/mraow_lexicon_engine.py
```

### 3. Synchronize Glossaries & Build Bidirectional Dictionaries
```bash
python scripts/build_mraow_books.py
```
