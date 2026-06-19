'use client'

import Image from 'next/image'
import Link from 'next/link'
import { motion } from 'framer-motion'
import { ArrowRight, Zap, Trophy, Users } from 'lucide-react'
import SectionHeader from '@/components/ui/section-header'
import TennisCourtBg from '@/components/ui/tennis-court-bg'

export default function PadelPage() {
  return (
    <>
      {/* Hero */}
      <section className="relative h-[60vh] min-h-[400px] flex items-end overflow-hidden">
        <Image
          src="https://images.unsplash.com/photo-1622163642998-1ea32b0bbc67?w=1920&h=800&fit=crop"
          alt="Pistes padel Châtaigneraie"
          fill
          priority
          className="object-cover"
          sizes="100vw"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-dark/90 via-dark/50 to-dark/20" style={{ '--tw-gradient-from': '#0F1F17' } as React.CSSProperties} />

        <div className="relative z-10 container-wide pb-16 w-full">
          <motion.p
            className="label-tag text-white/50 mb-3"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            Nos espaces · II / IV
          </motion.p>
          <motion.h1
            className="font-cormorant font-light text-white"
            style={{ fontSize: 'clamp(3rem, 7vw, 6rem)', lineHeight: 0.95 }}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
          >
            Padel
          </motion.h1>
          <motion.p
            className="font-cormorant italic text-2xl mt-2"
            style={{ color: '#C9A84C' }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            IV pistes couvertes · Dernière génération
          </motion.p>
        </div>
      </section>

      {/* Présentation */}
      <section className="section-padding" style={{ backgroundColor: '#F7F4EF' }}>
        <div className="container-wide">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              <SectionHeader
                roman="I"
                label="Le padel au club"
                title="Le sport qui réunit"
                subtitle="Le padel est le sport de raquette qui grandit le plus vite en France. Accessible, social, intense — il plaît à tous, dès la première session."
              />

              <p className="text-sm font-light leading-relaxed mb-6" style={{ color: '#7A7A72' }}>
                Nos 4 pistes couvertes et éclairées sont équipées des installations de dernière génération.
                Vitres panoramiques, sol antidérapant professionnel, éclairage LED — les conditions de jeu sont optimales 365 jours par an.
              </p>

              <div className="space-y-4 mb-8">
                {[
                  { icon: Zap, text: '4 pistes couvertes, éclairées toute l\'année' },
                  { icon: Users, text: 'Cours d\'initiation pour débutants complets' },
                  { icon: Trophy, text: 'Tournois internes et open mensuels' },
                ].map(({ icon: Icon, text }) => (
                  <div key={text} className="flex gap-3 items-center">
                    <Icon size={16} style={{ color: '#C9A84C' }} />
                    <p className="text-sm font-light" style={{ color: '#7A7A72' }}>{text}</p>
                  </div>
                ))}
              </div>

              {/* Offre découverte */}
              <div className="p-5 mb-6" style={{ backgroundColor: 'rgba(201,168,76,0.08)', borderLeft: '2px solid #C9A84C' }}>
                <p className="label-tag mb-1" style={{ color: '#C9A84C' }}>Offre découverte</p>
                <p className="font-cormorant text-xl font-light" style={{ color: '#1B3A2D' }}>
                  Premier cours offert pour les nouveaux membres
                </p>
              </div>

              <Link href="/contact" className="btn-primary">
                Réserver une piste <ArrowRight size={13} />
              </Link>
            </div>

            {/* Galerie */}
            <div className="grid grid-cols-2 gap-3">
              {[
                'https://images.unsplash.com/photo-1622163642998-1ea32b0bbc67?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1629901925121-8a141c2a42f4?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=600&h=400&fit=crop',
                'https://images.unsplash.com/photo-1571902943202-507ec2618e8f?w=600&h=400&fit=crop',
              ].map((src, i) => (
                <motion.div
                  key={i}
                  className="relative h-40 overflow-hidden"
                  initial={{ opacity: 0, scale: 0.95 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  viewport={{ once: true }}
                  transition={{ duration: 0.5, delay: i * 0.1 }}
                >
                  <Image src={src} alt={`Padel ${i + 1}`} fill className="object-cover" sizes="25vw" />
                </motion.div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Cours & Tournois */}
      <section className="section-padding" style={{ backgroundColor: 'white' }}>
        <div className="container-wide">
          <SectionHeader
            roman="II"
            label="Pratique"
            title="Votre programme padel"
          />

          <div className="grid md:grid-cols-3 gap-6">
            {[
              {
                number: '01',
                title: 'Initiation',
                desc: 'Vous n\'avez jamais joué ? Nos coaches vous apprennent les bases en 2h. Raquettes fournies. Premier cours offert.',
                cta: 'Je m\'inscris',
              },
              {
                number: '02',
                title: 'Cours collectifs',
                desc: 'En groupes de 4 par niveau, 1 à 2 fois par semaine. Perfectionnement technique et tactique.',
                cta: 'Voir les créneaux',
              },
              {
                number: '03',
                title: 'Tournois & Compétitions',
                desc: 'Open mensuel, tournois interclubs, padel apéro le vendredi soir. La vie du club en double.',
                cta: 'Prochain tournoi',
              },
            ].map((item, i) => (
              <motion.div
                key={item.title}
                className="relative p-8 border"
                style={{ borderColor: 'rgba(27,58,45,0.1)' }}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: i * 0.12 }}
                whileHover={{ y: -4, boxShadow: '0 8px 40px rgba(15,31,23,0.1)' }}
              >
                <span
                  className="font-cormorant text-6xl font-light block mb-4"
                  style={{ color: 'rgba(201,168,76,0.2)' }}
                >
                  {item.number}
                </span>
                <h3 className="font-cormorant text-2xl font-light mb-3" style={{ color: '#1B3A2D' }}>
                  {item.title}
                </h3>
                <p className="text-sm font-light leading-relaxed mb-5" style={{ color: '#7A7A72' }}>
                  {item.desc}
                </p>
                <Link href="/contact" className="label-tag inline-flex items-center gap-2 hover:gap-3 transition-all" style={{ color: '#C9A84C' }}>
                  {item.cta} <ArrowRight size={11} />
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Tarifs padel */}
      <section className="section-padding relative overflow-hidden" style={{ backgroundColor: '#1B3A2D' }}>
        <TennisCourtBg className="text-white opacity-[0.04]" />
        <div className="relative z-10 container-wide">
          <SectionHeader
            roman="III"
            label="Tarifs padel"
            title="Des tarifs accessibles"
            light
          />
          <div className="grid md:grid-cols-2 gap-8 max-w-2xl">
            {[
              { label: 'Location piste · 1h', price: '20€', note: 'Hors heures de pointe' },
              { label: 'Location piste · 1h', price: '28€', note: 'Heures de pointe (18h–22h)' },
              { label: 'Cours collectifs · 1h30', price: '18€', note: 'Par personne, min 4 joueurs' },
              { label: 'Cours particulier · 1h', price: '60€', note: 'Avec coach diplômé' },
            ].map((item) => (
              <div key={item.label + item.note} className="flex items-end justify-between border-b py-5" style={{ borderColor: 'rgba(255,255,255,0.1)' }}>
                <div>
                  <p className="font-cormorant text-xl font-light text-white">{item.label}</p>
                  <p className="label-tag mt-1" style={{ color: 'rgba(255,255,255,0.35)' }}>{item.note}</p>
                </div>
                <p className="font-cormorant text-3xl font-light" style={{ color: '#C9A84C' }}>{item.price}</p>
              </div>
            ))}
          </div>

          <div className="mt-10">
            <Link href="/contact" className="btn-outline-white">
              Essayez le padel <ArrowRight size={13} />
            </Link>
          </div>
        </div>
      </section>
    </>
  )
}
