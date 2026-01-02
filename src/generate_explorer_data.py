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

# OCR fixes: common li->h, ie->e substitutions from PDF extraction
OCR_FIXES = [
    # li -> h errors (word-bounded to avoid breaking German)
    (r'\bhfe\b', 'life'), (r'\bhves\b', 'lives'), (r'\bhved\b', 'lived'),
    (r'\bhve\b', 'live'), (r'\bhving\b', 'living'), (r'\bhvely\b', 'lively'),
    (r'\bhver\b', 'liver'), (r'\bhveher\b', 'livelier'),
    (r'\bhnes\b', 'lines'), (r'\bhne\b', 'line'),
    (r'\bhght\b', 'light'), (r'\bhke\b', 'like'), (r'\bhkely\b', 'likely'),
    (r'\bhst\b', 'list'), (r'\bhsten\b', 'listen'),
    (r'\bhterature\b', 'literature'), (r'\bhterary\b', 'literary'),
    (r'\bhberty\b', 'liberty'), (r'\bhberal\b', 'liberal'),
    (r'\bhmit', 'limit'), (r'\bhm\b', 'lim'),
    (r'\binchned\b', 'inclined'), (r'\bunchned\b', 'unlined'),
    (r'\bouthne', 'outline'), (r'\bdechne', 'decline'),
    # Compound words with life
    (r'afterhfe', 'afterlife'), (r'hfepreserving', 'life-preserving'),
    (r'hfe-', 'life-'),
    # ie -> e errors
    (r'\bbeheve', 'believe'), (r'\bbehef', 'belief'),
    (r'\brehgion', 'religion'), (r'\brehgious', 'religious'),
    (r'\bprohferat', 'proliferat'),
    # -ility/-ality/-ness errors
    (r'possibiht', 'possibilit'), (r'credibihty', 'credibility'),
    (r'sensibihty', 'sensibility'), (r'visibihty', 'visibility'),
    (r'moraht', 'moralit'), (r'reahty', 'reality'), (r'reahst', 'realist'),
    (r'personaht', 'personalit'), (r'nationaht', 'nationalit'),
    (r'Nihihsm', 'Nihilism'), (r'nihihsm', 'nihilism'),
    (r'silhness', 'silliness'), (r'foohshness', 'foolishness'),
    (r'wilhng', 'willing'), (r'unwilhng', 'unwilling'),
    # Other common errors
    (r'\bfeehngs\b', 'feelings'), (r'\bfeehng\b', 'feeling'),
    (r'\bfamihar\b', 'familiar'), (r'\bsimhar\b', 'similar'),
    (r'\bparticularh', 'particularli'), (r'\bespecialh', 'especialli'),
    (r'cahty', 'cality'), (r'ahty', 'ality'), (r'ihty', 'ility'),
]

HEADER_MARKERS = ['BEYOND GOOD AND EVIL', 'CHAPTER', 'PART ONE', 'PART TWO',
                  'PART THREE', 'PART FOUR', 'Part Three', 'Part Four']


def load_corpus(name: str) -> dict:
    """Load corpus JSON and return {aphorism_number: text}"""
    with open(CORPUS_DIR / f'{name}.json') as f:
        data = json.load(f)
    return {a['number']: a['text'] for a in data['aphorisms']}


def clean_ocr(text: str) -> str:
    """Apply OCR artifact fixes and strip junk"""
    if not text:
        return text

    # Apply word-level OCR fixes
    for pattern, replacement in OCR_FIXES:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)

    # Strip trailing page numbers and chapter headers
    # e.g., "ERLUDES 83", "D EVIL 135", "IRTUBS 151"
    text = re.sub(r'\s*\d{2,3}\s*$', '', text)
    text = re.sub(r'\s*[A-Z]{2,}(?:\s+[A-Z]{2,})*\s*\d*\s*$', '', text)

    # Strip stray footnotes at end (e.g., "* Apollo.")
    text = re.sub(r'\s*\*\s*[A-Z][a-z]+\.?\s*$', '', text)

    # Strip garbage OCR patterns (random chars/symbols) and preceding partial word
    text = re.sub(r'\b\w{1,4}[)\]}\d]\s*[a-z]\s+[a-z]\s+[A-Z]\s*', '', text)
    text = re.sub(r'[)\]}\d]\s*[a-z]\s+[a-z]\s+[A-Z]\s*', '', text)

    # Strip footnote markers mid-text
    text = re.sub(r'\s*\d+\s*$', '', text)  # trailing numbers

    # Clean up multiple newlines
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text.strip()


def is_valid(text: str, is_german: bool = False) -> bool:
    """Check if text is valid (not garbage, not wrong aphorism, properly ended)"""
    if not text or len(text) < 50:
        return False
    if text.count('\\') > 5 or text.count('^') > 3:
        return False
    if any(h in text[:200] for h in HEADER_MARKERS):
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
        embs = [e[i] for e in embeddings]
        sims = []
        for j in range(6):
            for k in range(j + 1, 6):
                sim = np.dot(embs[j], embs[k]) / (np.linalg.norm(embs[j]) * np.linalg.norm(embs[k]))
                sims.append(float(sim))
        divergences.append((i + 1, float(np.std(sims))))

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
