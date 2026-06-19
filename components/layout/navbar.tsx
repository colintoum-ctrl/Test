'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { motion, AnimatePresence } from 'framer-motion'
import { Menu, X, ArrowRight } from 'lucide-react'

const links = [
  { href: '/tennis', label: 'Tennis' },
  { href: '/padel', label: 'Padel' },
  { href: '/fitness', label: 'Fitness' },
  { href: '/club-house', label: 'Club House' },
  { href: '/evenements', label: 'Événements' },
  { href: '/actualites', label: 'Actualités' },
  { href: '/contact', label: 'Contact' },
]

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)
  const pathname = usePathname()

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 80)
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  useEffect(() => {
    setMobileOpen(false)
  }, [pathname])

  useEffect(() => {
    document.body.style.overflow = mobileOpen ? 'hidden' : ''
    return () => { document.body.style.overflow = '' }
  }, [mobileOpen])

  const isTransparent = !scrolled && pathname === '/'

  return (
    <>
      <motion.nav
        className="fixed top-0 left-0 right-0 z-50 transition-all duration-400"
        style={{
          backgroundColor: isTransparent ? 'transparent' : 'white',
          boxShadow: scrolled ? '0 1px 20px rgba(15,31,23,0.08)' : 'none',
        }}
        initial={{ y: -100 }}
        animate={{ y: 0 }}
        transition={{ duration: 0.6, ease: [0.22, 1, 0.36, 1] }}
      >
        <div className="container-wide">
          <div className="flex items-center justify-between h-16 md:h-20">
            {/* Logo */}
            <Link href="/" className="flex flex-col leading-none group">
              <span
                className="font-cormorant text-lg font-light tracking-wide transition-colors duration-300"
                style={{ color: isTransparent ? 'white' : '#1B3A2D' }}
              >
                TC Châtaigneraie
              </span>
              <span
                className="label-tag transition-colors duration-300"
                style={{ color: isTransparent ? 'rgba(255,255,255,0.5)' : '#C9A84C' }}
              >
                Rueil-Malmaison · Est. 1963
              </span>
            </Link>

            {/* Desktop links */}
            <div className="hidden lg:flex items-center gap-8">
              {links.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="label-tag transition-all duration-300 hover:opacity-60"
                  style={{ color: isTransparent ? 'white' : '#1B3A2D' }}
                >
                  {link.label}
                </Link>
              ))}
            </div>

            {/* CTA + Burger */}
            <div className="flex items-center gap-4">
              <Link
                href="/contact"
                className="hidden md:flex items-center gap-2 label-tag px-5 py-2.5 transition-all duration-300"
                style={{
                  border: isTransparent ? '1px solid rgba(255,255,255,0.6)' : '1px solid #1B3A2D',
                  color: isTransparent ? 'white' : 'white',
                  backgroundColor: isTransparent ? 'transparent' : '#1B3A2D',
                }}
              >
                Réserver
                <ArrowRight size={12} />
              </Link>

              <button
                onClick={() => setMobileOpen(true)}
                className="lg:hidden p-2 transition-colors"
                style={{ color: isTransparent ? 'white' : '#1B3A2D' }}
                aria-label="Ouvrir le menu"
              >
                <Menu size={22} />
              </button>
            </div>
          </div>
        </div>
      </motion.nav>

      {/* Mobile drawer */}
      <AnimatePresence>
        {mobileOpen && (
          <>
            <motion.div
              className="fixed inset-0 z-40 bg-black/40"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setMobileOpen(false)}
            />
            <motion.div
              className="fixed inset-0 z-50 flex flex-col"
              style={{ backgroundColor: '#0F1F17' }}
              initial={{ x: '100%' }}
              animate={{ x: 0 }}
              exit={{ x: '100%' }}
              transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
            >
              <div className="flex items-center justify-between p-6">
                <span className="font-cormorant text-white text-xl font-light">TC Châtaigneraie</span>
                <button onClick={() => setMobileOpen(false)} className="text-white/60 hover:text-white transition-colors">
                  <X size={24} />
                </button>
              </div>

              <div className="gold-line mx-6" />

              <nav className="flex flex-col px-6 py-8 gap-1 flex-1">
                {links.map((link, i) => (
                  <motion.div
                    key={link.href}
                    initial={{ opacity: 0, x: 20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.05 * i, duration: 0.3 }}
                  >
                    <Link
                      href={link.href}
                      className="block py-3 font-cormorant text-2xl font-light text-white/80 hover:text-white transition-colors"
                    >
                      {link.label}
                    </Link>
                  </motion.div>
                ))}
              </nav>

              <div className="p-6 border-t border-white/10">
                <Link href="/contact" className="btn-outline-white w-full justify-center">
                  Réserver un court <ArrowRight size={14} />
                </Link>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </>
  )
}
