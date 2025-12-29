#!/usr/bin/env python3
"""
Quick-start script for calibrating embeddings.

This applies the recommended low-compute adaptation techniques to
existing embeddings or generates new calibrated embeddings.

Usage:
    # Calibrate existing embeddings
    python calibrate_embeddings.py --input outputs/embeddings/

    # Generate and calibrate new embeddings
    python calibrate_embeddings.py --generate

    # Run diagnostics only
    python calibrate_embeddings.py --diagnose outputs/embeddings/
"""

import argparse
import json
import numpy as np
from pathlib import Path

from domain_adaptation import (
    PhilosophicalPromptEngineer,
    EmbeddingCalibrator,
    ContrastiveAnchor,
    diagnose_embedding_quality,
    compare_calibration_methods,
)
from embed import Embedder, load_aligned_corpus, align_aphorisms


def load_embeddings(embedding_dir: str) -> dict:
    """Load all saved embeddings."""
    emb_dir = Path(embedding_dir)
    embeddings = {}

    for npy_file in emb_dir.glob("*.npy"):
        name = npy_file.stem.replace("_", " ").title()
        embeddings[name] = np.load(npy_file)

    # Load index
    index_path = emb_dir / "index.json"
    if index_path.exists():
        with open(index_path) as f:
            index = json.load(f)
    else:
        index = None

    return embeddings, index


def diagnose_all(embeddings: dict) -> dict:
    """Run diagnostics on all embedding sets."""
    print("\n" + "=" * 60)
    print("EMBEDDING DIAGNOSTICS")
    print("=" * 60)

    all_diagnosis = {}

    for name, emb in embeddings.items():
        print(f"\n{name}:")
        diagnosis = diagnose_embedding_quality(emb)

        print(f"  Isotropy: {diagnosis['isotropy_score']:.4f}")
        print(f"  Mean similarity: {diagnosis['mean_similarity']:.4f}")
        print(f"  Max off-diagonal sim: {diagnosis['max_off_diagonal_similarity']:.4f}")
        print(f"  Hubness (max): {diagnosis['hubness_max']}")

        if diagnosis['issues']:
            print(f"  Issues:")
            for issue in diagnosis['issues']:
                print(f"    - {issue}")
        else:
            print("  No issues detected.")

        all_diagnosis[name] = diagnosis

    return all_diagnosis


def calibrate_all(embeddings: dict, methods: list = None) -> dict:
    """Apply calibration to all embedding sets."""
    if methods is None:
        methods = ["whiten", "remove_pc"]

    calibrator = EmbeddingCalibrator()
    calibrated = {}

    print("\n" + "=" * 60)
    print("APPLYING CALIBRATION")
    print("=" * 60)

    for name, emb in embeddings.items():
        print(f"\nCalibrating {name}...")

        result = emb.copy()

        for method in methods:
            if method == "whiten":
                print("  Applying whitening...")
                result = calibrator.whiten(result)

            elif method == "remove_pc":
                print("  Removing top principal component...")
                result = calibrator.remove_principal_components(result, n_components=1)

        # Show improvement
        before_iso = calibrator.isotropy_score(emb)
        after_iso = calibrator.isotropy_score(result)
        print(f"  Isotropy: {before_iso:.4f} -> {after_iso:.4f}")

        calibrated[name] = result

    return calibrated


