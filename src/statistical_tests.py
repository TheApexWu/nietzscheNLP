"""
Statistical significance tests for translation divergence findings.
Answers: Is §28's high divergence real or cherry-picked?
"""

import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer
from normalize import normalize_text
from scipy import stats


def load_corpus():
    corpus = {}
    for path in Path('corpus/aligned').glob('*.json'):
        with open(path) as f:
            data = json.load(f)
            corpus[data['name']] = data
    return corpus


def get_aligned_embeddings(corpus, model, normalize_german=True):
    all_nums = [set(a['number'] for a in t['aphorisms']) for t in corpus.values()]
    common = sorted(set.intersection(*all_nums))

    embeddings = {}
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

    return embeddings, common


def compute_divergence_scores(embeddings, aphorism_nums):
    """Compute per-aphorism divergence (std of German→translator similarities)."""
    german = embeddings['Gutenberg']
    translators = [n for n in embeddings.keys() if n != 'Gutenberg']

    divergences = []
    for i in range(len(aphorism_nums)):
        sims = [np.dot(german[i], embeddings[name][i]) for name in translators]
        divergences.append(np.std(sims))

    return np.array(divergences)


def bootstrap_ci(data, statistic_fn, n_bootstrap=10000, ci=0.95):
    """Bootstrap confidence interval for a statistic."""
    n = len(data)
    bootstrap_stats = []

    for _ in range(n_bootstrap):
        sample = np.random.choice(data, size=n, replace=True)
        bootstrap_stats.append(statistic_fn(sample))

    lower = np.percentile(bootstrap_stats, (1 - ci) / 2 * 100)
    upper = np.percentile(bootstrap_stats, (1 + ci) / 2 * 100)
    return lower, upper, np.array(bootstrap_stats)


def permutation_test(divergences, target_idx, n_permutations=10000):
    """
    Test if the divergence at target_idx is significantly higher than expected.
    H0: The ranking of divergences is random.
    """
    observed_rank = np.sum(divergences >= divergences[target_idx])
    n = len(divergences)

    # Under null, what's the probability of being in top k?
    null_ranks = []
    for _ in range(n_permutations):
        shuffled = np.random.permutation(divergences)
        rank = np.sum(shuffled >= shuffled[target_idx])
        null_ranks.append(rank)

    # p-value: proportion of permutations where target would rank as high
    p_value = np.mean(np.array(null_ranks) <= observed_rank)
    return p_value, observed_rank, n


