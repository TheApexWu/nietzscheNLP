'use client'

// Key term divergence data - pre-computed
const TERM_DATA = [
  {
    german: 'Rangordnung',
    english: ['order of rank', 'hierarchy'],
    consistency: 24,
    note: 'Faber prefers "hierarchy"; others use "order of rank"'
  },
  {
    german: 'Geist',
    english: ['spirit', 'mind', 'intellect'],
    consistency: 35,
    note: 'Central concept with major philosophical implications depending on choice'
  },
  {
    german: 'das Gemeine',
    english: ['common', 'vulgar', 'base', 'low'],
    consistency: 51,
    note: 'The opposite of "noble" - translators disagree on how harsh to make it'
  },
  {
    german: 'Trieb',
    english: ['drive', 'instinct', 'impulse'],
    consistency: 58,
    note: '"Drive" is more Freudian; "instinct" is more biological'
  },
  {
    german: 'Wert',
    english: ['value', 'worth'],
    consistency: 59,
    note: 'Root of "Umwertung" (revaluation of all values)'
  },
  {
    german: 'das Vornehme',
    english: ['noble', 'aristocratic', 'distinguished'],
    consistency: 75,
    note: 'Most agree on "noble" but some prefer less loaded terms'
  },
  {
    german: 'Wille zur Macht',
    english: ['will to power'],
    consistency: 100,
    note: 'Universally rendered as "will to power" - too iconic to vary'
  }
]

export default function KeyTermAnalysis() {
  return (
    <div className="term-analysis">
      <h3>Key Term Divergence</h3>
      <p className="intro">
        Some philosophical terms are translated consistently; others aren't.
        "Geist" as "spirit" vs "mind" changes the philosophical weight.
      </p>

      <div className="term-grid">
        {TERM_DATA.map(term => (
          <div key={term.german} className="term-card">
            <div className="term-header">
              <span className="german">{term.german}</span>
              <span className={`consistency ${term.consistency < 50 ? 'low' : term.consistency < 80 ? 'mid' : 'high'}`}>
                {term.consistency}%
              </span>
            </div>
            <div className="translations">
              {term.english.map((eng, i) => (
                <span key={i} className="translation">{eng}</span>
              ))}
            </div>
            <p className="note">{term.note}</p>
          </div>
        ))}
      </div>

      <style jsx>{`
        .term-analysis {
          margin: 2rem 0;
        }

        .term-analysis h3 {
          font-size: 1.15rem;
          color: var(--deep-wine, #722f37);
          margin: 0 0 0.5rem;
        }

        .intro {
          font-size: 0.95rem;
          color: var(--text-mid, #5c4a37);
          margin-bottom: 1.5rem;
        }

        .term-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
          gap: 1rem;
        }

        .term-card {
          background: var(--warm-cream, #fdf6e3);
          border: 1px solid var(--border-warm, #e6d5b8);
          border-radius: 8px;
          padding: 1rem;
        }

        .term-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.75rem;
        }

        .german {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.95rem;
          font-weight: 600;
          color: var(--deep-wine, #722f37);
        }

        .consistency {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.8rem;
          padding: 0.2rem 0.5rem;
          border-radius: 3px;
        }

        .consistency.low {
          background: #ffeeba;
          color: #856404;
        }

        .consistency.mid {
          background: #d1ecf1;
          color: #0c5460;
        }

        .consistency.high {
          background: #d4edda;
          color: #155724;
        }

        .translations {
          display: flex;
          flex-wrap: wrap;
          gap: 0.4rem;
          margin-bottom: 0.75rem;
        }

        .translation {
          font-size: 0.8rem;
          padding: 0.2rem 0.5rem;
          background: var(--warm-white, #fffef9);
          border: 1px solid var(--border-warm, #e6d5b8);
          border-radius: 3px;
          color: var(--text-mid, #5c4a37);
        }

        .note {
          font-size: 0.8rem;
          color: var(--text-light, #8b7355);
          margin: 0;
          line-height: 1.5;
        }
      `}</style>
    </div>
  )
}
