# Full Corpus LLM-as-Judge Analysis: Execution Plan

## Corpus Overview

| Translator | Aphorisms | Avg Chars | Language |
|------------|-----------|-----------|----------|
| Gutenberg (German) | 296 | 1,290 | de |
| Walter Kaufmann | 292 | 1,468 | en |
| RJ Hollingdale | 295 | 1,361 | en |
| Helen Zimmern | 252 | 1,372 | en |
| Marion Faber | 280 | 1,338 | en |
| Judith Norman | 275 | 835 | en |

**Common aphorisms (available in ALL translations): 231**

---

## Compute Estimates

### Token Count
| Component | Tokens |
|-----------|--------|
| Input per aphorism | ~2,435 |
| Output per aphorism | ~800 |
| **Total input** | 562,485 |
| **Total output** | 184,800 |
| **Grand total** | 747,285 |

### API Cost
| Model | Cost |
|-------|------|
| **Opus 4.5** | $22.30 |
| Sonnet 4 | $4.46 |
| Haiku | $0.37 |

**Recommendation:** Use **Sonnet** for production run (~$4.50). Reserve Opus for validation sample.

### Time Estimates
- Sequential: ~12 minutes
- Parallel (5 concurrent): ~2-3 minutes
- With rate limiting + retries: ~15-20 minutes

---

## Corpus Issues (Must Fix Before Full Run)

### Critical: OCR Errors (609 instances)
Primarily in **Judith Norman** and **Marion Faber** translations:
- `hfe` → `life` (most common)
- `behef` → `belief`
- `morahty` → `morality`
- `vomehm` → `vornehm` (German)

**Fix:** Run OCR correction script before analysis.

### Moderate: Truncation (114 instances)
Texts ending mid-sentence, likely from PDF extraction issues.
- Example: Aphorism 6 ends with "of"
- Example: Aphorism 13 ends with "The"

**Fix:** Re-extract from source PDFs or flag for manual review.

### Minor: Very Short Texts (26 instances)
Some aphorisms < 50 characters, likely incomplete.

**Fix:** Cross-reference with other translations to verify.

---

## Recommended Execution Strategy

### Phase 1: Corpus Cleanup
1. Run OCR correction: `sed` replacements for known patterns
2. Flag truncated texts for manual review
3. Validate aphorism count matches across translators

### Phase 2: Validation Run
1. Run on 20 aphorisms (evenly distributed)
2. Use Opus for highest quality
3. Manually validate output format
4. Estimate actual costs

### Phase 3: Production Run
1. Batch size: 10 aphorisms per request
2. Use Sonnet for cost efficiency
3. Checkpoint after each batch
4. Retry logic for API failures

### Phase 4: Post-Processing
1. Aggregate all JSON outputs
2. Compute agreement scores with embedding divergence
3. Identify aphorisms where methods disagree
4. Generate visualization comparing both methods

---

## Output Schema (per aphorism)

```json
{
  "passage_id": "BGE_XXX",
  "german_original": "...",
  "translations": [
    {
      "translator": "Kaufmann",
      "scores": {
        "philosophical_fidelity": 1-10,
        "tonal_preservation": 1-10,
        "interpretive_liberty": 1-10,
        "semantic_divergence": 1-10
      },
      "flagged_terms": ["term1", "term2"],
      "justification": "..."
    }
  ],
  "ranking": ["Kaufmann", "Hollingdale", ...],
  "embedding_divergence": 0.0XXX,
  "methods_agree": true/false
}
```

---

## Key Hypothesis to Test

From pilot analysis of 5 aphorisms:

| Aphorism | Embedding | LLM-Judge | Agreement |
|----------|-----------|-----------|-----------|
| 13 | HIGH (97%) | HIGH | YES |
| 257 | LOW (42%) | HIGH | **NO** |
| 259 | LOW (35%) | HIGH | **NO** |
| 260 | MEDIUM (87%) | HIGH | PARTIAL |
| 287 | LOW (39%) | HIGH | **NO** |

**Pilot agreement rate: 40%**

Full corpus analysis will determine if this pattern holds: embeddings systematically miss grammatical-philosophical divergence.
