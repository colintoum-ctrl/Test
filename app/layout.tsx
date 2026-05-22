import type { Metadata } from 'next'
import './globals.css'
import Navbar from '@/components/layout/navbar'
import Footer from '@/components/layout/footer'

export const metadata: Metadata = {
  title: 'Tennis Club de la Châtaigneraie · Rueil-Malmaison',
  description: 'Club de tennis premium fondé en 1963 à Rueil-Malmaison. 7 courts couverts, 4 pistes de padel, fitness, club house. Rejoignez la communauté.',
  keywords: 'tennis club châtaigneraie, rueil-malmaison, padel, courts couverts, terre battue',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="fr">
      <body>
        <Navbar />
        <main>{children}</main>
        <Footer />
      </body>
    </html>
  )
}
