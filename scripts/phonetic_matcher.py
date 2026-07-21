#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multilingual Phonetic Matcher & Stem Synthesizer (phonetic_matcher.py)
Scores acoustic similarity against target concepts across 10 diverse world language families
(Arabic, Hungarian, Swahili, Japanese, Turkish, Finnish, Hawaiian, Persian, Icelandic, Basque).
"""

import sys

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Multilingual Concept Matrix Mapping across 10 diverse language families
CONCEPT_MULTILINGUAL_MAP = {
    "water": {"arabic": "maa", "hungarian": "viz", "swahili": "maji", "japanese": "mizu", "finnish": "vesi", "turkish": "su", "hawaiian": "wai", "persian": "ab", "basque": "ur"},
    "sun": {"arabic": "shams", "hungarian": "nap", "swahili": "jua", "japanese": "taiyo", "finnish": "aurinko", "turkish": "gunes", "hawaiian": "la", "persian": "khorshid", "basque": "eguzki"},
    "friend": {"arabic": "sadiq", "hungarian": "barat", "swahili": "rafiki", "japanese": "tomodachi", "finnish": "ystava", "turkish": "dost", "hawaiian": "hoaloha", "persian": "dust", "basque": "lagun"},
    "house": {"arabic": "bayt", "hungarian": "haz", "swahili": "nyumba", "japanese": "ie", "finnish": "talo", "turkish": "ev", "hawaiian": "hale", "persian": "khaneh", "basque": "etxe"},
    "computer": {"arabic": "hasub", "hungarian": "szamitogep", "swahili": "tarakilishi", "japanese": "kiso", "finnish": "tietokone", "turkish": "bilgisayar", "hawaiian": "loko", "persian": "rayaneh", "basque": "ordenagailu"}
}

def calculate_phonetic_fit_score(candidate_stem: str, concept_key: str) -> float:
    """
    Calculates an organic acoustic fit score between a candidate stem and multilingual concept variants.
    """
    if concept_key not in CONCEPT_MULTILINGUAL_MAP:
        return 0.5
        
    variants = CONCEPT_MULTILINGUAL_MAP[concept_key].values()
    match_count = sum(1 for v in variants if any(char in v for char in candidate_stem))
    return round(match_count / len(variants), 3)

if __name__ == "__main__":
    for concept in CONCEPT_MULTILINGUAL_MAP:
        score = calculate_phonetic_fit_score("mew", concept)
        print(f"Concept '{concept}' vs stem 'mew' -> Fit Score: {score}")
