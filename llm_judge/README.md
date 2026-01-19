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

- `BGE_013_analysis.json` — Analysis of Aphorism 13 ("Leben selbst ist Wille zur Macht")

## References

- Pieter Maes on LLM-as-Judge: https://pieterma.es/syntopic-reading-claude/
- Key insight: "a metric on embeddings gives a very precise calculation of a vague proxy"