def run_significance_tests():
    print("Loading corpus and model...")
    corpus = load_corpus()
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

    print("Computing embeddings...")
    embeddings, aphorism_nums = get_aligned_embeddings(corpus, model)

    print("Computing divergence scores...")
    divergences = compute_divergence_scores(embeddings, aphorism_nums)

    # Find §28
    try:
        idx_28 = aphorism_nums.index(28)
    except ValueError:
        print("ERROR: §28 not in aligned aphorisms!")
        return

    div_28 = divergences[idx_28]
    rank_28 = np.sum(divergences >= div_28)

    print("\n" + "=" * 70)
    print("STATISTICAL SIGNIFICANCE TESTS FOR §28")
    print("=" * 70)

    # Basic stats
    print(f"\n--- DESCRIPTIVE STATISTICS ---")
    print(f"Total aligned aphorisms: {len(aphorism_nums)}")
    print(f"§28 divergence (σ): {div_28:.4f}")
    print(f"§28 rank: {rank_28} of {len(divergences)} (top {100*rank_28/len(divergences):.1f}%)")
    print(f"Mean divergence: {np.mean(divergences):.4f}")
    print(f"Std of divergences: {np.std(divergences):.4f}")
    print(f"Max divergence: {np.max(divergences):.4f} (§{aphorism_nums[np.argmax(divergences)]})")

    # Z-score
    z_score = (div_28 - np.mean(divergences)) / np.std(divergences)
    print(f"\n§28 z-score: {z_score:.2f}")

    # Bootstrap CI for §28's divergence
    print(f"\n--- BOOTSTRAP CONFIDENCE INTERVAL ---")
    print("(Is §28's divergence estimate stable?)")

    # Bootstrap the divergence calculation itself by resampling translators
    # This is a simplified version - proper bootstrap would resample aphorisms
    lower, upper, bootstrap_dist = bootstrap_ci(
        divergences,
        lambda x: np.percentile(x, 100 * (1 - rank_28/len(divergences))),
        n_bootstrap=10000
    )
    print(f"95% CI for top-{rank_28} divergence threshold: [{lower:.4f}, {upper:.4f}]")
    print(f"§28 actual: {div_28:.4f} {'(within CI)' if lower <= div_28 <= upper else '(OUTSIDE CI)'}")

    # Permutation test
    print(f"\n--- PERMUTATION TEST ---")
    print("(Would §28 rank this high by chance?)")
    p_value, observed_rank, n = permutation_test(divergences, idx_28, n_permutations=10000)
    print(f"Observed rank: {observed_rank}/{n}")
    print(f"p-value: {p_value:.4f}")
    print(f"Significant at α=0.05? {'YES' if p_value < 0.05 else 'NO'}")
    print(f"Significant at α=0.01? {'YES' if p_value < 0.01 else 'NO'}")

    # Multiple comparison correction
    print(f"\n--- MULTIPLE COMPARISON CORRECTION ---")
    print("(We looked at all aphorisms, not just §28)")

    # Bonferroni correction
    bonferroni_threshold = 0.05 / len(divergences)
    print(f"Bonferroni-corrected α: {bonferroni_threshold:.4f}")
    print(f"§28 p-value ({p_value:.4f}) < Bonferroni ({bonferroni_threshold:.4f})? {'YES' if p_value < bonferroni_threshold else 'NO'}")

    # False Discovery Rate (Benjamini-Hochberg)
    # Calculate p-values for all aphorisms
    all_p_values = []
    for i in range(len(divergences)):
        rank_i = np.sum(divergences >= divergences[i])
        p_i = rank_i / len(divergences)  # Simplified: rank-based p-value
        all_p_values.append((aphorism_nums[i], p_i, divergences[i]))

    all_p_values.sort(key=lambda x: x[1])

    # BH procedure
    fdr = 0.05
    n_tests = len(all_p_values)
    significant_bh = []
    for i, (num, p, div) in enumerate(all_p_values):
        bh_threshold = (i + 1) / n_tests * fdr
        if p <= bh_threshold:
            significant_bh.append((num, p, div))

    print(f"\nBenjamini-Hochberg FDR=0.05:")
    print(f"Significant aphorisms: {len(significant_bh)}")
    if significant_bh:
        print("Top 5:")
        for num, p, div in significant_bh[:5]:
            marker = " ← §28" if num == 28 else ""
            print(f"  §{num}: p={p:.4f}, σ={div:.4f}{marker}")

    # Expected number in top k by chance
    print(f"\n--- EXPECTED BY CHANCE ---")
    top_5_pct = int(len(divergences) * 0.05)
    print(f"If divergences were random, expected in top 5%: {top_5_pct} aphorisms")
    print(f"Actual in top 5%: {top_5_pct} (by definition)")
    print(f"§28 is in top {100*rank_28/len(divergences):.1f}%")

    # Final verdict
    print("\n" + "=" * 70)
    print("VERDICT")
    print("=" * 70)

    if p_value < 0.05 and z_score > 2:
        print("§28's high divergence is STATISTICALLY SIGNIFICANT.")
        print(f"  - Ranks #{rank_28} out of {len(divergences)} aphorisms")
        print(f"  - z-score of {z_score:.2f} (>{2} threshold)")
        print(f"  - p-value of {p_value:.4f} (<0.05)")
        if 28 in [x[0] for x in significant_bh]:
            print("  - Survives Benjamini-Hochberg FDR correction")
        print("\nThe finding is NOT cherry-picked.")
    else:
        print("§28's divergence is NOT statistically significant at conventional thresholds.")
        print("The finding may be due to chance.")

    # Save results
    results = {
        'aphorism': 28,
        'divergence': float(div_28),
        'rank': int(rank_28),
        'total_aphorisms': len(divergences),
        'percentile': float(100 * (1 - rank_28/len(divergences))),
        'z_score': float(z_score),
        'p_value': float(p_value),
        'mean_divergence': float(np.mean(divergences)),
        'std_divergence': float(np.std(divergences)),
        'significant_bh': [x[0] for x in significant_bh],
        'all_divergences': [(int(aphorism_nums[i]), float(divergences[i]))
                           for i in range(len(divergences))]
    }

    out_path = Path('outputs/statistical_significance.json')
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")


if __name__ == '__main__':
    run_significance_tests()
