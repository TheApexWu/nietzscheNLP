'use client'

import dynamic from 'next/dynamic'

// Dynamic imports for chart components (client-side only)
const SimilarityChart = dynamic(() => import('../components/SimilarityChart'), { ssr: false })
const DivergenceChart = dynamic(() => import('../components/DivergenceChart'), { ssr: false })
const HeatmapChart = dynamic(() => import('../components/HeatmapChart'), { ssr: false })
const UMAPChart = dynamic(() => import('../components/UMAPChart'), { ssr: false })

export default function Home() {
  return (
    <div className="nietzsche-page">
      {/* Sun decoration */}
      <div className="sun-decor" />

      {/* Hero */}
      <header className="hero">
        <span className="hero-tag">Computational Philology</span>
        <h1>Beyond Good and Evil,<br /><em>Beyond Translation</em></h1>
        <p className="subtitle">
          An NLP exploration of five English translations of Nietzsche's masterwork —
          measuring what resists translation, and what the embeddings reveal about
          interpretive schools.
        </p>
      </header>

      {/* The Hook */}
      <section className="section">
        <div className="epigraph">
          <blockquote>
            "Was sich am schlechtesten aus einer Sprache in die andere übersetzen lässt,
            ist das <strong>tempo</strong> ihres Stils..."
          </blockquote>
          <cite>— BGE §28</cite>
          <p className="translation">
            "That which translates worst from one language into another is the <strong>tempo</strong> of its style..."
          </p>
        </div>

        <p className="lead">
          Nietzsche wrote that a language's rhythm — rooted in what he called the "average tempo of its metabolism" —
          is fundamentally untranslatable. Our sentence embeddings confirm: this very passage shows the
          second-highest divergence among all five translators.
        </p>

        <p>
          The philosopher predicted his own untranslatability. The math proves him right.
        </p>
      </section>

      {/* Stats Row */}
      <section className="stats">
        <div className="stat">
          <span className="stat-value">231</span>
          <span className="stat-label">Aphorisms Aligned</span>
        </div>
        <div className="stat">
          <span className="stat-value">5</span>
          <span className="stat-label">English Translators</span>
        </div>
        <div className="stat">
          <span className="stat-value">0.833</span>
          <span className="stat-label">Max Fidelity Score</span>
        </div>
      </section>

      {/* Key Finding */}
      <section className="section finding-highlight">
        <h2>The Semantic Centroid</h2>
        <p>
          When we computed pairwise cosine similarity across all translator embeddings, one name emerged
          as the gravitational center: <strong>R.J. Hollingdale</strong>.
        </p>

        <div className="data-card">
          <h3>Similarity to Original German</h3>
          <SimilarityChart />
        </div>

        <p>
          Hollingdale also shows the highest similarity to other translators — he's not just closest to the German,
          he's closest to everyone. This suggests a "faithful center" that other interpretations orbit around.
        </p>
      </section>

      {/* Visualization: UMAP */}
      <section className="section viz-section">
        <h2>The Translator Fingerprint</h2>
        <p>
          UMAP projection of 1,386 aphorism embeddings (231 aphorisms × 6 sources) reveals distinct clusters.
          Each translator leaves a semantic fingerprint — a consistent stylistic signature that embeddings detect.
        </p>
        <div className="viz-container">
          <UMAPChart />
        </div>
        <p className="viz-caption">
          The German (orange) sits at the center, with Kaufmann/Hollingdale clustering nearby.
          Norman and Zimmern show more stylistic drift.
        </p>
      </section>

      {/* Divergence Section */}
      <section className="section">
        <h2>Where Translators Diverge</h2>
        <p>
          Some passages are translated consistently; others scatter wildly. The variance tells us
          where interpretive freedom lives — or where Nietzsche is hardest to render.
        </p>

        <div className="divergence-list">
          <div className="divergence-item">
            <span className="section-num">§35</span>
            <span className="variance">σ = 0.305</span>
            <p>Voltaire, truth-seeking, embedded French phrases</p>
          </div>
          <div className="divergence-item highlight">
            <span className="section-num">§28</span>
            <span className="variance">σ = 0.288</span>
            <p><em>Meta-aphorism about translation itself</em></p>
          </div>
          <div className="divergence-item">
            <span className="section-num">§59</span>
            <span className="variance">σ = 0.281</span>
            <p>Human superficiality as survival instinct</p>
          </div>
          <div className="divergence-item">
            <span className="section-num">§102</span>
            <span className="variance">σ = 0.233</span>
            <p>Discovering reciprocated love (very short)</p>
          </div>
          <div className="divergence-item">
            <span className="section-num">§83</span>
            <span className="variance">σ = 0.226</span>
            <p>Instinct — the house fire aphorism</p>
          </div>
        </div>

        <div className="viz-container">
          <DivergenceChart />
        </div>
      </section>

      {/* Orthography Section */}
      <section className="section">
        <h2>The Archaic Spelling Problem</h2>
        <p>
          Nietzsche wrote before the 1901 German orthography reform. Our Gutenberg source uses
          19th-century spellings that modern embedding models don't fully recognize:
        </p>

        <div className="spelling-table">
          <div className="spell-row header">
            <span>Archaic</span>
            <span>Modern</span>
            <span>Embedding Sim.</span>
          </div>
          <div className="spell-row">
            <span className="archaic">giebt</span>
            <span className="modern">gibt</span>
            <span className="sim">~0.52</span>
          </div>
          <div className="spell-row">
            <span className="archaic">Werth</span>
            <span className="modern">Wert</span>
            <span className="sim">~0.53</span>
          </div>
          <div className="spell-row">
            <span className="archaic">Theil</span>
            <span className="modern">Teil</span>
            <span className="sim">~0.55</span>
          </div>
          <div className="spell-row">
            <span className="archaic">seyn</span>
            <span className="modern">sein</span>
            <span className="sim">~0.48</span>
          </div>
        </div>

        <p>
          The model sees "Werth" and "Wert" as different words. We built a rule-based normalizer
          (~50 patterns) that improved German-English alignment by +0.002-0.003 across all translators.
          Small, but the rankings remained stable — confirming our findings aren't orthographic artifacts.
        </p>
      </section>

      {/* German Nuances */}
      <section className="section">
        <h2>German Philology Notes</h2>

        <div className="nuance-card">
          <h3>The "th" → "t" Shift (1901)</h3>
          <p>
            Words from Greek kept their original "th" spelling until the 1901 reform:
            <em>Theil</em> → <em>Teil</em>, <em>Thür</em> → <em>Tür</em>.
            But "Theater" kept the "th" — still perceived as foreign/learned.
          </p>
        </div>

        <div className="nuance-card">
          <h3>The "ie" → "i" Pattern</h3>
          <p>
            <em>Giebt</em> → <em>gibt</em>. The "ie" indicated vowel length, not the diphthong [iː].
            Modern German uses consonant doubling instead.
          </p>
        </div>

        <div className="nuance-card">
          <h3>The "c" → "k" Shift</h3>
          <p>
            <em>Cultur</em> → <em>Kultur</em>. German dropped Latin spellings to assert linguistic
            independence. The "Kultur vs Culture" debate was itself a culture war.
          </p>
        </div>
      </section>

      {/* Similarity Heatmap */}
      <section className="section viz-section">
        <h2>The Full Picture</h2>
        <div className="viz-container">
          <HeatmapChart />
        </div>
        <p className="viz-caption">
          Kaufmann and Hollingdale (both 1960s-70s academic translations) cluster at 0.886 similarity.
          Norman shows more interpretive freedom. Zimmern carries Victorian stylistic drift.
        </p>
      </section>

      {/* Meta Section */}
      <section className="section">
        <h2>On Applying NLP to Nietzsche</h2>

        <div className="epigraph small">
          <blockquote>
            "Der Wille zur Wahrheit... wer hat uns eigentlich diese Frage gestellt?"
          </blockquote>
          <cite>— BGE §1</cite>
          <p className="translation">"The will to truth... who among us has actually posed this question?"</p>
        </div>

        <p>
          There's something deliciously ironic about subjecting Nietzsche to computational analysis.
          The philosopher who attacked "the faith in opposite values" now has his words projected
          into a vector space where similarity is measured in cosines.
        </p>

        <p>
          What do embeddings actually capture? Semantic similarity in modern multilingual web-text space —
          not philosophical fidelity to Nietzsche's conceptual framework. The model learned "meaning as use"
          from Wikipedia, not from <em>Zarathustra</em>.
        </p>

        <p>
          We tested a philosophy-tuned model (fine-tuned on Stanford Encyclopedia triplets). It was
          better at distinguishing "das Vornehme" (the noble) from "das Gemeine" (the common) —
          concepts central to Nietzsche's aristocratic ethics. But worse at cross-lingual alignment.
        </p>

        <p className="caveat">
          <strong>The trade-off:</strong> conceptual nuance vs. translation alignment.
          You can't optimize for both with current models.
        </p>

        <p>
          So what are we actually measuring? Relative divergence patterns. Where translators cluster
          and where they scatter. The finding isn't which translation is "best" — it's that
          <em>interpretive schools exist</em>, and that §28's claim about untranslatable tempo is
          empirically verifiable.
        </p>
      </section>

      {/* Closing */}
      <section className="section closing">
        <h2>Amor Fati</h2>
        <p>
          This project began as a technical exercise: can embeddings detect translation differences?
          They can. But the more interesting discovery was §28 — Nietzsche's meta-commentary
          emerging as our highest-divergence passage.
        </p>
        <p>
          The philosopher spoke of eternal recurrence: all things returning, including this very moment
          of you reading these words. Perhaps that includes the irony of quantifying the unquantifiable,
          measuring the immeasurable, and finding — in the numbers — confirmation of what
          Nietzsche already knew.
        </p>
        <p className="sign-off">
          Some things resist translation. The embeddings agree.
        </p>
      </section>

      {/* Footer */}
      <footer className="page-footer">
        <a href="https://amadeuswoo.com" className="back-link">← Portfolio</a>
        <a
          href="https://github.com/TheApexWu/nietzcheNLP"
          target="_blank"
          rel="noopener noreferrer"
          className="github-link"
        >
          View Code on GitHub
        </a>
      </footer>

      <style jsx>{`
        .nietzsche-page {
          --sun-gold: #f4a623;
          --sun-light: #ffeaa7;
          --warm-cream: #fdf6e3;
          --warm-white: #fffef9;
          --terra-cotta: #c9784a;
          --deep-wine: #722f37;
          --text-dark: #2d2418;
          --text-mid: #5c4a37;
          --text-light: #8b7355;
          --border-warm: #e6d5b8;

          background: linear-gradient(180deg, var(--warm-white) 0%, var(--warm-cream) 100%);
          color: var(--text-dark);
          min-height: 100vh;
          font-family: var(--font-cormorant), Georgia, serif;
          position: relative;
          overflow-x: hidden;
        }

        .sun-decor {
          position: fixed;
          top: -150px;
          right: -150px;
          width: 400px;
          height: 400px;
          background: radial-gradient(circle, var(--sun-gold) 0%, var(--sun-light) 40%, transparent 70%);
          border-radius: 50%;
          opacity: 0.4;
          pointer-events: none;
          z-index: 0;
        }

        .hero {
          max-width: 800px;
          margin: 0 auto;
          padding: 6rem 2rem 4rem;
          text-align: center;
          position: relative;
          z-index: 1;
        }

        .hero-tag {
          display: inline-block;
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.7rem;
          letter-spacing: 0.2em;
          text-transform: uppercase;
          color: var(--terra-cotta);
          border: 1px solid var(--terra-cotta);
          padding: 0.5rem 1.25rem;
          margin-bottom: 2rem;
        }

        .hero h1 {
          font-size: clamp(2.5rem, 7vw, 4rem);
          font-weight: 400;
          line-height: 1.15;
          color: var(--text-dark);
          margin-bottom: 1.5rem;
        }

        .hero h1 em {
          font-style: italic;
          color: var(--deep-wine);
        }

        .subtitle {
          font-size: 1.2rem;
          color: var(--text-mid);
          max-width: 600px;
          margin: 0 auto;
          line-height: 1.7;
        }

        .section {
          max-width: 720px;
          margin: 0 auto;
          padding: 3rem 2rem;
          position: relative;
          z-index: 1;
        }

        .section h2 {
          font-size: 1.6rem;
          font-weight: 600;
          color: var(--text-dark);
          margin-bottom: 1.5rem;
          border-bottom: 2px solid var(--sun-gold);
          padding-bottom: 0.5rem;
          display: inline-block;
        }

        .section p {
          font-size: 1.1rem;
          line-height: 1.8;
          color: var(--text-mid);
          margin-bottom: 1.25rem;
        }

        .lead {
          font-size: 1.25rem !important;
          line-height: 1.9 !important;
          color: var(--text-dark) !important;
        }

        .epigraph {
          background: linear-gradient(135deg, var(--sun-light) 0%, var(--warm-cream) 100%);
          border-left: 4px solid var(--sun-gold);
          padding: 2rem;
          margin: 2rem 0;
          border-radius: 0 8px 8px 0;
        }

        .epigraph blockquote {
          font-size: 1.3rem;
          font-style: italic;
          color: var(--text-dark);
          margin-bottom: 0.75rem;
          line-height: 1.6;
        }

        .epigraph cite {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.85rem;
          color: var(--terra-cotta);
          display: block;
          margin-bottom: 1rem;
        }

        .epigraph .translation {
          font-size: 1rem;
          color: var(--text-mid);
          margin: 0;
          font-style: normal;
        }

        .epigraph.small {
          padding: 1.5rem;
        }

        .epigraph.small blockquote {
          font-size: 1.1rem;
        }

        .stats {
          display: flex;
          justify-content: center;
          gap: 4rem;
          padding: 3rem 2rem;
          margin: 2rem auto;
          max-width: 700px;
          border-top: 1px solid var(--border-warm);
          border-bottom: 1px solid var(--border-warm);
          position: relative;
          z-index: 1;
        }

        .stat {
          text-align: center;
        }

        .stat-value {
          display: block;
          font-family: var(--font-jetbrains), monospace;
          font-size: 2.5rem;
          font-weight: 600;
          color: var(--sun-gold);
        }

        .stat-label {
          font-size: 0.85rem;
          color: var(--text-light);
          text-transform: uppercase;
          letter-spacing: 0.1em;
        }

        .finding-highlight {
          background: var(--warm-cream);
          border-radius: 12px;
          margin: 2rem auto;
          padding: 3rem 2.5rem;
        }

        .data-card {
          background: var(--warm-white);
          border: 1px solid var(--border-warm);
          border-radius: 8px;
          padding: 1.5rem;
          margin: 2rem 0;
        }

        .data-card h3 {
          font-size: 1rem;
          font-weight: 600;
          color: var(--text-mid);
          margin-bottom: 1rem;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .ranking {
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .rank-item {
          display: grid;
          grid-template-columns: 2rem 1fr auto;
          align-items: center;
          gap: 1rem;
          padding: 0.75rem 1rem;
          background: var(--warm-cream);
          border-radius: 4px;
        }

        .rank-item.winner {
          background: linear-gradient(135deg, var(--sun-light) 0%, var(--warm-cream) 100%);
          border: 1px solid var(--sun-gold);
        }

        .rank {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.85rem;
          color: var(--text-light);
        }

        .translator {
          font-weight: 600;
          color: var(--text-dark);
        }

        .score {
          font-family: var(--font-jetbrains), monospace;
          font-size: 1.1rem;
          color: var(--terra-cotta);
        }

        .viz-section {
          max-width: 900px;
        }

        .viz-container {
          background: var(--warm-white);
          border: 1px solid var(--border-warm);
          border-radius: 8px;
          padding: 1.5rem;
          margin: 2rem 0;
          text-align: center;
        }

        .viz-image {
          max-width: 100%;
          height: auto;
          border-radius: 4px;
        }

        .viz-caption {
          font-size: 0.95rem;
          color: var(--text-light);
          font-style: italic;
          text-align: center;
          margin-top: 0;
        }

        .divergence-list {
          margin: 2rem 0;
        }

        .divergence-item {
          display: grid;
          grid-template-columns: 4rem 5rem 1fr;
          gap: 1rem;
          align-items: center;
          padding: 1rem;
          border-bottom: 1px solid var(--border-warm);
        }

        .divergence-item.highlight {
          background: linear-gradient(135deg, var(--sun-light) 0%, transparent 100%);
          border-radius: 4px;
          border: 1px solid var(--sun-gold);
        }

        .section-num {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.9rem;
          color: var(--deep-wine);
          font-weight: 600;
        }

        .variance {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.8rem;
          color: var(--terra-cotta);
        }

        .divergence-item p {
          font-size: 1rem;
          color: var(--text-mid);
          margin: 0;
        }

        .spelling-table {
          margin: 2rem 0;
          border: 1px solid var(--border-warm);
          border-radius: 8px;
          overflow: hidden;
        }

        .spell-row {
          display: grid;
          grid-template-columns: 1fr 1fr 1fr;
          padding: 0.75rem 1.25rem;
          border-bottom: 1px solid var(--border-warm);
        }

        .spell-row:last-child {
          border-bottom: none;
        }

        .spell-row.header {
          background: var(--warm-cream);
          font-weight: 600;
          font-size: 0.85rem;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          color: var(--text-mid);
        }

        .archaic {
          font-family: var(--font-jetbrains), monospace;
          color: var(--deep-wine);
        }

        .modern {
          font-family: var(--font-jetbrains), monospace;
          color: var(--text-dark);
        }

        .sim {
          font-family: var(--font-jetbrains), monospace;
          color: var(--terra-cotta);
        }

        .nuance-card {
          background: var(--warm-cream);
          border-left: 3px solid var(--sun-gold);
          padding: 1.25rem 1.5rem;
          margin: 1.5rem 0;
          border-radius: 0 8px 8px 0;
        }

        .nuance-card h3 {
          font-size: 1.1rem;
          color: var(--text-dark);
          margin-bottom: 0.5rem;
        }

        .nuance-card p {
          font-size: 1rem;
          margin: 0;
        }

        .nuance-card em {
          color: var(--deep-wine);
        }

        .caveat {
          background: linear-gradient(135deg, var(--warm-cream) 0%, var(--sun-light) 100%);
          border: 1px solid var(--sun-gold);
          padding: 1.25rem 1.5rem;
          border-radius: 8px;
          font-size: 1.05rem;
        }

        .caveat strong {
          color: var(--deep-wine);
        }

        .closing {
          text-align: center;
          padding-top: 4rem;
          border-top: 1px solid var(--border-warm);
        }

        .closing h2 {
          display: block;
          margin-left: auto;
          margin-right: auto;
        }

        .sign-off {
          font-size: 1.3rem;
          font-style: italic;
          color: var(--text-dark);
          margin-top: 2rem;
        }

        .page-footer {
          max-width: 720px;
          margin: 0 auto;
          padding: 3rem 2rem 4rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          border-top: 1px solid var(--border-warm);
          position: relative;
          z-index: 1;
        }

        .back-link, .github-link {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.9rem;
          color: var(--terra-cotta);
          text-decoration: none;
          padding: 0.75rem 1.25rem;
          border: 1px solid var(--terra-cotta);
          border-radius: 4px;
          transition: all 0.2s;
        }

        .back-link:hover, .github-link:hover {
          background: var(--terra-cotta);
          color: var(--warm-white);
        }

        @media (max-width: 768px) {
          .hero {
            padding: 4rem 1.5rem 3rem;
          }

          .stats {
            flex-direction: column;
            gap: 2rem;
          }

          .sun-decor {
            width: 250px;
            height: 250px;
            top: -100px;
            right: -100px;
          }

          .divergence-item {
            grid-template-columns: 3rem 4rem 1fr;
            gap: 0.5rem;
          }

          .rank-item {
            grid-template-columns: 1.5rem 1fr auto;
          }

          .page-footer {
            flex-direction: column;
            gap: 1rem;
          }
        }
      `}</style>
    </div>
  )
}
