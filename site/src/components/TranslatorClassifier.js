'use client'

import { useState } from 'react'

// Pre-computed translator style signatures based on common word choices
// These are simplified heuristics based on observed translation patterns
const STYLE_MARKERS = {
  zimmern: {
    patterns: ['hath', 'doth', 'whilst', 'wherefore', 'thereunto', 'viz.', '-isation'],
    words: ['one must', 'it is necessary', 'necessarily'],
    weight: 1.0
  },
  kaufmann: {
    patterns: ['indeed', 'precisely', 'essentially', 'fundamentally'],
    words: ['in fact', 'to be sure', 'as it were'],
    weight: 1.0
  },
  hollingdale: {
    patterns: ['what is more', 'on the other hand', 'that is to say'],
    words: ['perilous', 'hitherto', 'moreover'],
    weight: 1.0
  },
  faber: {
    patterns: ['in other words', 'that is', 'i.e.'],
    words: ['counterfeits', 'crudifications', 'bright'],
    weight: 1.0
  },
  norman: {
    patterns: ['in short', 'at any rate', 'after all'],
    words: ['debase', 'cheerful', 'grounded'],
    weight: 1.0
  }
}

function classifyText(text) {
  const lowerText = text.toLowerCase()
  const scores = {}

  for (const [translator, markers] of Object.entries(STYLE_MARKERS)) {
    let score = 0

    // Check patterns
    for (const pattern of markers.patterns) {
      if (lowerText.includes(pattern.toLowerCase())) {
        score += 2
      }
    }

    // Check words
    for (const word of markers.words) {
      if (lowerText.includes(word.toLowerCase())) {
        score += 1
      }
    }

    scores[translator] = score * markers.weight
  }

  // Find max score
  const maxScore = Math.max(...Object.values(scores))
  if (maxScore === 0) {
    return { prediction: null, confidence: 0, scores }
  }

  const prediction = Object.entries(scores).find(([_, s]) => s === maxScore)[0]
  const totalScore = Object.values(scores).reduce((a, b) => a + b, 0)
  const confidence = totalScore > 0 ? (maxScore / totalScore) : 0

  return { prediction, confidence, scores }
}

const TRANSLATOR_NAMES = {
  zimmern: 'Helen Zimmern (1906)',
  kaufmann: 'Walter Kaufmann (1966)',
  hollingdale: 'R.J. Hollingdale (1973)',
  faber: 'Marion Faber (1998)',
  norman: 'Judith Norman (2002)'
}

export default function TranslatorClassifier() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)

  const handleClassify = () => {
    if (text.trim().length < 20) {
      setResult({ error: 'Please enter at least 20 characters' })
      return
    }
    const classification = classifyText(text)
    setResult(classification)
  }

  return (
    <div className="classifier">
      <div className="classifier-header">
        <h3>Translator Fingerprint Detector</h3>
        <p>Paste a passage and see if we can guess the translator</p>
      </div>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Paste a passage from Beyond Good and Evil..."
        rows={5}
      />

      <button onClick={handleClassify} disabled={text.trim().length < 20}>
        Analyze Style
      </button>

      {result && (
        <div className="result">
          {result.error ? (
            <p className="error">{result.error}</p>
          ) : result.prediction ? (
            <>
              <div className="prediction">
                <span className="label">Best guess:</span>
                <span className="translator">{TRANSLATOR_NAMES[result.prediction]}</span>
                <span className="confidence">
                  ({Math.round(result.confidence * 100)}% confidence)
                </span>
              </div>
              <div className="scores">
                <span className="scores-label">Style markers detected:</span>
                {Object.entries(result.scores)
                  .sort((a, b) => b[1] - a[1])
                  .map(([t, s]) => (
                    <div key={t} className="score-bar">
                      <span className="score-name">{t}</span>
                      <div className="bar-container">
                        <div
                          className="bar"
                          style={{ width: `${Math.min(s * 20, 100)}%` }}
                        />
                      </div>
                      <span className="score-val">{s}</span>
                    </div>
                  ))}
              </div>
            </>
          ) : (
            <p className="no-match">
              No strong style markers detected. Try a longer passage or one with
              distinctive phrasing.
            </p>
          )}
        </div>
      )}

      <p className="disclaimer">
        This is a simplified heuristic based on word choice patterns.
        The actual embedding-based classification uses 1024-dimensional vectors
        and achieves much higher accuracy.
      </p>

      <style jsx>{`
        .classifier {
          margin: 2rem 0;
          padding: 1.5rem;
          background: var(--warm-cream, #fdf6e3);
          border-radius: 12px;
          border: 1px solid var(--border-warm, #e6d5b8);
        }

        .classifier-header {
          margin-bottom: 1rem;
        }

        .classifier-header h3 {
          font-size: 1.15rem;
          color: var(--deep-wine, #722f37);
          margin: 0 0 0.25rem;
        }

        .classifier-header p {
          font-size: 0.9rem;
          color: var(--text-light, #8b7355);
          margin: 0;
        }

        textarea {
          width: 100%;
          padding: 1rem;
          border: 1px solid var(--border-warm, #e6d5b8);
          border-radius: 6px;
          font-family: inherit;
          font-size: 0.95rem;
          line-height: 1.6;
          resize: vertical;
          background: var(--warm-white, #fffef9);
          color: var(--text-dark, #2d2418);
        }

        textarea:focus {
          outline: none;
          border-color: var(--terra-cotta, #c9784a);
        }

        button {
          margin-top: 1rem;
          padding: 0.75rem 1.5rem;
          background: var(--terra-cotta, #c9784a);
          color: white;
          border: none;
          border-radius: 4px;
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.85rem;
          cursor: pointer;
          transition: background 0.2s;
        }

        button:hover:not(:disabled) {
          background: var(--deep-wine, #722f37);
        }

        button:disabled {
          opacity: 0.5;
          cursor: not-allowed;
        }

        .result {
          margin-top: 1.5rem;
          padding: 1rem;
          background: var(--warm-white, #fffef9);
          border-radius: 6px;
          border: 1px solid var(--border-warm, #e6d5b8);
        }

        .prediction {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          flex-wrap: wrap;
          margin-bottom: 1rem;
        }

        .label {
          font-size: 0.85rem;
          color: var(--text-light, #8b7355);
        }

        .translator {
          font-weight: 600;
          color: var(--deep-wine, #722f37);
        }

        .confidence {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.8rem;
          color: var(--terra-cotta, #c9784a);
        }

        .scores {
          margin-top: 1rem;
        }

        .scores-label {
          font-size: 0.8rem;
          color: var(--text-light, #8b7355);
          display: block;
          margin-bottom: 0.5rem;
        }

        .score-bar {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-bottom: 0.35rem;
        }

        .score-name {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.75rem;
          width: 80px;
          text-transform: capitalize;
        }

        .bar-container {
          flex: 1;
          height: 8px;
          background: var(--warm-cream, #fdf6e3);
          border-radius: 4px;
          overflow: hidden;
        }

        .bar {
          height: 100%;
          background: var(--sun-gold, #f4a623);
          border-radius: 4px;
          transition: width 0.3s;
        }

        .score-val {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.75rem;
          width: 20px;
          text-align: right;
          color: var(--text-light, #8b7355);
        }

        .error, .no-match {
          font-size: 0.9rem;
          color: var(--text-mid, #5c4a37);
          font-style: italic;
        }

        .disclaimer {
          font-size: 0.8rem;
          color: var(--text-light, #8b7355);
          margin-top: 1rem;
          font-style: italic;
        }
      `}</style>
    </div>
  )
}
