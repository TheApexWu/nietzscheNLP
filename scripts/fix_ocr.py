#!/usr/bin/env python3
"""
Fix OCR errors in the aligned corpus.
Common pattern: 'li' scanned as 'h' (e.g., 'life' -> 'hfe')
"""

import json
import re
from pathlib import Path

# OCR replacement patterns (wrong -> correct)
# Sorted by length (longest first) to avoid partial replacements
OCR_FIXES = [
    # -ality words
    ('spirituahty', 'spirituality'),
    ('individuahty', 'individuality'),
    ('personahty', 'personality'),
    ('nationahty', 'nationality'),
    ('originahty', 'originality'),
    ('brutahty', 'brutality'),
    ('totahty', 'totality'),
    ('mortahty', 'mortality'),
    ('sensuahty', 'sensuality'),
    ('morahty', 'morality'),
    ('quahty', 'quality'),
    ('reahty', 'reality'),

    # -ibility/-ability words
    ('responsibihty', 'responsibility'),
    ('possibihty', 'possibility'),
    ('probabihty', 'probability'),
    ('sensibihty', 'sensibility'),
    ('nobihty', 'nobility'),

    # -ish words
    ('accomphsh', 'accomplish'),
    ('estabhsh', 'establish'),
    ('Enghsh', 'English'),
    ('foohsh', 'foolish'),
    ('pubhsh', 'publish'),
    ('abohsh', 'abolish'),
    ('pohsh', 'polish'),

    # -ight words
    ('enhghten', 'enlighten'),
    ('dehght', 'delight'),
    ('fhght', 'flight'),
    ('shght', 'slight'),
    ('phght', 'plight'),
    ('hght', 'light'),

    # -ieve/-ief words
    ('beheve', 'believe'),
    ('reheve', 'relieve'),
    ('acheve', 'achieve'),
    ('behef', 'belief'),
    ('rehef', 'relief'),

    # -ine words
    ('mascuhne', 'masculine'),
    ('femimne', 'feminine'),
    ('determme', 'determine'),
    ('examme', 'examine'),
    ('imagme', 'imagine'),
    ('divme', 'divine'),
    ('inchne', 'incline'),
    ('dechne', 'decline'),

    # -icate/-icit words
    ('comphcated', 'complicated'),
    ('duphcate', 'duplicate'),
    ('imphcit', 'implicit'),
    ('exphcit', 'explicit'),

    # -igion/-igious words
    ('rehgious', 'religious'),
    ('rehgion', 'religion'),

    # -igent/-igence words
    ('intelhgence', 'intelligence'),
    ('intelhgent', 'intelligent'),
    ('neghgence', 'negligence'),
    ('neghgent', 'negligent'),

    # -ies/-ily words
    ('supphes', 'supplies'),
    ('imphes', 'implies'),
    ('apphes', 'applies'),
    ('rephes', 'replies'),

    # -imit/-ind words
    ('hmit', 'limit'),
    ('behnd', 'behind'),
    ('bhnd', 'blind'),

    # -ive/-ife words
    ('hve', 'live'),
    ('hfe', 'life'),

    # -ite words
    ('pohte', 'polite'),
    ('ehte', 'elite'),

    # -iberal/-iberty
    ('hberal', 'liberal'),
    ('hberty', 'liberty'),

    # -inguistic
    ('hnguistic', 'linguistic'),

    # -ilieu
    ('mihieu', 'milieu'),
    ('miheu', 'milieu'),

    # German words
    ('vomehm', 'vornehm'),
    ('Vomehm', 'Vornehm'),

    # Spirit (common)
    ('spint', 'spirit'),
]

def fix_ocr_text(text: str) -> tuple[str, int]:
    """Fix OCR errors in text. Returns (fixed_text, num_fixes)."""
    total_fixes = 0

    for wrong, right in OCR_FIXES:
        # Case-sensitive replacement
        count = text.count(wrong)
        if count > 0:
            text = text.replace(wrong, right)
            total_fixes += count

        # Also try capitalized version
        wrong_cap = wrong.capitalize()
        right_cap = right.capitalize()
        count = text.count(wrong_cap)
        if count > 0:
            text = text.replace(wrong_cap, right_cap)
            total_fixes += count

        # And uppercase
        wrong_upper = wrong.upper()
        right_upper = right.upper()
        count = text.count(wrong_upper)
        if count > 0:
            text = text.replace(wrong_upper, right_upper)
            total_fixes += count

    return text, total_fixes


def fix_corpus_file(filepath: Path, dry_run: bool = False) -> dict:
    """Fix OCR errors in a corpus JSON file."""
    with open(filepath) as f:
        data = json.load(f)

    stats = {
        'file': filepath.name,
        'translator': data.get('name', 'Unknown'),
        'aphorisms_fixed': 0,
        'total_fixes': 0,
        'examples': []
    }

    for aph in data['aphorisms']:
        original = aph['text']
        fixed, num_fixes = fix_ocr_text(original)

        if num_fixes > 0:
            stats['aphorisms_fixed'] += 1
            stats['total_fixes'] += num_fixes

            if len(stats['examples']) < 3:
                # Find a short example of what was fixed
                for wrong, right in OCR_FIXES:
                    if wrong in original:
                        # Extract context around the error
                        idx = original.find(wrong)
                        start = max(0, idx - 20)
                        end = min(len(original), idx + len(wrong) + 20)
                        stats['examples'].append({
                            'aphorism': aph['number'],
                            'wrong': wrong,
                            'right': right,
                            'context': f'...{original[start:end]}...'
                        })
                        break

            if not dry_run:
                aph['text'] = fixed

    if not dry_run and stats['total_fixes'] > 0:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    return stats


def main():
    corpus_dir = Path('corpus/aligned')

    print('=' * 70)
    print('OCR FIX REPORT')
    print('=' * 70)

    total_files = 0
    total_aphorisms = 0
    total_fixes = 0

    for filepath in sorted(corpus_dir.glob('*.json')):
        stats = fix_corpus_file(filepath, dry_run=False)
        total_files += 1
        total_aphorisms += stats['aphorisms_fixed']
        total_fixes += stats['total_fixes']

        print(f"\n{stats['translator']}:")
        print(f"  Aphorisms fixed: {stats['aphorisms_fixed']}")
        print(f"  Total replacements: {stats['total_fixes']}")

        if stats['examples']:
            print("  Examples:")
            for ex in stats['examples'][:2]:
                print(f"    Aph {ex['aphorism']}: '{ex['wrong']}' -> '{ex['right']}'")

    print('\n' + '=' * 70)
    print(f'TOTAL: {total_fixes} fixes across {total_aphorisms} aphorisms in {total_files} files')
    print('=' * 70)


if __name__ == '__main__':
    main()
