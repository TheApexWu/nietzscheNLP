#!/usr/bin/env python3
"""
Full corpus LLM-as-Judge analysis for Nietzsche translations.
Evaluates all 231 aphorisms across 5 English translations + German original.
"""

import json
import os
import time
from pathlib import Path
from anthropic import Anthropic

# Configuration
CORPUS_DIR = Path('corpus/aligned')
OUTPUT_DIR = Path('llm_judge/full_analysis')
CHECKPOINT_FILE = OUTPUT_DIR / 'checkpoint.json'
BATCH_SIZE = 10
MODEL = "claude-sonnet-4-20250514"  # Use Sonnet for cost efficiency

# Evaluation prompt template
EVAL_PROMPT = """You are an expert in Nietzsche scholarship and translation studies. Analyze how the following aphorism from "Beyond Good and Evil" has been translated by different translators.

## German Original (Nietzsche)
{german}

## English Translations
{translations}

## Task
Evaluate each English translation on these dimensions (1-10 scale):

1. **Philosophical Fidelity**: Does it preserve Nietzsche's conceptual meaning?
2. **Tonal Preservation**: Does it capture Nietzsche's voice—ironic, aphoristic, provocative?
3. **Interpretive Liberty**: How much did the translator impose their own interpretation? (1=very literal, 10=heavily interpreted)
4. **Semantic Divergence**: How different is this from the other translations? (1=consensus, 10=outlier)

Pay special attention to:
- Key philosophical terms (Wille zur Macht, vornehm, Rangordnung, etc.)
- Grammatical choices that affect meaning (articles, singular/plural, noun vs verb)
- Register shifts (formal vs colloquial, technical vs everyday)

## Output Format
Return ONLY valid JSON (no markdown, no explanation outside JSON):
{{
  "aphorism": {aphorism_num},
  "translations": [
    {{
      "translator": "Name",
      "scores": {{
        "philosophical_fidelity": X,
        "tonal_preservation": X,
        "interpretive_liberty": X,
        "semantic_divergence": X
      }},
      "flagged_terms": ["term1", "term2"],
      "brief_note": "One sentence on key translation choice"
    }}
  ],
  "ranking": ["Best", "Second", ...],
  "critical_issue": "One sentence on most significant divergence across translations"
}}"""


def load_corpus():
    """Load all translations."""
    corpus = {}
    for path in CORPUS_DIR.glob('*.json'):
        with open(path) as f:
            data = json.load(f)
            corpus[data['name']] = {a['number']: a['text'] for a in data['aphorisms']}
    return corpus


def get_common_aphorisms(corpus):
    """Find aphorisms present in all translations."""
    all_nums = [set(t.keys()) for t in corpus.values()]
    return sorted(set.intersection(*all_nums))


def format_translations(corpus, aph_num):
    """Format translations for the prompt."""
    lines = []
    for name in ['Walter Kaufman', 'RJ Hollingdale', 'Helen Zimmern', 'Marion Faber', 'Judith Norman']:
        text = corpus.get(name, {}).get(aph_num, '')
        if text:
            # Truncate very long texts
            if len(text) > 2000:
                text = text[:2000] + "... [truncated]"
            lines.append(f"### {name}\n{text}\n")
    return "\n".join(lines)


def analyze_aphorism(client, corpus, aph_num):
    """Analyze a single aphorism using Claude."""
    german = corpus.get('Gutenberg', {}).get(aph_num, '')
    if not german:
        return None

    # Truncate German if needed
    if len(german) > 1500:
        german = german[:1500] + "... [truncated]"

    translations = format_translations(corpus, aph_num)

    prompt = EVAL_PROMPT.format(
        german=german,
        translations=translations,
        aphorism_num=aph_num
    )

    try:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}]
        )

        # Extract JSON from response
        text = response.text if hasattr(response, 'text') else response.content[0].text

        # Try to parse JSON
        # Handle potential markdown code blocks
        if '```json' in text:
            text = text.split('```json')[1].split('```')[0]
        elif '```' in text:
            text = text.split('```')[1].split('```')[0]

        result = json.loads(text.strip())
        result['aphorism'] = aph_num  # Ensure correct aphorism number
        return result

    except json.JSONDecodeError as e:
        print(f"  JSON parse error for §{aph_num}: {e}")
        return {"aphorism": aph_num, "error": "json_parse_error", "raw": text[:500]}
    except Exception as e:
        print(f"  API error for §{aph_num}: {e}")
        return {"aphorism": aph_num, "error": str(e)}


def load_checkpoint():
    """Load progress checkpoint."""
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return {"completed": [], "results": []}


def save_checkpoint(checkpoint):
    """Save progress checkpoint."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(CHECKPOINT_FILE, 'w') as f:
        json.dump(checkpoint, f, indent=2)


def main():
    # Check for API key
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set")
        print("Run: export ANTHROPIC_API_KEY='your-key-here'")
        return

    client = Anthropic(api_key=api_key)

    # Load corpus
    print("Loading corpus...")
    corpus = load_corpus()
    aphorisms = get_common_aphorisms(corpus)
    print(f"Found {len(aphorisms)} common aphorisms")

    # Load checkpoint
    checkpoint = load_checkpoint()
    completed = set(checkpoint['completed'])
    results = checkpoint['results']

    # Filter to remaining aphorisms
    remaining = [a for a in aphorisms if a not in completed]
    print(f"Already completed: {len(completed)}, Remaining: {len(remaining)}")

    if not remaining:
        print("All aphorisms already analyzed!")
        return

    # Process in batches
    total_cost = 0
    for i, aph_num in enumerate(remaining):
        print(f"[{i+1}/{len(remaining)}] Analyzing §{aph_num}...", end=" ")

        result = analyze_aphorism(client, corpus, aph_num)

        if result:
            results.append(result)
            completed.add(aph_num)

            if 'error' in result:
                print(f"ERROR: {result['error']}")
            else:
                ranking = result.get('ranking', [])
                print(f"OK - Top: {ranking[0] if ranking else 'N/A'}")

        # Save checkpoint every BATCH_SIZE aphorisms
        if (i + 1) % BATCH_SIZE == 0:
            checkpoint = {"completed": list(completed), "results": results}
            save_checkpoint(checkpoint)
            print(f"  [Checkpoint saved: {len(completed)} completed]")

        # Rate limiting
        time.sleep(0.5)

    # Final save
    checkpoint = {"completed": list(completed), "results": results}
    save_checkpoint(checkpoint)

    # Save final results
    final_output = OUTPUT_DIR / 'all_analyses.json'
    with open(final_output, 'w') as f:
        json.dump({
            "total_analyzed": len(results),
            "model": MODEL,
            "analyses": sorted(results, key=lambda x: x.get('aphorism', 0))
        }, f, indent=2)

    print(f"\n{'='*60}")
    print(f"COMPLETE: Analyzed {len(results)} aphorisms")
    print(f"Results saved to: {final_output}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
