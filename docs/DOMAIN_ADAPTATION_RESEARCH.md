# Low-Compute Domain Adaptation for 19th-Century German Philosophy

## Executive Summary

This document outlines practical methods to improve embedding quality for philosophical texts **without fine-tuning large models**. All techniques are designed for:

- **CPU-only execution** (no GPU required)
- **<16GB RAM**
- **Minimal storage** (no additional model downloads beyond base embedder)

The goal is to reduce "conceptual flattening" - making embeddings more sensitive to philosophical distinctions like the difference between "will to power" and "eternal recurrence."

---

## 1. Adapter-Based Methods (Lightweight)

### 1.1 Why Standard LoRA/Prefix Tuning Won't Work Here

LoRA (Low-Rank Adaptation) and prefix tuning are typically used for:
- Adapting **generative** models (LLMs)
- Requires gradient computation and backpropagation
- Still needs GPU for reasonable training times
- Typical LoRA adds ~1-10M parameters that still need training

**These are NOT suitable for our constraints.**

### 1.2 What DOES Work: Frozen Backbone + Linear Probe

Instead of adapter layers, we can add a **learned linear transformation** on top of frozen embeddings:

```python
# Linear adapter approach
class LinearAdapter:
    def __init__(self, input_dim, output_dim=None):
        self.input_dim = input_dim
        self.output_dim = output_dim or input_dim
        # Only need to store: d x d matrix = 384x384 = ~600KB
        self.W = np.eye(input_dim)[:, :self.output_dim]

    def fit(self, X_train, y_train, learning_rate=0.01, epochs=100):
        """
        Learn a linear transformation that improves separation.

        X_train: (n, d) embeddings
        y_train: (n,) class labels (e.g., philosophical concept)
        """
        from sklearn.linear_model import LogisticRegression

        # Use logistic regression to learn discriminative directions
        clf = LogisticRegression(max_iter=1000)
        clf.fit(X_train, y_train)

        # The coefficients give us discriminative directions
        # Use them to weight the embedding dimensions
        importance = np.abs(clf.coef_).sum(axis=0)
        importance = importance / importance.max()

        self.W = np.diag(importance)
        return self

    def transform(self, X):
        """Apply learned transformation."""
        transformed = X @ self.W
        # Re-normalize
        norms = np.linalg.norm(transformed, axis=1, keepdims=True)
        return transformed / (norms + 1e-8)
```

**Memory**: O(d^2) = ~600KB for 384-dim embeddings
**Compute**: O(n*d^2) - very fast on CPU

---

## 2. Prompt Engineering for Embeddings

### 2.1 The Key Insight

Modern embedding models like E5, BGE, and Instructor are trained with specific prompt formats. The model has learned that:
- `"query: ..."` means "find things related to this"
- `"passage: ..."` means "this is a document to be retrieved"

We can exploit this by **injecting domain context into the prompt**.

### 2.2 Effective Prompt Strategies

#### Strategy 1: Domain Context Prefix
```python
# Instead of:
"The strong must dominate the weak."

# Use:
"From Nietzsche's philosophical work: The strong must dominate the weak."
```

This tells the model to interpret the text in a philosophical context, not as a random statement.

#### Strategy 2: Concept-Specific Framing
```python
def get_concept_prompt(text, detected_concept):
    prompts = {
        "will_to_power": f"Passage about Nietzsche's concept of Wille zur Macht: {text}",
        "eternal_return": f"Passage on eternal recurrence in Nietzsche: {text}",
        "nihilism": f"Philosophical discussion of nihilism: {text}",
    }
    return prompts.get(detected_concept, f"Philosophical text: {text}")
```

#### Strategy 3: Bilingual Anchoring (for German texts)
```python
# For German source:
"Aus Nietzsches Jenseits von Gut und Böse: {german_text}"

# For English translation:
"English translation of Nietzsche's Beyond Good and Evil: {english_text}"
```

### 2.3 Empirical Evidence

Studies have shown that prompt engineering can improve retrieval quality by 5-15% without any training:
- Instructor models (Su et al., 2022) showed task-specific prompts improve performance
- BGE models benefit from "Represent this..." prefixes

---

## 3. Post-hoc Calibration Methods

### 3.1 Whitening (Highly Recommended)

**Problem**: Pre-trained embeddings are often anisotropic - clustered in a narrow cone of the vector space. This causes all texts to appear similar.

