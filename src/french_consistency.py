"""
Focused French phrase consistency check.
Tests if specific French phrases are preserved identically across translations.
"""

import json
import re
from pathlib import Path
from collections import defaultdict


def load_corpus():
    corpus = {}
    for path in Path('corpus/aligned').glob('*.json'):
        with open(path) as f:
            data = json.load(f)
            corpus[data['name']] = data
    return corpus


def find_phrase_in_text(text: str, phrase: str, context_chars: int = 50) -> dict | None:
    """Find a phrase and extract context."""
    # Case-insensitive search
    idx = text.lower().find(phrase.lower())
    if idx == -1:
        return None

    # Get actual text (preserving case)
    actual = text[idx:idx + len(phrase)]
    context_start = max(0, idx - context_chars)
    context_end = min(len(text), idx + len(phrase) + context_chars)
    context = text[context_start:context_end].replace('\n', ' ')

    return {
        'found': actual,
        'context': f'...{context}...'
    }


def check_french_consistency():
    """Check if known French phrases are preserved across translations."""
    corpus = load_corpus()

    # Known French phrases Nietzsche embeds in BGE
    # Format: (phrase, expected_aphorism or None if multiple)
    known_french = [
        # §35 - The famous Voltaire quote
        ("il ne cherche le vrai que pour faire le bien", 35),

        # §214 - French phrase about Jews
        ("sans gêne", 214),

        # §254 - About French culture
        ("l'art pour l'art", 254),

        # Various philosophical terms often kept in French
        ("ressentiment", None),
        ("par excellence", None),
        ("bon sens", None),
        ("raison d'être", None),

        # §28 - About tempo (check if "presto" is preserved)
        ("presto", 28),
        ("tempo", 28),
    ]

    print("=" * 70)
    print("FRENCH PHRASE CONSISTENCY CHECK")
    print("=" * 70)
    print("Testing if specific French phrases are preserved across translations\n")

    results = []

    for phrase, expected_aph in known_french:
        print(f"\n{'='*60}")
        print(f"PHRASE: '{phrase}'")
        if expected_aph:
            print(f"Expected in: §{expected_aph}")
        print("=" * 60)

        found_in = {}
        for name, data in corpus.items():
            for aph in data['aphorisms']:
                result = find_phrase_in_text(aph['text'], phrase)
                if result:
                    if name not in found_in:
                        found_in[name] = []
                    found_in[name].append({
                        'aphorism': aph['number'],
                        **result
                    })

        if not found_in:
            print("NOT FOUND in any translation")
            results.append({
                'phrase': phrase,
                'expected_aphorism': expected_aph,
                'found_in_count': 0,
                'consistent': None,
                'translators': {}
            })
            continue

        # Check consistency
        all_translators = set(corpus.keys())
        found_translators = set(found_in.keys())
        missing_translators = all_translators - found_translators

        print(f"\nFound in {len(found_translators)}/{len(all_translators)} translations:")

        all_versions = set()
        translator_data = {}
        for name in sorted(found_in.keys()):
            for occurrence in found_in[name]:
                version = occurrence['found'].lower()
                all_versions.add(version)
                print(f"  {name} §{occurrence['aphorism']}: '{occurrence['found']}'")
                translator_data[name] = {
                    'aphorism': occurrence['aphorism'],
                    'found': occurrence['found']
                }

        if missing_translators:
            print(f"\nNOT FOUND in: {missing_translators}")

        is_consistent = len(all_versions) == 1 and len(missing_translators) == 0

        if is_consistent:
            print("\n✓ CONSISTENT: Identical across all translations")
        elif len(all_versions) == 1 and missing_translators:
            print(f"\n⚠️  PARTIAL: Identical where present, but missing from {len(missing_translators)} translation(s)")
        else:
            print(f"\n✗ INCONSISTENT: {len(all_versions)} different versions found")
            print(f"   Versions: {all_versions}")

        results.append({
            'phrase': phrase,
            'expected_aphorism': expected_aph,
            'found_in_count': len(found_translators),
            'total_translators': len(all_translators),
            'consistent': is_consistent,
            'missing_from': list(missing_translators),
            'versions': list(all_versions),
            'translators': translator_data
        })

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    consistent_count = sum(1 for r in results if r['consistent'] is True)
    partial_count = sum(1 for r in results if r['consistent'] is False and len(r.get('versions', [])) == 1)
    inconsistent_count = sum(1 for r in results if r['consistent'] is False and len(r.get('versions', [])) > 1)
    not_found = sum(1 for r in results if r['found_in_count'] == 0)

    print(f"\nTotal phrases tested: {len(known_french)}")
    print(f"Consistent (identical in all): {consistent_count}")
    print(f"Partial (identical where present): {partial_count}")
    print(f"Inconsistent (variations exist): {inconsistent_count}")
    print(f"Not found: {not_found}")

    # Key finding for §35
    print("\n" + "-" * 70)
    print("KEY FINDING: §35 French Quote")
    print("-" * 70)

    for r in results:
        if r['phrase'] == "il ne cherche le vrai que pour faire le bien":
            if r['consistent']:
                print("The French quote IS preserved identically across all translations.")
                print("This is NOT a source of embedding divergence.")
            elif r['found_in_count'] > 0:
                print(f"The French quote is present in {r['found_in_count']} translations.")
                print(f"Missing from: {r['missing_from']}")
                if len(r['versions']) > 1:
                    print(f"Variations found: {r['versions']}")
                    print("This COULD contribute to embedding divergence.")
            else:
                print("The French quote was NOT FOUND in any translation.")
                print("May need manual verification or different detection approach.")
            break

    # Save results
    out_path = Path('outputs/french_consistency.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\nResults saved to {out_path}")

    return results


if __name__ == '__main__':
    check_french_consistency()
