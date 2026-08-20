#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Glossary & Dictionary Compiler for Mraow (build_mraow_books.py)

1. Synchronizes lesson chapter glossaries inside mraow/book_1_grammar/ between HTML comments.
2. Compiles Book 2 bidirectional dictionaries:
   - mraow_to_en.md (Mraow -> English with Dual-Dialect Trill/Ruh support)
   - en_to_mraow.md (English -> Mraow)
"""

import json
import os
import re
import sys
import unicodedata

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
VOCAB_FILE = os.path.join(DATA_DIR, "vocabulary.json")
BOOK1_DIR = os.path.join(BASE_DIR, "book_1_grammar")
BOOK2_DIR = os.path.join(BASE_DIR, "book_2_dictionary")

def strip_diacritics(text: str) -> str:
    """Removes diacritics for alphabetical grouping."""
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

def load_vocabulary() -> list:
    if not os.path.exists(VOCAB_FILE):
        print(f"Warning: Vocabulary file '{VOCAB_FILE}' not found.")
        return []
    with open(VOCAB_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_chapter_glossaries(vocab: list):
    """Injects synchronized chapter glossaries into lesson files."""
    if not os.path.exists(BOOK1_DIR):
        return
        
    print("Synchronizing chapter glossaries in book_1_grammar/...")
    for filename in sorted(os.listdir(BOOK1_DIR)):
        if filename.startswith("chapter_") and filename.endswith(".md"):
            filepath = os.path.join(BOOK1_DIR, filename)
            match = re.search(r'chapter_0*(\d+)', filename)
            if not match:
                continue
            ch_num = int(match.group(1))
            
            words = [w for w in vocab if w.get('chapter') == ch_num]
            words.sort(key=lambda x: strip_diacritics(x.get('word', '')).lower())
            
            table_lines = [
                "| Mraow (Trill) | Mraow (Ruh) | IPA | Valence | Part of Speech | English Definition | Example / Notes |",
                "| :--- | :--- | :--- | :--- | :--- | :--- | :--- |"
            ]
            for w in words:
                trill = w.get('word', '')
                ruh = w.get('word_ruh', convert_trill_to_ruh(trill))
                ipa = w.get('ipa', transcribe_to_ipa(trill))
                val = w.get('valence', 'neutral').capitalize()
                pos = w.get('pos', '')
                defn = w.get('en', '')
                notes = w.get('notes', '')
                table_lines.append(f"| **{trill}** | *{ruh}* | `{ipa}` | {val} | *{pos}* | {defn} | {notes} |")
                
            glossary_md = "\n".join(table_lines)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            start_tag = "<!-- CHAPTER_GLOSSARY_START -->"
            end_tag = "<!-- CHAPTER_GLOSSARY_END -->"
            
            if start_tag in content and end_tag in content:
                pattern = re.compile(rf"{re.escape(start_tag)}.*?{re.escape(end_tag)}", re.DOTALL)
                new_content = pattern.sub(f"{start_tag}\n\n{glossary_md}\n\n{end_tag}", content)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  [OK] Updated {filename} (Chapter {ch_num}: {len(words)} entries)")

def build_mraow_to_en_dictionary(vocab: list):
    """Compiles Mraow -> English bidirectional dictionary."""
    os.makedirs(BOOK2_DIR, exist_ok=True)
    out_file = os.path.join(BOOK2_DIR, "mraow_to_en.md")
    
    sorted_vocab = sorted(vocab, key=lambda x: strip_diacritics(x.get('word', '')).lower())
    
    lines = [
        "# Book 2: Complete Mraow to English Dictionary",
        "",
        "A dual-dialect bidirectional lexicon for the Mraow feline-derived human language.",
        "Entries include **Classical Mraow-Trill** and **Accessible Mraow-Ruh** lemmas, IPA transcription with tone pitch contours, valence class, grammar notes, and Leipzig interlinear glosses.",
        "",
        "---",
        ""
    ]
    
    current_letter = None
    for entry in sorted_vocab:
        trill = entry.get('word', '')
        ruh = entry.get('word_ruh', convert_trill_to_ruh(trill))
        ipa = entry.get('ipa', transcribe_to_ipa(trill))
        pos = entry.get('pos', '')
        val = entry.get('valence', 'neutral').capitalize()
        grammar = entry.get('grammar', '')
        defn = entry.get('en', '')
        etym = entry.get('etymology', '')
        lit = entry.get('literal', '')
        ex_trill = entry.get('example_target', '')
        ex_ruh = entry.get('example_ruh', convert_trill_to_ruh(ex_trill))
        gloss = entry.get('example_gloss', '')
        ex_en = entry.get('example_en', '')
        notes = entry.get('notes', '')
        
        first_char = strip_diacritics(trill)[0].upper() if trill else '#'
        if not first_char.isalpha():
            first_char = '#'
            
        if first_char != current_letter:
            current_letter = first_char
            lines.append(f"\n## {current_letter}\n")
            
        lines.append(f"### {trill} *(Ruh: {ruh})* `[{ipa}]`")
        lines.append(f"- **Part of Speech**: *{pos}* | **Valence**: {val}")
        if grammar:
            lines.append(f"- **Grammar**: {grammar}")
        lines.append(f"- **Definition**: {defn}")
        if etym:
            lines.append(f"- **Etymology**: {etym} *(Literal: \"{lit}\")*")
        if ex_trill:
            lines.append(f"- **Example (Trill)**: *{ex_trill}*")
            lines.append(f"- **Example (Ruh)**: *{ex_ruh}*")
            lines.append(f"- **Gloss**: `{gloss}`")
            lines.append(f"- **Translation**: \"{ex_en}\"")
        if notes:
            lines.append(f"- **Cultural Note**: {notes}")
        lines.append("")
        
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Compiled Mraow -> English Dictionary ({len(sorted_vocab)} entries) in '{out_file}'.")

def build_en_to_mraow_dictionary(vocab: list):
    """Compiles English -> Mraow dictionary."""
    os.makedirs(BOOK2_DIR, exist_ok=True)
    out_file = os.path.join(BOOK2_DIR, "en_to_mraow.md")
    
    # Flatten English definitions
    en_entries = []
    for entry in vocab:
        definitions = [d.strip() for d in entry.get('en', '').split(';')]
        for d in definitions:
            en_entries.append({
                "en_key": d,
                "entry": entry
            })
            
    en_entries.sort(key=lambda x: x["en_key"].lower())
    
    lines = [
        "# Book 2: English to Mraow Comprehensive Index",
        "",
        "A reverse lookup dictionary mapping English concepts to **Mraow-Trill** and **Mraow-Ruh** equivalents.",
        "",
        "| English Concept | Mraow (Trill) | Mraow (Ruh) | IPA | Valence | Part of Speech |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ]
    
    for item in en_entries:
        d = item["en_key"]
        e = item["entry"]
        trill = e.get('word', '')
        ruh = e.get('word_ruh', convert_trill_to_ruh(trill))
        ipa = e.get('ipa', '')
        val = e.get('valence', 'neutral').capitalize()
        pos = e.get('pos', '')
        lines.append(f"| **{d}** | `{trill}` | *{ruh}* | `{ipa}` | {val} | *{pos}* |")
        
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
    print(f"Compiled English -> Mraow Index ({len(en_entries)} index rows) in '{out_file}'.")

if __name__ == "__main__":
    vocab = load_vocabulary()
    if vocab:
        update_chapter_glossaries(vocab)
        build_mraow_to_en_dictionary(vocab)
        build_en_to_mraow_dictionary(vocab)
    else:
        print("Error: No vocabulary loaded.")
