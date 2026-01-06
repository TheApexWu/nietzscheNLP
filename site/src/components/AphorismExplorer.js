'use client'

import { useState, useEffect, useMemo } from 'react'

const TRANSLATOR_INFO = {
  'Gutenberg': { label: 'German Original', year: '1886' },
  'RJ Hollingdale': { label: 'RJ Hollingdale', year: '1973' },
  'Walter Kaufman': { label: 'Walter Kaufmann', year: '1966' },
  'Marion Faber': { label: 'Marion Faber', year: '1998' },
  'Judith Norman': { label: 'Judith Norman', year: '2002' },
  'Helen Zimmern': { label: 'Helen Zimmern', year: '1906' },
}

const TRANSLATOR_ORDER = ['Gutenberg', 'RJ Hollingdale', 'Walter Kaufman', 'Marion Faber', 'Judith Norman', 'Helen Zimmern']

export default function AphorismExplorer() {
  const [data, setData] = useState(null)
  const [selectedNum, setSelectedNum] = useState(38)
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [minDivergence, setMinDivergence] = useState(0)
  const [compareMode, setCompareMode] = useState(false)
  const [selectedTranslators, setSelectedTranslators] = useState(['Gutenberg', 'RJ Hollingdale'])

  // Read URL param on mount
  useEffect(() => {
    const params = new URLSearchParams(window.location.search)
    const aphorism = params.get('aphorism')
    if (aphorism) {
      setSelectedNum(Number(aphorism))
    }
  }, [])

  // Update URL when selection changes
  useEffect(() => {
    if (!loading && data) {
      const url = new URL(window.location)
      url.searchParams.set('aphorism', selectedNum)
      window.history.replaceState({}, '', url)
    }
  }, [selectedNum, loading, data])

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

  // Filter aphorisms by search and divergence
  const filteredAphorisms = useMemo(() => {
    if (!data) return []
    return data.aphorisms
      .filter(a => a.divergence >= minDivergence)
      .filter(a => {
        if (!searchQuery.trim()) return true
        const query = searchQuery.toLowerCase()
        return Object.values(a.translations).some(
          text => text && text.toLowerCase().includes(query)
        )
      })
      .sort((a, b) => a.number - b.number)
  }, [data, searchQuery, minDivergence])

  const handleSurpriseMe = () => {
    if (!data) return
    // Weight toward high divergence
    const highDivergence = data.aphorisms.filter(a => a.divergence > 0.15)
    const pool = highDivergence.length > 0 ? highDivergence : data.aphorisms
    const random = pool[Math.floor(Math.random() * pool.length)]
    setSelectedNum(random.number)
  }

  const toggleTranslator = (name) => {
    setSelectedTranslators(prev => {
      if (prev.includes(name)) {
        if (prev.length <= 2) return prev // Keep at least 2
        return prev.filter(t => t !== name)
      }
      return [...prev, name]
    })
  }

  const copyShareLink = () => {
    const url = `${window.location.origin}${window.location.pathname}?aphorism=${selectedNum}`
    navigator.clipboard.writeText(url)
  }

  if (loading) {
    return <div className="explorer-loading">Loading aphorisms...</div>
  }

  if (!data) {
    return <div className="explorer-error">Failed to load data</div>
  }

  const aphorism = data.aphorisms.find(a => a.number === selectedNum)
  const displayTranslators = compareMode ? selectedTranslators : TRANSLATOR_ORDER

  return (
    <div className="aphorism-explorer">
      <div className="explorer-header">
        <h3>Aphorism Explorer</h3>
        <p className="explorer-subtitle">Compare translations side-by-side</p>
      </div>

      {/* Search and Filter Row */}
      <div className="explorer-filters">
        <div className="search-box">
          <input
            type="text"
            placeholder="Search aphorisms..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
          />
        </div>
        <div className="divergence-filter">
          <label>Min divergence: {minDivergence.toFixed(2)}</label>
          <input
            type="range"
            min="0"
            max="0.3"
            step="0.02"
            value={minDivergence}
            onChange={(e) => setMinDivergence(Number(e.target.value))}
          />
        </div>
      </div>

      {/* Controls Row */}
      <div className="explorer-controls">
        <select
          id="aphorism-select"
          value={selectedNum}
          onChange={(e) => setSelectedNum(Number(e.target.value))}
        >
          {filteredAphorisms.map(a => (
            <option key={a.number} value={a.number}>
              §{a.number} {a.divergence > 0.2 ? '*' : ''}{a.divergence > 0.25 ? '*' : ''}
            </option>
          ))}
        </select>

        <button className="surprise-btn" onClick={handleSurpriseMe}>
          Surprise me
        </button>

        <button className="share-btn" onClick={copyShareLink} title="Copy link to this aphorism">
          Share §{selectedNum}
        </button>

        {aphorism && (
          <div className="divergence-badge">
            <span className="badge-label">Divergence:</span>
            <span className={`badge-value ${aphorism.divergence > 0.2 ? 'high' : ''}`}>
              σ = {aphorism.divergence.toFixed(3)}
            </span>
          </div>
        )}
      </div>

      {/* Compare Mode Toggle */}
      <div className="compare-mode">
        <label className="compare-toggle">
          <input
            type="checkbox"
            checked={compareMode}
            onChange={(e) => setCompareMode(e.target.checked)}
          />
          <span>Compare specific translators</span>
        </label>

        {compareMode && (
          <div className="translator-checkboxes">
            {TRANSLATOR_ORDER.map(name => (
              <label key={name} className="translator-checkbox">
                <input
                  type="checkbox"
                  checked={selectedTranslators.includes(name)}
                  onChange={() => toggleTranslator(name)}
                />
                <span>{TRANSLATOR_INFO[name].label}</span>
              </label>
            ))}
          </div>
        )}
      </div>

      {/* Translations Grid */}
      {aphorism && (
        <div className={`translations-grid ${compareMode ? 'compare-mode' : ''}`}>
          {displayTranslators.map(name => {
            const text = aphorism.translations[name]
            if (!text) return null

            const isGerman = name === 'Gutenberg'
            const info = TRANSLATOR_INFO[name]
            return (
              <div key={name} className={`translation-card ${isGerman ? 'german' : ''}`}>
                <div className="card-header">
                  <span className="translator-name">{info.label}</span>
                  <span className="translator-year">{info.year}</span>
                </div>
                <div className="card-text">{text}</div>
              </div>
            )
          })}
        </div>
      )}

      {filteredAphorisms.length === 0 && (
        <p className="no-results">No aphorisms match your filters.</p>
      )}

      <p className="explorer-note">
        Top 25 most divergent aphorisms. * = high, ** = very high.
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

        /* Search and Filter */
        .explorer-filters {
          display: flex;
          gap: 1.5rem;
          margin-bottom: 1rem;
          flex-wrap: wrap;
        }

        .search-box input {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.85rem;
          padding: 0.5rem 0.75rem;
          border: 1px solid var(--border-warm, #e6d5b8);
          border-radius: 4px;
          background: var(--warm-white, #fffef9);
          color: var(--text-dark, #2d2418);
          width: 200px;
        }

        .search-box input:focus {
          outline: none;
          border-color: var(--terra-cotta, #c9784a);
        }

        .divergence-filter {
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        .divergence-filter label {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.75rem;
          color: var(--text-mid, #5c4a37);
          min-width: 120px;
        }

        .divergence-filter input[type="range"] {
          width: 100px;
          accent-color: var(--terra-cotta, #c9784a);
        }

        /* Controls */
        .explorer-controls {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          flex-wrap: wrap;
          margin-bottom: 1rem;
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

        .surprise-btn, .share-btn {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.8rem;
          padding: 0.5rem 0.75rem;
          border: 1px solid var(--border-warm, #e6d5b8);
          border-radius: 4px;
          background: var(--warm-white, #fffef9);
          color: var(--text-mid, #5c4a37);
          cursor: pointer;
          transition: all 0.2s;
        }

        .surprise-btn:hover, .share-btn:hover {
          background: var(--terra-cotta, #c9784a);
          color: var(--warm-white, #fffef9);
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

        /* Compare Mode */
        .compare-mode {
          margin-bottom: 1rem;
          padding: 0.75rem;
          background: var(--warm-white, #fffef9);
          border-radius: 6px;
          border: 1px solid var(--border-warm, #e6d5b8);
        }

        .compare-toggle {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.85rem;
          color: var(--text-mid, #5c4a37);
          cursor: pointer;
        }

        .compare-toggle input {
          accent-color: var(--terra-cotta, #c9784a);
        }

        .translator-checkboxes {
          display: flex;
          flex-wrap: wrap;
          gap: 0.75rem;
          margin-top: 0.75rem;
          padding-top: 0.75rem;
          border-top: 1px solid var(--border-warm, #e6d5b8);
        }

        .translator-checkbox {
          display: flex;
          align-items: center;
          gap: 0.35rem;
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.75rem;
          color: var(--text-mid, #5c4a37);
          cursor: pointer;
        }

        .translator-checkbox input {
          accent-color: var(--terra-cotta, #c9784a);
        }

        /* Translations Grid */
        .translations-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 1rem;
        }

        .translations-grid.compare-mode {
          grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
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

        .no-results {
          text-align: center;
          color: var(--text-light, #8b7355);
          font-style: italic;
          padding: 2rem;
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

          .explorer-filters {
            flex-direction: column;
            gap: 1rem;
          }

          .search-box input {
            width: 100%;
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
