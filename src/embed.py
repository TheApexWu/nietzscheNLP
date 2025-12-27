"""
Embedding generation for Nietzsche translation analysis.
Uses multilingual-e5-large for cross-lingual comparison.
"""

import json
import numpy as np
from pathlib import Path
from sentence_transformers import SentenceTransformer


# E5 models need prefixes
def add_prefix(texts: list[str], prefix: str = "passage") -> list[str]:
    """E5 models expect 'query: ' or 'passage: ' prefixes."""
    return [f"{prefix}: {t}" for t in texts]


class Embedder:
    """Simple wrapper for sentence-transformers."""

    # Fast model for CPU, accurate model for GPU
    MODELS = {
        "fast": "paraphrase-multilingual-MiniLM-L12-v2",  # ~2 min total on CPU
        "accurate": "intfloat/multilingual-e5-large",      # ~4 hours on CPU, use with GPU
    }

    def __init__(self, model_name: str = None, mode: str = "fast"):
        if model_name is None:
            model_name = self.MODELS.get(mode, self.MODELS["fast"])
        print(f"Loading {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.uses_prefix = "e5" in model_name.lower()

    def embed(self, texts: list[str], is_query: bool = False) -> np.ndarray:
        """
        Embed a list of texts.
        For E5: use is_query=True for the source (German), False for translations.
        """
        if self.uses_prefix:
            prefix = "query" if is_query else "passage"
            texts = add_prefix(texts, prefix)

        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True
        )


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Cosine similarity between aligned vectors (already normalized)."""
    return np.sum(a * b, axis=1)


def load_aligned_corpus(corpus_dir: str = "corpus/aligned") -> dict:
    """Load all extracted translations."""
    corpus = {}
    for path in Path(corpus_dir).glob("*.json"):
        with open(path) as f:
            data = json.load(f)
            corpus[data["name"]] = data
    return corpus


def align_aphorisms(corpus: dict, numbers: list[int] = None) -> dict:
    """
    Align aphorisms across translations by number.
    Returns {number: {translator: text}}.
    """
    if numbers is None:
        # Find aphorisms present in ALL translations
        all_numbers = [
            {a["number"] for a in t["aphorisms"]}
            for t in corpus.values()
        ]
        numbers = sorted(set.intersection(*all_numbers))

    aligned = {}
    for num in numbers:
        aligned[num] = {}
        for name, data in corpus.items():
            for aph in data["aphorisms"]:
                if aph["number"] == num:
                    aligned[num][name] = aph["text"]
                    break

    return aligned


def compute_divergence(embeddings: dict, reference: str = None) -> dict:
    """
    Compute pairwise divergence between all translators.
    If reference given, compute divergence from that translator.
    Returns {(t1, t2): similarity_array} or {translator: divergence_array}.
    """
    names = list(embeddings.keys())

    if reference:
        ref_emb = embeddings[reference]
        return {
            name: 1.0 - cosine_similarity(ref_emb, emb)
            for name, emb in embeddings.items()
            if name != reference
        }

    # Pairwise comparison
    results = {}
    for i, n1 in enumerate(names):
        for n2 in names[i + 1:]:
            sim = cosine_similarity(embeddings[n1], embeddings[n2])
            results[(n1, n2)] = sim

    return results


if __name__ == "__main__":
    # Load corpus
    corpus = load_aligned_corpus()
    print(f"Loaded {len(corpus)} translations")

    # Align aphorisms (only those present in all)
    aligned = align_aphorisms(corpus)
    print(f"Aligned {len(aligned)} aphorisms across all translations")

    if len(aligned) < 10:
        print("Too few aligned aphorisms. Check extraction.")
        exit(1)

    # Initialize embedder
    embedder = Embedder()

    # Embed each translator's aphorisms
    aphorism_nums = sorted(aligned.keys())
    embeddings = {}

    for name in corpus.keys():
        texts = [aligned[n].get(name, "") for n in aphorism_nums]
        texts = [t if t else "[MISSING]" for t in texts]
        print(f"Embedding {name}...")
        embeddings[name] = embedder.embed(texts)

    # Compute pairwise similarities
    print("\n" + "=" * 50)
    print("TRANSLATOR SIMILARITY (mean cosine)")
    print("=" * 50)

    pairwise = compute_divergence(embeddings)
    for (t1, t2), sim in sorted(pairwise.items(), key=lambda x: -x[1].mean()):
        print(f"{t1:20} ↔ {t2:20}: {sim.mean():.4f}")

    # Save embeddings
    out_dir = Path("outputs/embeddings")
    out_dir.mkdir(parents=True, exist_ok=True)

    for name, emb in embeddings.items():
        np.save(out_dir / f"{name.replace(' ', '_').lower()}.npy", emb)

    # Save aphorism index
    with open(out_dir / "index.json", "w") as f:
        json.dump({"aphorism_numbers": aphorism_nums}, f)

    print(f"\nSaved embeddings to {out_dir}")
