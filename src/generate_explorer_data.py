#!/usr/bin/env python3
"""
Generate explorer_data.json for the Nietzsche translation site.
Selects top divergent aphorisms with quality filtering and OCR cleanup.
"""

import json
import re
import numpy as np
from pathlib import Path

# Paths
CORPUS_DIR = Path('corpus/aligned')
EMBEDDINGS_DIR = Path('outputs/embeddings')
OUTPUT_PATH = Path('site/public/explorer_data.json')

# OCR fixes: common li->h substitution from PDF extraction
# Pattern: 'li' scanned as 'h' (vertical strokes merge)
OCR_FIXES = [
    # -alist/-alism words
    (r'ideahst', 'idealist'), (r'ideahsm', 'idealism'), (r'ideahstic', 'idealistic'),
    (r'sensuahst', 'sensualist'), (r'sensuahsm', 'sensualism'),
    (r'reahst', 'realist'), (r'reahsm', 'realism'), (r'reahstic', 'realistic'),
    (r'nationahst', 'nationalist'), (r'nationahsm', 'nationalism'),
    (r'materiahst', 'materialist'), (r'materiahsm', 'materialism'),
    (r'spirituahst', 'spiritualist'), (r'spirituahsm', 'spiritualism'),
    (r'naturahst', 'naturalist'), (r'naturahsm', 'naturalism'),
    (r'nihihst', 'nihilist'), (r'nihihsm', 'nihilism'),
    (r'morahst', 'moralist'), (r'morahsm', 'moralism'),

    # -ality/-ility words
    (r'reahty', 'reality'), (r'personahty', 'personality'), (r'nationahty', 'nationality'),
    (r'morahty', 'morality'), (r'spirituahty', 'spirituality'), (r'originahty', 'originality'),
    (r'possibiht', 'possibilit'), (r'credibiht', 'credibilit'), (r'sensibiht', 'sensibilit'),
    (r'visibiht', 'visibilit'), (r'responsibiht', 'responsibilit'),

    # -tion/-sion with li
    (r'civihza', 'civiliza'), (r'reahza', 'realiza'),

    # -ly words
    (r'particularh\b', 'particularly'), (r'especialh\b', 'especially'),
    (r'essentiahh', 'essentially'), (r'originahh', 'originally'),
    (r'fundamentahh', 'fundamentally'), (r'actuahh', 'actually'),

    # -ling/-line words
    (r'\bouthne', 'outline'), (r'\bdechne', 'decline'), (r'\binchne', 'incline'),
    (r'\bmaschne', 'masculine'), (r'\bfemhne', 'feminine'),

    # -live/-life words
    (r'\bhfe\b', 'life'), (r'\bhves\b', 'lives'), (r'\bhved\b', 'lived'),
    (r'\bhve\b', 'live'), (r'\bhving\b', 'living'), (r'\bhvely\b', 'lively'),
    (r'afterhfe', 'afterlife'), (r'hfe-', 'life-'),

    # -like words
    (r'\bhke\b', 'like'), (r'\bhkely\b', 'likely'), (r'\bhkewise\b', 'likewise'),
    (r'warhke', 'warlike'), (r'godh ke', 'godlike'), (r'chhdh ke', 'childlike'),

    # -light words
    (r'\bhght\b', 'light'), (r'dayhght', 'daylight'), (r'moonhght', 'moonlight'),
    (r'sunhght', 'sunlight'), (r'twihght', 'twilight'),

    # -line/-lines words
    (r'\bhne\b', 'line'), (r'\bhnes\b', 'lines'), (r'outhnes', 'outlines'),

    # -list/-listen words
    (r'\bhst\b', 'list'), (r'\bhsten', 'listen'), (r'\bhstening', 'listening'),

    # -lit/-lity words
    (r'\bhterature', 'literature'), (r'\bhterary', 'literary'),
    (r'\bhberty', 'liberty'), (r'\bhberal', 'liberal'),
    (r'\bhmit', 'limit'), (r'\bhmited', 'limited'),
    (r'mihtant', 'militant'), (r'mihtary', 'military'),

    # -lief/-lieve words
    (r'\bbeheve', 'believe'), (r'\bbehef', 'belief'), (r'\bbeheved', 'believed'),
    (r'\breheve', 'relieve'), (r'\brehef', 'relief'),

    # -ligion/-ligious words
    (r'\brehgion', 'religion'), (r'\brehgious', 'religious'),
    (r'intelhgen', 'intelligen'), (r'intehgen', 'intelligen'),

    # -liness words
    (r'cleanhness', 'cleanliness'), (r'lonehness', 'loneliness'),
    (r'lovehness', 'loveliness'), (r'homehness', 'homeliness'),

    # -ling words
    (r'\bwilhng', 'willing'), (r'\bunwilhng', 'unwilling'),
    (r'\bfeehngs?\b', 'feelings'), (r'\bfeehng\b', 'feeling'),

    # -liar/-miliar words
    (r'\bfamihar', 'familiar'), (r'\bsimhar', 'similar'), (r'\bpeculhar', 'peculiar'),

    # -lic/-lick words
    (r'\bpubhc', 'public'), (r'\bcathohc', 'catholic'),

    # -ling suffix
    (r'darhng', 'darling'), (r'starhng', 'starling'),

    # Common standalone errors
    (r'\bphilosoply', 'philosophy'),
    (r'\bextemal\b', 'external'), (r'\bintemal\b', 'internal'),
    (r'\betemal\b', 'eternal'), (r'\bmatemal\b', 'maternal'),
    (r'\bfratema\b', 'fraterna'), (r'\bpatema\b', 'paterna'),
    (r'Marure', 'Mature'), (r'marure', 'mature'),
    (r'\bseff\b', 'self'), (r'\bseff-', 'self-'),
    (r'\bhimseh', 'himself'), (r'\bherseh', 'herself'), (r'\bitseh', 'itself'),
    (r'\bmyseh', 'myself'), (r'\bourseh', 'ourselves'), (r'\bthemseh', 'themselves'),
    (r'disciphne', 'discipline'), (r'disciphned', 'disciplined'),
    (r'\bpoht', 'polit'), (r'\bsphit', 'spirit'),
    (r'prohfer', 'prolifer'),
    (r'sihhness', 'silliness'), (r'foohshness', 'foolishness'),
    (r'utihty', 'utility'), (r'fertihty', 'fertility'), (r'hostihty', 'hostility'),
    (r'nobihty', 'nobility'), (r'possibiht', 'possibilit'),
    (r'quahty', 'quality'), (r'equahty', 'equality'),

    # rn -> m errors (common OCR)
    (r'\btom\b', 'torn'), (r'\bbom\b', 'born'), (r'\bwom\b', 'worn'),

    # Generic h -> li pattern (careful - only specific cases)
    (r'ahty\b', 'ality'), (r'ihty\b', 'ility'), (r'uhty\b', 'ulty'),
]

