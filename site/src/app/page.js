'use client'

import dynamic from 'next/dynamic'
import styles from './page.module.css'

const SimilarityChart = dynamic(() => import('../components/SimilarityChart'), { ssr: false })
const DivergenceChart = dynamic(() => import('../components/DivergenceChart'), { ssr: false })
const HeatmapChart = dynamic(() => import('../components/HeatmapChart'), { ssr: false })
const UMAPChart = dynamic(() => import('../components/UMAPChart'), { ssr: false })
const MethodologyButton = dynamic(() => import('../components/MethodologyButton'), { ssr: false })
const QuoteComparison = dynamic(() => import('../components/QuoteComparison'), { ssr: false })
const AphorismExplorer = dynamic(() => import('../components/AphorismExplorer'), { ssr: false })
const KeyTermAnalysis = dynamic(() => import('../components/KeyTermAnalysis'), { ssr: false })

export default function Home() {
  return (
    <div className={styles.nietzschePage}>
      <div className={styles.sunDecor} />

      <header className={styles.hero}>
        <span className={styles.heroTag}>Computational Philology</span>
        <h1>Beyond Good and Evil,<br /><em>Beyond Translation</em></h1>
        <p className={styles.subtitle}>
          Measuring how five English translations diverge from Nietzsche's German
          using sentence embeddings.
        </p>
      </header>

      <section className={styles.stats}>
        <div className={styles.stat}>
          <span className={styles.statValue}>231</span>
          <span className={styles.statLabel}>Aphorisms Aligned</span>
        </div>
        <div className={styles.stat}>
          <span className={styles.statValue}>6</span>
          <span className={styles.statLabel}>Versions Compared</span>
        </div>
        <div className={styles.stat}>
          <span className={styles.statValue}>0.806</span>
          <span className={styles.statLabel}>Max Fidelity</span>
        </div>
      </section>

      {/* Interactive explorer first */}
      <section className={styles.section}>
        <h2>Explore the Translations</h2>
        <p>
          Compare how different translators render the same aphorism. Search for keywords,
          filter by divergence, or hit "Surprise me" for a random high-divergence passage.
        </p>
        <AphorismExplorer />
      </section>

      <section className={styles.vizSection}>
        <h2>Translator Fingerprints</h2>
        <p>
          UMAP projection of 1,386 embeddings reveals distinct clusters.
          Each translator leaves a stylistic signature the model can detect.
        </p>
        <div className={styles.vizContainer}>
          <UMAPChart />
        </div>
        <p className={styles.vizCaption}>
          Hover to isolate clusters. German sits at center. Kaufmann and Hollingdale cluster nearby.
        </p>
      </section>

      <section className={`${styles.section} ${styles.findingHighlight}`}>
        <h2>The Semantic Centroid</h2>
        <p>
          Pairwise cosine similarity reveals Hollingdale as the gravitational center—closest
          to the German (0.806) and closest to every other translator.
        </p>
        <div className={styles.dataCard}>
          <h3>Similarity to Original German</h3>
          <SimilarityChart />
        </div>
      </section>

      <section className={styles.vizSection}>
        <h2>The Full Matrix</h2>
        <div className={styles.vizContainer}>
          <HeatmapChart />
        </div>
        <p className={styles.vizCaption}>
          Hover for exact scores. Kaufmann-Hollingdale (0.887) cluster tightest.
        </p>
      </section>

      {/* Context and methodology below the fold */}
      <section className={styles.section}>
        <h2>The Question</h2>
        <p className={styles.lead}>
          I kept switching translations—Kaufmann felt like a professor footnoting away the danger,
          Hollingdale felt rawer, Zimmern softened everything. Could NLP quantify what I felt?
        </p>
        <MethodologyButton />
      </section>

      <section className={styles.section}>
        <div className={styles.epigraph}>
          <blockquote>
            "Was sich am schlechtesten aus einer Sprache in die andere übersetzen lässt,
            ist das <strong>tempo</strong> ihres Stils..."
          </blockquote>
          <cite>— BGE §28</cite>
          <p className={styles.epigraphTranslation}>
            "That which translates worst from one language into another is the <strong>tempo</strong> of its style..."
          </p>
        </div>
        <p>
          Nietzsche argues that tempo is rooted in "the average tempo of its metabolism"—
          a language carries the physiological signature of its speakers. The translator
          who captures words but loses tempo has captured nothing.
        </p>
        <QuoteComparison />
      </section>

      <section className={styles.section}>
        <h2>Where They Diverge Most</h2>
        <p>
          Some passages translate consistently. Others scatter wildly—where the German
          underdetermines the English and translators must make choices no dictionary dictates.
        </p>
        <div className={styles.divergenceList}>
          <div className={styles.divergenceItemHighlight}>
            <span className={styles.sectionNum}>§38</span>
            <span className={styles.variance}>σ = 0.319</span>
            <p>French phrases, cultural critique</p>
          </div>
          <div className={styles.divergenceItem}>
            <span className={styles.sectionNum}>§130</span>
            <span className={styles.variance}>σ = 0.250</span>
            <p>Talent reveals character</p>
          </div>
          <div className={styles.divergenceItem}>
            <span className={styles.sectionNum}>§74</span>
            <span className={styles.variance}>σ = 0.242</span>
            <p>Genius requires gratitude</p>
          </div>
        </div>
        <p>
          Short aphorisms diverge more (less context = more ambiguity). Passages with
          embedded French scatter wildly. Self-referential passages about language itself
          prove hardest to render consistently.
        </p>
        <div className={styles.vizContainer}>
          <DivergenceChart />
        </div>
      </section>

      <section className={styles.section}>
        <h2>The Translators</h2>
        <div className={styles.translatorGrid}>
          <div className={styles.translatorCard}>
            <h3>Hollingdale, 1973</h3>
            <p>
              Self-taught translator, literary over academic. Sits at the semantic center—
              closest to German and everyone else. The faithful middle.
            </p>
          </div>
          <div className={styles.translatorCard}>
            <h3>Kaufmann, 1966</h3>
            <p>
              Academic standard. Careful, scholarly, heavily footnoted. Clusters tightly
              with Hollingdale (0.887)—same era, same context.
            </p>
          </div>
          <div className={styles.translatorCard}>
            <h3>Faber, 1998</h3>
            <p>
              Oxford World's Classics. Accuracy over style. Reliable but rarely surprising.
            </p>
          </div>
          <div className={styles.translatorCard}>
            <h3>Norman, 2002</h3>
            <p>
              Cambridge edition. Takes interpretive risks, modernizes idioms. Drifts further
              from German but reads more easily.
            </p>
          </div>
          <div className={styles.translatorCard}>
            <h3>Zimmern, 1906</h3>
            <p>
              First major translation. Victorian sensibilities filter the viciousness.
              Most distant from all others—the machine sees every year of that century.
            </p>
          </div>
        </div>
      </section>

      <section className={styles.section}>
        <h2>Limitations</h2>
        <p>
          Sentence embeddings capture semantic similarity in web-text space, not philosophical
          fidelity. The model learned "meaning" from Wikipedia, not <em>Zarathustra</em>.
          A philosophy-tuned model was better at Nietzsche's concepts but worse at
          cross-lingual alignment. You cannot optimize for both.
        </p>
        <p>
          What I measure: relative divergence patterns. Where translators cluster and scatter.
          Not which translation is "best"—but that interpretive schools exist and fingerprints are real.
        </p>
        <KeyTermAnalysis />
      </section>

      <section className={styles.section}>
        <h2>The Orthography Problem</h2>
        <p>
          Nietzsche wrote before the 1901 spelling reform. The model sees "Werth" and "Wert"
          as different words. I built a 95-rule normalizer that improved alignment by 0.002-0.003.
          Small, but rankings stayed stable.
        </p>
        <div className={styles.spellingTable}>
          <div className={styles.spellRowHeader}>
            <span>Archaic</span>
            <span>Modern</span>
            <span>Sim.</span>
          </div>
          <div className={styles.spellRow}>
            <span className={styles.archaic}>giebt</span>
            <span className={styles.modern}>gibt</span>
            <span className={styles.sim}>~0.52</span>
          </div>
          <div className={styles.spellRow}>
            <span className={styles.archaic}>Werth</span>
            <span className={styles.modern}>Wert</span>
            <span className={styles.sim}>~0.53</span>
          </div>
          <div className={styles.spellRow}>
            <span className={styles.archaic}>seyn</span>
            <span className={styles.modern}>sein</span>
            <span className={styles.sim}>~0.48</span>
          </div>
        </div>
      </section>

      <section className={styles.closing}>
        <h2>Takeaway</h2>
        <p>
          Translators have fingerprints. Hollingdale sits at the semantic center.
          And §28, where Nietzsche writes about tempo and the untranslatable?
          One of the least divergent passages (σ = 0.024). Poetically fitting.
        </p>
      </section>

      <footer className={styles.pageFooter}>
        <a href="https://amadeuswoo.com" className={styles.backLink}>← Home</a>
        <a
          href="https://github.com/TheApexWu/nietzcheNLP"
          target="_blank"
          rel="noopener noreferrer"
          className={styles.githubLink}
        >
          View Code
        </a>
      </footer>
    </div>
  )
}
