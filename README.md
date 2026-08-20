# Master Language Creation System

A generalized engineering specification, automation architecture, and Python software suite for designing, generating, compiling, and publishing complete language curricula, dictionaries, phrasebooks, and reference guides for both constructed languages (conlangs) and real/historical languages (e.g. Old English).

## Overview

This repository provides an end-to-end framework covering:
- **Phase 1: Script, Symbol & Orthography Engineering**: Decision matrix and step-by-step manuals for Unicode repurposing, original custom vector font design (`.ttf`/`.otf`), and hybrid prototyping workflows.
- **Phase 2: Phonology, Prosody & Rule-Based IPA Transcribers**: Context-sensitive rule cascades, dual-register accessibility (classical vs. human schwa "Ruh"), and syllable weight conservation.
- **Phase 3: Lexicon Generation & Multilingual Sound-Fit Engine**: Single-source JSON schema (`vocabulary.json`), 10-language family sound-fit matcher (`phonetic_matcher.py`), 4 coining strategies for neologisms, and zero-collision multi-tier stem depth (`generate_vocab.py`).
- **Phase 4: Morphosyntactic & Structural Rules**: V2 clause syntax vs. S-A-V-O subclauses, dynamic noun genders, enclitic definite article suffixes, and matrix pronoun paradigms.
- **Phase 5: Four-Volume Book Suite Architecture**: Book 1 (Grammar), Book 2 (Dictionaries), Book 3 (Phrasebook), Book 4 (History & Dialects) with dynamic chapter glossary injection (`<!-- CHAPTER_GLOSSARY_START -->`).
- **Phase 6: Typesetting & XeLaTeX Publication Engineering**: 8"x10" trim size, double-column dictionary switching (`\twocolumn\footnotesize`) with `longtable` single-column isolation, `{\small\bfseries}` header wrapping, Windows UTF-8 stdout safeguards, and PDF lock safety handlers.
- **Phase 7: Step-by-Step Execution Checklist**: Actionable launch checklist.
- **Resource Appendix**: Master Core English Concept & Seed Lexicon (Swadesh-plus core concepts, modern terms, and JSON starter schema).

## Project Structure

```
language_creation_system/
├── data/
│   └── vocabulary_starter_template.json   # Single-source JSON starter database
├── docs/
│   ├── CONLANG_ENGINEERING_MASTER_SPECIFICATION.md
│   ├── master_language_generation_guide.md
│   ├── MASTER_LANGUAGE_CREATION_SYSTEM.md # Complete master engineering manual
│   └── PDF_ENGINE_INTEGRATION_NOTES.md   # PDF engine integration notes & margin safeguards
├── scripts/
│   ├── build_books.py                     # Glossary injector & dictionary compiler
│   ├── build_latex.py                     # Dynamic Markdown-to-XeLaTeX PDF compiler
│   ├── phonetic_matcher.py                # 10-language family sound-fit matcher
│   └── transcribe_ipa.py                  # Rule-based IPA phonetic transcriber CLI
└── README.md
```

## Quick Start

### 1. Synchronize Chapter Glossaries & Build Dictionaries
```bash
python scripts/build_books.py
```

### 2. Transcribe Words to IPA
```bash
python scripts/transcribe_ipa.py "word1" "word2"
```

### 3. Test Multilingual Phonetic Fit Score
```bash
python scripts/phonetic_matcher.py
```

### 4. Compile Markdown Books to Print-Ready XeLaTeX PDFs
```bash
# Standard 8x10 compilation with parchment theme
python scripts/build_latex.py

# Custom geometry (e.g. Trade 6x9, A4, Letter) and theme (parchment, modern, classic, dark)
python scripts/build_latex.py --paper trade --theme classic

# Compiling a sub-language directory (e.g. mraow)
python scripts/build_latex.py --dir mraow --lang "Mraow" --author "Brian Odeen"
```

## Documentation

*   **Complete Master Specification**: [docs/MASTER_LANGUAGE_CREATION_SYSTEM.md](docs/MASTER_LANGUAGE_CREATION_SYSTEM.md)
*   **PDF Engine Architecture & Margin Safeguards**: [docs/PDF_ENGINE_INTEGRATION_NOTES.md](docs/PDF_ENGINE_INTEGRATION_NOTES.md)
*   **Conlang Engineering Guide**: [docs/CONLANG_ENGINEERING_MASTER_SPECIFICATION.md](docs/CONLANG_ENGINEERING_MASTER_SPECIFICATION.md)
