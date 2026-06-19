'use client'

import { motion } from 'framer-motion'
import Image from 'next/image'
import { Instagram } from 'lucide-react'

const posts = [
  {
    id: 1,
    image: 'https://images.unsplash.com/photo-1554068865-24cecd4e34b8?w=400&h=400&fit=crop',
    alt: 'Court de tennis',
  },
  {
    id: 2,
    image: 'https://images.unsplash.com/photo-1622163642998-1ea32b0bbc67?w=400&h=400&fit=crop',
    alt: 'Padel match',
  },
  {
    id: 3,
    image: 'https://images.unsplash.com/photo-1490481651871-ab68de25d43d?w=400&h=400&fit=crop',
    alt: 'Tennis joueur',
  },
  {
    id: 4,
    image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=400&h=400&fit=crop',
    alt: 'Fitness salle',
  },
  {
    id: 5,
    image: 'https://images.unsplash.com/photo-1529926706528-db9e5010cd3e?w=400&h=400&fit=crop',
    alt: 'Club house',
  },
  {
    id: 6,
    image: 'https://images.unsplash.com/photo-1606131731446-5568d87113aa?w=400&h=400&fit=crop',
    alt: 'Tennis court vue',
  },
]

export default function InstagramGrid() {
  return (
    <div>
      {/* Handle */}
      <div className="flex items-center justify-center gap-3 mb-8">
        <Instagram size={20} style={{ color: '#C9A84C' }} />
        <a
          href="https://www.instagram.com/tcchataigneraie/"
          target="_blank"
          rel="noopener noreferrer"
          className="font-cormorant text-3xl font-light hover:opacity-70 transition-opacity"
          style={{ color: '#1B3A2D' }}
        >
          @tcchataigneraie
        </a>
      </div>

      {/* Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 gap-2 md:gap-3 mb-8">
        {posts.map((post, i) => (
          <motion.a
            key={post.id}
            href="https://www.instagram.com/tcchataigneraie/"
            target="_blank"
            rel="noopener noreferrer"
            className="relative aspect-square overflow-hidden group block"
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true, margin: '-40px' }}
            transition={{ duration: 0.5, delay: i * 0.07 }}
          >
            <Image
              src={post.image}
              alt={post.alt}
              fill
              className="object-cover transition-transform duration-500 group-hover:scale-110"
              sizes="(max-width: 768px) 50vw, 33vw"
            />
            <div className="absolute inset-0 bg-primary opacity-0 group-hover:opacity-30 transition-opacity duration-300" style={{ backgroundColor: '#1B3A2D' }} />
            <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
              <Instagram size={28} className="text-white" />
            </div>
          </motion.a>
        ))}
      </div>

      <div className="text-center">
        <a
          href="https://www.instagram.com/tcchataigneraie/"
          target="_blank"
          rel="noopener noreferrer"
          className="btn-outline inline-flex"
        >
          Suivez notre actualité →
        </a>
      </div>
    </div>
  )
}
