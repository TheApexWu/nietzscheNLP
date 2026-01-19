# LLM-as-Judge Analysis

Qualitative translation analysis using large language models as evaluators, complementing the quantitative embedding-based approaches elsewhere in this repository.

## Methodology

Based on the framework in `../LLM_JUDGE_PRIMER.md`:

**Hypothesis:** LLM-as-Judge may capture nuances that embeddings miss—philosophical fidelity, tonal preservation, interpretive choices—while giving finer-grained control over what "divergence" means.

## Evaluation Dimensions

| Dimension | Scale | Description |
|-----------|-------|-------------|
| Philosophical Fidelity | 1-10 | Does the translation preserve Nietzsche's conceptual meaning? |
| Tonal Preservation | 1-10 | Does it capture Nietzsche's voice—ironic, aphoristic, provocative? |
| Interpretive Liberty | 1-10 | How much did the translator impose their own interpretation? |
| Semantic Divergence | 1-10 | How different is this translation from the consensus of others? |

## What This Captures That Embeddings Miss

1. **Grammatical-philosophical divergence** — e.g., "will to power" vs. "the will to power" (article insertion changes identity claim to attribution)
2. **Register shifts** — "bethink" vs. "think twice" vs. "reflect"
3. **Verb intensity** — "discharge" vs. "release" vs. "vent"
4. **Conceptual reification** — capitalization of "Will to Power"

## Relationship to Computational Philology

This project sits at the intersection of:
- **Traditional Philology**: Close reading, translation comparison, semantic analysis
- **Computational Philology**: Embeddings, corpus statistics, algorithmic text analysis
- **LLM-as-Judge**: A third method—qualitative evaluation at scale, neither purely statistical nor purely humanistic

## Files

| File | Aphorism | Key Concept |
|------|----------|-------------|
| `BGE_013_analysis.json` | 13 | "Leben selbst ist Wille zur Macht" (Life is will to power) |
| `BGE_257_analysis.json` | 257 | "Pathos der Distanz" (Pathos of distance) |
| `BGE_259_analysis.json` | 259 | Life as exploitation, appropriation, overpowering |
| `BGE_260_analysis.json` | 260 | "Herren-Moral und Sklaven-Moral" (Master/slave morality) |
| `BGE_287_analysis.json` | 287 | "Was ist vornehm?" (What is noble?) |

## Key Findings

### Patterns of Divergence Invisible to Embeddings

1. **Article insertion** — "will to power" vs. "the will to power" (identity vs. attribution)
2. **Noun vs. gerund** — "appropriation" vs. "appropriating" (essence vs. activity)
3. **Singular vs. plural** — "master morality" vs. "master moralities" (ideal type vs. variations)
4. **Register shifts** — "pathos of distance" vs. "grand feeling of distance" (philosophical vs. colloquial)
5. **Verb vs. noun predication** — "has reverence for itself" vs. "reveres itself" (state vs. action)

## References

- Pieter Maes on LLM-as-Judge: https://pieterma.es/syntopic-reading-claude/
- Key insight: "a metric on embeddings gives a very precise calculation of a vague proxy"