**Solution**: Whitening transforms the space to have isotropic (uniform) distribution.

```python
def whiten(embeddings, eps=1e-6):
    # Center
    mean = embeddings.mean(axis=0)
    centered = embeddings - mean

    # Covariance matrix
    cov = np.cov(centered, rowvar=False)

    # Whitening matrix via eigendecomposition
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    D_inv_sqrt = np.diag(1.0 / np.sqrt(eigenvalues + eps))
    W = eigenvectors @ D_inv_sqrt @ eigenvectors.T

    # Apply
    whitened = centered @ W

    # Re-normalize
    norms = np.linalg.norm(whitened, axis=1, keepdims=True)
    return whitened / (norms + eps)
```

**Why it helps philosophy:**
- Philosophical concepts often cluster together because models see them as "abstract"
- Whitening spreads them out, making distinctions more visible

**Reference**: Su et al. (2021) "Whitening Sentence Representations for Better Semantics and Faster Retrieval"

### 3.2 Principal Component Removal

**Problem**: The top principal components often capture corpus-specific artifacts (e.g., "this is 19th century writing") rather than semantic content.

**Solution**: Remove top 1-3 principal components.

```python
def remove_top_pcs(embeddings, n_remove=1):
    centered = embeddings - embeddings.mean(axis=0)

    # SVD
    U, S, Vt = np.linalg.svd(centered, full_matrices=False)

    # Project out top components
    for i in range(n_remove):
        pc = Vt[i]
        centered = centered - np.outer(centered @ pc, pc)

    # Re-normalize
    norms = np.linalg.norm(centered, axis=1, keepdims=True)
    return centered / (norms + 1e-8)
```

**Reference**: Arora et al. (2017) "A Simple but Tough-to-Beat Baseline for Sentence Embeddings"

### 3.3 CSLS (Cross-domain Similarity Local Scaling)

**Problem**: "Hubness" - some embeddings are nearest neighbors to many others, creating false matches.

**Solution**: CSLS penalizes "hub" points by subtracting their average similarity to neighbors.

```
CSLS(x, y) = 2*cos(x,y) - mean_k_nearest(x) - mean_k_nearest(y)
```

**Especially useful for**: Cross-lingual comparisons (German original vs. English translations)

**Reference**: Conneau et al. (2018) "Word Translation Without Parallel Data"

---

## 4. Contrastive Examples (Self-Supervision from Translations)

### 4.1 The Key Insight

**We have gold supervision**: We know that each German aphorism should be semantically identical to its English translations. This is **free labeled data**.

### 4.2 Technique 1: Compute Translation Offsets

Each translator has a characteristic "style" in embedding space:

```python
def compute_translation_offset(german_emb, english_emb):
    """Average difference between translation and source."""
    return (english_emb - german_emb).mean(axis=0)

# Kaufmann tends to be +0.1 in dimensions [23, 45, 78]
# Common tends to be +0.15 in dimensions [12, 34, 90]
```

**Use**: Detect when a translation deviates from typical style (potential interpretive choice).

### 4.3 Technique 2: Procrustes Alignment

Find the optimal rotation to align translation space with German space:

```python
def procrustes_align(source, target):
    """
    Find rotation W such that source @ W ≈ target.
    source and target must be aligned by index.
    """
    M = target.T @ source
    U, S, Vt = np.linalg.svd(M)
    W = Vt.T @ U.T
    return W

# Now (translation @ W) is in same space as German
aligned_translation = translation_emb @ W
```

**Use**: Makes cross-lingual similarity more meaningful.

### 4.4 Technique 3: Triangulation

If most translations agree on meaning, outliers are interesting:

```python
def find_outlier_translations(aphorism_idx, translation_embs):
    """Find translations that diverge from consensus."""
    vectors = [emb[aphorism_idx] for emb in translation_embs.values()]
    centroid = np.mean(vectors, axis=0)
    centroid = centroid / np.linalg.norm(centroid)

    deviations = {
        name: 1 - float(emb[aphorism_idx] @ centroid)
        for name, emb in translation_embs.items()
    }
    return deviations
```

---

## 5. Embedding Surgery (Dimension Weighting)

### 5.1 The Intuition

Different dimensions in the embedding capture different semantic features. If we knew which dimensions were "philosophical concept" dimensions vs. "writing style" dimensions, we could weight accordingly.

