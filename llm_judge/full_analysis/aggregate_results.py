#!/usr/bin/env python3
"""
Aggregate LLM-as-Judge batch results into summary statistics.
"""

import json
from pathlib import Path
from collections import defaultdict

def load_batch(filepath):
    """Load a batch file and normalize its format."""
    with open(filepath) as f:
        data = json.load(f)

    analyses = data.get('analyses', [])
    results = []

    for a in analyses:
        # Normalize different formats
        aph_num = a.get('aphorism') or a.get('aphorism_number')

        # Get scores - handle different naming conventions
        scores = a.get('scores') or a.get('translations') or a.get('translator_scores') or a.get('translators')
        if not scores:
            continue

        # Normalize translator names
        normalized = {}
        for name, score_data in scores.items():
            # Handle both "Walter Kaufman" and "Kaufmann" variants
            if 'Kaufman' in name or name == 'Kaufmann':
                key = 'Kaufmann'
            elif 'Hollingdale' in name:
                key = 'Hollingdale'
            elif 'Zimmern' in name:
                key = 'Zimmern'
            elif 'Faber' in name:
                key = 'Faber'
            elif 'Norman' in name:
                key = 'Norman'
            else:
                key = name
            normalized[key] = score_data

        results.append({
            'aphorism': aph_num,
            'scores': normalized,
            'ranking': a.get('ranking', []),
            'key_issue': a.get('key_issue', '')
        })

    return results

def calculate_statistics(all_analyses):
    """Calculate aggregate statistics across all translators."""
    translator_scores = defaultdict(lambda: {
        'philosophical_fidelity': [],
        'tonal_preservation': [],
        'interpretive_liberty': [],
        'top_rankings': 0,
        'total_ranked': 0
    })

    for analysis in all_analyses:
        scores = analysis.get('scores', {})
        ranking = analysis.get('ranking', [])

        for translator, score_data in scores.items():
            # Extract scores - handle nested 'scores' key
            if isinstance(score_data, dict):
                if 'scores' in score_data:
                    score_data = score_data['scores']

                pf = score_data.get('philosophical_fidelity')
                tp = score_data.get('tonal_preservation')
                il = score_data.get('interpretive_liberty')

                if pf is not None and pf > 0:  # Skip corrupted entries (score of 2 or less often indicates corpus issues)
                    translator_scores[translator]['philosophical_fidelity'].append(pf)
                if tp is not None and tp > 0:
                    translator_scores[translator]['tonal_preservation'].append(tp)
                if il is not None:
                    translator_scores[translator]['interpretive_liberty'].append(il)

        # Count top rankings
        if ranking:
            # Normalize first ranked name
            first = ranking[0] if ranking else None
            if first:
                for key in translator_scores.keys():
                    if key in first or first in key:
                        translator_scores[key]['top_rankings'] += 1
                        break
            for t in translator_scores.keys():
                translator_scores[t]['total_ranked'] += 1

    return dict(translator_scores)

def main():
    batch_dir = Path(__file__).parent

    # Load all batches
    all_analyses = []
    for batch_file in sorted(batch_dir.glob('batch_*.json')):
        print(f"Loading {batch_file.name}...")
        analyses = load_batch(batch_file)
        all_analyses.extend(analyses)
        print(f"  -> {len(analyses)} aphorisms")

    print(f"\nTotal aphorisms analyzed: {len(all_analyses)}")

    # Calculate statistics
    stats = calculate_statistics(all_analyses)

    # Compute averages
    summary = {}
    for translator, data in stats.items():
        pf_scores = data['philosophical_fidelity']
        tp_scores = data['tonal_preservation']
        il_scores = data['interpretive_liberty']

        summary[translator] = {
            'philosophical_fidelity_avg': round(sum(pf_scores) / len(pf_scores), 2) if pf_scores else 0,
            'tonal_preservation_avg': round(sum(tp_scores) / len(tp_scores), 2) if tp_scores else 0,
            'interpretive_liberty_avg': round(sum(il_scores) / len(il_scores), 2) if il_scores else 0,
            'top_ranking_count': data['top_rankings'],
            'sample_size': len(pf_scores)
        }

    # Sort by philosophical fidelity
    sorted_translators = sorted(
        summary.items(),
        key=lambda x: x[1]['philosophical_fidelity_avg'],
        reverse=True
    )

    # Print results
    print("\n" + "="*70)
    print("LLM-AS-JUDGE AGGREGATED RESULTS")
    print("="*70)
    print(f"\nTotal aphorisms analyzed: {len(all_analyses)}")
    print("\nTranslator Rankings (by philosophical fidelity):\n")

    for rank, (translator, data) in enumerate(sorted_translators, 1):
        print(f"{rank}. {translator}")
        print(f"   Philosophical Fidelity: {data['philosophical_fidelity_avg']}/10")
        print(f"   Tonal Preservation:     {data['tonal_preservation_avg']}/10")
        print(f"   Interpretive Liberty:   {data['interpretive_liberty_avg']}/10 (lower = more literal)")
        print(f"   Top Rankings:           {data['top_ranking_count']}")
        print(f"   Sample Size:            {data['sample_size']} aphorisms")
        print()

    # Save results
    output = {
        'total_aphorisms': len(all_analyses),
        'translator_summary': dict(sorted_translators),
        'methodology': {
            'philosophical_fidelity': '1-10: Preserves Nietzsche\'s philosophical concepts',
            'tonal_preservation': '1-10: Captures ironic, provocative voice',
            'interpretive_liberty': '1-10: 1=literal, 10=heavily interpreted'
        }
    }

    output_file = batch_dir / 'AGGREGATED_SUMMARY.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    return output

if __name__ == '__main__':
    main()
