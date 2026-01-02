'use client'

import { useState } from 'react'

// §28 quotes - all 6 translations verified
const QUOTES = {
  german: {
    translator: "Nietzsche (German)",
    year: 1886,
    text: `Was sich am schlechtesten aus einer Sprache in die andere übersetzen lässt, ist das Tempo ihres Stils: als welcher im Charakter der Rasse seinen Grund hat, physiologisch gesprochen, im Durchschnitts-Tempo ihres „Stoffwechsels". Es giebt ehrlich gemeinte Übersetzungen, die beinahe Fälschungen sind, als unfreiwillige Vergemeinerungen des Originals, bloss weil sein tapferes und lustiges Tempo nicht mit übersetzt werden konnte, welches über alles Gefährliche in Dingen und Worten wegspringt, weghilft.`,
    note: null
  },
  zimmern: {
    translator: "Helen Zimmern",
    year: 1906,
    text: `What is most difficult to render from one language into another is the tempo of its style, which has its basis in the character of the race, or to speak more physiologically, in the average tempo of the assimilation of its nutriment. There are honestly meant translations, which, as involuntary vulgarisations, are almost falsifications of the original, merely because its lively and merry tempo (which overleaps and obviates all dangers in word and expression) could not also be rendered.`,
    note: "First English translation, Victorian era"
  },
  kaufmann: {
    translator: "Walter Kaufmann",
    year: 1966,
    text: `What is most difficult to render from one language into another is the tempo of its style, which has its basis in the character of the race, or to speak more physiologically, in the average tempo of its metabolism. There are honestly meant translations that, as involuntary vulgarizations, are almost falsifications of the original, merely because its bold and merry tempo (which leaps over and obviates all dangers in things and words) could not be translated.`,
    note: "Academic standard for 50 years"
  },
  hollingdale: {
    translator: "R.J. Hollingdale",
    year: 1973,
    text: `That which translates worst from one language into another is the tempo of its style, which has its origin in the character of the race, or, expressed more physiologically, in the average tempo of its 'metabolism'. There are honestly meant translations which, as involuntary vulgarizations of the original, are almost falsifications simply because it was not possible to translate also its brave and happy tempo, which leaps over and puts behind it all that is perilous in things and words.`,
    note: "Semantic centroid (0.806 fidelity to German)"
  },
  faber: {
    translator: "Marion Faber",
    year: 1998,
    text: `The hardest thing to translate from one language to another is the tempo of its style; this style has its basis in the character of the race, or to speak more physiologically, in the average tempo of the race's 'metabolism'. There are some well-intended translations that are almost counterfeits, involuntary crudifications of the original, simply because they could not capture its bright, brave tempo, one that leaps over, transports over all the dangers in words and things.`,
    note: "Oxford World's Classics"
  },
  norman: {
    translator: "Judith Norman",
    year: 2002,
    text: `The hardest thing to translate from one language into another is the tempo of its style, which is grounded in the character of the race, or — to be more physiological — in the average tempo of its metabolism. There are well-meaning interpretations that are practically falsifications; they involuntarily debase the original, simply because it has a tempo that cannot be translated — a tempo that is brave and cheerful and leaps over and out of every danger in things and in words.`,
    note: "Cambridge edition, most modern"
  }
}

export default function QuoteComparison() {
  const [selectedQuote, setSelectedQuote] = useState('german')
  const [showAll, setShowAll] = useState(false)

  const quote = QUOTES[selectedQuote]

  if (showAll) {
    return (
      <div className="quote-comparison">
        <div className="comparison-header">
          <h3>§28: On the Untranslatable</h3>
          <button className="toggle-view" onClick={() => setShowAll(false)}>
            Show selector view
          </button>
        </div>

        <div className="all-quotes">
          {Object.entries(QUOTES).map(([key, q]) => (
            <div key={key} className={`quote-card ${key === 'german' ? 'german' : ''}`}>
              <div className="quote-meta">
                <span className="translator-name">{q.translator}</span>
                <span className="year">{q.year}</span>
              </div>
              <blockquote>{q.text}</blockquote>
              {q.note && <p className="quote-note">{q.note}</p>}
            </div>
          ))}
        </div>

        <style jsx>{styles}</style>
      </div>
    )
  }

  return (
    <div className="quote-comparison">
      <div className="comparison-header">
        <h3>§28: On the Untranslatable</h3>
        <button className="toggle-view" onClick={() => setShowAll(true)}>
          Show all side-by-side
        </button>
      </div>

      <div className="selector-row">
        {Object.entries(QUOTES).map(([key, q]) => (
          <button
            key={key}
            className={`selector-btn ${selectedQuote === key ? 'active' : ''} ${key === 'german' ? 'german' : ''}`}
            onClick={() => setSelectedQuote(key)}
          >
            <span className="btn-name">{q.translator.split(' ').pop()}</span>
            <span className="btn-year">{q.year}</span>
          </button>
        ))}
      </div>

      <div className="quote-display">
        <div className="quote-meta">
          <span className="translator-name">{quote.translator}</span>
          <span className="year">{quote.year}</span>
        </div>
        <blockquote>{quote.text}</blockquote>
        {quote.note && <p className="quote-note">{quote.note}</p>}
      </div>

      <p className="comparison-caption">
        Notice how each translator handles "Tempo" and "metabolism" differently.
        Hollingdale's "brave and happy" vs Kaufmann's "bold and merry" vs Faber's "bright, brave" —
        small choices that compound across 296 aphorisms.
      </p>

      <style jsx>{styles}</style>
    </div>
  )
}

