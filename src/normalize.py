"""
Archaic German orthography normalization for 19th-century texts.
Converts Nietzsche-era spellings to modern German for better embedding alignment.
"""

import re


# Common 19th-century → modern German substitutions
# Sourced from historical German linguistics literature
ORTHOGRAPHY_MAP = {
    # ie → i (older convention for long i)
    'giebt': 'gibt',
    'gieb': 'gib',
    'blieb': 'blieb',  # exception: stays the same

    # th → t (Greek-derived spelling abandoned)
    'Theil': 'Teil',
    'theil': 'teil',
    'theilen': 'teilen',
    'Thier': 'Tier',
    'thier': 'tier',
    'Thür': 'Tür',
    'thür': 'tür',
    'Thun': 'Tun',
    'thun': 'tun',
    'That': 'Tat',
    'that': 'tat',
    'gethan': 'getan',
    'Thatbestand': 'Tatbestand',
    'Thatsache': 'Tatsache',
    'thatsächlich': 'tatsächlich',
    'Werth': 'Wert',
    'werth': 'wert',
    'werthvoll': 'wertvoll',
    'Unwerth': 'Unwert',
    'Muth': 'Mut',
    'muth': 'mut',
    'muthig': 'mutig',
    'Demuth': 'Demut',
    'Wehmuth': 'Wehmut',
    'Armuth': 'Armut',
    'Noth': 'Not',
    'noth': 'not',
    'nöthig': 'nötig',
    'Nothwendigkeit': 'Notwendigkeit',
    'nothwendig': 'notwendig',
    'Rath': 'Rat',
    'rath': 'rat',
    'rathen': 'raten',
    'Räthsel': 'Rätsel',
    'räthselhaft': 'rätselhaft',

    # ey → ei
    'seyn': 'sein',
    'sey': 'sei',
    'Seyn': 'Sein',

    # c → k or z (Latin spelling abandoned)
    'Cultur': 'Kultur',
    'cultur': 'kultur',
    'Accent': 'Akzent',
    'Concert': 'Konzert',
    'Medicin': 'Medizin',

    # ph → f (Greek spelling simplified)
    'Phantasie': 'Fantasie',
    'phantastisch': 'fantastisch',
    'Photographie': 'Fotografie',

    # ß variations (pre-1996 but still relevant)
    'daß': 'dass',
    'muß': 'muss',
    'Fluß': 'Fluss',
    'Schluß': 'Schluss',
    'Genuß': 'Genuss',
    'Bewußtsein': 'Bewusstsein',
    'bewußt': 'bewusst',
    'unbewußt': 'unbewusst',
    'gewiß': 'gewiss',
    'Gewißheit': 'Gewissheit',

    # Double consonant variations
    'Litteratur': 'Literatur',
    'litterarisch': 'literarisch',

    # Capitalization of nouns (already standard, but some edge cases)
    'etwas anderes': 'etwas Anderes',

    # Specific Nietzsche vocabulary
    'Jenseits': 'Jenseits',  # stays same
    'jenseitig': 'jenseitig',
    'Diesseits': 'Diesseits',
    'diesseitig': 'diesseitig',
}

# Regex patterns for systematic transformations
PATTERNS = [
    # th followed by vowel → t (but not in words like "Athlet")
    (r'\b([Tt])h([aeiouäöü])', r'\1\2'),

    # Final -iren → -ieren (verb infinitives)
    (r'(\w+)iren\b', r'\1ieren'),

    # -irung → -ierung
    (r'(\w+)irung\b', r'\1ierung'),

    # -irt → -iert
    (r'(\w+)irt\b', r'\1iert'),
]


def normalize_word(word: str) -> str:
    """Normalize a single word using the lookup table."""
    return ORTHOGRAPHY_MAP.get(word, word)


def normalize_text(text: str) -> str:
    """
    Normalize archaic German orthography to modern spelling.
    Preserves whitespace and punctuation.
    """
    # First pass: direct word substitutions
    words = re.findall(r'\b\w+\b|\W+', text)
    normalized = [normalize_word(w) if w.isalpha() else w for w in words]
    result = ''.join(normalized)

    # Second pass: regex pattern substitutions
    for pattern, replacement in PATTERNS:
        result = re.sub(pattern, replacement, result)

    return result


def analyze_normalization(text: str) -> dict:
    """
    Analyze what would be normalized in a text.
    Returns statistics and examples.
    """
    changes = []

    words = re.findall(r'\b\w+\b', text)
    for word in words:
        normalized = normalize_word(word)
        if normalized != word:
            changes.append((word, normalized))

    # Also check regex patterns
    for pattern, replacement in PATTERNS:
        matches = re.findall(pattern, text)
        if matches:
            for match in matches:
                if isinstance(match, tuple):
                    original = ''.join(match)
                else:
                    original = match
                # Reconstruct the normalized form
                normalized = re.sub(pattern, replacement, original)
                if normalized != original:
                    changes.append((original, normalized))

    unique_changes = list(set(changes))

    return {
        'total_changes': len(changes),
        'unique_changes': len(unique_changes),
        'examples': unique_changes[:20],
        'change_rate': len(changes) / max(len(words), 1)
    }


if __name__ == '__main__':
    # Test with sample Nietzsche text
    sample = """
    Der Wille zur Wahrheit, der uns noch zu manchem Wagnisse verführen wird,
    jene berühmte Wahrhaftigkeit, von der alle Philosophen bisher mit Ehrerbietung
    geredet haben: was für Fragen hat uns dieser Wille zur Wahrheit schon vorgelegt!
    Welche wunderlichen schlimmen fragwürdigen Fragen! Das ist bereits eine lange
    Geschichte, — und doch scheint es, daß sie kaum eben angefangen hat?

    Gesetzt, wir wollen Wahrheit: warum nicht lieber Unwahrheit? Und Ungewißheit?
    Selbst Unwissenheit? — Das Problem vom Werthe der Wahrheit trat vor uns hin.
    """

    print("Original:")
    print(sample[:200])
    print("\nNormalized:")
    print(normalize_text(sample)[:200])
    print("\nAnalysis:")
    analysis = analyze_normalization(sample)
    print(f"  Changes: {analysis['total_changes']}")
    print(f"  Unique: {analysis['unique_changes']}")
    print(f"  Examples: {analysis['examples']}")
