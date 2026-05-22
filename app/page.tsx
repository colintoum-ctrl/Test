'use client'

import Image from 'next/image'
import Link from 'next/link'
import { motion, useInView } from 'framer-motion'
import { useRef, useEffect, useState } from 'react'
import { ArrowRight, ChevronDown, Quote } from 'lucide-react'
import SectionHeader from '@/components/ui/section-header'
import CardSpace from '@/components/ui/card-space'
import CardEvent from '@/components/ui/card-event'
import InstagramGrid from '@/components/ui/instagram-grid'
import TennisCourtBg from '@/components/ui/tennis-court-bg'

function AnimatedNumber({ target, duration = 2 }: { target: number; duration?: number }) {
  const [count, setCount] = useState(0)
  const ref = useRef(null)
  const inView = useInView(ref, { once: true })

  useEffect(() => {
    if (!inView) return
    let start = 0
    const step = target / (duration * 60)
    const interval = setInterval(() => {
      start += step
      if (start >= target) {
        setCount(target)
        clearInterval(interval)
      } else {
        setCount(Math.floor(start))
      }
    }, 1000 / 60)
    return () => clearInterval(interval)
  }, [inView, target, duration])

  return <span ref={ref}>{count}</span>
}

const spaces = [
  {
    roman: 'I',
    title: 'Tennis',
    stat: 'VII Courts · Couverts · Terre battue',
    description: '7 courts en terre battue intégralement couverts. Jouez sous la pluie, la nuit, toute l\'année — sans exception.',
    image: 'https://images.unsplash.com/photo-1595435934249-5df7ed86e1c0?w=640&h=448&fit=crop',
    href: '/tennis',
  },
  {
    roman: 'II',
    title: 'Padel',
    stat: 'IV Pistes · Couvertes · Dernière génération',
    description: '4 pistes couvertes et éclairées. Le padel nouvelle génération, accessible aux débutants comme aux compétiteurs.',
    image: 'https://images.unsplash.com/photo-1622163642998-1ea32b0bbc67?w=640&h=448&fit=crop',
    href: '/padel',
  },
  {
    roman: 'III',
    title: 'Fitness',
    stat: 'Espace · Cardio & Musculation',
    description: 'Équipements professionnels, espace cardio, salle de musculation. Votre performance commence ici.',
    image: 'https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=640&h=448&fit=crop',
    href: '/fitness',
  },
  {
    roman: 'IV',
    title: 'Club House',
    stat: 'Bar · Terrasse · Vestiaires premium',
    description: 'Un espace de vie à part entière. Bar, terrasse panoramique, vestiaires haut de gamme. Le club après le club.',
    image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=640&h=448&fit=crop',
    href: '/club-house',
  },
]

const events = [
  {
    day: '14',
    month: 'Juin',
    year: '2025',
    title: 'Tournoi Interne Printemps',
    description: 'Simple et double mixte, toutes catégories. Un tournoi convivial ouvert à tous les membres du club.',
    category: 'Tournoi',
    badge: 'members' as const,
  },
  {
    day: '21',
    month: 'Juin',
    year: '2025',
    title: 'Open Padel Châtaigneraie',
    description: 'Premier open padel du club. Inscriptions par équipes de 2, toutes catégories bienvenues.',
    category: 'Padel',
    badge: 'open' as const,
  },
  {
    day: '05',
    month: 'Jul',
    year: '2025',
    title: 'Stage Intensif Été — Junior',
    description: 'Stage tennis encadré par nos coaches pour les 10-17 ans. Techniques, matchs, convivialité.',
    category: 'Stage',
    badge: 'open' as const,
  },
]

