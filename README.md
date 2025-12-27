# Nietzsche Translation Embedding Analysis

Computational analysis of translation divergence across English translations of Nietzsche's *Beyond Good and Evil*.

## Research Question

Can embedding models surface where translation loss occurs in philosophical texts? Do philosophically loaded terms (*Wille zur Macht*, *Übermensch*, *vornehm*) show more semantic scatter across translators than mundane passages?

## Translations Analyzed

| Translator | Year | Status |
|------------|------|--------|
| German Original | 1886 | Ground truth |
| Helen Zimmern | 1906 | Public domain |
| Walter Kaufmann | 1966 | Excerpts (fair use) |
| R.J. Hollingdale | 1973 | Excerpts (fair use) |

## Project Structure

```
/corpus/aligned/       # Aligned passage JSONs (safe to commit)
/src/                  # Analysis code
/notebooks/            # Exploration notebooks
/outputs/              # Visualizations, results
```

## Setup

```bash
pip install -r requirements.txt
```

## License

Code: MIT
Corpus: Not included (acquire translations independently)
