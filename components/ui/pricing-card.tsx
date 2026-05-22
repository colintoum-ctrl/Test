'use client'

import { motion } from 'framer-motion'
import Link from 'next/link'
import { ArrowRight, Check } from 'lucide-react'

interface PricingCardProps {
  hook: string
  title: string
  price: string
  period: string
  features: string[]
  cta: string
  href?: string
  highlighted?: boolean
  index?: number
}

export default function PricingCard({
  hook,
  title,
  price,
  period,
  features,
  cta,
  href = '/contact',
  highlighted = false,
  index = 0,
}: PricingCardProps) {
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
        className="relative p-8 h-full"
        style={{
          backgroundColor: highlighted ? '#1B3A2D' : 'white',
          boxShadow: highlighted
            ? '0 8px 40px rgba(15,31,23,0.25)'
            : '0 4px 24px rgba(15,31,23,0.07)',
        }}
      >
        {highlighted && (
          <div className="absolute top-0 left-0 right-0 h-0.5" style={{ backgroundColor: '#C9A84C' }} />
        )}

        <div className="corner-decoration corner-tl" style={{ borderColor: highlighted ? 'rgba(201,168,76,0.4)' : '#C9A84C' }} />

        <p
          className="label-tag mb-2"
          style={{ color: highlighted ? 'rgba(201,168,76,0.8)' : '#C9A84C' }}
        >
          {hook}
        </p>

        <h3
          className="font-cormorant text-2xl font-light mb-5"
          style={{ color: highlighted ? 'white' : '#1B3A2D' }}
        >
          {title}
        </h3>

        <div className="flex items-end gap-2 mb-1">
          <span
            className="font-cormorant font-light leading-none"
            style={{ fontSize: 'clamp(2.5rem, 5vw, 3.5rem)', color: highlighted ? 'white' : '#1B3A2D' }}
          >
            {price}
          </span>
        </div>
        <p className="label-tag mb-6" style={{ color: highlighted ? 'rgba(255,255,255,0.4)' : '#7A7A72' }}>
          {period}
        </p>

        <div className="gold-line mb-6" style={{ opacity: highlighted ? 0.2 : 0.15 }} />

        <ul className="space-y-3 mb-8">
          {features.map((f) => (
            <li key={f} className="flex items-start gap-3">
              <Check size={13} className="mt-0.5 shrink-0" style={{ color: '#C9A84C' }} />
              <span className="text-sm font-light" style={{ color: highlighted ? 'rgba(255,255,255,0.7)' : '#7A7A72' }}>
                {f}
              </span>
            </li>
          ))}
        </ul>

        <Link
          href={href}
          className={highlighted ? 'btn-outline-white w-full justify-center' : 'btn-outline w-full justify-center'}
        >
          {cta} <ArrowRight size={13} />
        </Link>
      </div>
    </motion.div>
  )
}
