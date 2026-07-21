#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Automated Glossary & Dictionary Compiler Engine (build_books.py)
1. Synchronizes lesson chapter glossaries inside book_1_grammar/ between HTML comments.
2. Compiles Book 2 bidirectional dictionaries (target_to_en.md and en_to_target.md) using custom sorting.
"""

import json
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOCAB_FILE = os.path.join(BASE_DIR, "data", "vocabulary.json")
BOOK1_DIR = os.path.join(BASE_DIR, "book_1_grammar")
BOOK2_DIR = os.path.join(BASE_DIR, "book_2_dictionary")

# Target language character priority map for custom sorting
CHAR_PRIORITY_MAP = {
    'a': 1, 'æ': 2, 'b': 3, 'c': 4, 'd': 5, 'e': 6,
    'f': 7, 'g': 8, 'h': 9, 'i': 10, 'l': 11, 'm': 12,
    'n': 13, 'o': 14, 'p': 15, 'r': 16, 's': 17, 't': 18,
    'u': 19, 'w': 20, 'y': 21, 'þ': 22, 'ð': 22
}

def get_alphabetical_sort_key(word: str) -> list:
    """Returns a list of character weight indices for language-specific sorting."""
    word = word.lower().strip()
    clean_word = word.replace('ā', 'a').replace('ē', 'e').replace('ī', 'i') \
                     .replace('ō', 'o').replace('ū', 'u').replace('ȳ', 'y') \
                     .replace('ċ', 'c').replace('ġ', 'g')
    return [CHAR_PRIORITY_MAP.get(char, 99) for char in clean_word]

def get_letter_group(word: str) -> str:
    """Determines the primary section header letter."""
    word = word.lower().strip()
    if not word:
        return '#'
    char = word[0]
    if char in ('ā', 'a'): return 'A'
    if char in ('æ', 'ǣ'): return 'Æ'
    if char in ('þ', 'ð'): return 'Þ'
    return char.upper() if char.isalpha() else '#'

def load_vocabulary():
    """Loads vocabulary database from JSON single source of truth."""
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
            match = re.search(r'chapter_(\d+)', filename)
            if not match:
                continue
            ch_num = int(match.group(1))
            
            words = [w for w in vocab if w.get('chapter') == ch_num]
            words.sort(key=lambda x: get_alphabetical_sort_key(x.get('word', x.get('oe', ''))))
            
            table_lines = [
                "| Target Word | IPA | Part of Speech | Grammar Notes | English Definition | Notes |",
                "| :--- | :--- | :--- | :--- | :--- | :--- |"
            ]
            for w in words:
                word_str = w.get('word', w.get('oe', ''))
                m_tag = " [Manufactured]" if w.get('manufactured') else ""
                table_lines.append(f"| **{word_str}** | `{w.get('ipa','')}` | *{w.get('pos','')}* | {w.get('grammar','')} | {w.get('en','')}{m_tag} | {w.get('notes','')} |")
                
            glossary_md = "\n".join(table_lines)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            start_tag = "<!-- CHAPTER_GLOSSARY_START -->"
            end_tag = "<!-- CHAPTER_GLOSSARY_END -->"
            
            if start_tag in content and end_tag in content:
                pattern = f"{start_tag}.*?{end_tag}"
                replacement = f"{start_tag}\n\n{glossary_md}\n\n{end_tag}"
                new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"  Updated glossary in {filename} (Chapter {ch_num}).")

def build_dictionaries(vocab: list):
    """Compiles bidirectional target-to-English and English-to-target dictionary markdown files."""
    if not os.path.exists(BOOK2_DIR):
        os.makedirs(BOOK2_DIR, exist_ok=True)
        
    print("Compiling Book 2 Dictionaries...")
    # 1. Target -> English Dictionary
    target_sorted = sorted(vocab, key=lambda w: get_alphabetical_sort_key(w.get('word', w.get('oe', ''))))
    target_to_en_path = os.path.join(BOOK2_DIR, "target_to_en.md")
    
    t_lines = ["# Target Language to English Dictionary\n"]
    current_group = None
    for entry in target_sorted:
        w_str = entry.get('word', entry.get('oe', ''))
        group = get_letter_group(w_str)
        if group != current_group:
            current_group = group
            t_lines.append(f"\n## {current_group}\n")
        m_tag = " [Manufactured Word]" if entry.get('manufactured') else ""
        t_lines.append(f"- **{w_str}** `{entry.get('ipa','')}` *{entry.get('pos','')}* - {entry.get('en','')}{m_tag} ({entry.get('notes','')})")
        
    with open(target_to_en_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(t_lines))
    print(f"  Created '{target_to_en_path}'.")
    
    # 2. English -> Target Dictionary
    en_sorted = sorted(vocab, key=lambda w: w.get('en', '').lower())
    en_to_target_path = os.path.join(BOOK2_DIR, "en_to_target.md")
    
    e_lines = ["# English to Target Language Dictionary\n"]
    current_en_group = None
    for entry in en_sorted:
        en_str = entry.get('en', '')
        group = en_str[0].upper() if en_str and en_str[0].isalpha() else '#'
        if group != current_en_group:
            current_en_group = group
            e_lines.append(f"\n## {current_en_group}\n")
        w_str = entry.get('word', entry.get('oe', ''))
        m_tag = " [Manufactured Word]" if entry.get('manufactured') else ""
        e_lines.append(f"- **{en_str}**: **{w_str}** `{entry.get('ipa','')}` *{entry.get('pos','')}*{m_tag} ({entry.get('notes','')})")
        
    with open(en_to_target_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(e_lines))
    print(f"  Created '{en_to_target_path}'.")

if __name__ == "__main__":
    vocab_db = load_vocabulary()
    if vocab_db:
        update_chapter_glossaries(vocab_db)
        build_dictionaries(vocab_db)
        print("Build books completed successfully!")
