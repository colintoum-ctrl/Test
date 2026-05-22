'use client'

import { motion } from 'framer-motion'
import Image from 'next/image'
import Link from 'next/link'
import { ArrowRight } from 'lucide-react'

interface CardSpaceProps {
  roman: string
  title: string
  stat: string
  description: string
  image: string
  href: string
  index?: number
}

export default function CardSpace({ roman, title, stat, description, image, href, index = 0 }: CardSpaceProps) {
  return (
    <motion.div
      className="relative flex-shrink-0 w-72 md:w-80 group"
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-60px' }}
      transition={{ duration: 0.6, delay: index * 0.1, ease: [0.22, 1, 0.36, 1] }}
      whileHover={{ y: -4 }}
    >
      <div
        className="relative overflow-hidden bg-white"
        style={{ boxShadow: '0 4px 24px rgba(15,31,23,0.08)' }}
      >
        {/* Corner decoration */}
        <div className="corner-decoration corner-tl z-10" />
        <div className="corner-decoration corner-br z-10" />

        {/* Image */}
        <div className="relative h-56 overflow-hidden">
          <Image
            src={image}
            alt={title}
            fill
            className="object-cover transition-transform duration-700 group-hover:scale-105"
            sizes="320px"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/50 to-transparent" />

          {/* Roman numeral overlay */}
          <span
            className="absolute bottom-3 left-4 font-cormorant text-6xl font-light text-white/25 leading-none select-none"
          >
            {roman}
          </span>
        </div>

        {/* Content */}
        <div className="p-6">
          <p className="label-tag mb-2" style={{ color: '#C9A84C' }}>{stat}</p>
          <h3
            className="font-cormorant text-2xl font-light mb-3"
            style={{ color: '#1B3A2D' }}
          >
            {title}
          </h3>
          <p className="text-sm font-light leading-relaxed mb-5" style={{ color: '#7A7A72' }}>
            {description}
          </p>
          <Link
            href={href}
            className="inline-flex items-center gap-2 label-tag transition-all duration-300 hover:gap-3"
            style={{ color: '#1B3A2D' }}
          >
            Découvrir <ArrowRight size={12} />
          </Link>
        </div>
      </div>
    </motion.div>
  )
}
