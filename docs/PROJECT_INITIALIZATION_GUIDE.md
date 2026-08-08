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

#### Step 1: Define the Style & Stems
1.  Determine your conlang's glyph catalog or character set (Option 1, 2, or 3 from the Master Script Decision Matrix).
2.  Open `scripts/phonetic_matcher.py` and populate the `CONCEPT_MULTILINGUAL_MAP` with target concept spellings across the 10 reference language families.
3.  Implement the phonetic-fit scoring algorithm in `calculate_phonetic_fit_score()` to evaluate how closely candidate stems match the desired acoustic style.

#### Step 2: Algorithmic Lexicon Generation
1.  Configure `scripts/generate_vocab.py` with your syllable structures, vowel/consonant weight rules, and prefix/suffix morphological additions.
2.  Run the generator to compile your conlang's vocabulary:
    ```bash
    python scripts/generate_vocab.py
    ```
    This automatically exports a finished `data/vocabulary.json` file populated with generated words, IPA, and translations.

#### Step 3: Integrate the Conversation Guide
1.  Navigate to `templates/conversation_guide/`.
2.  Open the categories relevant to your story or setting.
3.  Copy the baseline English dialogues and translate them into your generated conlang vocabulary using the grammar guidelines specified in the file's **Grammatical Mapping & Analysis** section.

#### Step 4: Typeset and Publish
1.  Adjust your page layouts and color schemes (e.g. changing colors to match your conlang's mood) inside `scripts/build_latex.py`.
2.  Run the build scripts to compile the finished multi-volume PDF collection:
    ```bash
    python scripts/build_books.py
    python scripts/build_latex.py
    ```
