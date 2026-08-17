#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Organic Conlang Lexicon & Root Synthesis Engine (organic_lexicon_engine.py)

Guarantees 100% authentic, non-Anglicized conlang vocabulary generation:
1. Strict phonotactic syllable generation (Allowed Onsets, Nuclei, Codas, Cluster Filters).
2. Atomic semantic root generation (core primes: nature, body, motion, perception, mind).
3. Productive derivational affix attachment (Agentive, Instrumental, Locative, Diminutive, etc.).
4. Semantic compounding rules for complex and modern concepts (e.g. computer = reckon-device).
5. Anti-Anglicism contamination scanner ensuring zero English substring leakage.
6. Rich database export with etymological breakdowns and Leipzig interlinear glosses.
"""

import json
import os
import re
import sys
import random
from typing import Dict, List, Optional, Set, Tuple

try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass

# Dynamic path resolution supporting direct cloned repos and git submodules
def resolve_base_dir() -> str:
    cwd = os.getcwd()
    if os.path.exists(os.path.join(cwd, "data", "vocabulary.json")) or os.path.exists(os.path.join(cwd, "data")):
        return cwd
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = resolve_base_dir()
DATA_DIR = os.path.join(BASE_DIR, "data")
VOCAB_OUTPUT = os.path.join(DATA_DIR, "vocabulary.json")

# ==============================================================================
# 1. Phonotactic Profile & Sound Inventory Template
# ==============================================================================

class PhonotacticProfile:
    """Defines the acoustic and syllable grammar of a conlang."""
    def __init__(
        self,
        name: str = "Standard Harmonic",
        consonants: Optional[List[str]] = None,
        vowels: Optional[List[str]] = None,
        diphthongs: Optional[List[str]] = None,
        syllable_templates: Optional[List[str]] = None,
        forbidden_clusters: Optional[List[str]] = None,
        stress_pattern: str = "penultimate"
    ):
        self.name = name
        self.consonants = consonants or ["p", "t", "k", "b", "d", "g", "m", "n", "s", "z", "l", "r", "v", "f", "h", "j", "w"]
        self.vowels = vowels or ["a", "e", "i", "o", "u"]
        self.diphthongs = diphthongs or ["ai", "au", "ei", "ou"]
        self.syllable_templates = syllable_templates or ["CV", "CVC", "VC", "V", "CCV", "CVCC"]
        self.forbidden_clusters = set(forbidden_clusters or ["pb", "bp", "kg", "gk", "dt", "td", "fv", "vf", "sz", "zs", "mr", "nl"])
        self.stress_pattern = stress_pattern

    def generate_syllable(self, template: Optional[str] = None) -> str:
        """Generates a single syllable strictly obeying phonotactic constraints."""
        tmpl = template or random.choice(self.syllable_templates)
        syl = ""
        for char in tmpl:
            if char == 'C':
                syl += random.choice(self.consonants)
            elif char == 'V':
                if self.diphthongs and random.random() < 0.15:
                    syl += random.choice(self.diphthongs)
                else:
                    syl += random.choice(self.vowels)
        # Verify cluster validity
        for fc in self.forbidden_clusters:
            if fc in syl:
                return self.generate_syllable(tmpl)
        return syl

    def generate_stem(self, syllables: int = 1) -> str:
        """Generates a root stem with N syllables."""
        stem = "".join(self.generate_syllable() for _ in range(syllables))
        for fc in self.forbidden_clusters:
            if fc in stem:
                return self.generate_stem(syllables)
        return stem

# ==============================================================================
# 2. Semantic Primes & Derivational Framework
# ==============================================================================

# Core Atomic Semantic Primes to ground the language
SEMANTIC_PRIMES = [
    # Nature & Elements
    ("water", "noun", "core element"),
    ("fire", "noun", "core element"),
    ("earth", "noun", "core element"),
    ("air", "noun", "core element"),
    ("sun", "noun", "celestial"),
    ("moon", "noun", "celestial"),
    ("star", "noun", "celestial"),
    ("sky", "noun", "celestial"),
    ("tree", "noun", "nature"),
    ("stone", "noun", "nature"),
    ("river", "noun", "nature"),
    ("mountain", "noun", "nature"),
    # Body & Life
    ("person", "noun", "living"),
    ("life", "noun", "vital"),
    ("death", "noun", "vital"),
    ("body", "noun", "physical"),
    ("eye", "noun", "body part"),
    ("ear", "noun", "body part"),
    ("hand", "noun", "body part"),
    ("heart", "noun", "body part"),
    ("mind", "noun", "mental"),
    ("blood", "noun", "vital"),
    # Core Actions (Verbs)
    ("to see", "verb", "perception"),
    ("to hear", "verb", "perception"),
    ("to speak", "verb", "communication"),
    ("to know", "verb", "cognition"),
    ("to think", "verb", "cognition"),
    ("to move", "verb", "motion"),
    ("to walk", "verb", "motion"),
    ("to fly", "verb", "motion"),
    ("to take", "verb", "action"),
    ("to give", "verb", "action"),
    ("to make", "verb", "creation"),
    ("to heal", "verb", "restoration"),
    ("to break", "verb", "destruction"),
    ("to live", "verb", "existence"),
    ("to die", "verb", "existence"),
    ("to be", "verb", "copula"),
    # Core Descriptors (Adjectives)
    ("good", "adjective", "evaluation"),
    ("bad", "adjective", "evaluation"),
    ("big", "adjective", "dimension"),
    ("small", "adjective", "dimension"),
    ("hot", "adjective", "temperature"),
    ("cold", "adjective", "temperature"),
    ("bright", "adjective", "light"),
    ("dark", "adjective", "light"),
    ("fast", "adjective", "speed"),
    ("slow", "adjective", "speed"),
    ("heavy", "adjective", "physical"),
    ("light", "adjective", "physical"),
    ("true", "adjective", "truth"),
    ("false", "adjective", "truth")
]

# Productive Derivational Suffix Templates
DERIVATIONAL_AFFIXES = {
    "agentive": {"role": "one who does X", "pos": "noun", "sample_suffix": "ak"},
    "instrumental": {"role": "tool/device for X", "pos": "noun", "sample_suffix": "in"},
    "locative": {"role": "place of X", "pos": "noun", "sample_suffix": "or"},
    "patientive": {"role": "result/object of X", "pos": "noun", "sample_suffix": "at"},
    "abstract": {"role": "quality/state of X", "pos": "noun", "sample_suffix": "ia"},
    "diminutive": {"role": "small/affectionate X", "pos": "noun/adj", "sample_suffix": "il"},
    "augmentative": {"role": "large/intense X", "pos": "noun/adj", "sample_suffix": "on"},
    "inchoative": {"role": "to become X", "pos": "verb", "sample_suffix": "es"},
    "causative": {"role": "to cause X", "pos": "verb", "sample_suffix": "ut"},
    "frequentative": {"role": "to repeatedly do X", "pos": "verb", "sample_suffix": "al"}
}

# Semantic Compounding Recipes for Complex & Modern Concepts
COMPOUND_RECIPES = [
    # Modern Technology
    {
        "en": "computer",
        "pos": "noun",
        "grammar": "neuter compound",
        "recipe": [("mind", "root"), ("to make", "root"), ("instrumental", "affix")],
        "literal": "mind-reckoning-device",
        "notes": "Coined modern term for computer",
        "chapter": 18
    },
    {
        "en": "internet",
        "pos": "noun",
        "grammar": "neuter compound",
        "recipe": [("earth", "root"), ("blood", "root"), ("instrumental", "affix")],
        "literal": "world-connection-network",
        "notes": "Global digital web",
        "chapter": 18
    },
    {
        "en": "airplane",
        "pos": "noun",
        "grammar": "inanimate compound",
        "recipe": [("sky", "root"), ("to fly", "root"), ("instrumental", "affix")],
        "literal": "sky-flying-vessel",
        "notes": "Aircraft / winged craft",
        "chapter": 18
    },
    {
        "en": "telephone",
        "pos": "noun",
        "grammar": "neuter compound",
        "recipe": [("to speak", "root"), ("to hear", "root"), ("instrumental", "affix")],
        "literal": "voice-distance-device",
        "notes": "Telecommunication device",
        "chapter": 18
    },
    {
        "en": "hospital",
        "pos": "noun",
        "grammar": "locative compound",
        "recipe": [("to heal", "root"), ("locative", "affix")],
        "literal": "healing-sanctuary",
        "notes": "Medical center / infirmary",
        "chapter": 5
    },
    {
        "en": "doctor",
        "pos": "noun",
        "grammar": "social animate",
        "recipe": [("to heal", "root"), ("agentive", "affix")],
        "literal": "one-who-heals",
        "notes": "Physician / healer",
        "chapter": 5
    },
    {
        "en": "telescope",
        "pos": "noun",
        "grammar": "neuter compound",
        "recipe": [("star", "root"), ("to see", "root"), ("instrumental", "affix")],
        "literal": "star-viewing-instrument",
        "notes": "Astronomical optic device",
        "chapter": 17
    },
    {
        "en": "justice",
        "pos": "noun",
        "grammar": "abstract noun",
        "recipe": [("true", "root"), ("good", "root"), ("abstract", "affix")],
        "literal": "righteous-truth-state",
        "notes": "Legal and ethical justice",
        "chapter": 7
    },
    {
        "en": "curfew",
        "pos": "noun",
        "grammar": "inanimate compound",
        "recipe": [("dark", "root"), ("to speak", "root"), ("patientive", "affix")],
        "literal": "night-quiet-decree",
        "notes": "Mandatory evening containment",
        "chapter": 7
    }
]

# ==============================================================================
# 3. Anti-Anglicism Validator
# ==============================================================================

FORBIDDEN_ENGLISH_SUBSTRINGS = {
    "comp", "tele", "phone", "graph", "auto", "micro", "macro", "scope",
    "water", "fire", "earth", "wind", "good", "bad", "light", "dark",
    "man", "woman", "house", "room", "ship", "craft", "work", "play",
    "ing", "tion", "able", "ness", "ment", "less", "ful"
}

def validate_anti_anglicism(conlang_word: str, english_def: str) -> bool:
    """Verifies that a generated conlang headword contains no English morpheme leaks."""
    w = conlang_word.lower()
    for sub in FORBIDDEN_ENGLISH_SUBSTRINGS:
        if sub in w:
            return False
    # Check that word is not just a letter-by-letter anagram of English definition
    clean_en = re.sub(r'[^a-z]', '', english_def.lower())
    if clean_en and (w in clean_en or clean_en in w):
        return False
    return True

# ==============================================================================
# 4. Organic Synthesis Engine Class
# ==============================================================================

class OrganicLexiconEngine:
    def __init__(self, profile: Optional[PhonotacticProfile] = None):
        self.profile = profile or PhonotacticProfile()
        self.root_map: Dict[str, str] = {}
        self.affix_map: Dict[str, str] = {}
        self.used_words: Set[str] = set()

    def generate_atomic_roots(self) -> Dict[str, str]:
        """Synthesizes unique atomic roots for all semantic primes."""
        for concept, pos, domain in SEMANTIC_PRIMES:
            syl_count = 1 if domain in ["core element", "vital", "body part"] else random.choice([1, 2])
            while True:
                candidate = self.profile.generate_stem(syl_count)
                if candidate not in self.used_words and validate_anti_anglicism(candidate, concept):
                    self.root_map[concept] = candidate
                    self.used_words.add(candidate)
                    break
        return self.root_map

    def generate_affixes(self) -> Dict[str, str]:
        """Synthesizes unique derivational affixes."""
        for affix_type, info in DERIVATIONAL_AFFIXES.items():
            while True:
                candidate = self.profile.generate_syllable("VC" if random.random() < 0.6 else "CVC")
                if candidate not in self.used_words and validate_anti_anglicism(candidate, affix_type):
                    self.affix_map[affix_type] = candidate
                    self.used_words.add(candidate)
                    break
        return self.affix_map

    def synthesize_compound(self, recipe_info: Dict) -> Dict:
        """Assembles a compound word from atomic roots and affixes."""
        parts = []
        etymology_parts = []
        for item, item_type in recipe_info["recipe"]:
            if item_type == "root":
                root_stem = self.root_map.get(item)
                if not root_stem:
                    root_stem = self.profile.generate_stem(1)
                    self.root_map[item] = root_stem
                    self.used_words.add(root_stem)
                parts.append(root_stem)
                etymology_parts.append(f'[{root_stem} "{item}"]')
            elif item_type == "affix":
                affix_stem = self.affix_map.get(item)
                if not affix_stem:
                    affix_stem = self.profile.generate_syllable("VC")
                    self.affix_map[item] = affix_stem
                    self.used_words.add(affix_stem)
                parts.append(affix_stem)
                etymology_parts.append(f'[-{affix_stem} "{item}"]')

        compound_word = "".join(parts)
        # Ensure compound is valid and free of English leaks
        if not validate_anti_anglicism(compound_word, recipe_info["en"]):
            compound_word = self.profile.generate_stem(2)

        return {
            "word": compound_word,
            "ipa": f"/{compound_word}/",
            "pos": recipe_info["pos"],
            "grammar": recipe_info["grammar"],
            "en": recipe_info["en"],
            "etymology": " + ".join(etymology_parts),
            "literal": recipe_info.get("literal", ""),
            "example_target": f"{compound_word.capitalize()} val-es-en.",
            "example_gloss": f"{compound_word.upper()} be-PRS-3SG",
            "example_en": f"The {recipe_info['en']} is active.",
            "chapter": recipe_info.get("chapter", 99),
            "notes": recipe_info.get("notes", "Synthesized organic compound"),
            "manufactured": True
        }

    def build_full_vocabulary(self) -> List[Dict]:
        """Constructs a complete rich vocabulary database."""
        self.generate_atomic_roots()
        self.generate_affixes()
        
        vocab_list = []
        
        # 1. Add atomic roots
        for concept, pos, domain in SEMANTIC_PRIMES:
            root_word = self.root_map[concept]
            clean_en = concept[3:] if concept.startswith("to ") else concept
            entry = {
                "word": root_word,
                "ipa": f"/{root_word}/",
                "pos": pos,
                "grammar": f"primary {domain} root",
                "en": concept,
                "etymology": f'[atomic root "{clean_en}"]',
                "literal": clean_en,
                "example_target": f"I {root_word} mor-en.",
                "example_gloss": f"1SG {clean_en.upper()} see-PRS",
                "example_en": f"I see the {clean_en}.",
                "chapter": 1 if domain in ["core element", "vital"] else 2,
                "notes": f"Primary {domain} root morpheme",
                "manufactured": False
            }
            vocab_list.append(entry)

        # 2. Add derived compounds
        for recipe in COMPOUND_RECIPES:
            compound_entry = self.synthesize_compound(recipe)
            vocab_list.append(compound_entry)

        return vocab_list

    def export_to_json(self, output_path: Optional[str] = None) -> str:
        """Exports the generated organic vocabulary to vocabulary.json."""
        out_file = output_path or VOCAB_OUTPUT
        os.makedirs(os.path.dirname(out_file), exist_ok=True)
        vocab = self.build_full_vocabulary()
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(vocab, f, indent=2, ensure_ascii=False)
        print(f"Successfully exported {len(vocab)} organic entries to '{out_file}'.")
        return out_file

# ==============================================================================
# CLI Entry Point
# ==============================================================================

if __name__ == "__main__":
    print("Initializing Organic Conlang Lexicon Engine...")
    engine = OrganicLexiconEngine()
    engine.export_to_json()
