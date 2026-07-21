#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generalized Rule-Based Phonetic Transcriber CLI (transcribe_ipa.py)
Transforms target language orthography into International Phonetic Alphabet (IPA).
"""

import sys
import re

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

def transcribe_to_ipa(word: str) -> str:
    """
    Converts target language orthography into exact IPA phonetics via rule cascades.
    Handles vowel length macrons, palatalization, and context-sensitive fricative voicing.
    """
    word = word.lower().strip()
    
    # Phase 1: Vowel Length Macrons
    vowel_map = {
        'ā': 'aː', 'ē': 'eː', 'ī': 'iː', 'ō': 'oː', 'ū': 'uː', 'ȳ': 'yː', 'ǣ': 'æː'
    }
    
    # Phase 2: Digraphs & Palatalization
    word = word.replace('ċċ', 'tʃː').replace('ċ', 'tʃ')
    word = word.replace('cg', 'ddʒ').replace('sc', 'ʃ')
    word = word.replace('ġġ', 'jː').replace('ġ', 'j')
    
    # Phase 3: Context-Sensitive Fricative Voicing (f -> v, s -> z, þ -> ð)
    vowels = set("aæeiouyāēīōūȳǣ")
    chars = list(word)
    for i in range(len(chars)):
        if chars[i] in ['f', 's', 'þ']:
            in_vocalic_env = (i > 0 and chars[i-1] in vowels) and (i < len(chars)-1 and chars[i+1] in vowels)
            if in_vocalic_env:
                chars[i] = {'f': 'v', 's': 'z', 'þ': 'ð'}[chars[i]]
            else:
                if chars[i] == 'þ': chars[i] = 'θ'
                
    ipa = "".join(chars)
    for v_orig, v_ipa in vowel_map.items():
        ipa = ipa.replace(v_orig, v_ipa)
        
    return f"/{ipa}/"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        words = sys.argv[1:]
        for w in words:
            print(f"'{w}' -> {transcribe_to_ipa(w)}")
    else:
        print("Usage: python transcribe_ipa.py <word1> <word2> ...")
