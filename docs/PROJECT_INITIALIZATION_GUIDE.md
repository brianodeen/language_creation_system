# Project Initialization & Usage Guide

This guide explains how to use the **Master Language Creation System** as a template and automation engine for launching a new language book project. It details the repository structures and directory bindings for both **Existing/Historical Languages** and **New Artificial Languages (Conlangs)**.

---

## Architectural Setup: How to Structure Your Project

You have two options for structuring your new project directory relative to this master repository:

### Option 1: The Template Forking Model (Recommended for Single Languages)
Best if you are building a standalone language and want to bundle the automation scripts directly inside your repository.

1.  **Clone or Copy the Master Repository**:
    Duplicate the `language_creation_system` directory and rename the root folder to your target language name (e.g., `language_gothic` or `language_elvish`).
2.  **Clear Starter Data**:
    - Keep the `scripts/` directory intact.
    - Reset `data/vocabulary.json` by copying the contents of `data/vocabulary_starter_template.json` into it.
    - Delete any sample lessons in `book_1_grammar/` and replace them with your own markdown lessons.
3.  **Run Locally**:
    All build scripts are self-contained and run directly within your project directory.

### Option 2: The Shared Core Submodule Model (Recommended for Multi-Language Developers)
Best if you are developing multiple languages in parallel and want to keep a single, centralized copy of the build scripts to receive upstream updates.

1.  **Create a New Repository**:
    Initialize a new git repository for your target language (e.g., `language_latin`).
2.  **Bind the Core System as a Git Submodule**:
    Add the master system as a submodule inside a `core_system/` subdirectory:
    ```bash
    git submodule add https://github.com/brianodeen/language_creation_system.git core_system
    ```
3.  **Configure Local Directories**:
    Create your own local `data/` and `book_` directories at your repository root.
4.  **Execute via the Core Submodule**:
    Run scripts from the submodule directory, pointing them to your local project data:
    ```bash
    python core_system/scripts/build_books.py
    ```

> [!NOTE]
> **Dynamic Path Resolution**: All automation scripts (`build_books.py`, `build_latex.py`, etc.) are engineered with a dynamic path resolver. They automatically detect if they are running inside a direct cloned structure (Option 1) or being executed as an external tool folder (Option 2) by checking for local data folders relative to the shell execution path (`os.getcwd()`). You do not need to modify any script paths to switch between the two models.

---

## Step-by-Step Launch Workbooks

### Pathway A: Generating Books for an Existing or Historical Language

If you specified: **"make a set of language books for language: Latin"**

#### Step 1: Establish the Alphabet & Sorting
1.  Open your project's copy of `scripts/build_books.py`.
2.  Define the language's unique alphabetical sort weights in the `CHAR_PRIORITY_MAP` dictionary (e.g. mapping custom letters or character hierarchies).
3.  Configure `get_letter_group()` to return the correct section headers for your target dictionary index (e.g. grouping under 'Æ' or 'Þ').

#### Step 2: Configure the IPA Transcriber
1.  Open `scripts/transcribe_ipa.py`.
2.  Update the rule cascades inside `transcribe_to_ipa()` to match the target language's spelling-to-sound rules (e.g. handling silent letters, vowel length diacritics, or soft/hard consonant conditions).

#### Step 3: Populate the Vocabulary
1.  Open `data/vocabulary.json`.
2.  Populate it with your historical dictionary terms using the single-source schema:
    ```json
    {
      "word": "water",
      "en": "water",
      "pos": "noun",
      "grammar": "neuter",
      "chapter": 1,
      "notes": "Core element",
      "ipa": "/water_ipa/",
      "manufactured": false
    }
    ```

#### Step 4: Write Lessons & Compile
1.  Write your textbook chapters under `book_1_grammar/chapter_1.md`, etc.
2.  Insert `<!-- CHAPTER_GLOSSARY_START -->` and `<!-- CHAPTER_GLOSSARY_END -->` comments where you want the vocab lists to display.
3.  Run the compilers to generate your markdown dictionaries and print-ready PDFs:
    ```bash
    python scripts/build_books.py
    python scripts/build_latex.py
    ```

---

### Pathway B: Generating Books for a New Artificial Language (Conlang)

If you specified: **"create a set of language books for a new artificial language of this style: Elvish"**

#### Step 1: Complete the Idea Elicitation Protocol
1.  Review [docs/CONLANG_IDEA_ELICITATION_PROTOCOL.md](file:///c:/Users/brian/Documents/antigravity/language_creation_system/docs/CONLANG_IDEA_ELICITATION_PROTOCOL.md) with the assistant.
2.  Define the **Aesthetic Soul**, phoneme inventory, syllable shapes (e.g. `CV`, `CVC`), forbidden cluster rules, and cultural worldview metaphors.
3.  Establish the morphological typology (Agglutinative, Fusional, Isolating) and clause syntax (V2, SVO, SOV).

#### Step 2: Configure the Organic Lexicon Engine
1.  Open `scripts/organic_lexicon_engine.py`.
2.  Set up the `PhonotacticProfile` with your conlang's allowed consonants, vowels, diphthongs, and syllable templates.
3.  Customize the `DERIVATIONAL_AFFIXES` map (Agentive, Instrumental, Locative, Diminutive, etc.).
4.  Run the organic synthesis engine to generate atomic roots and semantic compounds with automatic anti-Anglicism verification:
    ```bash
    python scripts/organic_lexicon_engine.py
    ```
    This outputs a rich `data/vocabulary.json` database with etymological derivations, literal compound translations, and Leipzig-glossed example sentences.

#### Step 3: Integrate the Conversation Guide
1.  Navigate to `templates/conversation_guide/`.
2.  Select the relevant dialogue categories (e.g. `01_greetings_protocol.md`, `06_conflict_warfare.md`, `24_supernatural_magic.md`).
3.  Translate the baseline English dialogues into your conlang's generated vocabulary, following the grammar blueprints provided in each template's **Grammatical Mapping & Analysis** section.

#### Step 4: Typeset and Publish the Multi-Volume Suite
1.  Adjust page trim geometry, color palettes (parchment/burgundy), and fonts inside `scripts/build_latex.py`.
2.  Execute the automated build pipeline to compile your lessons, rich dictionaries, phrasebooks, and PDFs:
    ```bash
    python scripts/build_books.py
    python scripts/build_latex.py
    ```