### 5.2 Learning Dimension Weights from Known Pairs

```python
def learn_dimension_weights(similar_pairs, dissimilar_pairs, n_iter=100, lr=0.1):
    """
    Learn which dimensions help distinguish pairs.

    similar_pairs: [(emb1, emb2), ...] that should be close
    dissimilar_pairs: [(emb1, emb2), ...] that should be far
    """
    d = similar_pairs[0][0].shape[0]
    weights = np.ones(d)

    for _ in range(n_iter):
        grad = np.zeros(d)

        # Similar pairs: reduce weight on differing dimensions
        for e1, e2 in similar_pairs:
            grad -= np.abs(e1 - e2)

        # Dissimilar pairs: increase weight on differing dimensions
        for e1, e2 in dissimilar_pairs:
            grad += np.abs(e1 - e2)

        # Update
        grad = grad / (np.linalg.norm(grad) + 1e-8)
        weights = weights + lr * grad
        weights = np.maximum(weights, 0.1)
        weights = weights / weights.mean()

    return weights
```

### 5.3 Application: Concept-Focused Comparison

```python
# If comparing "will to power" passages, boost relevant dimensions
def focus_on_concept(embeddings, concept_dims, strength=1.5):
    boosted = embeddings * (1 + concept_dims * strength)
    norms = np.linalg.norm(boosted, axis=1, keepdims=True)
    return boosted / norms
```

---

## 6. Ensemble / Triangulation Methods

### 6.1 Multi-Model Ensemble

Run multiple lightweight models and combine:

| Model | Size | Speed on CPU |
|-------|------|--------------|
| MiniLM | 420MB | ~2 min for corpus |
| DistilUSE | 520MB | ~3 min for corpus |
| MPNet | 1GB | ~5 min for corpus |

```python
def ensemble_similarity(emb_dict, translator1, translator2, idx):
    """Weighted average similarity across models."""
    sims = []
    for model_embs in emb_dict.values():
        e1 = model_embs[translator1][idx]
        e2 = model_embs[translator2][idx]
        sims.append(float(e1 @ e2))
    return np.mean(sims)
```

### 6.2 Disagreement Detection

When models disagree, the passage may have subtle nuances:

```python
def model_disagreement(emb_dict, translator1, translator2, idx):
    """High std = models see this differently."""
    sims = [...]  # compute as above
    return np.std(sims)
```

**Use**: Flag passages where models disagree for human review.

### 6.3 Rank Fusion

Combine rankings from multiple models using Reciprocal Rank Fusion:

```
RRF_score(d) = sum(1 / (k + rank_i(d))) for each model i
```

Standard k=60 works well. This is robust even when models have different similarity scales.

---

## 7. Zero-Shot Domain Adaptation

### 7.1 Concept Anchors

Create "anchor" embeddings for key philosophical concepts:

```python
concept_definitions = {
    "will_to_power": "The fundamental drive underlying all action...",
    "eternal_return": "The cosmological idea that all events recur...",
    "ubermensch": "The higher human who creates new values...",
}

# Embed definitions to create anchors
anchors = {name: embedder.embed([defn])[0] for name, defn in concept_definitions.items()}
```

### 7.2 Semantic Neighborhood Adjustment

Pull embeddings slightly toward their nearest concept anchor:

```python
def adjust_to_nearest_anchor(emb, anchors, pull_strength=0.1):
    similarities = {name: float(emb @ anchor) for name, anchor in anchors.items()}
    nearest = max(similarities, key=similarities.get)

    if similarities[nearest] > 0.5:
        adjusted = (1 - pull_strength) * emb + pull_strength * anchors[nearest]
        return adjusted / np.linalg.norm(adjusted)
    return emb
```

**Effect**: Reinforces conceptual clustering without training.

---

## 8. Practical Recommendations

### Recommended Pipeline (In Order)

1. **Prompt Engineering** (free, always apply)
   - Use domain context prefix for all texts
   - Preserve key terms with markers

2. **Whitening** (always apply)
   - Improves isotropy
   - Reduces baseline similarity

3. **PC Removal** (if still anisotropic)
   - Remove 1 component typically sufficient
   - Test with 2 if needed

4. **CSLS** (for cross-lingual comparison)
   - Use when comparing German to translations
   - k=10 is standard

