'use client'

import Image from 'next/image'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowRight, Clock, Calendar, Users } from 'lucide-react'
import SectionHeader from '@/components/ui/section-header'
import PricingCard from '@/components/ui/pricing-card'
import TennisCourtBg from '@/components/ui/tennis-court-bg'

const courts = [
  { id: 1, image: 'https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=800&h=500&fit=crop', label: 'Court central' },
  { id: 2, image: 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=800&h=500&fit=crop', label: 'Courts couverts' },
  { id: 3, image: 'https://images.unsplash.com/photo-1553068577-ef1e7f9bbc72?w=800&h=500&fit=crop', label: 'Vue panoramique' },
  { id: 4, image: 'https://images.unsplash.com/photo-1588667030534-a8f9c32e20b9?w=800&h=500&fit=crop', label: 'Éclairage nocturne' },
]

const pricing = [
  {
    hook: 'Jouez sans limite',
    title: 'Adhésion Adulte',
    price: '450€',
    period: 'par an · courts disponibles dès demain',
    features: [
      'Accès à tous les courts couverts',
      'Réservation en ligne 7j/7',
      'Accès club house et bar',
      'Tarifs préférentiels cours collectifs',
    ],
    cta: 'S\'inscrire',
  },
  {
    hook: 'L\'excellence dès le début',
    title: 'Adhésion Famille',
    price: '850€',
    period: 'par an · 2 adultes + enfants',
    features: [
      'Tout l\'offre adulte × 2',
      'École de tennis enfants incluse',
      'Stages vacances prioritaires',
      'Soirées famille mensuelles',
      'Casier vestiaire attribué',
    ],
    cta: 'Choisir la famille',
    highlighted: true,
  },
  {
    hook: 'Commencez l\'aventure',
    title: 'Adhésion Junior',
    price: '280€',
    period: 'par an · 6 à 17 ans',
    features: [
      'École de tennis (cours collectifs)',
      'Accès libre aux courts',
      'Tournois juniors internes',
      'Suivi par nos coaches diplômés',
    ],
    cta: 'Inscrire mon enfant',
  },
]

export default function TennisPage() {
  return (
    <>
      {/* Hero */}
      <section className="relative h-[60vh] min-h-[400px] flex items-end overflow-hidden">
        <Image
          src="https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=1920&h=800&fit=crop"
          alt="Courts tennis Châtaigneraie"
          fill
          priority
          className="object-cover"
          sizes="100vw"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-dark/90 via-dark/40 to-dark/20" style={{ '--tw-gradient-from': '#0F1F17' } as React.CSSProperties} />
        <TennisCourtBg className="text-white opacity-[0.05]" />

        <div className="relative z-10 container-wide pb-16 w-full">
          <motion.p
            className="label-tag text-white/50 mb-3"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Nos espaces · I / IV
          </motion.p>
          <motion.h1
            className="font-cormorant font-light text-white"
            style={{ fontSize: 'clamp(3rem, 7vw, 6rem)', lineHeight: 0.95 }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
          >
            Tennis
          </motion.h1>
          <motion.p
            className="font-cormorant italic text-2xl mt-2"
            style={{ color: '#C9A84C' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            VII courts couverts · Terre battue
          </motion.p>
        </div>
      </section>

      {/* Galerie courts */}
      <section className="section-padding" style={{ backgroundColor: '#F7F4EF' }}>
        <div className="container-wide">
          <SectionHeader
            roman="I"
            label="Nos installations"
            title="7 courts, zéro compromis"
            subtitle="Entièrement couverts, en terre battue, disponibles de 8h à 23h. Quel que soit le temps, votre court vous attend."
          />

          <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-12">
            {courts.map((court, i) => (
              <motion.div
                key={court.id}
                className={`relative overflow-hidden group ${i === 0 ? 'col-span-2 row-span-2' : ''}`}
                style={{ height: i === 0 ? '400px' : '195px' }}
                initial={{ opacity: 0, scale: 0.96 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
              >
                <Image
                  src={court.image}
                  alt={court.label}
                  fill
                  className="object-cover transition-transform duration-700 group-hover:scale-105"
                  sizes="(max-width: 768px) 50vw, 25vw"
                />
                <div className="absolute bottom-0 left-0 right-0 p-3 bg-gradient-to-t from-black/60 to-transparent">
                  <p className="label-tag text-white/70">{court.label}</p>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            {[
              { value: '7', label: 'Courts couverts' },
              { value: '100%', label: 'Terre battue' },
              { value: '8h–23h', label: 'Ouverture' },
              { value: '365j', label: 'Par an' },
            ].map((stat) => (
              <div key={stat.label} className="text-center p-6 bg-white" style={{ boxShadow: '0 2px 12px rgba(15,31,23,0.06)' }}>
                <p className="font-cormorant text-4xl font-light mb-1" style={{ color: '#1B3A2D' }}>{stat.value}</p>
                <p className="label-tag" style={{ color: '#7A7A72' }}>{stat.label}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* École de tennis */}
      <section className="section-padding" style={{ backgroundColor: 'white' }}>
        <div className="container-wide">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              <SectionHeader
                roman="II"
                label="École de tennis"
                title="Apprendre, progresser, exceller"
                subtitle="Nos coaches diplômés vous accompagnent, que vous soyez débutant, compétiteur ou que vous souhaitiez simplement retrouver le plaisir du jeu."
              />

              <div className="space-y-4 mb-8">
                {[
                  { icon: Users, title: 'Cours collectifs', desc: 'En petits groupes par niveau, adultes et enfants' },
                  { icon: Calendar, title: 'Stages vacances', desc: 'Stages intensifs été et toutes vacances scolaires' },
                  { icon: ArrowRight, title: 'Compétition', desc: 'Préparation circuits FFT, tournois interclubs' },
                ].map(({ icon: Icon, title, desc }) => (
                  <div key={title} className="flex gap-4 p-4 border border-transparent hover:border-gold transition-colors" style={{ borderColor: 'rgba(201,168,76,0)' }}>
                    <div className="w-10 h-10 flex items-center justify-center shrink-0" style={{ backgroundColor: 'rgba(201,168,76,0.12)' }}>
                      <Icon size={16} style={{ color: '#C9A84C' }} />
                    </div>
                    <div>
                      <p className="font-dm font-medium text-sm mb-0.5" style={{ color: '#1B3A2D' }}>{title}</p>
                      <p className="text-sm font-light" style={{ color: '#7A7A72' }}>{desc}</p>
                    </div>
                  </div>
                ))}
              </div>

              <Link href="/contact" className="btn-primary">
                Réserver mon premier cours <ArrowRight size={13} />
              </Link>
            </div>

            <div className="relative h-[400px] overflow-hidden">
              <Image
                src="https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=800&h=800&fit=crop"
                alt="École de tennis"
                fill
                className="object-cover"
                sizes="(max-width: 768px) 100vw, 50vw"
              />
              <div className="corner-decoration corner-br z-10" style={{ borderColor: '#C9A84C' }} />
            </div>
          </div>
        </div>
      </section>

      {/* Tarifs */}
      <section className="section-padding relative overflow-hidden" style={{ backgroundColor: '#F7F4EF' }}>
        <TennisCourtBg className="opacity-[0.035]" color="#1B3A2D" />
        <div className="relative z-10 container-wide">
          <SectionHeader
            roman="III"
            label="Tarifs"
            title="Investissez dans votre passion"
            subtitle="Des formules pour chaque profil, sans frais cachés."
            centered
          />
          <div className="grid md:grid-cols-3 gap-6">
            {pricing.map((plan, i) => (
              <PricingCard key={plan.title} {...plan} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* Horaires */}
      <section className="section-padding" style={{ backgroundColor: 'white' }}>
        <div className="container-wide">
          <div className="max-w-2xl mx-auto text-center">
            <SectionHeader
              roman="IV"
              label="Horaires"
              title="Toujours ouvert pour vous"
              centered
            />
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {[
                { period: 'Lundi – Vendredi', hours: '8h00 – 23h00' },
                { period: 'Samedi – Dimanche', hours: '8h00 – 22h00' },
                { period: 'Jours fériés', hours: '9h00 – 20h00' },
              ].map((h) => (
                <div key={h.period} className="p-6 border" style={{ borderColor: 'rgba(27,58,45,0.1)' }}>
                  <Clock size={18} className="mx-auto mb-3" style={{ color: '#C9A84C' }} />
                  <p className="label-tag mb-2" style={{ color: '#7A7A72' }}>{h.period}</p>
                  <p className="font-cormorant text-2xl font-light" style={{ color: '#1B3A2D' }}>{h.hours}</p>
                </div>
              ))}
            </div>

            <div className="mt-10">
              <Link href="/contact" className="btn-primary">
                Réserver un court maintenant <ArrowRight size={13} />
              </Link>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
