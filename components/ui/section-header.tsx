'use client'

import { motion } from 'framer-motion'
import { useInView } from 'framer-motion'
import { useRef } from 'react'

interface SectionHeaderProps {
  roman: string
  label: string
  title: string
  subtitle?: string
  centered?: boolean
  light?: boolean
}

export default function SectionHeader({
  roman,
  label,
  title,
  subtitle,
  centered = false,
  light = false,
}: SectionHeaderProps) {
  const ref = useRef(null)
  const inView = useInView(ref, { once: true, margin: '-80px' })

  return (
    <motion.div
      ref={ref}
      className={`mb-14 ${centered ? 'text-center' : ''}`}
      initial={{ opacity: 0, y: 30 }}
      animate={inView ? { opacity: 1, y: 0 } : {}}
      transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
    >
      <div className={`flex items-center gap-4 mb-4 ${centered ? 'justify-center' : ''}`}>
        <span
          className="font-cormorant text-5xl font-light leading-none"
          style={{ color: '#C9A84C', opacity: 0.5 }}
        >
          {roman}
        </span>
        <div className="gold-line flex-1 max-w-12" style={{ opacity: 0.4 }} />
        <span className="label-tag" style={{ color: light ? 'rgba(255,255,255,0.5)' : '#C9A84C' }}>
          {label}
        </span>
      </div>

      <h2
        className="font-cormorant font-light leading-tight"
        style={{
          fontSize: 'clamp(2rem, 4vw, 3.2rem)',
          color: light ? 'white' : '#1B3A2D',
        }}
      >
        {title}
      </h2>

      {subtitle && (
        <p
          className="mt-4 text-sm font-light leading-relaxed max-w-xl"
          style={{ color: light ? 'rgba(255,255,255,0.6)' : '#7A7A72' }}
        >
          {subtitle}
        </p>
      )}
    </motion.div>
  )
}
