import Image from 'next/image'
import Link from 'next/link'
import { ArrowLeft, ArrowRight } from 'lucide-react'
import { notFound } from 'next/navigation'

const articles: Record<string, {
  title: string
  date: string
  category: string
  image: string
  content: string[]
}> = {
  'tournoi-printemps-2025-resultats': {
    title: 'Tournoi Printemps 2025 : les résultats complets',
    date: '18 mai 2025',
    category: 'Résultats',
    image: 'https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=1200&h=600&fit=crop',
    content: [
      'Le Tournoi du Printemps 2025 a réuni plus de 80 participants sur trois jours de compétition intense. Les courts de la Châtaigneraie ont vibré au rythme des échanges de haut niveau.',
      'En simple messieurs, c\'est Marc Delacroix (TC Châtaigneraie) qui s\'impose en finale face à Antoine Lebrun, dans un match serré en trois sets (6-4, 3-6, 7-5). En dames, Sophie Martin remporte son troisième titre consécutif.',
      'Le double mixte a offert les échanges les plus spectaculaires du weekend, avec une finale mémorable remportée par la paire Guillot-Ferrand.',
      'Rendez-vous l\'année prochaine pour une nouvelle édition encore plus ambitieuse. Toutes les inscriptions se feront via le formulaire en ligne à partir de janvier 2026.',
    ],
  },
  'nouveau-coach-padel-2025': {
    title: 'Bienvenue à notre nouveau coach padel',
    date: '10 mai 2025',
    category: 'Padel',
    image: 'https://images.unsplash.com/photo-1622163642998-1ea32b0bbc67?w=1200&h=600&fit=crop',
    content: [
      'Le Tennis Club de la Châtaigneraie est fier d\'accueillir Thomas Boyer dans son équipe pédagogique. Ancien joueur professionnel classé dans le top 50 padel français, Thomas apporte une expertise rare.',
      'Formé à l\'Académie Nationale de Padel de Toulouse, il a officié pendant 4 ans comme entraîneur au PCA (Padel Club Aix) avant de rejoindre notre club.',
      'Thomas prend en charge dès juin les cours collectifs intermédiaires et avancés, ainsi que les séances de coaching individuel. Les stages intensifs de l\'été seront également co-animés avec notre équipe.',
      'Bienvenue Thomas !',
    ],
  },
}

export async function generateStaticParams() {
  return Object.keys(articles).map((slug) => ({ slug }))
}

export default function ArticlePage({ params }: { params: { slug: string } }) {
  const article = articles[params.slug]
  if (!article) notFound()

  return (
    <article>
      {/* Hero article */}
      <div className="relative h-[50vh] min-h-[320px] overflow-hidden mt-16 md:mt-20">
        <Image
          src={article.image}
          alt={article.title}
          fill
          priority
          className="object-cover"
          sizes="100vw"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-dark/80 to-transparent" style={{ '--tw-gradient-from': '#0F1F17' } as React.CSSProperties} />
        <div className="absolute bottom-0 left-0 right-0 container-wide pb-10">
          <span className="label-tag px-3 py-1.5 text-white mb-4 inline-block" style={{ backgroundColor: '#C9A84C' }}>
            {article.category}
          </span>
          <h1 className="font-cormorant text-white font-light max-w-3xl" style={{ fontSize: 'clamp(1.8rem, 4vw, 3rem)', lineHeight: 1.1 }}>
            {article.title}
          </h1>
          <p className="label-tag text-white/50 mt-3">{article.date}</p>
        </div>
      </div>

      {/* Contenu */}
      <section className="section-padding" style={{ backgroundColor: '#F7F4EF' }}>
        <div className="container-wide">
          <div className="max-w-2xl">
            <Link href="/actualites" className="inline-flex items-center gap-2 label-tag mb-10 hover:opacity-70 transition-opacity" style={{ color: '#7A7A72' }}>
              <ArrowLeft size={12} /> Toutes les actualités
            </Link>

            <div className="space-y-6">
              {article.content.map((paragraph, i) => (
                <p key={i} className="font-light leading-relaxed" style={{ color: '#2C2C2C', fontSize: '15px', lineHeight: '1.9' }}>
                  {paragraph}
                </p>
              ))}
            </div>

            <div className="gold-line my-12 opacity-30" />

            <div className="flex items-center justify-between">
              <p className="label-tag" style={{ color: '#7A7A72' }}>Partager cet article</p>
              <Link href="/actualites" className="inline-flex items-center gap-2 label-tag hover:gap-3 transition-all" style={{ color: '#1B3A2D' }}>
                Voir d'autres articles <ArrowRight size={12} />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </article>
  )
}
