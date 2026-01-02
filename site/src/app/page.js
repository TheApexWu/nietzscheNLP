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
          Sentence embeddings, five translators, and discovering that the patterns
          you expect aren't always the patterns you find.
        </p>
      </header>

      <section className={styles.section}>
        <p className={styles.lead}>
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
          In aphorism 28, Nietzsche argues that the tempo of a language, its rhythm and cadence,
          is rooted in what he calls the "average tempo of its metabolism." This is not metaphor.
          He means it literally: a language carries the physiological signature of its speakers.
          German moves differently than French. The translator who captures the words but loses
          the tempo has captured nothing.
        </p>

        <QuoteComparison />
      </section>

      <section className={styles.stats}>
        <div className={styles.stat}>
          <span className={styles.statValue}>231</span>
          <span className={styles.statLabel}>Aphorisms Aligned</span>
        </div>
        <div className={styles.stat}>
          <span className={styles.statValue}>5</span>
          <span className={styles.statLabel}>Translators</span>
        </div>
        <div className={styles.stat}>
          <span className={styles.statValue}>0.806</span>
          <span className={styles.statLabel}>Max Fidelity</span>
        </div>
      </section>

      <section className={styles.section}>
        <h2>The Translators and Their Projects</h2>

        <p>
          These are not interchangeable renderings. Each translator brought a theory of
          what Nietzsche was doing and how to make it work in English. Understanding the
          numbers requires understanding the people.
        </p>

        <div className={styles.translatorCard}>
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

        <div className={styles.translatorCard}>
          <h3>Walter Kaufmann, 1966</h3>
          <p>
            The academic standard for fifty years. Kaufmann's project was rehabilitation: rescuing
            Nietzsche from the Nazis, proving he was a serious philosopher, not a proto-fascist lunatic.
            The translation reflects this mission. Careful. Scholarly. Heavily footnoted. Sometimes
            you feel Kaufmann interpreting before you can interpret for yourself. The embeddings
            place him close to Hollingdale (0.887 similarity), which makes sense: same era, same
            academic context, probably reading each other's work.
          </p>
        </div>

        <div className={styles.translatorCard}>
          <h3>R.J. Hollingdale, 1973</h3>
          <p>
            My favorite, and the embeddings agree. Hollingdale was self-taught, not a professor
            but a translator by trade. He rendered almost everything Nietzsche wrote. His approach
            was literary rather than academic: trust the reader to handle Nietzsche raw, without
            protective footnotes. The prose moves. He sits at the semantic center of all translations,
            closest to the German (0.806) and closest to everyone else. Whether this makes him
            "best" depends on what you want. It makes him the faithful middle, the point other
            interpretations orbit.
          </p>
        </div>

        <div className={styles.translatorCard}>
          <h3>Marion Faber, 1998</h3>
          <p>
            Oxford World's Classics. Faber aimed for accuracy over style. The result is reliable
            but rarely surprising. Good for study, less good for feeling the text. She sits
            between the academic Kaufmann and the literary Hollingdale, a sensible median.
          </p>
        </div>

        <div className={styles.translatorCard}>
          <h3>Judith Norman, 2002</h3>
          <p>
            The Cambridge edition, co-edited with Rolf-Peter Horstmann. Norman takes interpretive
            risks the others avoid, updating dated references, modernizing idioms. The result
            reads more easily but drifts further from the German. The embeddings detect this:
            she clusters with Zimmern in interpretive distance, though a century apart in time.
          </p>
        </div>
      </section>

      <section className={`${styles.section} ${styles.findingHighlight}`}>
        <h2>The Semantic Centroid</h2>

        <p>
          I computed pairwise cosine similarity across all translator embeddings. One name
          emerged as the gravitational center: Hollingdale.
        </p>

        <div className={styles.dataCard}>
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

      <section className={styles.vizSection}>
        <h2>The Fingerprint</h2>

        <p>
          UMAP projection of 1,386 aphorism embeddings (231 aphorisms across 6 sources)
          reveals distinct clusters. Each translator leaves a signature. The model can
          classify who translated what without being told.
        </p>

        <div className={styles.vizContainer}>
          <UMAPChart />
        </div>

        <p className={styles.vizCaption}>
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

      <section className={styles.section}>
        <h2>Where They Diverge</h2>

        <p>
          Some passages translate consistently across all five versions. Others scatter wildly.
          The variance tells you where the German underdetermines the English, where translators
          had to make choices no dictionary could dictate.
        </p>

        <div className={styles.divergenceList}>
          <div className={styles.divergenceItemHighlight}>
            <span className={styles.sectionNum}>§21</span>
            <span className={styles.variance}>σ = 0.368</span>
            <p>The <em>causa sui</em> paradox</p>
          </div>
          <div className={styles.divergenceItem}>
            <span className={styles.sectionNum}>§1</span>
            <span className={styles.variance}>σ = 0.331</span>
            <p>The will to truth</p>
          </div>
          <div className={styles.divergenceItem}>
            <span className={styles.sectionNum}>§38</span>
            <span className={styles.variance}>σ = 0.319</span>
            <p>French phrases, cultural critique</p>
          </div>
          <div className={styles.divergenceItem}>
            <span className={styles.sectionNum}>§82</span>
            <span className={styles.variance}>σ = 0.276</span>
            <p>Short aphorism, high ambiguity</p>
          </div>
          <div className={styles.divergenceItem}>
            <span className={styles.sectionNum}>§130</span>
            <span className={styles.variance}>σ = 0.250</span>
            <p>Purpose of punishment</p>
          </div>
        </div>

        <p>
          The pattern: short aphorisms diverge more. Less context means more ambiguity,
          more room for interpretive freedom. Passages with embedded French scatter wildly
          because translators handle code-switching differently. And self-referential passages,
          where Nietzsche writes about language itself, prove hardest to render consistently.
        </p>

        <div className={styles.vizContainer}>
          <DivergenceChart />
        </div>

        <AphorismExplorer />
      </section>

      <section className={styles.section}>
        <h2>The Orthography Problem</h2>

        <p>
          Nietzsche wrote before the 1901 German orthography reform. My source text uses
          19th century spellings that modern embedding models do not fully recognize:
        </p>

        <div className={styles.spellingTable}>
          <div className={styles.spellRowHeader}>
            <span>Archaic</span>
            <span>Modern</span>
            <span>Embedding Sim.</span>
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
            <span className={styles.archaic}>Theil</span>
            <span className={styles.modern}>Teil</span>
            <span className={styles.sim}>~0.55</span>
          </div>
          <div className={styles.spellRow}>
            <span className={styles.archaic}>seyn</span>
            <span className={styles.modern}>sein</span>
            <span className={styles.sim}>~0.48</span>
          </div>
        </div>

        <p>
          The model sees "Werth" and "Wert" as different words. I built a normalizer,
          ninety-five substitution rules, that improved German-English alignment by 0.002-0.003
          across all translators. Small, but the rankings stayed stable. Hollingdale still wins.
        </p>

        <p>
          The "th" to "t" shift came in 1901. Words derived from Greek lost their classical
          spellings. "Theater" kept its "th" because Germans still perceived it as foreign.
          Language politics, then as now.
        </p>
      </section>

      <section className={styles.vizSection}>
        <h2>The Full Matrix</h2>

        <div className={styles.vizContainer}>
          <HeatmapChart />
        </div>

        <p className={styles.vizCaption}>
          Hover to see exact similarity scores. The Kaufmann-Hollingdale cluster (0.887)
          is the tightest. Norman-Zimmern (0.811) are most distant from each other.
        </p>
      </section>

      <section className={styles.section}>
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
          It is that interpretive schools exist, and that translator fingerprints are real.
        </p>

        <KeyTermAnalysis />

        <div className={styles.epigraphSmall}>
          <blockquote>
            "Der Wille zur Wahrheit... wer hat uns eigentlich diese Frage gestellt?"
          </blockquote>
          <cite>— BGE §1</cite>
          <p className={styles.epigraphTranslation}>"The will to truth... who among us has actually posed this question?"</p>
        </div>

        <p>
          There is something ironic about subjecting Nietzsche to computational analysis.
          The philosopher who attacked "the faith in opposite values" now has his words
          projected into a vector space where similarity is a cosine distance. He would
          probably despise it. Or find it amusing that we keep trying to systematize
          what resists systematization.
        </p>
      </section>

      <section className={styles.closing}>
        <h2>What I Learned</h2>

        <p>
          I started this project to see if embeddings could detect translation differences.
          They can. Translators have fingerprints—consistent stylistic signatures that cluster
          in embedding space. Hollingdale sits at the semantic center, closest to the German
          and closest to everyone else. The machinery works.
        </p>

        <p>
          As for §28, where Nietzsche writes about tempo and the untranslatable, translators
          largely agree. It ranks as one of the least divergent passages in the book (0.024), how poetically fitting.
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
