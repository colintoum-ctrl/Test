'use client'

import Image from 'next/image'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowRight, Coffee, Utensils, Wind, Star } from 'lucide-react'
import SectionHeader from '@/components/ui/section-header'
import TennisCourtBg from '@/components/ui/tennis-court-bg'

const spaces = [
  {
    icon: Coffee,
    title: 'Bar & Lounge',
    description: 'Boissons chaudes, cocktails, bières artisanales. Notre bar accueille membres et invités dans une ambiance chaleureuse, avant ou après le jeu.',
    image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&h=400&fit=crop',
  },
  {
    icon: Wind,
    title: 'Terrasse panoramique',
    description: 'Vue directe sur les courts. Un espace ensoleillé pour profiter du club entre les matchs, idéal pour observer les rencontres depuis la hauteur.',
    image: 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=600&h=400&fit=crop',
  },
  {
    icon: Star,
    title: 'Vestiaires premium',
    description: 'Vestiaires séparés hommes/femmes, douches individuelles, casiers sécurisés. Un niveau de confort rare dans les clubs parisiens.',
    image: 'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=600&h=400&fit=crop',
  },
  {
    icon: Utensils,
    title: 'Restauration',
    description: 'Petite restauration le midi et en soirée. Sandwiches, salades, formules légères pour déjeuner entre amis avant de reprendre le court.',
    image: 'https://images.unsplash.com/photo-1600891964092-4316c288032e?w=600&h=400&fit=crop',
  },
]

export default function ClubHousePage() {
  return (
    <>
      {/* Hero */}
      <section className="relative h-[60vh] min-h-[400px] flex items-end overflow-hidden">
        <Image
          src="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1920&h=800&fit=crop"
          alt="Club House Châtaigneraie"
          fill
          priority
          className="object-cover"
          sizes="100vw"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-dark/90 via-dark/40 to-dark/15" style={{ '--tw-gradient-from': '#0F1F17' } as React.CSSProperties} />

        <div className="relative z-10 container-wide pb-16 w-full">
          <motion.p className="label-tag text-white/50 mb-3" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}>
            Nos espaces · IV / IV
          </motion.p>
          <motion.h1
            className="font-cormorant font-light text-white"
            style={{ fontSize: 'clamp(3rem, 7vw, 6rem)', lineHeight: 0.95 }}
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
          >
            Club House
          </motion.h1>
          <motion.p className="font-cormorant italic text-2xl mt-2" style={{ color: '#C9A84C' }} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}>
            Bar · Terrasse · Vestiaires premium
          </motion.p>
        </div>
      </section>

      {/* Espaces */}
      <section className="section-padding" style={{ backgroundColor: '#F7F4EF' }}>
        <div className="container-wide">
          <SectionHeader
            roman="I"
            label="Nos espaces"
            title="La vie de club, réinventée"
            subtitle="Un club, c'est aussi un lieu de vie. Notre club house réunit tout ce qui fait l'esprit d'appartenance."
          />

          <div className="grid md:grid-cols-2 gap-8">
            {spaces.map(({ icon: Icon, title, description, image }, i) => (
              <motion.div
                key={title}
                className="group relative bg-white overflow-hidden"
                style={{ boxShadow: '0 4px 24px rgba(15,31,23,0.07)' }}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: i * 0.1 }}
                whileHover={{ y: -4 }}
              >
                <div className="corner-decoration corner-tl" />
                <div className="relative h-48 overflow-hidden">
                  <Image src={image} alt={title} fill className="object-cover transition-transform duration-700 group-hover:scale-105" sizes="(max-width: 768px) 100vw, 50vw" />
                </div>
                <div className="p-6">
                  <div className="flex items-center gap-3 mb-3">
                    <Icon size={16} style={{ color: '#C9A84C' }} />
                    <p className="label-tag" style={{ color: '#C9A84C' }}>{title}</p>
                  </div>
                  <p className="text-sm font-light leading-relaxed" style={{ color: '#7A7A72' }}>{description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Ambiance */}
      <section className="section-padding relative overflow-hidden" style={{ backgroundColor: '#1B3A2D' }}>
        <TennisCourtBg className="text-white opacity-[0.04]" />
        <div className="relative z-10 container-wide text-center">
          <SectionHeader roman="II" label="L'esprit du club" title="Votre club, votre communauté" centered light />
          <p className="text-sm font-light max-w-xl mx-auto mb-10" style={{ color: 'rgba(255,255,255,0.55)' }}>
            Plus de 60 ans de convivialité, de matchs mémorables et d'amitiés nées sur les courts. Le club house, c'est l'endroit où tout ça continue.
          </p>
          <Link href="/contact" className="btn-outline-white">
            Devenir membre <ArrowRight size={13} />
          </Link>
        </div>
      </section>
    </>
  )
}
