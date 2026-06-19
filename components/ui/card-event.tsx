'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowRight } from 'lucide-react'

type BadgeType = 'members' | 'open' | 'full'

interface CardEventProps {
  day: string
  month: string
  year: string
  title: string
  description: string
  category: string
  badge: BadgeType
  href?: string
  index?: number
}

const badgeConfig: Record<BadgeType, { label: string; color: string; bg: string }> = {
  members: { label: 'Membres uniquement', color: '#1B3A2D', bg: 'rgba(27,58,45,0.08)' },
  open: { label: 'Ouvert à tous', color: '#2D5A42', bg: 'rgba(45,90,66,0.08)' },
  full: { label: 'Complet', color: '#7A7A72', bg: 'rgba(122,122,114,0.08)' },
}

export default function CardEvent({ day, month, year, title, description, category, badge, href = '#', index = 0 }: CardEventProps) {
  const { label, color, bg } = badgeConfig[badge]

  return (
    <motion.div
      className="relative group"
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-60px' }}
      transition={{ duration: 0.6, delay: index * 0.12, ease: [0.22, 1, 0.36, 1] }}
      whileHover={{ y: -4 }}
    >
      <div
        className="relative bg-white p-7 h-full"
        style={{ boxShadow: '0 4px 24px rgba(15,31,23,0.07)' }}
      >
        {/* Corner */}
        <div className="corner-decoration corner-tl" />

        {/* Date */}
        <div className="flex items-end gap-3 mb-5">
          <span
            className="font-cormorant leading-none"
            style={{ fontSize: 'clamp(3.5rem, 7vw, 5rem)', color: '#1B3A2D', opacity: 0.15 }}
          >
            {day}
          </span>
          <div className="mb-1">
            <p className="label-tag" style={{ color: '#C9A84C' }}>{month} {year}</p>
            <p className="label-tag mt-1" style={{ color: '#7A7A72' }}>{category}</p>
          </div>
        </div>

        <div className="gold-line mb-5 opacity-20" />

        <h3
          className="font-cormorant text-xl font-light mb-3"
          style={{ color: '#1B3A2D' }}
        >
          {title}
        </h3>
        <p className="text-sm font-light leading-relaxed mb-5" style={{ color: '#7A7A72' }}>
          {description}
        </p>

        <div className="flex items-center justify-between">
          <span
            className="label-tag px-3 py-1"
            style={{ color, backgroundColor: bg }}
          >
            {label}
          </span>

          {badge !== 'full' && (
            <Link
              href={href}
              className="inline-flex items-center gap-1.5 label-tag transition-all hover:gap-2.5"
              style={{ color: '#1B3A2D' }}
            >
              S'inscrire <ArrowRight size={11} />
            </Link>
          )}
        </div>
      </div>
    </motion.div>
  )
}
