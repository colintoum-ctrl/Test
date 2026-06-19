'use client'

import Image from 'next/image'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowRight, Dumbbell, Heart, Zap, Timer, Users, Star } from 'lucide-react'
import SectionHeader from '@/components/ui/section-header'
import TennisCourtBg from '@/components/ui/tennis-court-bg'

const equipments = [
  { icon: Heart, label: 'Cardio', items: ['Tapis de course · 8 postes', 'Vélos elliptiques · 6 postes', 'Rameurs professionnels', 'Vélos de spinning'] },
  { icon: Dumbbell, label: 'Musculation', items: ['Appareils guidés 20 stations', 'Espace haltères libre', 'Barres & disques Olympic', 'Bancs multifonctions'] },
  { icon: Users, label: 'Cours collectifs', items: ['Yoga · 3×/semaine', 'Pilates · 2×/semaine', 'HIIT · 4×/semaine', 'Étirements & mobilité'] },
  { icon: Star, label: 'Services', items: ['Coaches personnels diplômés', 'Bilan forme offert', 'Vestiaires & douches premium', 'Serviettes fournies'] },
]

const fitnessImages = [
  { src: 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=800&h=600&fit=crop', alt: 'Salle de fitness moderne', featured: true },
  { src: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=300&fit=crop', alt: 'Cardio training' },
  { src: 'https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=400&h=300&fit=crop', alt: 'Musculation' },
  { src: 'https://images.unsplash.com/photo-1518611012118-696072aa579a?w=400&h=300&fit=crop', alt: 'Cours collectifs' },
]

export default function FitnessPage() {
  return (
    <>
      {/* Hero */}
      <section className="relative h-[65vh] min-h-[420px] flex items-end overflow-hidden">
        <Image
          src="https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1920&h=900&fit=crop"
          alt="Espace fitness Châtaigneraie"
          fill
          priority
          className="object-cover"
          sizes="100vw"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-dark/95 via-dark/50 to-dark/15" style={{ '--tw-gradient-from': '#0F1F17' } as React.CSSProperties} />

        <div className="relative z-10 container-wide pb-16 w-full">
          <motion.p
            className="label-tag text-white/50 mb-3"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Nos espaces · III / IV
          </motion.p>
          <motion.h1
            className="font-cormorant font-light text-white"
            style={{ fontSize: 'clamp(3rem, 7vw, 6rem)', lineHeight: 0.95 }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
          >
            Fitness
          </motion.h1>
          <motion.p
            className="font-cormorant italic text-2xl mt-2 mb-6"
            style={{ color: '#C9A84C' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            Votre performance commence ici
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.7 }}
          >
            <Link href="/contact" className="btn-outline-white">
              Essai gratuit <ArrowRight size={13} />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Accroche + galerie */}
      <section className="section-padding" style={{ backgroundColor: '#F7F4EF' }}>
        <div className="container-wide">
          {/* Grille d'images */}
          <div className="grid grid-cols-2 md:grid-cols-3 gap-3 mb-16">
            {fitnessImages.map((img, i) => (
              <motion.div
                key={img.alt}
                className={`relative overflow-hidden group ${img.featured ? 'row-span-2 col-span-2 md:col-span-1 md:row-span-2' : ''}`}
                style={{ height: img.featured ? '420px' : '200px' }}
                initial={{ opacity: 0, scale: 0.96 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.08 }}
              >
                <Image
                  src={img.src}
                  alt={img.alt}
                  fill
                  className="object-cover transition-transform duration-700 group-hover:scale-105"
                  sizes="(max-width: 768px) 50vw, 33vw"
                />
              </motion.div>
            ))}
          </div>

          {/* 3 phrases clés */}
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: Zap, stat: '200m²', text: 'Un espace de 200m² entièrement rénové, lumineux, ventilé.' },
              { icon: Timer, stat: '8h–23h', text: 'Ouvert tous les jours. Avant le travail, après le tennis, quand vous voulez.' },
              { icon: Dumbbell, stat: '40+', text: 'Plus de 40 machines professionnelles pour tous niveaux.' },
            ].map(({ icon: Icon, stat, text }) => (
              <motion.div
                key={stat}
                className="flex flex-col items-center text-center"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5 }}
              >
                <div className="w-12 h-12 flex items-center justify-center mb-4" style={{ backgroundColor: 'rgba(201,168,76,0.12)' }}>
                  <Icon size={20} style={{ color: '#C9A84C' }} />
                </div>
                <p className="font-cormorant text-4xl font-light mb-2" style={{ color: '#1B3A2D' }}>{stat}</p>
                <p className="text-sm font-light leading-relaxed" style={{ color: '#7A7A72' }}>{text}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Équipements */}
      <section className="section-padding" style={{ backgroundColor: 'white' }}>
        <div className="container-wide">
          <SectionHeader
            roman="I"
            label="Équipements"
            title="Tout pour performer"
            subtitle="Des équipements professionnels organisés en zones distinctes pour une expérience optimale."
          />

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {equipments.map(({ icon: Icon, label, items }, i) => (
              <motion.div
                key={label}
                className="p-6 relative"
                style={{ backgroundColor: '#F7F4EF' }}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.5, delay: i * 0.1 }}
              >
                <div className="corner-decoration corner-tl" />
                <div className="w-10 h-10 flex items-center justify-center mb-5" style={{ backgroundColor: '#1B3A2D' }}>
                  <Icon size={18} className="text-white" />
                </div>
                <p className="label-tag mb-4" style={{ color: '#C9A84C' }}>{label}</p>
                <ul className="space-y-2">
                  {items.map((item) => (
                    <li key={item} className="text-sm font-light flex items-start gap-2" style={{ color: '#7A7A72' }}>
                      <span className="mt-2 w-1 h-1 rounded-full shrink-0" style={{ backgroundColor: '#C9A84C' }} />
                      {item}
                    </li>
                  ))}
                </ul>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Coaching perso */}
      <section className="section-padding relative overflow-hidden" style={{ backgroundColor: '#1B3A2D' }}>
        <TennisCourtBg className="text-white opacity-[0.04]" />
        <div className="relative z-10 container-wide">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              <SectionHeader
                roman="II"
                label="Coaching"
                title="Accompagné par un expert"
                subtitle="Nos coaches certifiés conçoivent votre programme sur mesure, suivent vos progrès et ajustent votre entraînement en temps réel."
                light
              />
              <Link href="/contact" className="btn-outline-white">
                Réserver un bilan offert <ArrowRight size={13} />
              </Link>
            </div>

            <div className="relative h-72 overflow-hidden">
              <Image
                src="https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=800&h=600&fit=crop"
                alt="Coach fitness"
                fill
                className="object-cover"
                sizes="(max-width: 768px) 100vw, 50vw"
              />
              <div className="absolute inset-0 flex items-end p-6 bg-gradient-to-t from-dark/60 to-transparent" style={{ '--tw-gradient-from': '#0F1F17' } as React.CSSProperties}>
                <div>
                  <p className="label-tag text-white/50 mb-1">Inclus dans votre adhésion</p>
                  <p className="font-cormorant text-xl font-light text-white">Bilan forme offert à l'inscription</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA final */}
      <section className="py-20 text-center" style={{ backgroundColor: '#F7F4EF' }}>
        <div className="container-wide">
          <p className="label-tag mb-4" style={{ color: '#C9A84C' }}>Premier pas</p>
          <h2 className="font-cormorant text-4xl font-light mb-6" style={{ color: '#1B3A2D' }}>
            Prêt à vous dépasser ?
          </h2>
          <p className="text-sm font-light mb-8 max-w-md mx-auto" style={{ color: '#7A7A72' }}>
            Essai gratuit sans engagement. Venez visiter l'espace, rencontrer nos coaches, essayer les machines.
          </p>
          <Link href="/contact" className="btn-primary">
            Visiter l'espace fitness <ArrowRight size={13} />
          </Link>
        </div>
      </section>
    </>
  )
}