def save_calibrated(calibrated: dict, output_dir: str, suffix: str = "_calibrated"):
    """Save calibrated embeddings."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for name, emb in calibrated.items():
        filename = name.lower().replace(" ", "_") + suffix + ".npy"
        np.save(out_dir / filename, emb)
        print(f"Saved: {out_dir / filename}")


def find_translation_outliers(embeddings: dict, german_key: str = None, top_n: int = 10):
    """Find passages where translations diverge most."""
    print("\n" + "=" * 60)
    print("TRANSLATION OUTLIER ANALYSIS")
    print("=" * 60)

    # Determine German source
    if german_key is None:
        # Try to find German embedding
        german_candidates = [k for k in embeddings if "german" in k.lower() or "original" in k.lower()]
        if not german_candidates:
            print("No German source found. Skipping outlier analysis.")
            return None
        german_key = german_candidates[0]

    german_emb = embeddings[german_key]
    translation_embs = {k: v for k, v in embeddings.items() if k != german_key}

    if not translation_embs:
        print("No translations found. Skipping outlier analysis.")
        return None

    anchor = ContrastiveAnchor(german_emb, translation_embs)

    # Find outliers
    outliers = []
    for idx in range(len(german_emb)):
        triangulation = anchor.triangulate_meaning(idx)
        similarities = list(triangulation.values())
        spread = max(similarities) - min(similarities)
        outliers.append((idx, spread, triangulation))

    outliers.sort(key=lambda x: -x[1])

    print(f"\nTop {top_n} passages with most translation disagreement:")
    for idx, spread, tri in outliers[:top_n]:
        print(f"\n  Aphorism index {idx} (spread: {spread:.4f}):")
        for trans, sim in sorted(tri.items(), key=lambda x: -x[1]):
            print(f"    {trans}: {sim:.4f}")

    return outliers[:top_n]


def generate_calibrated_embeddings(corpus_dir: str = "corpus/aligned",
                                    output_dir: str = "outputs/embeddings"):
    """Generate new embeddings with calibration applied."""
    print("=" * 60)
    print("GENERATING CALIBRATED EMBEDDINGS")
    print("=" * 60)

    # Load corpus
    corpus = load_aligned_corpus(corpus_dir)
    print(f"Loaded {len(corpus)} translations")

    # Align aphorisms
    aligned = align_aphorisms(corpus)
    print(f"Aligned {len(aligned)} aphorisms")

    if len(aligned) < 10:
        print("Too few aligned aphorisms. Check extraction.")
        return

    # Initialize components
    embedder = Embedder(mode="fast")
    prompter = PhilosophicalPromptEngineer()
    calibrator = EmbeddingCalibrator()

    aphorism_nums = sorted(aligned.keys())
    embeddings = {}
    calibrated = {}

    for name in corpus.keys():
        texts = [aligned[n].get(name, "") for n in aphorism_nums]
        texts = [t if t else "[MISSING]" for t in texts]

        # Determine language for prompting
        is_german = "german" in name.lower() or "original" in name.lower()
        language = "german" if is_german else "english"

        # Apply prompting
        prompted_texts = [
            prompter.apply_prompt(t, style="context_prefix", language=language)
            for t in texts
        ]

        print(f"\nEmbedding {name}...")
        raw_emb = embedder.embed(prompted_texts)
        embeddings[name] = raw_emb

        # Calibrate
        print(f"Calibrating {name}...")
        cal_emb = calibrator.whiten(raw_emb)

        # Check if we need PC removal
        diagnosis = diagnose_embedding_quality(cal_emb)
        if diagnosis['isotropy_score'] < 0.1:
            cal_emb = calibrator.remove_principal_components(cal_emb, 1)

        calibrated[name] = cal_emb

    # Save
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Save raw embeddings
    for name, emb in embeddings.items():
        filename = name.lower().replace(" ", "_") + ".npy"
        np.save(out_dir / filename, emb)

    # Save calibrated embeddings
    for name, emb in calibrated.items():
        filename = name.lower().replace(" ", "_") + "_calibrated.npy"
        np.save(out_dir / filename, emb)

    # Save index
    with open(out_dir / "index.json", "w") as f:
        json.dump({
            "aphorism_numbers": aphorism_nums,
            "translators": list(corpus.keys()),
            "calibration_methods": ["whiten", "remove_pc_if_needed"]
        }, f, indent=2)

    print(f"\nSaved to {out_dir}")
    print("  - Raw embeddings: *.npy")
    print("  - Calibrated embeddings: *_calibrated.npy")


def main():
    parser = argparse.ArgumentParser(
        description="Calibrate embeddings for philosophical analysis"
    )

    parser.add_argument(
        "--input", "-i",
        help="Directory containing existing embeddings"
    )

    parser.add_argument(
        "--output", "-o",
        default="outputs/embeddings",
        help="Output directory"
    )

    parser.add_argument(
        "--diagnose", "-d",
        nargs="?",
        const="outputs/embeddings",
        help="Run diagnostics only (optionally specify directory)"
    )

    parser.add_argument(
        "--generate", "-g",
        action="store_true",
        help="Generate new calibrated embeddings from corpus"
    )

    parser.add_argument(
        "--outliers", "-l",
        action="store_true",
        help="Find translation outliers"
    )

    parser.add_argument(
        "--methods", "-m",
        nargs="+",
        default=["whiten", "remove_pc"],
        choices=["whiten", "remove_pc", "both"],
        help="Calibration methods to apply"
    )

    args = parser.parse_args()

    if args.generate:
        generate_calibrated_embeddings(output_dir=args.output)
        return

    if args.diagnose:
        embeddings, _ = load_embeddings(args.diagnose)
        if embeddings:
            diagnose_all(embeddings)
        else:
            print(f"No embeddings found in {args.diagnose}")
        return

    if args.input:
        embeddings, index = load_embeddings(args.input)

        if not embeddings:
            print(f"No embeddings found in {args.input}")
            return

        # Diagnose
        diagnose_all(embeddings)

        # Calibrate
        calibrated = calibrate_all(embeddings, args.methods)

        # Find outliers if requested
        if args.outliers:
            find_translation_outliers(calibrated)

        # Save
        save_calibrated(calibrated, args.output)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
