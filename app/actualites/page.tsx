'use client'

import Image from 'next/image'
import { motion } from 'framer-motion'
import { useState } from 'react'
import { Filter } from 'lucide-react'
import SectionHeader from '@/components/ui/section-header'
import CardArticle from '@/components/ui/card-article'

type Cat = 'Tous' | 'Résultats' | 'Club' | 'Padel' | 'Tennis' | 'Fitness'

const articles = [
  {
    slug: 'tournoi-printemps-2025-resultats',
    image: 'https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=600&h=400&fit=crop',
    date: '18 mai 2025',
    category: 'Résultats',
    title: 'Tournoi Printemps 2025 : les résultats complets',
    excerpt: 'Plus de 80 participants, 3 jours de compétition intense. Retour sur un weekend exceptionnel avec tous les palmares.',
  },
  {
    slug: 'nouveau-coach-padel-2025',
    image: 'https://images.unsplash.com/photo-1622163642998-1ea32b0bbc67?w=600&h=400&fit=crop',
    date: '10 mai 2025',
    category: 'Padel',
    title: 'Bienvenue à notre nouveau coach padel',
    excerpt: 'Ancien joueur professionnel, Thomas Boyer rejoint notre équipe pour développer le programme padel du club.',
  },
  {
    slug: 'renovation-courts-3-4-terminee',
    image: 'https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=600&h=400&fit=crop',
    date: '02 mai 2025',
    category: 'Club',
    title: 'Rénovation des courts 3 & 4 terminée',
    excerpt: 'Après 3 semaines de travaux, les courts 3 et 4 offrent une surface de jeu renouvelée. Une nouvelle terre battue de qualité professionnelle.',
  },
  {
    slug: 'stage-ete-2025-inscriptions-ouvertes',
    image: 'https://images.unsplash.com/photo-1567427017947-545c5f8d16ad?w=600&h=400&fit=crop',
    date: '28 avr. 2025',
    category: 'Tennis',
    title: 'Stages été 2025 : les inscriptions sont ouvertes',
    excerpt: 'Du 5 au 25 juillet, nos stages intensifs pour juniors et adultes. Places limitées — première arrivée, première servie.',
  },
  {
    slug: 'nouveau-materiel-fitness',
    image: 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=600&h=400&fit=crop',
    date: '15 avr. 2025',
    category: 'Fitness',
    title: 'L\'espace fitness s\'équipe de nouveaux appareils',
    excerpt: '12 nouveaux appareils cardio et 8 stations de musculation viennent enrichir notre salle de 200m². Une nouvelle ère pour votre entraînement.',
  },
  {
    slug: 'interclubs-resultats-mars-2025',
    image: 'https://images.unsplash.com/photo-1588667030534-a8f9c32e20b9?w=600&h=400&fit=crop',
    date: '05 avr. 2025',
    category: 'Résultats',
    title: 'Interclubs masculins : 3ème journée, notre équipe 1ère monte en N3',
    excerpt: 'Belle victoire 5-1 contre Boulogne-Billancourt. Notre équipe première confirme sa domination en poule et monte en N3 pour 2026.',
  },
]

const categories: Cat[] = ['Tous', 'Résultats', 'Club', 'Tennis', 'Padel', 'Fitness']

export default function ActualitesPage() {
  const [active, setActive] = useState<Cat>('Tous')

  const filtered = active === 'Tous' ? articles : articles.filter((a) => a.category === active)

  return (
    <>
      {/* Hero */}
      <section className="relative h-[45vh] min-h-[320px] flex items-end overflow-hidden">
        <Image
          src="https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1920&h=600&fit=crop"
          alt="Actualités TC Châtaigneraie"
          fill
          priority
          className="object-cover"
          sizes="100vw"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-dark/90 via-dark/50 to-dark/20" style={{ '--tw-gradient-from': '#0F1F17' } as React.CSSProperties} />

        <div className="relative z-10 container-wide pb-14 w-full">
          <motion.p className="label-tag text-white/50 mb-3" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}>
            Le club en direct
          </motion.p>
          <motion.h1
            className="font-cormorant font-light text-white"
            style={{ fontSize: 'clamp(3rem, 7vw, 6rem)', lineHeight: 0.95 }}
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
          >
            Actualités
          </motion.h1>
        </div>
      </section>

      {/* Filtres */}
      <section className="py-8 border-b" style={{ backgroundColor: 'white', borderColor: 'rgba(27,58,45,0.08)' }}>
        <div className="container-wide">
          <div className="flex flex-wrap items-center gap-3">
            <Filter size={14} style={{ color: '#7A7A72' }} />
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setActive(cat)}
                className="label-tag px-4 py-2 transition-all"
                style={{
                  backgroundColor: active === cat ? '#1B3A2D' : 'transparent',
                  color: active === cat ? 'white' : '#7A7A72',
                  border: `1px solid ${active === cat ? '#1B3A2D' : 'rgba(27,58,45,0.15)'}`,
                }}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Article à la une */}
      {active === 'Tous' && (
        <section className="pt-16 pb-8" style={{ backgroundColor: '#F7F4EF' }}>
          <div className="container-wide">
            <SectionHeader roman="I" label="À la une" title="Le dernier article" />
            <motion.div
              className="grid md:grid-cols-2 gap-8 bg-white overflow-hidden"
              style={{ boxShadow: '0 4px 24px rgba(15,31,23,0.08)' }}
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <div className="relative h-64 md:h-auto">
                <Image
                  src={articles[0].image}
                  alt={articles[0].title}
                  fill
                  className="object-cover"
                  sizes="(max-width: 768px) 100vw, 50vw"
                />
              </div>
              <div className="p-8 flex flex-col justify-center">
                <span className="label-tag mb-3" style={{ color: '#C9A84C' }}>{articles[0].date} · {articles[0].category}</span>
                <h2 className="font-cormorant text-3xl font-light mb-4" style={{ color: '#1B3A2D' }}>{articles[0].title}</h2>
                <p className="text-sm font-light leading-relaxed mb-6" style={{ color: '#7A7A72' }}>{articles[0].excerpt}</p>
                <a href={`/actualites/${articles[0].slug}`} className="btn-primary self-start">
                  Lire l'article
                </a>
              </div>
            </motion.div>
          </div>
        </section>
      )}

      {/* Grille articles */}
      <section className="py-12 pb-20" style={{ backgroundColor: '#F7F4EF' }}>
        <div className="container-wide">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {(active === 'Tous' ? filtered.slice(1) : filtered).map((article, i) => (
              <CardArticle key={article.slug} {...article} index={i} />
            ))}
          </div>
        </div>
      </section>
    </>
  )
}
