'use client'

import { useState } from 'react'

export default function MethodologyButton() {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="methodology-wrapper">
      <button
        className="methodology-toggle"
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
      >
        <span className="toggle-icon">{isOpen ? '−' : '+'}</span>
        <span>Methodology & Tech Stack</span>
      </button>

      {isOpen && (
        <div className="methodology-content">
          <div className="method-section">
            <h4>Embedding Model</h4>
            <p>
              <code>multilingual-e5-large</code> from Sentence Transformers. 1024-dimensional
              vectors trained on multilingual web text. Maps German and English into the same
              semantic space, enabling cross-lingual similarity without parallel corpora.
            </p>
          </div>

          <div className="method-section">
            <h4>Corpus Alignment</h4>
            <p>
              231 aphorisms aligned across 6 sources (5 English translations + German original).
              Texts extracted from PDFs via regex on aphorism markers. Set intersection ensures
              only aphorisms present in all translations are compared.
            </p>
          </div>

          <div className="method-section">
            <h4>Orthography Normalization</h4>
            <p>
              95 substitution rules convert pre-1901 German spelling to modern orthography
              (giebt→gibt, Werth→Wert, seyn→sein, etc.). Improves embedding alignment by
              0.002-0.003 cosine similarity across all translator pairs.
            </p>
          </div>

          <div className="method-section">
            <h4>OCR Cleaning</h4>
            <p>
              Scanned PDFs (especially the 1906 Zimmern) contained recognition errors.
              Built a cleaning pipeline that fixed 1,335 aphorism instances. Example: French
              phrases like "il ne cherche le vrai" were corrupted to "sl ne cherche" in some
              sources, causing spurious divergence.
            </p>
          </div>

          <div className="method-section">
            <h4>Statistical Validation</h4>
            <p>
              Permutation test (10,000 iterations) with Benjamini-Hochberg FDR correction.
              Top divergent passages: §35 (French phrases), §59 (short), §83 (ambiguous).
              Divergence correlates with passage length (shorter = more ambiguous) and
              presence of foreign language phrases.
            </p>
          </div>

          <div className="method-section">
            <h4>Limitations</h4>
            <ul>
              <li>Embeddings trained on web text, not philosophy corpora</li>
              <li>No explicit handling of Nietzsche's embedded French phrases</li>
              <li>Cosine similarity captures semantic overlap, not philosophical fidelity</li>
              <li>I don't speak German—findings are relative patterns, not absolute judgments</li>
            </ul>
          </div>

          <div className="method-section">
            <h4>Source Code</h4>
            <p>
              Full pipeline available at{' '}
              <a href="https://github.com/TheApexWu/nietzcheNLP" target="_blank" rel="noopener noreferrer">
                github.com/TheApexWu/nietzcheNLP
              </a>
            </p>
          </div>
        </div>
      )}

      <style jsx>{`
        .methodology-wrapper {
          margin: 2rem 0;
        }

        .methodology-toggle {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          background: transparent;
          border: 1px solid var(--terra-cotta, #c9784a);
          color: var(--terra-cotta, #c9784a);
          padding: 0.75rem 1.25rem;
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.85rem;
          cursor: pointer;
          border-radius: 4px;
          transition: all 0.2s;
        }

        .methodology-toggle:hover {
          background: var(--terra-cotta, #c9784a);
          color: var(--warm-white, #fffef9);
        }

        .toggle-icon {
          font-size: 1.1rem;
          font-weight: 600;
          width: 1rem;
          text-align: center;
        }

        .methodology-content {
          margin-top: 1.5rem;
          padding: 1.5rem;
          background: var(--warm-cream, #fdf6e3);
          border: 1px solid var(--border-warm, #e6d5b8);
          border-radius: 8px;
        }

        .method-section {
          margin-bottom: 1.5rem;
        }

        .method-section:last-child {
          margin-bottom: 0;
        }

        .method-section h4 {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.8rem;
          text-transform: uppercase;
          letter-spacing: 0.1em;
          color: var(--deep-wine, #722f37);
          margin-bottom: 0.5rem;
        }

        .method-section p {
          font-size: 0.95rem;
          line-height: 1.7;
          color: var(--text-mid, #5c4a37);
          margin: 0;
        }

        .method-section code {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.85rem;
          background: var(--warm-white, #fffef9);
          padding: 0.15rem 0.4rem;
          border-radius: 3px;
          color: var(--terra-cotta, #c9784a);
        }

        .method-section ul {
          margin: 0;
          padding-left: 1.25rem;
          font-size: 0.95rem;
          line-height: 1.7;
          color: var(--text-mid, #5c4a37);
        }

        .method-section li {
          margin-bottom: 0.35rem;
        }

        .method-section a {
          color: var(--terra-cotta, #c9784a);
          text-decoration: none;
          border-bottom: 1px solid var(--terra-cotta, #c9784a);
        }

        .method-section a:hover {
          color: var(--deep-wine, #722f37);
          border-color: var(--deep-wine, #722f37);
        }
      `}</style>
    </div>
  )
}
