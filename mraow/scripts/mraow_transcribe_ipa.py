#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mraow Rule-Based Phonetic Transcriber CLI (mraow_transcribe_ipa.py)
Converts Mraow orthography (Trill and Ruh dialects) into International Phonetic Alphabet (IPA).
Includes tone pitch contour numbers (55, 15, 51, 414, 252) and dialect conversion utilities.
"""

import sys
import re
import unicodedata
from typing import Tuple

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Tone Diacritic to IPA Pitch Contour Number Mapping
DIACRITIC_MAP = {
    '\u0304': '⁵⁵',      # Combining Macron: Level / Stative (Tone 1)
    '\u0301': '¹⁵',       # Combining Acute: Rising / Interrogative (Tone 2)
    '\u0300': '⁵¹',       # Combining Grave: Falling / Imperative (Tone 3)
    '\u030c': '⁴¹⁴',      # Combining Caron: Dipping / Playful / Stalking (Tone 4)
    '\u0302': '²⁵²',      # Combining Circumflex: Peaking / Surprise / Alert (Tone 5)
    'macron': '⁵⁵',
    'acute': '¹⁵',
    'grave': '⁵¹',
    'caron': '⁴¹⁴',
    'circumflex': '²⁵²'
}

def convert_trill_to_ruh(word: str) -> str:
    """Converts a Classical Mraow-Trill word into the accessible Mraow-Ruh dialect."""
    w = word
    # Initial clusters
    w = re.sub(r'\bpr([aeiouāēīōūáéíóúàèìòùǎěǐǒǔâêîôû])', r'pur\1', w, flags=re.IGNORECASE)
    w = re.sub(r'\btr([aeiouāēīōūáéíóúàèìòùǎěǐǒǔâêîôû])', r'tur\1', w, flags=re.IGNORECASE)
    w = re.sub(r'\bgr([aeiouāēīōūáéíóúàèìòùǎěǐǒǔâêîôû])', r'gur\1', w, flags=re.IGNORECASE)
    w = re.sub(r'\bmr([aeiouāēīōūáéíóúàèìòùǎěǐǒǔâêîôû])', r'mər\1', w, flags=re.IGNORECASE)
    
    # Syllabic root onomatopoeia with optional diacritics
    w = re.sub(r'prrr', 'puruh', w, flags=re.IGNORECASE)
    w = re.sub(r'pr̂t', 'pûruht', w, flags=re.IGNORECASE)
    w = re.sub(r'trrrt', 'tùruht', w, flags=re.IGNORECASE)
    w = re.sub(r'chírr', 'chíruh', w, flags=re.IGNORECASE)
    w = re.sub(r'mrrr', 'muruh', w, flags=re.IGNORECASE)
    w = re.sub(r'grrr', 'gùruh', w, flags=re.IGNORECASE)
    w = re.sub(r'skrēe', 'skēe', w, flags=re.IGNORECASE)
    w = re.sub(r'skree', 'skee', w, flags=re.IGNORECASE)
    
    # Suffix clitics
    w = re.sub(r'-prr\b', '-pur', w)
    w = re.sub(r'-trr\b', '-tur', w)
    w = re.sub(r'-mrr\b', '-mur', w)
    w = re.sub(r'-grr\b', '-gur', w)
    
    return w

def transcribe_to_ipa(word: str) -> str:
    """Converts Mraow orthography into IPA transcription with tone pitch contours."""
    raw = word.strip().lower()
    
    # Normalize apostrophes
    raw = raw.replace("’", "'")
    
    # Normalize unicode to NFD (canonical decomposition)
    decomposed = unicodedata.normalize('NFD', raw)
    
    detected_tone = ""
    clean_chars = []
    
    for ch in decomposed:
        if ch in DIACRITIC_MAP:
            if not detected_tone:
                detected_tone = DIACRITIC_MAP[ch]
        elif unicodedata.category(ch) == 'Mn':
            # Skip unmapped nonspacing marks
            pass
        else:
            clean_chars.append(ch)
            
    text = "".join(clean_chars)
    
    # Phonetic replacements
    text = text.replace("sh", "ʃ")
    text = text.replace("ch", "tʃ")
    text = text.replace("ny", "ɲ")
    text = text.replace("ng", "ŋ")
    
    # Feline special phonetics
    text = text.replace("aow", "aʊ")
    text = text.replace("mraow", "mraʊ")
    text = text.replace("prrr", "prː")
    text = text.replace("trrrt", "trːt")
    text = text.replace("mrrr", "mrː")
    text = text.replace("grrr", "grː")
    text = text.replace("hss", "hsː")
    text = text.replace("k-k-k", "k.k.k")
    text = text.replace("pft", "pft")
    text = text.replace("k'a", "kʼa")
    text = text.replace("h'm", "hm̥")
    text = text.replace("'", "ʔ")
    
    # Vowels
    text = text.replace("ee", "eː")
    text = text.replace("oo", "oː")
    text = text.replace("aa", "aː")
    text = text.replace("ii", "iː")
    text = text.replace("uu", "uː")
    
    return f"/{text}{detected_tone}/"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        words = sys.argv[1:]
        print(f"{'Input Word':<20} | {'Mraow-Ruh (Accessible)':<24} | {'IPA Transcription'}")
        print("-" * 70)
        for w in words:
            ruh = convert_trill_to_ruh(w)
            ipa = transcribe_to_ipa(w)
            print(f"{w:<20} | {ruh:<24} | {ipa}")
    else:
        sample_words = ["mrāow", "pr̂t", "hsìss", "chírr", "grr̄", "skrēe", "k-k-k", "prīna", "hsaow"]
        print("Usage: python mraow_transcribe_ipa.py <word1> <word2> ...\n")
        print("Sample Demonstrations:")
        print(f"{'Classical (Trill)':<20} | {'Accessible (Ruh)':<24} | {'IPA Transcription'}")
        print("-" * 70)
        for w in sample_words:
            ruh = convert_trill_to_ruh(w)
            ipa = transcribe_to_ipa(w)
            print(f"{w:<20} | {ruh:<24} | {ipa}")