5. **Contrastive Anchoring** (for outlier detection)
   - Use Procrustes alignment for cross-lingual
   - Use triangulation to find unusual translations

### Memory Budget

| Component | Memory |
|-----------|--------|
| MiniLM model | 420MB |
| 1000 embeddings (384d) | 1.5MB |
| Whitening matrix | 0.6MB |
| Concept anchors (20) | 30KB |
| **Total** | **~425MB** |

Well under 16GB limit.

### What NOT to Do

1. **Don't fine-tune embedding models** - requires GPU, training data
2. **Don't use LoRA/adapters** - still needs training
3. **Don't load multiple large models simultaneously** - use sequentially
4. **Don't skip whitening** - most impactful technique

---

## 9. Code Examples

### Complete Pipeline

```python
from domain_adaptation import (
    PhilosophicalPromptEngineer,
    EmbeddingCalibrator,
    ContrastiveAnchor,
    diagnose_embedding_quality
)
from embed import Embedder

def adapt_philosophical_embeddings(texts, language="english"):
    """Full adaptation pipeline for philosophical texts."""

    # 1. Initialize components
    embedder = Embedder(mode="fast")  # MiniLM
    prompter = PhilosophicalPromptEngineer()
    calibrator = EmbeddingCalibrator()

    # 2. Apply prompting
    prompted = [prompter.apply_prompt(t, language=language) for t in texts]

    # 3. Generate embeddings
    raw_emb = embedder.embed(prompted)

    # 4. Diagnose
    diagnosis = diagnose_embedding_quality(raw_emb)
    print(f"Pre-calibration isotropy: {diagnosis['isotropy_score']:.4f}")

    # 5. Calibrate
    calibrated = calibrator.whiten(raw_emb)

    if diagnosis['isotropy_score'] < 0.05:
        calibrated = calibrator.remove_principal_components(calibrated, 1)

    # 6. Final check
    final = diagnose_embedding_quality(calibrated)
    print(f"Post-calibration isotropy: {final['isotropy_score']:.4f}")

    return calibrated
```

### Finding Interesting Translation Differences

```python
def find_translation_outliers(german_emb, translation_embs, top_n=10):
    """Find passages where translations diverge most."""
    anchor = ContrastiveAnchor(german_emb, translation_embs)

    outliers = []
    for idx in range(len(german_emb)):
        triangulation = anchor.triangulate_meaning(idx)
        min_sim = min(triangulation.values())
        max_sim = max(triangulation.values())
        spread = max_sim - min_sim

        outliers.append((idx, spread, triangulation))

    # Sort by spread (highest = most disagreement)
    outliers.sort(key=lambda x: -x[1])

    return outliers[:top_n]
```

---

## 10. References

1. Su, J. et al. (2021). "Whitening Sentence Representations for Better Semantics and Faster Retrieval." arXiv:2103.15316

2. Conneau, A. et al. (2018). "Word Translation Without Parallel Data." ICLR 2018.

3. Arora, S. et al. (2017). "A Simple but Tough-to-Beat Baseline for Sentence Embeddings." ICLR 2017.

4. Gao, T. et al. (2021). "SimCSE: Simple Contrastive Learning of Sentence Embeddings." EMNLP 2021.

5. Su, H. et al. (2022). "One Embedder, Any Task: Instruction-Finetuned Text Embeddings." arXiv:2212.09741 (Instructor models)

---

## Appendix A: Diagnosing Embedding Quality

Run this to understand your embedding space:

```python
from domain_adaptation import diagnose_embedding_quality

diagnosis = diagnose_embedding_quality(your_embeddings)

print("Isotropy:", diagnosis["isotropy_score"])
# < 0.1 = anisotropic (bad), > 0.3 = good

print("Mean similarity:", diagnosis["mean_similarity"])
# > 0.7 = everything looks the same (bad)

print("Issues:", diagnosis["issues"])
# Will tell you what to fix
```

## Appendix B: Quick Reference Table

| Problem | Symptom | Solution |
|---------|---------|----------|
| All texts similar | mean_sim > 0.7 | Whitening + PC removal |
| Anisotropic space | isotropy < 0.1 | Whitening |
| Hubness | some points are universal neighbors | CSLS |
| Cross-lingual mismatch | German-English pairs have low similarity | Procrustes alignment |
| Conceptual flattening | philosophical distinctions lost | Concept anchors + dimension weighting |
