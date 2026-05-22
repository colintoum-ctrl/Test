'use client'

import Image from 'next/image'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { useState } from 'react'
import { ArrowRight, Filter } from 'lucide-react'
import SectionHeader from '@/components/ui/section-header'
import CardEvent from '@/components/ui/card-event'

type Category = 'Tous' | 'Tournois' | 'Cours collectifs' | 'Soirées club' | 'Stages'
type BadgeType = 'members' | 'open' | 'full'

const events = [
  {
    day: '07', month: 'Juin', year: '2025',
    title: 'Cours collectif découverte padel',
    description: 'Session ouverte à tous. Raquettes fournies, aucune expérience requise.',
    category: 'Cours collectifs',
    badge: 'open' as BadgeType,
  },
  {
    day: '14', month: 'Juin', year: '2025',
    title: 'Tournoi Interne Printemps',
    description: 'Simple et double mixte, toutes catégories membres. Inscription avant le 10 juin.',
    category: 'Tournois',
    badge: 'members' as BadgeType,
  },
  {
    day: '21', month: 'Juin', year: '2025',
    title: 'Open Padel Châtaigneraie',
    description: 'Premier open padel du club. Inscriptions par équipes de 2.',
    category: 'Tournois',
    badge: 'open' as BadgeType,
  },
  {
    day: '27', month: 'Juin', year: '2025',
    title: 'Soirée Apéro Tennis',
    description: 'Vendredi soir au club house. Matchs amicaux suivis d\'un apéritif partagé en terrasse.',
    category: 'Soirées club',
    badge: 'members' as BadgeType,
  },
  {
    day: '05', month: 'Jul', year: '2025',
    title: 'Stage Intensif Été — Junior',
    description: 'Stage tennis 5 jours pour les 10-17 ans. Techniques, matchs, tournoi final.',
    category: 'Stages',
    badge: 'open' as BadgeType,
  },
  {
    day: '12', month: 'Jul', year: '2025',
    title: 'Championnat Interne Été',
    description: 'Tableaux toutes catégories. Le grand tournoi interne de l\'été, sur 3 weekends.',
    category: 'Tournois',
    badge: 'members' as BadgeType,
  },
  {
    day: '19', month: 'Jul', year: '2025',
    title: 'Stage Adultes Perfectionnement',
    description: 'Stage intensif adultes 3 jours. Focus placement, jeu en fond de court, montée au filet.',
    category: 'Stages',
    badge: 'open' as BadgeType,
  },
  {
    day: '26', month: 'Jul', year: '2025',
    title: 'Tournoi de Doubles Mixtes',
    description: 'Formule conviviale en doubles mixtes. Tirage au sort des équipes pour mélanger les niveaux.',
    category: 'Tournois',
    badge: 'full' as BadgeType,
  },
  {
    day: '09', month: 'Août', year: '2025',
    title: 'Nuit du Padel',
    description: 'Tournoi nocturne padel de 20h à minuit. Ambiance festive, music & bar.',
    category: 'Soirées club',
    badge: 'open' as BadgeType,
  },
]

const pastEvents = [
  {
    src: 'https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=400&h=300&fit=crop',
    title: 'Tournoi Printemps 2024',
  },
  {
    src: 'https://images.unsplash.com/photo-1622163642998-1ea32b0bbc67?w=400&h=300&fit=crop',
    title: 'Open Padel Mars 2025',
  },
  {
    src: 'https://images.unsplash.com/photo-1567427017947-545c5f8d16ad?w=400&h=300&fit=crop',
    title: 'Soirée Gala 2024',
  },
]

const categories: Category[] = ['Tous', 'Tournois', 'Cours collectifs', 'Soirées club', 'Stages']

export default function EvenementsPage() {
  const [activeCategory, setActiveCategory] = useState<Category>('Tous')

  const filtered = activeCategory === 'Tous'
    ? events
    : events.filter((e) => e.category === activeCategory)

  return (
    <>
      {/* Hero */}
      <section className="relative h-[50vh] min-h-[360px] flex items-end overflow-hidden">
        <Image
          src="https://images.unsplash.com/photo-1529926706528-db9e5010cd3e?w=1920&h=700&fit=crop"
          alt="Événements TC Châtaigneraie"
          fill
          priority
          className="object-cover"
          sizes="100vw"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-dark/90 via-dark/50 to-dark/20" style={{ '--tw-gradient-from': '#0F1F17' } as React.CSSProperties} />

        <div className="relative z-10 container-wide pb-16 w-full">
          <motion.p className="label-tag text-white/50 mb-3" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}>
            Agenda du club
          </motion.p>
          <motion.h1
            className="font-cormorant font-light text-white"
            style={{ fontSize: 'clamp(3rem, 7vw, 6rem)', lineHeight: 0.95 }}
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
          >
            Événements & Tournois
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
                onClick={() => setActiveCategory(cat)}
                className="label-tag px-4 py-2 transition-all"
                style={{
                  backgroundColor: activeCategory === cat ? '#1B3A2D' : 'transparent',
                  color: activeCategory === cat ? 'white' : '#7A7A72',
                  border: `1px solid ${activeCategory === cat ? '#1B3A2D' : 'rgba(27,58,45,0.15)'}`,
                }}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      </section>

      {/* Grille événements */}
      <section className="section-padding" style={{ backgroundColor: '#F7F4EF' }}>
        <div className="container-wide">
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filtered.map((event, i) => (
              <CardEvent key={event.title + event.day} {...event} index={i} />
            ))}
          </div>

          {filtered.length === 0 && (
            <div className="text-center py-16">
              <p className="font-cormorant text-2xl font-light" style={{ color: '#7A7A72' }}>
                Aucun événement dans cette catégorie.
              </p>
            </div>
          )}
        </div>
      </section>

      {/* Événements passés */}
      <section className="section-padding" style={{ backgroundColor: 'white' }}>
        <div className="container-wide">
          <SectionHeader
            roman="II"
            label="Archives"
            title="Événements passés"
          />

          <div className="grid md:grid-cols-3 gap-4">
            {pastEvents.map((ev, i) => (
              <motion.div
                key={ev.title}
                className="relative h-52 overflow-hidden group"
                initial={{ opacity: 0, scale: 0.95 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
              >
                <Image src={ev.src} alt={ev.title} fill className="object-cover transition-transform duration-700 group-hover:scale-105" sizes="33vw" />
                <div className="absolute inset-0 bg-gradient-to-t from-dark/70 to-transparent flex items-end p-5" style={{ '--tw-gradient-from': '#0F1F17' } as React.CSSProperties}>
                  <p className="font-cormorant text-lg font-light text-white">{ev.title}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA inscription */}
      <section className="py-20 relative overflow-hidden" style={{ backgroundColor: '#1B3A2D' }}>
        <div className="container-wide text-center">
          <p className="label-tag mb-4" style={{ color: '#C9A84C' }}>Participez</p>
          <h2 className="font-cormorant text-4xl font-light text-white mb-4">
            Vous organisez un événement ?
          </h2>
          <p className="text-sm font-light mb-8" style={{ color: 'rgba(255,255,255,0.55)' }}>
            Séminaire d'entreprise, tournoi privé, anniversaire — nos installations sont disponibles à la privatisation.
          </p>
          <Link href="/contact" className="btn-outline-white">
            Nous contacter <ArrowRight size={13} />
          </Link>
        </div>
      </section>
    </>
  )
}