# Page headers/footers to strip (appear mid-text from PDF extraction)
PAGE_HEADERS = [
    r'ON THE [FP]RE[JU]UDICES OF PHILOSOPHERS\s*\d*',
    r'BEYOND GOOD AND EVIL\s*\d*',
    r'THE FREE SPIRIT\s*\d*',
    r'THE RELIGIOUS CHARACTER\s*\d*',
    r'PEOPLES AND FATHERLANDS\s*\d*',
    r'WHAT IS NOBLE\s*\d*',
    r'OUR VIRTUES\s*\d*',
    r'EPIGRAMS AND INTERLUDES\s*\d*',
    r'NATURAL HISTORY OF MORALS\s*\d*',
    r'\d{1,3}\s+BEYOND GOOD AND EVIL',
    r'PART\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE)',
    r'CHAPTER\s+\w+',
]

HEADER_MARKERS = ['BEYOND GOOD AND EVIL', 'CHAPTER', 'PART ONE', 'PART TWO',
                  'PART THREE', 'PART FOUR', 'Part Three', 'Part Four',
                  'Zarathustra', 'THE END']

# Aphorisms with corrupted/empty text in some translations (detected by LLM-as-Judge)
CORRUPTED_APHORISMS = {4, 24, 35, 59, 72, 113}


def load_corpus(name: str) -> dict:
    """Load corpus JSON and return {aphorism_number: text}"""
    with open(CORPUS_DIR / f'{name}.json') as f:
        data = json.load(f)
    return {a['number']: a['text'] for a in data['aphorisms']}


def clean_ocr(text: str) -> str:
    """Apply OCR artifact fixes and strip junk"""
    if not text:
        return text

    # Strip page headers/footers embedded in text
    for pattern in PAGE_HEADERS:
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)

    # Apply word-level OCR fixes
    for pattern, replacement in OCR_FIXES:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # Strip trailing page numbers and chapter headers
    text = re.sub(r'\s*\d{2,3}\s*$', '', text)
    text = re.sub(r'\s*[A-Z]{2,}(?:\s+[A-Z]{2,})*\s*\d*\s*$', '', text)

    # Strip stray footnotes at end (e.g., "* Apollo.")
    text = re.sub(r'\s*\*\s*[A-Z][a-z]+\.?\s*$', '', text)

    # Strip garbage characters (®, ©, etc.)
    text = re.sub(r'[®©™�]', '', text)
    text = re.sub(r'!\s*®', '', text)  # "!®" pattern

    # Strip footnote numbers mid-sentence (superscript artifacts)
    text = re.sub(r'(?<=[a-z])\d{1,2}(?=\s)', '', text)

    # Strip garbage OCR patterns
    text = re.sub(r'\b\w{1,4}[)\]}\d]\s*[a-z]\s+[a-z]\s+[A-Z]\s*', '', text)
    text = re.sub(r'[)\]}\d]\s*[a-z]\s+[a-z]\s+[A-Z]\s*', '', text)

    # Clean up multiple newlines and spaces
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)

    return text.strip()


