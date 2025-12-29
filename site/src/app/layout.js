import { Cormorant_Garamond, JetBrains_Mono } from 'next/font/google'
import './globals.css'

const cormorant = Cormorant_Garamond({
  subsets: ['latin'],
  weight: ['400', '500', '600'],
  variable: '--font-cormorant',
  display: 'swap',
})

const jetbrains = JetBrains_Mono({
  subsets: ['latin'],
  weight: ['400', '500'],
  variable: '--font-jetbrains',
  display: 'swap',
})

export const metadata = {
  title: 'NietzcheNLP — Beyond Good and Evil, Beyond Translation',
  description: 'An NLP exploration of five English translations of Nietzsche\'s Beyond Good and Evil',
}

export default function RootLayout({ children }) {
  return (
    <html lang="en" className={`${cormorant.variable} ${jetbrains.variable}`}>
      <body>{children}</body>
    </html>
  )
}
