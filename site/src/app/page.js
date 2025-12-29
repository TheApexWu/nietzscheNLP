'use client'

import dynamic from 'next/dynamic'

const SimilarityChart = dynamic(() => import('../components/SimilarityChart'), { ssr: false })
const DivergenceChart = dynamic(() => import('../components/DivergenceChart'), { ssr: false })
const HeatmapChart = dynamic(() => import('../components/HeatmapChart'), { ssr: false })
const UMAPChart = dynamic(() => import('../components/UMAPChart'), { ssr: false })

export default function Home() {
  return (
    <div className="nietzsche-page">
      <div className="sun-decor" />

      <header className="hero">
        <span className="hero-tag">Computational Philology</span>
        <h1>Beyond Good and Evil,<br /><em>Beyond Translation</em></h1>
        <p className="subtitle">
          Sentence embeddings, five translators, and a philosopher who predicted
          his own untranslatability 140 years before I could measure it.
        </p>
      </header>

      <section className="section">
        <p className="lead">
          I have read Beyond Good and Evil in four translations. Not because I am thorough,
          but because I kept switching, unsatisfied. Kaufmann felt like a professor standing
          between me and the text, footnoting away the danger. Hollingdale felt closer, rawer.
          Zimmern, the Victorian, softened everything that should bite. Each version claimed
          to be Nietzsche, yet none felt like the same book.
        </p>

        <p>
          This is not a complaint. Translation is impossible. Every translator knows this.
          The question is what kind of impossibility you prefer: the careful academic who
          explains the joke, or the literary stylist who rewrites it for a new audience.
          Neither is wrong. Both are betrayals.
        </p>

        <p>
          So I did what seemed natural: I ran the translations through sentence embeddings
          to see if the machine could detect what I felt. Could NLP quantify the distance
          between interpretations? Could it identify where translators diverge most?
        </p>

        <p>
          What I found was stranger than I expected.
        </p>
      </section>

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

        <p>
          In aphorism 28, Nietzsche argues that the tempo of a language, its rhythm and cadence,
          is rooted in what he calls the "average tempo of its metabolism." This is not metaphor.
          He means it literally: a language carries the physiological signature of its speakers.
          German moves differently than French. The translator who captures the words but loses
          the tempo has captured nothing.
        </p>

        <p>
          This aphorism showed the <em>second highest divergence</em> among all five translators
          in my analysis. The passage about untranslatability was itself the hardest to translate
          consistently. Either this is a beautiful confirmation or a suspicious coincidence.
          I choose to find it beautiful.
        </p>
      </section>

      <section className="stats">
        <div className="stat">
          <span className="stat-value">231</span>
          <span className="stat-label">Aphorisms Aligned</span>
        </div>
        <div className="stat">
          <span className="stat-value">5</span>
          <span className="stat-label">Translators</span>
        </div>
        <div className="stat">
          <span className="stat-value">0.833</span>
          <span className="stat-label">Max Fidelity</span>
        </div>
      </section>

      <section className="section">
        <h2>The Translators and Their Projects</h2>

        <p>
          These are not interchangeable renderings. Each translator brought a theory of
          what Nietzsche was doing and how to make it work in English. Understanding the
          numbers requires understanding the people.
        </p>

        <div className="translator-card">
          <h3>Helen Zimmern, 1906</h3>
          <p>
            The first major English translation, and it shows. Zimmern knew Nietzsche personally,
            which sounds impressive until you realize she was filtering him through Victorian sensibilities.
            Her prose is stiff where his is vicious. She writes "one must consider" where Nietzsche spits.
            The embedding model detects her as the most distant from the German, and from the other
            English translators. A century of language evolution separates her from Norman, and
            the machine sees every year.
          </p>
        </div>

        <div className="translator-card">
          <h3>Walter Kaufmann, 1966</h3>
          <p>
            The academic standard for fifty years. Kaufmann's project was rehabilitation: rescuing
            Nietzsche from the Nazis, proving he was a serious philosopher, not a proto-fascist lunatic.
            The translation reflects this mission. Careful. Scholarly. Heavily footnoted. Sometimes
            you feel Kaufmann interpreting before you can interpret for yourself. The embeddings
            place him close to Hollingdale (0.886 similarity), which makes sense: same era, same
            academic context, probably reading each other's work.
          </p>
        </div>

        <div className="translator-card">
          <h3>R.J. Hollingdale, 1973</h3>
          <p>
            My favorite, and the embeddings agree. Hollingdale was self-taught, not a professor
            but a translator by trade. He rendered almost everything Nietzsche wrote. His approach
            was literary rather than academic: trust the reader to handle Nietzsche raw, without
            protective footnotes. The prose moves. He sits at the semantic center of all translations,
            closest to the German (0.833) and closest to everyone else. Whether this makes him
            "best" depends on what you want. It makes him the faithful middle, the point other
            interpretations orbit.
          </p>
        </div>

        <div className="translator-card">
          <h3>Marion Faber, 1998</h3>
          <p>
            Oxford World's Classics. Faber aimed for accuracy over style. The result is reliable
            but rarely surprising. Good for study, less good for feeling the text. She sits
            between the academic Kaufmann and the literary Hollingdale, a sensible median.
          </p>
        </div>

        <div className="translator-card">
          <h3>Judith Norman, 2002</h3>
          <p>
            The Cambridge edition, co-edited with Rolf-Peter Horstmann. Norman takes interpretive
            risks the others avoid, updating dated references, modernizing idioms. The result
            reads more easily but drifts further from the German. The embeddings detect this:
            she clusters with Zimmern in interpretive distance, though a century apart in time.
          </p>
        </div>
      </section>

      <section className="section finding-highlight">
        <h2>The Semantic Centroid</h2>

        <p>
          I computed pairwise cosine similarity across all translator embeddings. One name
          emerged as the gravitational center: Hollingdale.
        </p>

        <div className="data-card">
          <h3>Similarity to Original German</h3>
          <SimilarityChart />
        </div>

        <p>
          Hollingdale is not just closest to the German. He is closest to everyone.
          This does not mean he is "best." It means his translation occupies the semantic
          middle ground. The others deviate from it in different directions: Zimmern toward
          Victorian formality, Norman toward modern accessibility, Kaufmann toward academic precision.
        </p>

        <p>
          What does it mean to be the centroid? Perhaps that Hollingdale made the fewest
          interpretive choices, stayed closest to the literal while remaining readable.
          Or perhaps he simply averaged out the possibilities. The machine cannot tell us
          which. Only that the pattern exists.
        </p>
      </section>

      <section className="section viz-section">
        <h2>The Fingerprint</h2>

        <p>
          UMAP projection of 1,386 aphorism embeddings (231 aphorisms across 6 sources)
          reveals distinct clusters. Each translator leaves a signature. The model can
          classify who translated what without being told.
        </p>

        <div className="viz-container">
          <UMAPChart />
        </div>

        <p className="viz-caption">
          Hover over the legend to isolate each cluster. German sits at center.
          Kaufmann and Hollingdale cluster nearby. Norman and Zimmern drift further.
        </p>

        <p>
          This is perhaps the most striking result. Translators have fingerprints.
          Their stylistic choices are consistent enough across 231 aphorisms that a
          dimensionality reduction algorithm can separate them visually. Whatever
          "voice" means, it shows up in vector space.
        </p>
      </section>

      <section className="section">
        <h2>Where They Diverge</h2>

        <p>
          Some passages translate consistently across all five versions. Others scatter wildly.
          The variance tells you where the German underdetermines the English, where translators
          had to make choices no dictionary could dictate.
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
            <p><em>The meta-aphorism on translation itself</em></p>
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
            <p>Instinct and the house fire</p>
          </div>
        </div>

        <p>
          The pattern: short aphorisms diverge more. Less context means more ambiguity,
          more room for interpretive freedom. Passages with embedded French scatter wildly
          because translators handle code-switching differently. And self-referential passages,
          where Nietzsche writes about language itself, prove hardest to render consistently.
        </p>

        <div className="viz-container">
          <DivergenceChart />
        </div>
      </section>

      <section className="section">
        <h2>The Orthography Problem</h2>

        <p>
          Nietzsche wrote before the 1901 German orthography reform. My source text uses
          19th century spellings that modern embedding models do not fully recognize:
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
          The model sees "Werth" and "Wert" as different words. I built a normalizer,
          about fifty substitution rules, that improved German-English alignment by 0.002-0.003
          across all translators. Small, but the rankings stayed stable. Hollingdale still wins.
        </p>

        <p>
          The "th" to "t" shift came in 1901. Words derived from Greek lost their classical
          spellings. "Theater" kept its "th" because Germans still perceived it as foreign.
          Language politics, then as now.
        </p>
      </section>

      <section className="section viz-section">
        <h2>The Full Matrix</h2>

        <div className="viz-container">
          <HeatmapChart />
        </div>

        <p className="viz-caption">
          Hover to see exact similarity scores. The Kaufmann-Hollingdale cluster (0.886)
          is the tightest. Norman-Zimmern (0.806) are most distant from each other.
        </p>
      </section>

      <section className="section">
        <h2>What This Actually Measures</h2>

        <p>
          I should be honest about the limitations. Sentence embeddings capture semantic
          similarity in modern multilingual web-text space. They do not capture philosophical
          fidelity to Nietzsche's conceptual framework. The model learned "meaning" from
          Wikipedia and Reddit, not from <em>Thus Spoke Zarathustra</em>.
        </p>

        <p>
          I tested a philosophy-tuned model, fine-tuned on Stanford Encyclopedia triplets.
          It was better at distinguishing "das Vornehme" (the noble) from "das Gemeine" (the common),
          concepts central to Nietzsche's aristocratic ethics. But worse at cross-lingual alignment.
          You cannot optimize for both. The trade-off is real.
        </p>

        <p>
          So what am I actually measuring? Relative divergence patterns. Where translators
          cluster and where they scatter. The finding is not which translation is best.
          It is that interpretive schools exist, that translator fingerprints are real,
          and that §28's claim about untranslatable tempo shows up in the math.
        </p>

        <div className="epigraph small">
          <blockquote>
            "Der Wille zur Wahrheit... wer hat uns eigentlich diese Frage gestellt?"
          </blockquote>
          <cite>— BGE §1</cite>
          <p className="translation">"The will to truth... who among us has actually posed this question?"</p>
        </div>

        <p>
          There is something ironic about subjecting Nietzsche to computational analysis.
          The philosopher who attacked "the faith in opposite values" now has his words
          projected into a vector space where similarity is a cosine distance. He would
          probably despise it. Or find it amusing that we keep trying to systematize
          what resists systematization.
        </p>
      </section>

      <section className="section closing">
        <h2>What I Learned</h2>

        <p>
          I started this project to see if embeddings could detect translation differences.
          They can. The more interesting discovery was §28. I did not go looking for it.
          The variance analysis surfaced it. Nietzsche's meta-commentary about the impossibility
          of translation emerged as one of the hardest passages to translate consistently.
        </p>

        <p>
          The man was right. Some things resist translation. The embeddings agree.
        </p>
      </section>

      <footer className="page-footer">
        <a href="https://amadeuswoo.substack.com" className="back-link">← Substack</a>
        <a
          href="https://github.com/TheApexWu/nietzcheNLP"
          target="_blank"
          rel="noopener noreferrer"
          className="github-link"
        >
          View Code
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
          font-size: 1.15rem;
          color: var(--text-mid);
          max-width: 600px;
          margin: 0 auto;
          line-height: 1.7;
        }

        .section {
          max-width: 720px;
          margin: 0 auto;
          padding: 2.5rem 2rem;
          position: relative;
          z-index: 1;
        }

        .section h2 {
          font-size: 1.5rem;
          font-weight: 600;
          color: var(--text-dark);
          margin-bottom: 1.5rem;
          border-bottom: 2px solid var(--sun-gold);
          padding-bottom: 0.5rem;
          display: inline-block;
        }

        .section p {
          font-size: 1.05rem;
          line-height: 1.85;
          color: var(--text-mid);
          margin-bottom: 1.25rem;
        }

        .lead {
          font-size: 1.15rem !important;
          line-height: 1.9 !important;
          color: var(--text-dark) !important;
        }

        .translator-card {
          background: var(--warm-cream);
          border-left: 3px solid var(--sun-gold);
          padding: 1.25rem 1.5rem;
          margin: 1.5rem 0;
          border-radius: 0 8px 8px 0;
        }

        .translator-card h3 {
          font-size: 1.1rem;
          color: var(--deep-wine);
          margin-bottom: 0.5rem;
          font-weight: 600;
        }

        .translator-card p {
          font-size: 0.95rem;
          margin: 0;
          line-height: 1.75;
        }

        .epigraph {
          background: linear-gradient(135deg, var(--sun-light) 0%, var(--warm-cream) 100%);
          border-left: 4px solid var(--sun-gold);
          padding: 2rem;
          margin: 2rem 0;
          border-radius: 0 8px 8px 0;
        }

        .epigraph blockquote {
          font-size: 1.25rem;
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
          padding: 2.5rem 2rem;
          margin: 1.5rem auto;
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
          font-size: 2.25rem;
          font-weight: 600;
          color: var(--sun-gold);
        }

        .stat-label {
          font-size: 0.8rem;
          color: var(--text-light);
          text-transform: uppercase;
          letter-spacing: 0.1em;
        }

        .finding-highlight {
          background: var(--warm-cream);
          border-radius: 12px;
          margin: 2rem auto;
          padding: 2.5rem;
        }

        .data-card {
          background: var(--warm-white);
          border: 1px solid var(--border-warm);
          border-radius: 8px;
          padding: 1.5rem;
          margin: 2rem 0;
        }

        .data-card h3 {
          font-size: 0.9rem;
          font-weight: 600;
          color: var(--text-mid);
          margin-bottom: 1rem;
          text-transform: uppercase;
          letter-spacing: 0.05em;
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

        .viz-caption {
          font-size: 0.9rem;
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
          font-size: 0.95rem;
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
          font-size: 0.8rem;
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

        .closing {
          text-align: center;
          padding-top: 3rem;
          border-top: 1px solid var(--border-warm);
        }

        .closing h2 {
          display: block;
          margin-left: auto;
          margin-right: auto;
        }

        .page-footer {
          max-width: 720px;
          margin: 0 auto;
          padding: 2.5rem 2rem 4rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          border-top: 1px solid var(--border-warm);
          position: relative;
          z-index: 1;
        }

        .back-link, .github-link {
          font-family: var(--font-jetbrains), monospace;
          font-size: 0.85rem;
          color: var(--terra-cotta);
          text-decoration: none;
          padding: 0.65rem 1.1rem;
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

          .page-footer {
            flex-direction: column;
            gap: 1rem;
          }
        }
      `}</style>
    </div>
  )
}