def is_valid(text: str, is_german: bool = False) -> bool:
    """Check if text is valid (not garbage, not wrong aphorism, properly ended)"""
    if not text or len(text) < 50:
        return False
    if text.count('\\') > 5 or text.count('^') > 3:
        return False

    # Check for wrong content (other works mixed in)
    if any(h in text[:200] for h in HEADER_MARKERS):
        return False

    # Check for Zarathustra content mixed in
    if 'Zarathustra' in text and 'Feast' in text:
        return False

    # Skip ending check for German (different punctuation conventions)
    if is_german:
        return True

    # Check for proper ending (sentence-final punctuation)
    last_char = text.rstrip()[-1] if text.rstrip() else ''
    if last_char not in '.!?"\'—–-':
        return False

    # Check for garbage patterns (OCR failures)
    if re.search(r'[)\]}\d][a-z]{2,}', text):
        return False

    # Check for missing spaces (corrupted text)
    if re.search(r'[a-z]{4,}[A-Z][a-z]', text):
        return False

    # Check for obvious word corruption (uncommon consonant clusters)
    if re.search(r'[bcdfghjklmnpqrstvwxz]{4,}', text.lower()):
        return False
    if re.search(r'pitmy|tymy|tmy\b', text.lower()):
        return False

    return True


def compute_divergences(n_aphorisms: int) -> list:
    """Compute divergence (std of pairwise similarities) for each aphorism"""
    embeddings = [
        np.load(EMBEDDINGS_DIR / 'gutenberg.npy'),
        np.load(EMBEDDINGS_DIR / 'rj_hollingdale.npy'),
        np.load(EMBEDDINGS_DIR / 'walter_kaufman.npy'),
        np.load(EMBEDDINGS_DIR / 'marion_faber.npy'),
        np.load(EMBEDDINGS_DIR / 'judith_norman.npy'),
        np.load(EMBEDDINGS_DIR / 'helen_zimmern.npy'),
    ]

    divergences = []
    for i in range(n_aphorisms):
        aph_num = i + 1
        # Skip corrupted aphorisms (artificially inflate divergence due to empty text)
        if aph_num in CORRUPTED_APHORISMS:
            continue
        embs = [e[i] for e in embeddings]
        sims = []
        for j in range(6):
            for k in range(j + 1, 6):
                sim = np.dot(embs[j], embs[k]) / (np.linalg.norm(embs[j]) * np.linalg.norm(embs[k]))
                sims.append(float(sim))
        divergences.append((aph_num, float(np.std(sims))))

    return sorted(divergences, key=lambda x: -x[1])


def main():
    # Load corpora
    corpora = {
        'Gutenberg': load_corpus('gutenberg'),
        'RJ Hollingdale': load_corpus('rj_hollingdale'),
        'Walter Kaufman': load_corpus('walter_kaufman'),
        'Marion Faber': load_corpus('marion_faber'),
        'Judith Norman': load_corpus('judith_norman'),
        'Helen Zimmern': load_corpus('helen_zimmern'),
    }

    # Use embedding count (may differ from corpus count due to alignment)
    n_aphorisms = len(np.load(EMBEDDINGS_DIR / 'gutenberg.npy'))
    divergences = compute_divergences(n_aphorisms)

    # Select top 25 with at least 4/6 valid translations
    aphorisms = []
    for num, div in divergences:
        if len(aphorisms) >= 25:
            break

        translations = {}
        valid_count = 0

        for name, corpus in corpora.items():
            text = clean_ocr(corpus.get(num, ''))
            is_german = (name == 'Gutenberg')
            if is_valid(text, is_german=is_german):
                translations[name] = text.strip()
                valid_count += 1
            else:
                translations[name] = None

        if valid_count >= 4:
            aphorisms.append({
                'number': num,
                'divergence': round(div, 4),
                'translations': translations
            })
            print(f"✓ §{num}: {valid_count}/6 valid, σ={div:.3f}")

    # Sort by aphorism number
    aphorisms.sort(key=lambda x: x['number'])

    # Save
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w') as f:
        json.dump({'aphorisms': aphorisms, 'total': len(aphorisms)}, f, indent=2)

    print(f"\nSaved {len(aphorisms)} aphorisms to {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
