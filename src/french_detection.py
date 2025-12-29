"""
French phrase detection in Nietzsche's Beyond Good and Evil.
Goal: Identify embedded French and verify consistency across translations.
"""

import json
import re
from pathlib import Path
from collections import defaultdict


# Common French phrases and words Nietzsche uses
FRENCH_PATTERNS = [
    # Quoted French phrases (most reliable)
    r'"[^"]*(?:le|la|les|un|une|de|du|des|à|et|est|sont|pour|que|qui|ne|pas|plus|bien|mal|tout|rien|faire|avoir|être|dit|fait)[^"]*"',

    # Known Nietzsche French phrases
    r'il ne cherche le vrai que pour faire le bien',
    r'bon sens',
    r'bel esprit',
    r'l\'art pour l\'art',
    r'ressentiment',  # Often kept in French even in translations
    r'par excellence',
    r'vis-à-vis',
    r'raison d\'être',
    r'entre nous',
    r'c\'est',
    r'n\'est-ce pas',
    r'tout comprendre',
    r'noblesse oblige',
    r'cause première',
    r'idée fixe',
    r'esprit',
    r'savoir vivre',
    r'je ne sais quoi',
    r'laissez',
    r'chez',

    # French articles/prepositions as markers
    r'\b(?:le|la|les|l\')\s+\w+(?:\s+\w+)?(?:\s+(?:de|du|des|à)\s+\w+)?',
]

# Compile patterns
FRENCH_REGEX = [re.compile(p, re.IGNORECASE) for p in FRENCH_PATTERNS]


def detect_french(text: str) -> list[dict]:
    """Detect French phrases in text."""
    matches = []
    for pattern in FRENCH_REGEX:
        for match in pattern.finditer(text):
            phrase = match.group().strip()
            # Filter out false positives (common English words)
            if phrase.lower() not in ['le', 'la', 'a', 'the', 'de', 'to']:
                matches.append({
                    'phrase': phrase,
                    'start': match.start(),
                    'end': match.end(),
                    'context': text[max(0, match.start()-30):min(len(text), match.end()+30)]
                })
    return matches


def load_corpus():
    corpus = {}
    for path in Path('corpus/aligned').glob('*.json'):
        with open(path) as f:
            data = json.load(f)
            corpus[data['name']] = data
    return corpus


