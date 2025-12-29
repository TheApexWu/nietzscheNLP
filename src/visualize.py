"""
UMAP visualization of Nietzsche translation embeddings.
Shows how translators cluster in semantic space.
"""

import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
import umap
import matplotlib.pyplot as plt
from normalize import normalize_text


def load_corpus():
    """Load all translations."""
    corpus = {}
    for path in Path('corpus/aligned').glob('*.json'):
        with open(path) as f:
            data = json.load(f)
            corpus[data['name']] = data
    return corpus


def get_aligned_embeddings(corpus, model, normalize_german=True):
    """Get embeddings for all translators, aligned by aphorism number."""
    # Find common aphorisms
    all_nums = [set(a['number'] for a in t['aphorisms']) for t in corpus.values()]
    common = sorted(set.intersection(*all_nums))

    embeddings = {}
    aphorism_nums = common

    for name, data in corpus.items():
        texts = []
        for num in common:
            for aph in data['aphorisms']:
                if aph['number'] == num:
                    text = aph['text']
                    if normalize_german and name == 'Gutenberg':
                        text = normalize_text(text)
                    texts.append(text)
                    break

        embeddings[name] = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)

    return embeddings, aphorism_nums


def create_translator_umap(embeddings, output_path='outputs/visualizations/translator_umap.png'):
    """Create UMAP plot colored by translator."""

    # Combine all embeddings
    all_emb = []
    labels = []
    for name, emb in embeddings.items():
        all_emb.append(emb)
        labels.extend([name] * len(emb))

    all_emb = np.vstack(all_emb)

    print(f"Running UMAP on {len(all_emb)} embeddings...")
    reducer = umap.UMAP(n_neighbors=15, min_dist=0.1, metric='cosine', random_state=42)
    reduced = reducer.fit_transform(all_emb)

    # Plot
    fig, ax = plt.subplots(figsize=(12, 10))

    # Color map
    colors = {
        'Gutenberg': '#2E7D32',      # German - green
        'RJ Hollingdale': '#1976D2', # Blue
        'Walter Kaufman': '#7B1FA2', # Purple
        'Judith Norman': '#E64A19',  # Orange
        'Marion Faber': '#00796B',   # Teal
        'Helen Zimmern': '#C2185B',  # Pink
    }

    for name in embeddings.keys():
        mask = [l == name for l in labels]
        pts = reduced[mask]
        ax.scatter(pts[:, 0], pts[:, 1],
                   c=colors.get(name, '#666666'),
                   label=name, alpha=0.6, s=30)

    ax.legend(loc='upper left', fontsize=10)
    ax.set_title('Nietzsche Translations in Embedding Space (UMAP)', fontsize=14)
    ax.set_xlabel('UMAP 1')
    ax.set_ylabel('UMAP 2')

    # Clean up
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved to {output_path}")

    return reduced, labels


def create_high_variance_plot(embeddings, aphorism_nums,
                              output_path='outputs/visualizations/high_variance.png'):
    """Plot aphorisms by translator variance (divergence)."""

    # Compute per-aphorism variance across translators
    n_aphorisms = len(aphorism_nums)
    variances = []

    german = embeddings['Gutenberg']
    translators = [n for n in embeddings.keys() if n != 'Gutenberg']

    for i in range(n_aphorisms):
        # Get similarities from German to each translator for this aphorism
        sims = []
        for name in translators:
            sim = np.dot(german[i], embeddings[name][i])
            sims.append(sim)

        # High variance = translators disagree about this aphorism
        variances.append(np.std(sims))

    # Sort by variance
    sorted_idx = np.argsort(variances)[::-1]

    fig, ax = plt.subplots(figsize=(14, 6))

    # Plot top 30 highest variance aphorisms
    top_n = 30
    top_indices = sorted_idx[:top_n]
    top_nums = [aphorism_nums[i] for i in top_indices]
    top_vars = [variances[i] for i in top_indices]

    bars = ax.bar(range(top_n), top_vars, color='#E64A19', alpha=0.8)
    ax.set_xticks(range(top_n))
    ax.set_xticklabels([f'§{n}' for n in top_nums], rotation=45, ha='right', fontsize=8)
    ax.set_ylabel('Translator Variance (σ)')
    ax.set_title('Aphorisms with Highest Translator Divergence', fontsize=14)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved to {output_path}")

    return list(zip(top_nums, top_vars))


def create_heatmap(embeddings, output_path='outputs/visualizations/similarity_heatmap.png'):
    """Create translator similarity heatmap."""

    names = list(embeddings.keys())
    n = len(names)

    # Compute mean pairwise similarity
    sim_matrix = np.zeros((n, n))
    for i, n1 in enumerate(names):
        for j, n2 in enumerate(names):
            sims = [np.dot(embeddings[n1][k], embeddings[n2][k])
                    for k in range(len(embeddings[n1]))]
            sim_matrix[i, j] = np.mean(sims)

    fig, ax = plt.subplots(figsize=(10, 8))

    im = ax.imshow(sim_matrix, cmap='RdYlGn', vmin=0.7, vmax=1.0)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))

    # Shorten names for readability
    short_names = [n.split()[0] if n != 'RJ Hollingdale' else 'Hollingdale' for n in names]
    ax.set_xticklabels(short_names, rotation=45, ha='right')
    ax.set_yticklabels(short_names)

    # Add values
    for i in range(n):
        for j in range(n):
            val = sim_matrix[i, j]
            color = 'white' if val < 0.85 else 'black'
            ax.text(j, i, f'{val:.2f}', ha='center', va='center', color=color, fontsize=9)

    ax.set_title('Translator Similarity Matrix (Mean Cosine)', fontsize=14)
    plt.colorbar(im, ax=ax, shrink=0.8)

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f"Saved to {output_path}")


if __name__ == '__main__':
    print("Loading corpus...")
    corpus = load_corpus()

    print("Loading model...")
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    print("Generating embeddings...")
    embeddings, aphorism_nums = get_aligned_embeddings(corpus, model)

    print(f"\nGenerating visualizations for {len(aphorism_nums)} aligned aphorisms...")

    # 1. UMAP scatter plot
    create_translator_umap(embeddings)

    # 2. High variance aphorisms
    top_variance = create_high_variance_plot(embeddings, aphorism_nums)
    print("\nTop 10 highest-divergence aphorisms:")
    for num, var in top_variance[:10]:
        print(f"  §{num}: σ={var:.4f}")

    # 3. Similarity heatmap
    create_heatmap(embeddings)

    print("\nDone!")
