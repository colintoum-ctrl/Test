'use client'

import { motion } from 'framer-motion'
import Image from 'next/image'
import Link from 'next/link'
import { ArrowRight } from 'lucide-react'

interface CardArticleProps {
  slug: string
  image: string
  date: string
  category: string
  title: string
  excerpt: string
  index?: number
}

const categoryColors: Record<string, string> = {
  Résultats: '#C9A84C',
  Club: '#1B3A2D',
  Padel: '#2D5A42',
  Tennis: '#1B3A2D',
  Fitness: '#2D5A42',
}

export default function CardArticle({ slug, image, date, category, title, excerpt, index = 0 }: CardArticleProps) {
  return (
    <motion.div
      className="group"
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: '-60px' }}
      transition={{ duration: 0.6, delay: index * 0.1, ease: [0.22, 1, 0.36, 1] }}
      whileHover={{ y: -4 }}
    >
      <Link href={`/actualites/${slug}`} className="block">
        <div
          className="relative bg-white overflow-hidden"
          style={{ boxShadow: '0 4px 24px rgba(15,31,23,0.07)' }}
        >
          {/* Image */}
          <div className="relative h-48 overflow-hidden">
            <Image
              src={image}
              alt={title}
              fill
              className="object-cover transition-transform duration-700 group-hover:scale-105"
              sizes="(max-width: 768px) 100vw, 33vw"
            />
            <div className="absolute top-4 left-4">
              <span
                className="label-tag px-2.5 py-1 text-white"
                style={{ backgroundColor: categoryColors[category] || '#1B3A2D' }}
              >
                {category}
              </span>
            </div>
          </div>

          {/* Content */}
          <div className="p-6">
            <p className="label-tag mb-3" style={{ color: '#7A7A72' }}>{date}</p>
            <h3
              className="font-cormorant text-xl font-light mb-3 leading-snug group-hover:text-primary transition-colors"
              style={{ color: '#1B3A2D' }}
            >
              {title}
            </h3>
            <p className="text-sm font-light leading-relaxed mb-4" style={{ color: '#7A7A72' }}>
              {excerpt}
            </p>
            <span
              className="inline-flex items-center gap-1.5 label-tag group-hover:gap-3 transition-all"
              style={{ color: '#C9A84C' }}
            >
              Lire la suite <ArrowRight size={11} />
            </span>
          </div>
        </div>
      </Link>
    </motion.div>
  )
}