def analyze_french_in_corpus():
    """Find all French phrases and check consistency across translations."""
    corpus = load_corpus()

    # Find common aphorisms
    all_nums = [set(a['number'] for a in t['aphorisms']) for t in corpus.values()]
    common = sorted(set.intersection(*all_nums))

    print("=" * 70)
    print("FRENCH PHRASE DETECTION IN BGE TRANSLATIONS")
    print("=" * 70)

    # Track French by aphorism
    french_by_aphorism = defaultdict(lambda: defaultdict(list))

    for name, data in corpus.items():
        for aph in data['aphorisms']:
            if aph['number'] in common:
                matches = detect_french(aph['text'])
                for m in matches:
                    french_by_aphorism[aph['number']][name].append(m['phrase'])

    # Find aphorisms with French
    aphorisms_with_french = {num: phrases for num, phrases in french_by_aphorism.items()
                            if any(phrases.values())}

    print(f"\nAphorisms with detected French: {len(aphorisms_with_french)}/{len(common)}")

    # Analyze each aphorism with French
    print("\n" + "-" * 70)
    print("FRENCH PHRASES BY APHORISM")
    print("-" * 70)

    consistent = []
    inconsistent = []

    for num in sorted(aphorisms_with_french.keys()):
        phrases_by_translator = french_by_aphorism[num]

        # Get unique phrases across all translators
        all_phrases = set()
        for translator_phrases in phrases_by_translator.values():
            all_phrases.update([p.lower().strip('"\'') for p in translator_phrases])

        # Check if German has the French
        german_phrases = set(p.lower().strip('"\'') for p in phrases_by_translator.get('Gutenberg', []))
        english_translators = [n for n in phrases_by_translator.keys() if n != 'Gutenberg']

        # Check consistency
        english_phrases = defaultdict(set)
        for name in english_translators:
            for p in phrases_by_translator.get(name, []):
                english_phrases[name].add(p.lower().strip('"\''))

        # Are the English translations consistent with each other?
        all_english = [english_phrases[n] for n in english_translators if english_phrases[n]]
        if all_english:
            common_english = set.intersection(*all_english) if len(all_english) > 1 else all_english[0]
            all_english_union = set.union(*all_english)
        else:
            common_english = set()
            all_english_union = set()

        is_consistent = len(all_english) <= 1 or common_english == all_english_union

        print(f"\n§{num}:")
        print(f"  German: {list(german_phrases) if german_phrases else '(none detected)'}")
        for name in english_translators:
            if english_phrases[name]:
                print(f"  {name}: {list(english_phrases[name])}")

        if not is_consistent:
            print(f"  ⚠️  INCONSISTENT across translators")
            inconsistent.append(num)
        elif german_phrases and all_english_union:
            if german_phrases & all_english_union:
                print(f"  ✓ French preserved from German")
                consistent.append(num)
            else:
                print(f"  ? Different French detected")
        elif german_phrases and not all_english_union:
            print(f"  ✗ French in German, not detected in English")

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    print(f"\nTotal aphorisms with French: {len(aphorisms_with_french)}")
    print(f"Consistent across translations: {len(consistent)}")
    print(f"Inconsistent across translations: {len(inconsistent)}")

    if inconsistent:
        print(f"\nInconsistent aphorisms: {inconsistent}")
        print("(These may need manual review)")

    # Check §35 specifically (highest divergence, has French)
    print("\n" + "-" * 70)
    print("DETAILED CHECK: §35 (Highest Divergence)")
    print("-" * 70)

    if 35 in aphorisms_with_french:
        for name, data in corpus.items():
            for aph in data['aphorisms']:
                if aph['number'] == 35:
                    print(f"\n{name}:")
                    # Find the French quote
                    french_match = re.search(r'"il ne cherche.*?"', aph['text'], re.IGNORECASE)
                    if french_match:
                        print(f"  Found: {french_match.group()}")
                    else:
                        # Try broader search
                        french_match = re.search(r'cherche.*?bien', aph['text'], re.IGNORECASE)
                        if french_match:
                            print(f"  Found (partial): ...{french_match.group()}...")
                        else:
                            print(f"  No French quote detected")
                            print(f"  First 200 chars: {aph['text'][:200]}...")
                    break

    # Save results
    results = {
        'total_aphorisms': len(common),
        'aphorisms_with_french': len(aphorisms_with_french),
        'consistent': consistent,
        'inconsistent': inconsistent,
        'french_by_aphorism': {
            num: {name: phrases for name, phrases in translators.items()}
            for num, translators in french_by_aphorism.items()
            if any(translators.values())
        }
    }

    out_path = Path('outputs/french_detection.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {out_path}")


def check_french_consistency_detailed():
    """Deep dive: Check if French phrases are identical across all translations."""
    corpus = load_corpus()

    print("\n" + "=" * 70)
    print("FRENCH PHRASE CONSISTENCY CHECK")
    print("=" * 70)
    print("Checking if French text is preserved identically across translations\n")

    # Known French phrases to look for
    known_french = [
        ('il ne cherche le vrai que pour faire le bien', 35),
        ('ressentiment', None),  # Appears multiple times
        ('par excellence', None),
        ('l\'art pour l\'art', None),
        ('bon sens', None),
    ]

    for phrase, expected_aph in known_french:
        print(f"\n--- Searching for: '{phrase}' ---")

        found_in = defaultdict(list)
        for name, data in corpus.items():
            for aph in data['aphorisms']:
                if phrase.lower() in aph['text'].lower():
                    # Extract the actual text around the phrase
                    idx = aph['text'].lower().find(phrase.lower())
                    actual = aph['text'][idx:idx+len(phrase)+20].split()[0:len(phrase.split())+2]
                    found_in[name].append((aph['number'], ' '.join(actual[:len(phrase.split())])))

        if found_in:
            # Check if all translations have it
            all_translators = set(corpus.keys())
            translators_with = set(found_in.keys())
            translators_without = all_translators - translators_with

            print(f"Found in {len(translators_with)}/{len(all_translators)} translations:")
            for name in sorted(found_in.keys()):
                for aph_num, actual_text in found_in[name]:
                    print(f"  {name} §{aph_num}: '{actual_text}'")

            if translators_without:
                print(f"NOT found in: {translators_without}")

            # Check if the phrase is identical
            all_versions = set()
            for name, occurrences in found_in.items():
                for aph_num, actual_text in occurrences:
                    all_versions.add(actual_text.lower())

            if len(all_versions) == 1:
                print("✓ IDENTICAL across all translations")
            else:
                print(f"⚠️  VARIATIONS: {all_versions}")
        else:
            print("Not found in any translation")


if __name__ == '__main__':
    analyze_french_in_corpus()
    check_french_consistency_detailed()
