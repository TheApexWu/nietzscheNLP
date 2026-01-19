#!/usr/bin/env python3
"""
Fix corpus assembly errors:
1. Remove page headers from aphorism text (e.g., "Beyond Good and Evil", "BEYOND GOOD AND EVIL 73")
2. Mark completely corrupted/empty entries
3. Fix Zimmern and Norman specific issues
"""

import json
import re
from pathlib import Path

# Page headers to strip from beginning of aphorisms
PAGE_HEADERS = [
    r'^Beyond Good and Evil\s*\n',
    r'^BEYOND GOOD AND EVIL\s*\d*\s*\n',
    r'^On the prejudices of philosophers\s*\n',
    r'^The free spirit\s*\n',
    r'^Part\s*\d+\s*.*\n',
    r'^PART\s*\d+\s*.*\n',
    r'^Chapter\s*\d+\s*.*\n',
]

# Patterns that indicate complete garbage (not salvageable)
GARBAGE_PATTERNS = [
    r'^y\\/',  # Zimmern decorative element
    r'^[\\\/\^\s€]+$',  # Only special chars
    r'^J\s*$',  # Single letter
    r'^BEYOND GOOD AND EVIL\s*\d+\s*$',  # Just a page header, no content
]


def clean_aphorism_text(text: str) -> tuple[str, list[str]]:
    """Clean page headers from aphorism text. Returns (cleaned_text, list_of_fixes)."""
    fixes = []
    original = text

    # Strip page headers
    for pattern in PAGE_HEADERS:
        match = re.match(pattern, text, re.IGNORECASE)
        if match:
            header = match.group(0).strip()
            text = text[match.end():]
            fixes.append(f"Removed header: '{header[:50]}...'")

    # Check if result is garbage
    text_stripped = text.strip()
    for pattern in GARBAGE_PATTERNS:
        if re.match(pattern, text_stripped, re.DOTALL):
            return '', [f"Marked as corrupted (matched garbage pattern)"]

    # Check if too short to be valid (less than 20 chars of actual content)
    if len(text_stripped) < 20:
        return '', [f"Marked as corrupted (too short: {len(text_stripped)} chars)"]

    return text.strip(), fixes


def fix_corpus_file(filepath: Path) -> dict:
    """Fix assembly errors in a corpus file."""
    with open(filepath) as f:
        data = json.load(f)

    stats = {
        'file': filepath.name,
        'translator': data.get('name', 'Unknown'),
        'headers_stripped': 0,
        'marked_corrupted': 0,
        'fixes': []
    }

    for aph in data['aphorisms']:
        original = aph['text']
        cleaned, fixes = clean_aphorism_text(original)

        if fixes:
            for fix in fixes:
                stats['fixes'].append({
                    'aphorism': aph['number'],
                    'fix': fix,
                    'original_preview': original[:100] + '...' if len(original) > 100 else original
                })

            if cleaned:
                stats['headers_stripped'] += 1
                aph['text'] = cleaned
            else:
                stats['marked_corrupted'] += 1
                aph['text'] = ''  # Mark as empty/corrupted

    # Save fixed file
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return stats


def main():
    corpus_dir = Path('corpus/aligned')

    print('=' * 70)
    print('CORPUS ASSEMBLY FIX REPORT')
    print('=' * 70)

    total_headers = 0
    total_corrupted = 0

    for filepath in sorted(corpus_dir.glob('*.json')):
        stats = fix_corpus_file(filepath)

        if stats['headers_stripped'] > 0 or stats['marked_corrupted'] > 0:
            print(f"\n{stats['translator']}:")
            print(f"  Headers stripped: {stats['headers_stripped']}")
            print(f"  Marked corrupted: {stats['marked_corrupted']}")

            if stats['fixes']:
                print("  Details:")
                for fix in stats['fixes'][:5]:  # Show first 5
                    print(f"    §{fix['aphorism']}: {fix['fix']}")
                if len(stats['fixes']) > 5:
                    print(f"    ... and {len(stats['fixes']) - 5} more")

        total_headers += stats['headers_stripped']
        total_corrupted += stats['marked_corrupted']

    print('\n' + '=' * 70)
    print(f'TOTAL: {total_headers} headers stripped, {total_corrupted} entries marked corrupted')
    print('=' * 70)


if __name__ == '__main__':
    main()
