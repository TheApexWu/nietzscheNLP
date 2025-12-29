"""
Low-Compute Domain Adaptation for Philosophical Embeddings

This module implements several lightweight techniques to improve embedding quality
for 19th-century German philosophy without fine-tuning large models.

Designed for: CPU only, <16GB RAM
Goal: Reduce "conceptual flattening" - make embeddings more sensitive to
philosophical distinctions.

Techniques implemented:
1. Prompt Engineering for Embeddings
2. Post-hoc Calibration (Whitening, CSLS)
3. Contrastive Anchoring (using known translation pairs)
4. Embedding Surgery (dimension weighting)
5. Ensemble/Triangulation methods
6. Zero-shot Domain Adaptation

References:
- Su et al. (2021) "Whitening Sentence Representations"
- Conneau et al. (2018) "Cross-lingual Language Model Pretraining" (CSLS)
- Gao et al. (2021) "SimCSE: Simple Contrastive Learning"
- Arora et al. (2017) "A Simple but Tough-to-Beat Baseline for Sentence Embeddings"
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
from collections import defaultdict
import json
from pathlib import Path


# =============================================================================
# 1. PROMPT ENGINEERING FOR EMBEDDINGS
# =============================================================================

class PhilosophicalPromptEngineer:
    """
    Enhance embedding quality through strategic prompting.

    Key insight: Many embedding models (especially E5, BGE, Instructor) are
    trained with specific prompt formats. We can leverage this to inject
    domain context without any training.

    Works on CPU with <1GB additional RAM.
    """

    # Domain-specific prompt templates
    PROMPTS = {
        # For E5 models
        "e5_philosophical": {
            "query": "query: Analyze the philosophical meaning of: {text}",
            "passage": "passage: In 19th-century German philosophy, {text}"
        },

        # For Instructor models (if used instead)
        "instructor_nietzsche": {
            "instruction": "Represent this passage from Nietzsche's philosophy for semantic comparison:",
            "text": "{text}"
        },

        # Context injection (works with any model)
        "context_prefix": {
            "german": "Aus Nietzsches Philosophie: {text}",
            "english": "From Nietzsche's philosophical work: {text}"
        },

        # Concept-specific prompts
        "concept_focused": {
            "will_to_power": "Passage discussing Wille zur Macht (will to power): {text}",
            "eternal_return": "Passage on ewige Wiederkunft (eternal recurrence): {text}",
            "ubermensch": "Passage about the Übermensch concept: {text}",
            "nihilism": "Passage examining nihilism and value creation: {text}",
            "ressentiment": "Passage on ressentiment and slave morality: {text}",
        }
    }

    # Key philosophical terms that should be preserved
    PHILOSOPHICAL_MARKERS = {
        "german": [
            "Wille zur Macht", "Übermensch", "ewige Wiederkunft",
            "Umwertung", "Ressentiment", "Nihilismus", "Werden",
            "Dasein", "Geist", "Weltanschauung", "Zeitgeist"
        ],
        "english": [
            "will to power", "overman", "superman", "eternal recurrence",
            "revaluation", "ressentiment", "nihilism", "becoming",
            "existence", "spirit", "worldview", "zeitgeist"
        ]
    }

    @classmethod
    def detect_concept(cls, text: str) -> Optional[str]:
        """Detect which major concept a passage discusses."""
        text_lower = text.lower()

        concept_keywords = {
            "will_to_power": ["will to power", "wille zur macht", "power", "macht"],
            "eternal_return": ["eternal", "recurrence", "return", "wiederkunft", "wiederkehr"],
            "ubermensch": ["übermensch", "overman", "superman", "higher man"],
            "nihilism": ["nihil", "nothing", "value", "meaning", "worthless"],
            "ressentiment": ["ressentiment", "slave", "revenge", "weak", "herd"],
        }

        for concept, keywords in concept_keywords.items():
            if any(kw in text_lower for kw in keywords):
                return concept
        return None

    @classmethod
    def apply_prompt(cls, text: str, style: str = "context_prefix",
                     language: str = "english") -> str:
        """
        Apply domain-aware prompting to text before embedding.

        Example:
            >>> text = "The strong must dominate the weak"
            >>> PhilosophicalPromptEngineer.apply_prompt(text)
            "From Nietzsche's philosophical work: The strong must dominate the weak"
        """
        prompts = cls.PROMPTS.get(style, cls.PROMPTS["context_prefix"])

        if style == "concept_focused":
            concept = cls.detect_concept(text)
            if concept and concept in prompts:
                return prompts[concept].format(text=text)

        if language in prompts:
            return prompts[language].format(text=text)

        return prompts.get("english", "{text}").format(text=text)

    @classmethod
    def preserve_terms(cls, text: str) -> str:
        """
        Add markers to preserve important philosophical terms.

        The idea: Wrap key terms so they're treated as units, not split.
        """
        for term in cls.PHILOSOPHICAL_MARKERS["german"]:
            if term in text:
                text = text.replace(term, f"[{term}]")
        for term in cls.PHILOSOPHICAL_MARKERS["english"]:
            if term.lower() in text.lower():
                # Case-insensitive replacement with markers
                import re
                pattern = re.compile(re.escape(term), re.IGNORECASE)
                text = pattern.sub(f"[{term}]", text)
        return text


# =============================================================================
# 2. POST-HOC CALIBRATION METHODS
# =============================================================================

class EmbeddingCalibrator:
    """
    Post-hoc methods to adjust embedding space without retraining.

    These methods work AFTER embeddings are computed and require only
    basic linear algebra operations.

    Memory: O(d^2) where d = embedding dimension (typically 384-1024)
    Compute: O(n * d^2) for n embeddings - very fast on CPU
    """

    @staticmethod
    def whiten(embeddings: np.ndarray, eps: float = 1e-6) -> np.ndarray:
        """
        Whitening transformation to make embedding space isotropic.

        Problem: Pre-trained embeddings often have anisotropic distributions,
        meaning some directions dominate. This causes all texts to appear
        similar (the "similarity collapse" problem).

        Solution: Whiten the embeddings so each dimension has unit variance
        and dimensions are uncorrelated.

        Reference: Su et al. (2021) "Whitening Sentence Representations"

        Args:
            embeddings: (n, d) array of embeddings
            eps: Small constant for numerical stability

        Returns:
            Whitened embeddings with same shape
        """
        # Center the embeddings
        mean = embeddings.mean(axis=0)
        centered = embeddings - mean

        # Compute covariance matrix
        cov = np.cov(centered, rowvar=False)

        # Eigendecomposition
        eigenvalues, eigenvectors = np.linalg.eigh(cov)

        # Compute whitening matrix: W = V * D^(-1/2) * V^T
        # where D is diagonal matrix of eigenvalues, V is eigenvectors
        D_inv_sqrt = np.diag(1.0 / np.sqrt(eigenvalues + eps))
        W = eigenvectors @ D_inv_sqrt @ eigenvectors.T

        # Apply whitening
        whitened = centered @ W

        # Re-normalize
        norms = np.linalg.norm(whitened, axis=1, keepdims=True)
        whitened = whitened / (norms + eps)

        return whitened

    @staticmethod
    def csls_similarity(source: np.ndarray, target: np.ndarray,
                       k: int = 10) -> np.ndarray:
        """
        Cross-domain Similarity Local Scaling (CSLS).

        Problem: Standard cosine similarity suffers from "hubness" - some
        points are nearest neighbors to many others, creating false matches.

        Solution: CSLS penalizes "hub" points by subtracting their average
        similarity to their k nearest neighbors.

        Reference: Conneau et al. (2018) "Word Translation Without Parallel Data"

        Args:
            source: (n, d) source embeddings
            target: (m, d) target embeddings
            k: Number of neighbors for averaging

        Returns:
            (n, m) CSLS similarity matrix
        """
        # Compute full similarity matrix
        sim_matrix = source @ target.T  # (n, m)

        # For each source point, get mean similarity to k nearest targets
        source_knn_sim = np.partition(sim_matrix, -k, axis=1)[:, -k:].mean(axis=1)

        # For each target point, get mean similarity to k nearest sources
        target_knn_sim = np.partition(sim_matrix.T, -k, axis=1)[:, -k:].mean(axis=1)

        # CSLS score: 2 * cos(x,y) - mean_knn(x) - mean_knn(y)
        csls = 2 * sim_matrix - source_knn_sim[:, np.newaxis] - target_knn_sim[np.newaxis, :]

        return csls

    @staticmethod
    def remove_principal_components(embeddings: np.ndarray,
                                     n_components: int = 1) -> np.ndarray:
        """
        Remove top principal components to reduce anisotropy.

        The idea: The top PCs often capture corpus-specific artifacts
        rather than semantic meaning. Removing them improves similarity.

        Reference: Arora et al. (2017) "A Simple but Tough-to-Beat Baseline"

        Args:
            embeddings: (n, d) embeddings
            n_components: Number of PCs to remove (usually 1-3)

        Returns:
            Adjusted embeddings
        """
        # Center
        mean = embeddings.mean(axis=0)
        centered = embeddings - mean

        # Get top principal components via SVD (more stable than PCA)
        U, S, Vt = np.linalg.svd(centered, full_matrices=False)

        # Project out top components
        for i in range(n_components):
            pc = Vt[i]  # i-th principal component
            centered = centered - np.outer(centered @ pc, pc)

        # Re-normalize
        norms = np.linalg.norm(centered, axis=1, keepdims=True)
        centered = centered / (norms + 1e-8)

        return centered

    @staticmethod
    def isotropy_score(embeddings: np.ndarray) -> float:
        """
        Measure how isotropic (uniform) the embedding distribution is.

        Returns value between 0 (highly anisotropic) and 1 (perfectly isotropic).
        """
        # Compute eigenvalues of covariance matrix
        centered = embeddings - embeddings.mean(axis=0)
        cov = np.cov(centered, rowvar=False)
        eigenvalues = np.linalg.eigvalsh(cov)

        # Isotropy = min(eigenvalue) / max(eigenvalue)
        # Perfectly isotropic = 1.0
        return float(eigenvalues.min() / (eigenvalues.max() + 1e-8))


# =============================================================================
# 3. CONTRASTIVE ANCHORING (Using Translation Pairs)
# =============================================================================

class ContrastiveAnchor:
    """
    Use known translation pairs to calibrate the embedding space.

    Key insight: We KNOW certain German-English pairs are translations.
    This provides supervised signal we can use to adjust similarities.

    This is a form of self-supervision using the translations themselves.
    """

    def __init__(self, german_embeddings: np.ndarray,
                 translation_embeddings: Dict[str, np.ndarray]):
        """
        Args:
            german_embeddings: (n, d) embeddings of German source texts
            translation_embeddings: {translator_name: (n, d) embeddings}
        """
        self.german = german_embeddings
        self.translations = translation_embeddings
        self.n_aphorisms = german_embeddings.shape[0]

    def compute_translation_offsets(self) -> Dict[str, np.ndarray]:
        """
        Compute the average offset vector from German to each translation.

        This captures the "translation direction" in embedding space.
        """
        offsets = {}
        for name, trans_emb in self.translations.items():
            # Average difference: translation - german
            offset = (trans_emb - self.german).mean(axis=0)
            offsets[name] = offset
        return offsets

    def align_to_german(self, translation_emb: np.ndarray,
                        offset: np.ndarray) -> np.ndarray:
        """
        Shift translations toward German embedding space.

        Useful for making cross-lingual comparisons more accurate.
        """
        aligned = translation_emb - offset
        # Re-normalize
        norms = np.linalg.norm(aligned, axis=1, keepdims=True)
        return aligned / (norms + 1e-8)

    def compute_procrustes_alignment(self, source: np.ndarray,
                                      target: np.ndarray) -> np.ndarray:
        """
        Orthogonal Procrustes alignment between two embedding spaces.

        Finds optimal rotation matrix W such that source @ W ≈ target.

        Reference: Conneau et al. (2018) "Word Translation Without Parallel Data"

        Args:
            source: (n, d) source embeddings
            target: (n, d) target embeddings (must be aligned by index)

        Returns:
            (d, d) rotation matrix W
        """
        # SVD of cross-covariance matrix
        M = target.T @ source
        U, S, Vt = np.linalg.svd(M)

        # Optimal rotation
        W = Vt.T @ U.T

        return W

    def compute_translation_quality(self) -> Dict[str, Dict[int, float]]:
        """
        Use German source as anchor to identify unusual translations.

        Returns per-aphorism "translation fidelity" scores for each translator.
        Higher score = closer to typical translation offset.
        """
        offsets = self.compute_translation_offsets()

        quality = {}
        for name, trans_emb in self.translations.items():
            expected_pos = self.german + offsets[name]

            # Compute per-aphorism deviation from expected
            deviations = np.linalg.norm(trans_emb - expected_pos, axis=1)

            # Convert to quality score (inverse of deviation)
            # Normalize by mean deviation
            mean_dev = deviations.mean()
            quality_scores = 1.0 - (deviations / (mean_dev * 2))
            quality_scores = np.clip(quality_scores, 0, 1)

            quality[name] = {i: float(q) for i, q in enumerate(quality_scores)}

        return quality

    def triangulate_meaning(self, aphorism_idx: int) -> Dict[str, float]:
        """
        Use multiple translations to triangulate semantic content.

        Idea: If most translations agree on a meaning, outliers may be
        interpretive choices worth investigating.

        Returns similarity of each translation to the centroid of all translations.
        """
        # Get all translation embeddings for this aphorism
        trans_vectors = []
        trans_names = []
        for name, emb in self.translations.items():
            trans_vectors.append(emb[aphorism_idx])
            trans_names.append(name)

        trans_vectors = np.array(trans_vectors)

        # Compute centroid
        centroid = trans_vectors.mean(axis=0)
        centroid = centroid / np.linalg.norm(centroid)

        # Compute similarity of each translation to centroid
        similarities = trans_vectors @ centroid

        return {name: float(sim) for name, sim in zip(trans_names, similarities)}


# =============================================================================
# 4. EMBEDDING SURGERY (Dimension Weighting)
# =============================================================================

class EmbeddingSurgeon:
    """
    Modify specific dimensions of embeddings to emphasize domain-relevant features.

    Theory: Different dimensions capture different semantic features.
    We can identify and weight dimensions that are most relevant to
    philosophical distinctions.

    Memory efficient: Only stores dimension weights (d floats).
    """

    def __init__(self, embedding_dim: int):
        self.dim = embedding_dim
        self.weights = np.ones(embedding_dim)
        self.dimension_roles = {}

    def identify_discriminative_dimensions(self,
                                           group1: np.ndarray,
                                           group2: np.ndarray) -> np.ndarray:
        """
        Find dimensions that best distinguish two groups of embeddings.

        Use case: Given embeddings of "will to power" vs "eternal return"
        passages, find which dimensions differ most.

        Returns: Per-dimension discriminative score.
        """
        # Mean difference per dimension
        diff = np.abs(group1.mean(axis=0) - group2.mean(axis=0))

        # Variance within each group (for normalization)
        var1 = group1.var(axis=0) + 1e-8
        var2 = group2.var(axis=0) + 1e-8

        # Fisher's criterion: between-class variance / within-class variance
        fisher_score = diff / np.sqrt(var1 + var2)

        return fisher_score

    def learn_concept_dimensions(self,
                                  concept_embeddings: Dict[str, np.ndarray]) -> Dict[str, np.ndarray]:
        """
        Learn which dimensions are associated with each philosophical concept.

        Args:
            concept_embeddings: {concept_name: (n, d) embeddings of that concept}

        Returns:
            {concept_name: dimension_importance_vector}
        """
        concept_dims = {}

        # Compute centroid for each concept
        centroids = {name: emb.mean(axis=0) for name, emb in concept_embeddings.items()}

        # Overall mean
        all_embs = np.vstack(list(concept_embeddings.values()))
        global_mean = all_embs.mean(axis=0)

        # Per-concept deviation from global mean
        for name, centroid in centroids.items():
            deviation = np.abs(centroid - global_mean)
            # Normalize to sum to 1
            concept_dims[name] = deviation / (deviation.sum() + 1e-8)

        self.dimension_roles = concept_dims
        return concept_dims

    def set_weights_from_supervision(self,
                                      similar_pairs: List[Tuple[np.ndarray, np.ndarray]],
                                      dissimilar_pairs: List[Tuple[np.ndarray, np.ndarray]],
                                      learning_rate: float = 0.1,
                                      iterations: int = 100) -> np.ndarray:
        """
        Learn dimension weights using known similar/dissimilar pairs.

        This is lightweight "training" - just adjusting d floats based
        on which dimensions help distinguish known pairs.

        Args:
            similar_pairs: List of (emb1, emb2) that SHOULD be similar
            dissimilar_pairs: List of (emb1, emb2) that SHOULD be different

        Returns:
            Learned dimension weights
        """
        weights = np.ones(self.dim)

        for _ in range(iterations):
            gradient = np.zeros(self.dim)

            # Similar pairs: reward dimensions where values are close
            for e1, e2 in similar_pairs:
                diff = np.abs(e1 - e2)
                gradient -= diff  # Decrease weight on differing dimensions

            # Dissimilar pairs: reward dimensions where values differ
            for e1, e2 in dissimilar_pairs:
                diff = np.abs(e1 - e2)
                gradient += diff  # Increase weight on differing dimensions

            # Normalize gradient
            gradient = gradient / (np.linalg.norm(gradient) + 1e-8)

            # Update weights
            weights = weights + learning_rate * gradient

            # Keep weights positive
            weights = np.maximum(weights, 0.1)

            # Normalize
            weights = weights / weights.mean()

        self.weights = weights
        return weights

    def apply_weights(self, embeddings: np.ndarray) -> np.ndarray:
        """Apply learned dimension weights to embeddings."""
        weighted = embeddings * self.weights
        # Re-normalize
        norms = np.linalg.norm(weighted, axis=1, keepdims=True)
        return weighted / (norms + 1e-8)

    def focus_on_concept(self, embeddings: np.ndarray,
                         concept: str, strength: float = 1.5) -> np.ndarray:
        """
        Emphasize dimensions relevant to a specific concept.

        Useful when comparing passages specifically about e.g. "will to power".
        """
        if concept not in self.dimension_roles:
            return embeddings

        # Boost relevant dimensions
        concept_weights = 1.0 + (self.dimension_roles[concept] * strength)

        weighted = embeddings * concept_weights
        norms = np.linalg.norm(weighted, axis=1, keepdims=True)
        return weighted / (norms + 1e-8)


# =============================================================================
# 5. ENSEMBLE / TRIANGULATION METHODS
# =============================================================================

class EmbeddingEnsemble:
    """
    Combine multiple embedding models or views for more robust comparisons.

    Even without GPU, you can run multiple small models and combine results.
    This reduces model-specific biases.
    """

    # Lightweight models that work on CPU
    LIGHTWEIGHT_MODELS = {
        "minilm": "paraphrase-multilingual-MiniLM-L12-v2",  # 420MB, fast
        "mpnet": "paraphrase-multilingual-mpnet-base-v2",   # 1GB, balanced
        "distiluse": "distiluse-base-multilingual-cased-v1",  # 520MB, fast
    }

    def __init__(self):
        self.embeddings = {}  # {model_name: {translator: embeddings}}
        self.weights = {}

    def add_embeddings(self, model_name: str,
                       translator_embeddings: Dict[str, np.ndarray]):
        """Add embeddings from a specific model."""
        self.embeddings[model_name] = translator_embeddings
        self.weights[model_name] = 1.0

    def set_model_weight(self, model_name: str, weight: float):
        """Adjust weight for a specific model in ensemble."""
        if model_name in self.weights:
            self.weights[model_name] = weight

    def weighted_similarity(self, translator1: str, translator2: str,
                            aphorism_idx: int) -> float:
        """
        Compute ensemble-weighted similarity between two translations.
        """
        total_weight = 0
        weighted_sim = 0

        for model_name, trans_embs in self.embeddings.items():
            weight = self.weights.get(model_name, 1.0)

            emb1 = trans_embs[translator1][aphorism_idx]
            emb2 = trans_embs[translator2][aphorism_idx]

            sim = float(np.dot(emb1, emb2))

            weighted_sim += weight * sim
            total_weight += weight

        return weighted_sim / total_weight if total_weight > 0 else 0.0

    def disagreement_score(self, translator1: str, translator2: str,
                           aphorism_idx: int) -> float:
        """
        Measure how much models disagree about similarity.

        High disagreement = the passage may have subtle nuances that
        different models capture differently.
        """
        similarities = []

        for trans_embs in self.embeddings.values():
            emb1 = trans_embs[translator1][aphorism_idx]
            emb2 = trans_embs[translator2][aphorism_idx]
            similarities.append(float(np.dot(emb1, emb2)))

        if len(similarities) < 2:
            return 0.0

        return float(np.std(similarities))

    def rank_fusion(self, query_emb: np.ndarray,
                    candidate_embs: np.ndarray,
                    method: str = "rrf") -> np.ndarray:
        """
        Combine rankings from multiple models using rank fusion.

        Methods:
        - "rrf": Reciprocal Rank Fusion (robust, parameter-free)
        - "borda": Borda count

        Returns: Fused ranking scores for each candidate.
        """
        n_candidates = candidate_embs.shape[0]
        fused_scores = np.zeros(n_candidates)

        for model_name, trans_embs in self.embeddings.items():
            # This is simplified - in practice you'd pass model-specific embeddings
            # For now, just demonstrate the fusion logic
            similarities = candidate_embs @ query_emb
            ranks = np.argsort(-similarities)  # Higher sim = lower rank

            if method == "rrf":
                # RRF: score = sum(1 / (k + rank)) where k=60 is standard
                k = 60
                for rank, idx in enumerate(ranks):
                    fused_scores[idx] += 1.0 / (k + rank)
            elif method == "borda":
                # Borda: score = n_candidates - rank
                for rank, idx in enumerate(ranks):
                    fused_scores[idx] += n_candidates - rank

        return fused_scores


# =============================================================================
# 6. ZERO-SHOT DOMAIN ADAPTATION
# =============================================================================

class ZeroShotAdapter:
    """
    Domain adaptation without any training on target domain data.

    Uses only the structure of the embedding space and known
    relationships between concepts.
    """

    def __init__(self):
        # Define philosophical concept relationships
        self.concept_hierarchy = {
            "metaphysics": ["will_to_power", "eternal_return", "becoming", "being"],
            "ethics": ["good_evil", "master_slave", "values", "nobility"],
            "epistemology": ["perspectivism", "truth", "interpretation"],
            "psychology": ["ressentiment", "drives", "sublimation"],
        }

        # Antonym pairs (should have low similarity)
        self.antonym_pairs = [
            ("master_morality", "slave_morality"),
            ("life_affirmation", "nihilism"),
            ("strength", "weakness"),
            ("creation", "reaction"),
        ]

    def create_concept_anchors(self, embedder) -> Dict[str, np.ndarray]:
        """
        Create anchor embeddings for key concepts using definitions.

        These anchors can be used to calibrate similarities.
        """
        concept_definitions = {
            "will_to_power": "The fundamental drive underlying all action, the desire to grow, overcome, and create",
            "eternal_return": "The cosmological idea that all events recur infinitely, demanding affirmation of life",
            "ubermensch": "The higher human who creates new values and affirms life unconditionally",
            "nihilism": "The condition where highest values devalue themselves, leaving meaninglessness",
            "ressentiment": "Reactive hatred of the powerful by the weak, inverting values out of revenge",
            "master_morality": "Morality of the strong, valuing nobility, strength, and self-affirmation",
            "slave_morality": "Morality of the weak, valuing pity, humility, and resentment of the strong",
            "perspectivism": "There are no facts, only interpretations from different perspectives",
            "amor_fati": "Love of fate, affirming everything that happens as necessary",
            "last_man": "The degraded human who seeks only comfort and cannot create values",
        }

        # Embed concept definitions
        texts = list(concept_definitions.values())
        embeddings = embedder.embed(texts)

        return {name: emb for name, emb in zip(concept_definitions.keys(), embeddings)}

    def semantic_neighborhood_adjustment(self,
                                          embeddings: np.ndarray,
                                          concept_anchors: Dict[str, np.ndarray]) -> np.ndarray:
        """
        Adjust embeddings based on proximity to concept anchors.

        Embeddings near known concept anchors are pulled slightly closer
        to those anchors, reinforcing conceptual clustering.
        """
        anchors = np.array(list(concept_anchors.values()))

        adjusted = embeddings.copy()

        for i in range(len(embeddings)):
            # Find nearest anchor
            similarities = embeddings[i] @ anchors.T
            nearest_idx = similarities.argmax()
            nearest_sim = similarities[nearest_idx]

            if nearest_sim > 0.5:  # Only adjust if reasonably close
                # Pull slightly toward anchor
                pull_strength = 0.1 * (nearest_sim - 0.5)
                adjusted[i] = (1 - pull_strength) * embeddings[i] + pull_strength * anchors[nearest_idx]

        # Re-normalize
        norms = np.linalg.norm(adjusted, axis=1, keepdims=True)
        adjusted = adjusted / (norms + 1e-8)

        return adjusted

    def contrastive_rescaling(self,
                               embeddings: np.ndarray,
                               positive_pairs: List[Tuple[int, int]],
                               negative_pairs: List[Tuple[int, int]],
                               scale_factor: float = 0.1) -> np.ndarray:
        """
        Rescale similarities based on known positive/negative pairs.

        Without training, we adjust the space geometry by:
        1. Computing ideal vs actual similarities
        2. Learning a global rescaling function

        Args:
            positive_pairs: Indices of embeddings that should be similar
            negative_pairs: Indices of embeddings that should be dissimilar
        """
        # Compute current similarities for known pairs
        pos_sims = [float(embeddings[i] @ embeddings[j]) for i, j in positive_pairs]
        neg_sims = [float(embeddings[i] @ embeddings[j]) for i, j in negative_pairs]

        # Target: positives should be > 0.7, negatives should be < 0.3
        pos_target = 0.8
        neg_target = 0.2

        # Simple linear rescaling
        # new_sim = a * old_sim + b
        # Solve for a, b using least squares

        old_sims = np.array(pos_sims + neg_sims)
        targets = np.array([pos_target] * len(pos_sims) + [neg_target] * len(neg_sims))

        # Linear regression
        A = np.vstack([old_sims, np.ones(len(old_sims))]).T
        a, b = np.linalg.lstsq(A, targets, rcond=None)[0]

        print(f"Learned rescaling: new_sim = {a:.3f} * old_sim + {b:.3f}")

        # Note: We can't directly apply this to embeddings, but we can
        # return the rescaling parameters for use in similarity computation
        return {"scale": a, "offset": b}


# =============================================================================
# INTEGRATED PIPELINE
# =============================================================================

class DomainAdaptedEmbedder:
    """
    Complete pipeline combining multiple adaptation techniques.

    Designed for CPU-only operation with <16GB RAM.
    """

    def __init__(self, base_embedder=None, calibration_methods=None):
        """
        Args:
            base_embedder: An Embedder instance (from embed.py)
            calibration_methods: List of calibration methods to apply
                Options: ["whiten", "remove_pc", "csls"]
        """
        self.embedder = base_embedder
        self.calibration_methods = calibration_methods or ["whiten", "remove_pc"]
        self.calibrator = EmbeddingCalibrator()
        self.prompter = PhilosophicalPromptEngineer()
        self.surgeon = None  # Initialized when dimension is known

    def embed_with_prompting(self, texts: List[str],
                              language: str = "english",
                              prompt_style: str = "context_prefix") -> np.ndarray:
        """
        Embed texts with domain-aware prompting.
        """
        # Apply prompting
        prompted = [
            self.prompter.apply_prompt(t, style=prompt_style, language=language)
            for t in texts
        ]

        # Embed
        embeddings = self.embedder.embed(prompted)

        return embeddings

    def calibrate(self, embeddings: np.ndarray) -> np.ndarray:
        """Apply all configured calibration methods."""
        result = embeddings.copy()

        for method in self.calibration_methods:
            if method == "whiten":
                result = self.calibrator.whiten(result)
            elif method == "remove_pc":
                result = self.calibrator.remove_principal_components(result, n_components=1)

        return result

    def embed_and_calibrate(self, texts: List[str], **kwargs) -> np.ndarray:
        """Full pipeline: prompt -> embed -> calibrate."""
        embeddings = self.embed_with_prompting(texts, **kwargs)
        calibrated = self.calibrate(embeddings)
        return calibrated


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def diagnose_embedding_quality(embeddings: np.ndarray, labels: List[str] = None) -> Dict:
    """
    Diagnose common issues with embedding quality.

    Returns metrics that indicate potential problems.
    """
    calibrator = EmbeddingCalibrator()

    # Compute similarity matrix
    sim_matrix = embeddings @ embeddings.T
    np.fill_diagonal(sim_matrix, 0)  # Ignore self-similarity

    # Metrics
    metrics = {
        "isotropy_score": calibrator.isotropy_score(embeddings),
        "mean_similarity": float(sim_matrix.mean()),
        "max_off_diagonal_similarity": float(sim_matrix.max()),
        "similarity_std": float(sim_matrix.std()),
    }

    # Hubness: how often each point is a nearest neighbor
    nn_counts = np.zeros(len(embeddings))
    for i in range(len(embeddings)):
        nn = sim_matrix[i].argmax()
        nn_counts[nn] += 1

    metrics["hubness_max"] = int(nn_counts.max())
    metrics["hubness_std"] = float(nn_counts.std())

    # Interpretation
    issues = []
    if metrics["isotropy_score"] < 0.1:
        issues.append("LOW_ISOTROPY: Embedding space is highly anisotropic. Try whitening.")
    if metrics["mean_similarity"] > 0.7:
        issues.append("HIGH_BASELINE_SIM: All embeddings are too similar. Apply PC removal.")
    if metrics["hubness_max"] > len(embeddings) * 0.2:
        issues.append("HUBNESS: Some points are universal neighbors. Try CSLS similarity.")

    metrics["issues"] = issues

    return metrics


def compare_calibration_methods(embeddings: np.ndarray,
                                 known_similar: List[Tuple[int, int]],
                                 known_different: List[Tuple[int, int]]) -> Dict:
    """
    Compare different calibration methods using known pairs.

    Args:
        known_similar: Index pairs that should have high similarity
        known_different: Index pairs that should have low similarity
    """
    calibrator = EmbeddingCalibrator()

    methods = {
        "original": embeddings,
        "whitened": calibrator.whiten(embeddings),
        "pc_removed_1": calibrator.remove_principal_components(embeddings, 1),
        "pc_removed_2": calibrator.remove_principal_components(embeddings, 2),
    }

    results = {}

    for name, emb in methods.items():
        # Compute similarities for known pairs
        sim_similar = [float(emb[i] @ emb[j]) for i, j in known_similar]
        sim_different = [float(emb[i] @ emb[j]) for i, j in known_different]

        # Quality metrics
        mean_similar = np.mean(sim_similar)
        mean_different = np.mean(sim_different)
        separation = mean_similar - mean_different

        results[name] = {
            "mean_similar_pair_sim": float(mean_similar),
            "mean_different_pair_sim": float(mean_different),
            "separation": float(separation),
            "isotropy": calibrator.isotropy_score(emb),
        }

    return results


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == "__main__":
    print("Domain Adaptation Module for Philosophical Embeddings")
    print("=" * 60)
    print("\nThis module provides the following techniques:")
    print("1. PhilosophicalPromptEngineer - Domain-aware prompting")
    print("2. EmbeddingCalibrator - Whitening, CSLS, PC removal")
    print("3. ContrastiveAnchor - Use translation pairs for calibration")
    print("4. EmbeddingSurgeon - Dimension weighting")
    print("5. EmbeddingEnsemble - Multi-model combination")
    print("6. ZeroShotAdapter - Concept-based adjustment")
    print("\nSee docstrings for detailed usage examples.")