const styles = `
  .quote-comparison {
    margin: 2rem 0;
  }

  .comparison-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  .comparison-header h3 {
    font-size: 1.25rem;
    color: var(--deep-wine, #722f37);
    margin: 0;
  }

  .toggle-view {
    font-family: var(--font-jetbrains), monospace;
    font-size: 0.75rem;
    color: var(--terra-cotta, #c9784a);
    background: transparent;
    border: 1px solid var(--terra-cotta, #c9784a);
    padding: 0.4rem 0.8rem;
    border-radius: 3px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .toggle-view:hover {
    background: var(--terra-cotta, #c9784a);
    color: white;
  }

  .selector-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin-bottom: 1.5rem;
  }

  .selector-btn {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0.6rem 1rem;
    background: var(--warm-cream, #fdf6e3);
    border: 1px solid var(--border-warm, #e6d5b8);
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .selector-btn:hover {
    border-color: var(--terra-cotta, #c9784a);
  }

  .selector-btn.active {
    background: var(--terra-cotta, #c9784a);
    border-color: var(--terra-cotta, #c9784a);
    color: white;
  }

  .selector-btn.german {
    border-color: var(--deep-wine, #722f37);
  }

  .selector-btn.german.active {
    background: var(--deep-wine, #722f37);
    border-color: var(--deep-wine, #722f37);
  }

  .btn-name {
    font-family: var(--font-jetbrains), monospace;
    font-size: 0.8rem;
    font-weight: 600;
  }

  .btn-year {
    font-size: 0.7rem;
    opacity: 0.7;
  }

  .quote-display {
    background: var(--warm-cream, #fdf6e3);
    border-left: 3px solid var(--sun-gold, #f4a623);
    padding: 1.5rem;
    border-radius: 0 8px 8px 0;
  }

  .quote-meta {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1rem;
  }

  .translator-name {
    font-family: var(--font-jetbrains), monospace;
    font-size: 0.85rem;
    color: var(--deep-wine, #722f37);
    font-weight: 600;
  }

  .year {
    font-family: var(--font-jetbrains), monospace;
    font-size: 0.8rem;
    color: var(--text-light, #8b7355);
  }

  .quote-display blockquote {
    font-size: 1rem;
    line-height: 1.8;
    color: var(--text-mid, #5c4a37);
    margin: 0;
    font-style: italic;
  }

  .quote-note {
    font-size: 0.8rem;
    color: var(--terra-cotta, #c9784a);
    margin: 1rem 0 0;
    font-style: normal;
  }

  .comparison-caption {
    font-size: 0.9rem;
    color: var(--text-light, #8b7355);
    margin-top: 1.5rem;
    line-height: 1.6;
  }

  /* All quotes view */
  .all-quotes {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .quote-card {
    background: var(--warm-cream, #fdf6e3);
    border-left: 3px solid var(--sun-gold, #f4a623);
    padding: 1.25rem;
    border-radius: 0 8px 8px 0;
  }

  .quote-card.german {
    border-left-color: var(--deep-wine, #722f37);
    background: linear-gradient(135deg, var(--sun-light, #ffeaa7) 0%, var(--warm-cream, #fdf6e3) 100%);
  }

  .quote-card blockquote {
    font-size: 0.95rem;
    line-height: 1.75;
    color: var(--text-mid, #5c4a37);
    margin: 0;
    font-style: italic;
  }

  .extraction-note {
    background: var(--warm-white, #fffef9);
    border: 1px dashed var(--border-warm, #e6d5b8);
    padding: 1.25rem;
    border-radius: 8px;
    margin-top: 1rem;
  }

  .extraction-note h4 {
    font-size: 0.85rem;
    color: var(--text-mid, #5c4a37);
    margin: 0 0 0.75rem;
  }

  .extraction-note p {
    font-size: 0.85rem;
    color: var(--text-light, #8b7355);
    margin: 0 0 0.5rem;
  }

  .extraction-note ul {
    margin: 0.5rem 0;
    padding-left: 1.25rem;
    font-size: 0.85rem;
    color: var(--text-light, #8b7355);
  }

  .honest-note {
    font-style: italic;
    margin-top: 0.75rem !important;
  }

  @media (max-width: 600px) {
    .selector-row {
      justify-content: center;
    }

    .selector-btn {
      padding: 0.5rem 0.75rem;
    }
  }
`
