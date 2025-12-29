"""
OCR error cleaning for scanned PDF translations.
Fixes common recognition errors from Internet Archive digitization.
"""

import re
import json
from pathlib import Path


# Known OCR errors found in the corpus
# Format: (wrong, correct, context_hint)
OCR_FIXES = [
    # French phrase errors in §35
    ("sl ne cherche", "il ne cherche", "French quote"),
    ("le hien", "le bien", "French quote"),

    # Common OCR confusions
    ("rn", "m", None),  # "rn" often misread as "m" - be careful with this
    ("vv", "w", None),  # double-v misread
    ("li", "h", None),  # in some fonts

    # Specific errors found in Zimmern (Victorian PDF)
    ("tlie", "the", None),
    ("liave", "have", None),
    ("wliich", "which", None),
    ("tliis", "this", None),
    ("tliat", "that", None),
    ("wlien", "when", None),
    ("tlien", "then", None),
    ("otlier", "other", None),
    ("tliere", "there", None),
    ("tliey", "they", None),
    ("tlieir", "their", None),
    ("tliose", "those", None),
    ("tliough", "though", None),
    ("tlirough", "through", None),
    ("witli", "with", None),
    ("notliing", "nothing", None),
    ("sometliing", "something", None),
    ("everytliing", "everything", None),
    ("anytliing", "anything", None),

    # Common letter confusions
    ("cliange", "change", None),
    ("cliaracter", "character", None),
    ("pliilosophy", "philosophy", None),
    ("pliilosopher", "philosopher", None),

    # Hyphenation artifacts (line breaks in PDFs)
    ("philoso- pher", "philosopher", None),
    ("philoso-\npher", "philosopher", None),

    # Extra spaces from column layouts
    ("  ", " ", None),  # Double spaces to single
]

# Regex-based fixes for patterns
OCR_REGEX_FIXES = [
    # Fix "li" -> "h" only in specific contexts (careful - "li" is valid in many words)
    # (r'\bwli', 'wh'),  # Too aggressive, skip

    # Fix split words from line breaks
    (r'(\w+)-\s*\n\s*(\w+)', r'\1\2'),  # word-\nword -> wordword

    # Normalize multiple spaces
    (r'  +', ' '),

    # Fix common PDF artifacts
    (r'\s*-\s*\n\s*', ''),  # Hyphenated line breaks
]


def clean_ocr_errors(text: str, aggressive: bool = False) -> str:
    """
    Clean common OCR errors from scanned text.

    Args:
        text: Raw text from PDF extraction
        aggressive: If True, apply more fixes that might have false positives

    Returns:
        Cleaned text
    """
    # Apply direct substitutions
    for wrong, correct, _ in OCR_FIXES:
        if wrong in text:
            text = text.replace(wrong, correct)

    # Apply regex fixes
    for pattern, replacement in OCR_REGEX_FIXES:
        text = re.sub(pattern, replacement, text)

    return text


def clean_corpus_file(json_path: str, output_path: str = None) -> dict:
    """
    Clean OCR errors in a corpus JSON file.

    Args:
        json_path: Path to corpus JSON file
        output_path: Where to save cleaned version (default: overwrite)

    Returns:
        Cleaned data dict
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    changes = []
    for aph in data['aphorisms']:
        original = aph['text']
        cleaned = clean_ocr_errors(original)

        if cleaned != original:
            changes.append({
                'aphorism': aph['number'],
                'original_len': len(original),
                'cleaned_len': len(cleaned),
                'diff': len(original) - len(cleaned)
            })
            aph['text'] = cleaned

    if output_path is None:
        output_path = json_path

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    return {
        'file': json_path,
        'total_aphorisms': len(data['aphorisms']),
        'aphorisms_changed': len(changes),
        'changes': changes
    }


def clean_all_corpus(corpus_dir: str = 'corpus/aligned') -> dict:
    """Clean all corpus files and report changes."""
    results = {}

    for path in Path(corpus_dir).glob('*.json'):
        print(f"Cleaning {path.name}...")
        result = clean_corpus_file(str(path))
        results[path.name] = result
        print(f"  → {result['aphorisms_changed']} aphorisms modified")

    return results


def verify_french_quote(corpus_dir: str = 'corpus/aligned'):
    """Verify the French quote in §35 is now consistent."""
    print("\n" + "=" * 60)
    print("VERIFYING §35 FRENCH QUOTE AFTER CLEANING")
    print("=" * 60)

    target_phrase = "il ne cherche le vrai que pour faire le bien"

    for path in sorted(Path(corpus_dir).glob('*.json')):
        with open(path) as f:
            data = json.load(f)

        for aph in data['aphorisms']:
            if aph['number'] == 35:
                text = aph['text'].lower()
                if target_phrase in text:
                    print(f"✓ {data['name']}: French quote found")
                else:
                    # Check for partial match
                    if "cherche" in text and "vrai" in text:
                        print(f"⚠ {data['name']}: Partial match (may have other OCR issues)")
                    else:
                        print(f"✗ {data['name']}: French quote NOT FOUND")
                break


if __name__ == '__main__':
    print("Cleaning OCR errors in corpus...\n")
    results = clean_all_corpus()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    total_changed = sum(r['aphorisms_changed'] for r in results.values())
    print(f"\nTotal files processed: {len(results)}")
    print(f"Total aphorisms modified: {total_changed}")

    for filename, result in results.items():
        if result['aphorisms_changed'] > 0:
            print(f"\n{filename}:")
            for change in result['changes'][:5]:
                print(f"  §{change['aphorism']}: {change['diff']:+d} chars")
            if len(result['changes']) > 5:
                print(f"  ... and {len(result['changes']) - 5} more")

    # Verify the fix worked
    verify_french_quote()
