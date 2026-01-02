'use client'

import { useState, useEffect } from 'react'

export default function AphorismExplorer() {
  const [data, setData] = useState(null)
  const [selectedNum, setSelectedNum] = useState(28)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/explorer_data.json')
      .then(res => res.json())
      .then(d => {
        setData(d)
        setLoading(false)
      })
      .catch(err => {
        console.error('Failed to load explorer data:', err)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return <div className="explorer-loading">Loading aphorisms...</div>
  }

  if (!data) {
    return <div className="explorer-error">Failed to load data</div>
  }

  const aphorism = data.aphorisms.find(a => a.number === selectedNum)
  const translatorOrder = ['Gutenberg', 'RJ Hollingdale', 'Walter Kaufman', 'Marion Faber', 'Judith Norman', 'Helen Zimmern']

  return (
    <div className="aphorism-explorer">
      <div className="explorer-header">
        <h3>Aphorism Explorer</h3>
        <p className="explorer-subtitle">Compare translations side-by-side</p>
      </div>

      <div className="explorer-controls">
        <label htmlFor="aphorism-select">Select aphorism:</label>
        <select
          id="aphorism-select"
          value={selectedNum}
          onChange={(e) => setSelectedNum(Number(e.target.value))}
        >
          {data.aphorisms.map(a => (
            <option key={a.number} value={a.number}>
              §{a.number} {a.divergence > 0.2 ? '⚡' : ''} {a.divergence > 0.25 ? '⚡' : ''}
            </option>
          ))}
        </select>

        {aphorism && (
          <div className="divergence-badge">
            <span className="badge-label">Divergence:</span>
            <span className={`badge-value ${aphorism.divergence > 0.2 ? 'high' : ''}`}>
              σ = {aphorism.divergence.toFixed(3)}
            </span>
          </div>
        )}
      </div>

      {aphorism && (
        <div className="translations-grid">
          {translatorOrder.map(name => {
            const text = aphorism.translations[name]
            if (!text) return null

            const isGerman = name === 'Gutenberg'
            return (
              <div key={name} className={`translation-card ${isGerman ? 'german' : ''}`}>
                <div className="card-header">
                  <span className="translator-name">
                    {isGerman ? 'German Original' : name}
                  </span>
                  <span className="translator-year">
                    {name === 'Gutenberg' && '1886'}
                    {name === 'Helen Zimmern' && '1906'}
                    {name === 'Walter Kaufman' && '1966'}
                    {name === 'RJ Hollingdale' && '1973'}
                    {name === 'Marion Faber' && '1998'}
                    {name === 'Judith Norman' && '2002'}
                  </span>
                </div>
                <div className="card-text">{text}</div>
              </div>
            )
          })}
        </div>
      )}

      <p className="explorer-note">
        ⚡ = high divergence aphorism. First 50 aphorisms available.
        Full dataset on <a href="https://github.com/TheApexWu/nietzcheNLP" target="_blank" rel="noopener noreferrer">GitHub</a>.
      </p>

      <style jsx>{`
        .aphorism-explorer {
          margin: 2rem 0;
          padding: 1.5rem;
          background: var(--warm-cream, #fdf6e3);
          border-radius: 12px;
          border: 1px solid var(--border-warm, #e6d5b8);
        }

        .explorer-header {
          margin-bottom: 1.5rem;
        }

        .explorer-header h3 {
          font-size: 1.25rem;
          color: var(--deep-wine, #722f37);
          margin: 0 0 0.25rem;
        }

        .explorer-subtitle {
          font-size: 0.9rem;
          color: var(--text-light, #8b7355);
          margin: 0;
        }

        .explorer-controls {
          display: flex;
          align-items: center;
          gap: 1rem;
          flex-wrap: wrap;
          margin-bottom: 1.5rem;
        }

        .explorer-controls label {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.8rem;
          color: var(--text-mid, #5c4a37);
        }

        .explorer-controls select {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.9rem;
          padding: 0.5rem 1rem;
          border: 1px solid var(--border-warm, #e6d5b8);
          border-radius: 4px;
          background: var(--warm-white, #fffef9);
          color: var(--text-dark, #2d2418);
          cursor: pointer;
        }

        .explorer-controls select:focus {
          outline: none;
          border-color: var(--terra-cotta, #c9784a);
        }

        .divergence-badge {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          margin-left: auto;
        }

        .badge-label {
          font-size: 0.75rem;
          color: var(--text-light, #8b7355);
        }

        .badge-value {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.85rem;
          padding: 0.25rem 0.5rem;
          background: var(--warm-white, #fffef9);
          border-radius: 3px;
          color: var(--text-mid, #5c4a37);
        }

        .badge-value.high {
          background: var(--sun-light, #ffeaa7);
          color: var(--deep-wine, #722f37);
          font-weight: 600;
        }

        .translations-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 1rem;
        }

        .translation-card {
          background: var(--warm-white, #fffef9);
          border: 1px solid var(--border-warm, #e6d5b8);
          border-radius: 8px;
          padding: 1rem;
          transition: border-color 0.2s;
        }

        .translation-card:hover {
          border-color: var(--terra-cotta, #c9784a);
        }

        .translation-card.german {
          border-left: 3px solid var(--deep-wine, #722f37);
          background: linear-gradient(135deg, var(--sun-light, #ffeaa7) 0%, var(--warm-white, #fffef9) 100%);
        }

        .card-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.75rem;
          padding-bottom: 0.5rem;
          border-bottom: 1px solid var(--border-warm, #e6d5b8);
        }

        .translator-name {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.8rem;
          font-weight: 600;
          color: var(--deep-wine, #722f37);
        }

        .translator-year {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.75rem;
          color: var(--text-light, #8b7355);
        }

        .card-text {
          font-size: 0.9rem;
          line-height: 1.7;
          color: var(--text-mid, #5c4a37);
          max-height: 200px;
          overflow-y: auto;
        }

        .explorer-note {
          font-size: 0.8rem;
          color: var(--text-light, #8b7355);
          margin: 1.5rem 0 0;
          text-align: center;
        }

        .explorer-note a {
          color: var(--terra-cotta, #c9784a);
          text-decoration: none;
        }

        .explorer-note a:hover {
          text-decoration: underline;
        }

        .explorer-loading,
        .explorer-error {
          padding: 2rem;
          text-align: center;
          color: var(--text-light, #8b7355);
          font-style: italic;
        }

        @media (max-width: 768px) {
          .translations-grid {
            grid-template-columns: 1fr;
          }

          .explorer-controls {
            flex-direction: column;
            align-items: flex-start;
          }

          .divergence-badge {
            margin-left: 0;
          }
        }
      `}</style>
    </div>
  )
}
