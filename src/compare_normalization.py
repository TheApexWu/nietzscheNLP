"""
Compare embeddings before/after archaic German normalization.
Measures the impact of orthography normalization on cross-lingual similarity.
"""

import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer

from normalize import normalize_text


def load_corpus():
    """Load all translations."""
    corpus = {}
    for path in Path('corpus/aligned').glob('*.json'):
        with open(path) as f:
            data = json.load(f)
            corpus[data['name']] = data
    return corpus


def get_aligned_texts(corpus, numbers):
    """Get aligned texts for given aphorism numbers."""
    aligned = {}
    for name, data in corpus.items():
        aligned[name] = {}
        for aph in data['aphorisms']:
            if aph['number'] in numbers:
                aligned[name][aph['number']] = aph['text']
    return aligned


def cosine_sim(a, b):
    """Cosine similarity for normalized vectors."""
    return np.dot(a, b)


def run_comparison():
    print("Loading corpus...")
    corpus = load_corpus()

    # Find common aphorisms
    all_nums = [set(a['number'] for a in t['aphorisms']) for t in corpus.values()]
    common = sorted(set.intersection(*all_nums))
    print(f"Common aphorisms: {len(common)}")

    # Get aligned texts
    aligned = get_aligned_texts(corpus, common)

    # Prepare German texts (original and normalized)
    german_original = [aligned['Gutenberg'][n] for n in common]
    german_normalized = [normalize_text(t) for t in german_original]

    # Pick one English translation for comparison (Hollingdale was closest)
    english = [aligned['RJ Hollingdale'][n] for n in common]

    # Load model (fast for quick comparison)
    print("Loading model...")
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    # Embed all three
    print("Embedding original German...")
    emb_original = model.encode(german_original, normalize_embeddings=True, show_progress_bar=True)

    print("Embedding normalized German...")
    emb_normalized = model.encode(german_normalized, normalize_embeddings=True, show_progress_bar=True)

    print("Embedding English (Hollingdale)...")
    emb_english = model.encode(english, normalize_embeddings=True, show_progress_bar=True)

    # Compute similarities
    sim_orig_en = [cosine_sim(emb_original[i], emb_english[i]) for i in range(len(common))]
    sim_norm_en = [cosine_sim(emb_normalized[i], emb_english[i]) for i in range(len(common))]
    sim_orig_norm = [cosine_sim(emb_original[i], emb_normalized[i]) for i in range(len(common))]

    # Results
    print("\n" + "=" * 60)
    print("NORMALIZATION IMPACT ANALYSIS")
    print("=" * 60)

    print(f"\nGerman (original) ↔ English:    {np.mean(sim_orig_en):.4f}")
    print(f"German (normalized) ↔ English:  {np.mean(sim_norm_en):.4f}")
    print(f"Improvement:                     {np.mean(sim_norm_en) - np.mean(sim_orig_en):+.4f}")

    print(f"\nOriginal ↔ Normalized German:   {np.mean(sim_orig_norm):.4f}")
    print("(1.0 = identical, lower = more changes)")

    # Find aphorisms with biggest improvement
    improvements = [(common[i], sim_norm_en[i] - sim_orig_en[i]) for i in range(len(common))]
    improvements.sort(key=lambda x: -x[1])

    print("\nTop 5 aphorisms with biggest improvement:")
    for num, imp in improvements[:5]:
        print(f"  §{num}: +{imp:.4f}")

    print("\nTop 5 aphorisms with negative impact (rare):")
    for num, imp in improvements[-5:]:
        print(f"  §{num}: {imp:+.4f}")

    # Save detailed results
    results = {
        'mean_original_english': float(np.mean(sim_orig_en)),
        'mean_normalized_english': float(np.mean(sim_norm_en)),
        'improvement': float(np.mean(sim_norm_en) - np.mean(sim_orig_en)),
        'per_aphorism': [
            {
                'number': common[i],
                'original_sim': float(sim_orig_en[i]),
                'normalized_sim': float(sim_norm_en[i]),
                'improvement': float(sim_norm_en[i] - sim_orig_en[i])
            }
            for i in range(len(common))
        ]
    }

    out_path = Path('outputs/normalization_impact.json')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nDetailed results saved to {out_path}")


if __name__ == '__main__':
    run_comparison()