export default function HomePage() {
  return (
    <>
      {/* ──────────── HERO ──────────── */}
      <section className="relative h-screen min-h-[600px] flex items-center overflow-hidden">
        <Image
          src="https://images.unsplash.com/photo-1581091226033-d5c48150dbaa?w=1920&h=1080&fit=crop"
          alt="Courts couverts TC Châtaigneraie"
          fill
          priority
          className="object-cover"
          sizes="100vw"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-dark/70 via-dark/40 to-dark/85" style={{ '--tw-gradient-from': '#0F1F17' } as React.CSSProperties} />

        {/* Tennis court pattern */}
        <TennisCourtBg className="text-white opacity-[0.04]" />

        <div className="relative z-10 container-wide w-full">
          <div className="max-w-3xl">
            <motion.p
              className="label-tag text-white/50 mb-6"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
            >
              Un lieu d'exception · Rueil-Malmaison
            </motion.p>

            <div className="overflow-hidden mb-2">
              <motion.h1
                className="font-cormorant font-light text-white leading-none"
                style={{ fontSize: 'clamp(3.5rem, 8vw, 7rem)' }}
                initial={{ x: -80, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ duration: 0.9, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
              >
                La Châtaigneraie
              </motion.h1>
            </div>
            <div className="overflow-hidden mb-10">
              <motion.p
                className="font-cormorant italic font-light"
                style={{ fontSize: 'clamp(2rem, 5vw, 4.5rem)', color: '#C9A84C' }}
                initial={{ x: 80, opacity: 0 }}
                animate={{ x: 0, opacity: 1 }}
                transition={{ duration: 0.9, delay: 0.5, ease: [0.22, 1, 0.36, 1] }}
              >
                depuis 1963
              </motion.p>
            </div>

            <motion.div
              className="flex flex-wrap items-center gap-4"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.7, delay: 0.8 }}
            >
              <Link href="/tennis" className="btn-outline-white">
                Découvrir le club
              </Link>
              <Link
                href="/contact"
                className="inline-flex items-center gap-2 text-white/70 hover:text-white transition-colors font-dm text-sm tracking-widest uppercase"
              >
                Réserver un court <ArrowRight size={14} />
              </Link>
            </motion.div>
          </div>
        </div>

        {/* Stats bar */}
        <motion.div
          className="absolute bottom-0 left-0 right-0 border-t border-white/10"
          style={{ backgroundColor: 'rgba(15,31,23,0.6)', backdropFilter: 'blur(8px)' }}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.7, delay: 1.2 }}
        >
          <div className="container-wide">
            <div className="grid grid-cols-2 md:grid-cols-4 divide-x divide-white/10">
              {[
                { number: 7, suffix: '', label: 'Courts couverts' },
                { number: 4, suffix: '', label: 'Pistes padel' },
                { number: 1963, suffix: '', label: 'Année de fondation' },
                { number: 365, suffix: 'j/an', label: 'Ouvert' },
              ].map((stat) => (
                <div key={stat.label} className="py-5 px-6 text-center">
                  <p className="font-cormorant text-3xl font-light text-white">
                    <AnimatedNumber target={stat.number} />
                    <span className="text-lg">{stat.suffix}</span>
                  </p>
                  <p className="label-tag text-white/40 mt-1">{stat.label}</p>
                </div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          className="absolute bottom-28 right-8 md:right-12 flex flex-col items-center gap-2"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.5 }}
        >
          <motion.div
            animate={{ y: [0, 8, 0] }}
            transition={{ duration: 2, repeat: Infinity, ease: 'easeInOut' }}
          >
            <ChevronDown size={20} className="text-white/40" />
          </motion.div>
          <div className="w-px h-12 bg-gradient-to-b from-white/30 to-transparent" />
        </motion.div>
      </section>

      {/* ──────────── QUI SOMMES-NOUS ──────────── */}
      <section id="qui-sommes-nous" className="section-padding" style={{ backgroundColor: '#F7F4EF' }}>
        <div className="container-wide">
          <div className="grid md:grid-cols-2 gap-16 items-center">
            <div>
              <SectionHeader
                roman="I"
                label="Notre histoire"
                title="Plus qu'un club, une institution"
                subtitle="Fondé en 1963 à Rueil-Malmaison, le Tennis Club de la Châtaigneraie est l'un des clubs les plus prestigieux d'Île-de-France."
              />
              <p className="text-sm font-light leading-relaxed mb-6" style={{ color: '#7A7A72' }}>
                Depuis plus de 60 ans, nous cultivons un équilibre unique entre excellence sportive et art de vivre à la française.
                Nos installations — 7 courts couverts en terre battue, 4 pistes de padel — accueillent amateurs et compétiteurs dans un cadre verdoyant exceptionnel.
              </p>

              {/* Citation bloc */}
              <div
                className="relative p-6 mb-8"
                style={{ backgroundColor: '#1B3A2D', borderLeft: '2px solid #C9A84C' }}
              >
                <Quote size={20} className="mb-3 opacity-30 text-white" />
                <p className="font-cormorant italic text-xl font-light text-white leading-relaxed mb-3">
                  "Un club où l'on revient toujours avec plaisir. L'ambiance, les courts, le niveau — tout est réuni."
                </p>
                <p className="label-tag text-white/40">Membre depuis 2018</p>
              </div>

              <Link href="/#histoire" className="btn-outline">
                Notre histoire complète <ArrowRight size={13} />
              </Link>
            </div>

            <div className="relative">
              <div className="relative h-[480px] overflow-hidden">
                <Image
                  src="https://images.unsplash.com/photo-1567427017947-545c5f8d16ad?w=800&h=960&fit=crop"
                  alt="Courts de tennis Châtaigneraie"
                  fill
                  className="object-cover"
                  sizes="(max-width: 768px) 100vw, 50vw"
                />
              </div>
              {/* Floating notoriety card */}
              <motion.div
                className="absolute -bottom-6 -left-6 bg-white p-5 shadow-card"
                initial={{ opacity: 0, x: -20 }}
                whileInView={{ opacity: 1, x: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: 0.4 }}
              >
                <p className="label-tag mb-2" style={{ color: '#C9A84C' }}>Ils nous ont fait confiance</p>
                <div className="flex flex-col gap-1">
                  {['Yannick Noah', 'Amélie Mauresmo', 'Jo-Wilfried Tsonga'].map((name) => (
                    <p key={name} className="font-cormorant text-lg font-light" style={{ color: '#1B3A2D' }}>
                      {name}
                    </p>
                  ))}
                </div>
              </motion.div>
            </div>
          </div>
        </div>
      </section>

      {/* ──────────── NOS ESPACES ──────────── */}
      <section className="section-padding overflow-hidden" style={{ backgroundColor: 'white' }}>
        <div className="container-wide">
          <SectionHeader
            roman="II"
            label="Nos espaces"
            title="Un club, quatre univers"
            subtitle="Tennis, padel, fitness, club house — chaque espace a été pensé pour vous offrir l'excellence."
          />
        </div>

        {/* Horizontal scroll */}
        <div className="pl-6 md:pl-12 lg:pl-24">
          <div className="flex gap-5 overflow-x-auto pb-6 scrollbar-hide" style={{ scrollbarWidth: 'none' }}>
            {spaces.map((space, i) => (
              <CardSpace key={space.title} {...space} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* ──────────── POURQUOI NOUS ──────────── */}
      <section className="section-padding relative overflow-hidden" style={{ backgroundColor: '#1B3A2D' }}>
        <TennisCourtBg className="text-white opacity-[0.04]" />

        <div className="relative z-10 container-wide">
          <SectionHeader
            roman="III"
            label="Nos engagements"
            title="Pourquoi choisir la Châtaigneraie"
            light
          />

          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                number: '07',
                headline: 'Jouer sous la pluie ? Jamais.',
                text: '7 courts 100 % couverts, ouverts de 8h à 23h, 365 jours par an. La météo n\'est plus une excuse.',
              },
              {
                number: '∞',
                headline: 'Un coach pour chaque ambition.',
                text: 'École de tennis, cours adultes et enfants, préparation à la compétition. Nos coaches s\'adaptent à votre niveau et vos objectifs.',
              },
              {
                number: '60',
                headline: 'Votre club, pas juste une salle.',
                text: 'Plus de 60 ans de vie de club. Événements, tournois, bar, terrasse, vestiaires premium. Une communauté qui vous attend.',
              },
            ].map((item, i) => (
              <motion.div
                key={item.headline}
                className="relative p-8 border border-white/10"
                initial={{ opacity: 0, y: 40 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true, margin: '-60px' }}
                transition={{ duration: 0.6, delay: i * 0.15 }}
              >
                <span
                  className="font-cormorant font-light leading-none block mb-6 select-none"
                  style={{ fontSize: '5rem', color: 'rgba(201,168,76,0.15)' }}
                >
                  {item.number}
                </span>
                <h3 className="font-cormorant text-2xl font-light text-white mb-4 leading-snug">
                  {item.headline}
                </h3>
                <p className="text-sm font-light leading-relaxed" style={{ color: 'rgba(255,255,255,0.55)' }}>
                  {item.text}
                </p>
              </motion.div>
            ))}
          </div>

          <motion.div
            className="mt-12 text-center"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.5 }}
          >
            <Link href="/contact" className="btn-outline-white">
              Rejoindre le club <ArrowRight size={13} />
            </Link>
          </motion.div>
        </div>
      </section>

      {/* ──────────── ÉVÉNEMENTS ──────────── */}
      <section className="section-padding" style={{ backgroundColor: '#F7F4EF' }}>
        <div className="container-wide">
          <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
            <SectionHeader
              roman="IV"
              label="Agenda"
              title="Prochains événements"
              subtitle="Tournois, stages, soirées — la vie du club ne s'arrête jamais."
            />
            <Link href="/evenements" className="btn-outline shrink-0 self-start md:self-auto mb-14">
              Voir tout l'agenda <ArrowRight size={13} />
            </Link>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {events.map((event, i) => (
              <CardEvent key={event.title} {...event} index={i} />
            ))}
          </div>
        </div>
      </section>

      {/* ──────────── INSTAGRAM ──────────── */}
      <section className="section-padding" style={{ backgroundColor: 'white' }}>
        <div className="container-wide">
          <SectionHeader
            roman="V"
            label="Instagram"
            title="La vie du club en images"
            centered
          />
          <InstagramGrid />
        </div>
      </section>

      {/* ──────────── NEWSLETTER ──────────── */}
      <section className="section-padding relative overflow-hidden" style={{ backgroundColor: '#F7F4EF' }}>
        <TennisCourtBg className="opacity-[0.04]" color="#1B3A2D" />

        <div className="relative z-10 container-wide">
          <div className="max-w-2xl mx-auto text-center">
            <SectionHeader
              roman="VI"
              label="Newsletter"
              title="Ne manquez rien"
              subtitle="Tournois, nouveaux cours, événements — restez dans la boucle."
              centered
            />

            <div className="flex flex-col sm:flex-row gap-3 justify-center mb-10">
              <input
                type="email"
                placeholder="votre@email.com"
                className="flex-1 max-w-xs px-4 py-3 text-sm border focus:outline-none focus:border-primary transition-colors font-light"
                style={{ borderColor: 'rgba(27,58,45,0.2)', color: '#2C2C2C' }}
              />
              <button className="btn-primary">
                S'abonner <ArrowRight size={13} />
              </button>
            </div>

            <div className="flex items-center justify-center gap-6">
              <p className="label-tag" style={{ color: '#7A7A72' }}>Suivez-nous</p>
              <div className="flex gap-3">
                {[
                  { href: 'https://www.instagram.com/tcchataigneraie/', label: 'Instagram' },
                  { href: '#', label: 'Facebook' },
                  { href: '#', label: 'YouTube' },
                ].map(({ href, label }) => (
                  <a
                    key={label}
                    href={href}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="label-tag px-4 py-2 border transition-all hover:border-primary hover:text-primary"
                    style={{ borderColor: 'rgba(27,58,45,0.2)', color: '#7A7A72' }}
                  >
                    {label}
                  </a>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
