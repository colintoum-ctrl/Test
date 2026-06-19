import Link from 'next/link'
import { Instagram, Facebook, Youtube, ArrowRight, MapPin, Clock, Phone } from 'lucide-react'

const footerLinks = {
  club: [
    { href: '/#histoire', label: 'Notre histoire' },
    { href: '/#qui-sommes-nous', label: 'Qui sommes-nous' },
    { href: '/actualites', label: 'Actualités' },
    { href: '/contact', label: 'Partenaires' },
  ],
  espaces: [
    { href: '/tennis', label: 'Tennis' },
    { href: '/padel', label: 'Padel' },
    { href: '/fitness', label: 'Fitness' },
    { href: '/club-house', label: 'Club House' },
  ],
  infos: [
    { href: '/contact', label: 'Nous contacter' },
    { href: '/evenements', label: 'Événements' },
    { href: '/contact#acces', label: 'Accès & transports' },
    { href: '/#tarifs', label: 'Tarifs' },
  ],
}

export default function Footer() {
  return (
    <footer style={{ backgroundColor: '#0F1F17' }} className="text-white">
      <div className="container-wide py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12 lg:gap-8">

          {/* Col 1 — Logo + tagline + réseaux */}
          <div className="lg:col-span-1">
            <div className="mb-6">
              <p className="font-cormorant text-2xl font-light text-white mb-1">TC Châtaigneraie</p>
              <p className="label-tag text-white/40">Rueil-Malmaison · Est. 1963</p>
            </div>
            <p className="text-sm text-white/50 font-light leading-relaxed mb-6">
              Un club d'exception au cœur de l'Île-de-France, alliant tradition tennistique et modernité.
            </p>
            <div className="flex gap-3">
              {[
                { href: 'https://www.instagram.com/tcchataigneraie/', icon: Instagram, label: 'Instagram' },
                { href: '#', icon: Facebook, label: 'Facebook' },
                { href: '#', icon: Youtube, label: 'YouTube' },
              ].map(({ href, icon: Icon, label }) => (
                <a
                  key={label}
                  href={href}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={label}
                  className="w-9 h-9 border border-white/20 flex items-center justify-center text-white/50 hover:text-white hover:border-white/60 transition-all"
                >
                  <Icon size={15} />
                </a>
              ))}
            </div>
          </div>

          {/* Col 2 — Le Club */}
          <div>
            <p className="label-tag text-white/30 mb-6">Le Club</p>
            <ul className="space-y-3">
              {footerLinks.club.map((link) => (
                <li key={link.href}>
                  <Link href={link.href} className="text-sm text-white/55 hover:text-white transition-colors font-light">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Col 3 — Nos espaces */}
          <div>
            <p className="label-tag text-white/30 mb-6">Nos Espaces</p>
            <ul className="space-y-3">
              {footerLinks.espaces.map((link) => (
                <li key={link.href}>
                  <Link href={link.href} className="text-sm text-white/55 hover:text-white transition-colors font-light">
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Col 4 — Infos pratiques */}
          <div>
            <p className="label-tag text-white/30 mb-6">Infos Pratiques</p>
            <ul className="space-y-4">
              <li className="flex gap-3 text-sm text-white/55 font-light">
                <MapPin size={14} className="mt-0.5 shrink-0 text-gold" style={{ color: '#C9A84C' }} />
                <span>1 Chemin de la Châtaigneraie<br />92500 Rueil-Malmaison</span>
              </li>
              <li className="flex gap-3 text-sm text-white/55 font-light">
                <Clock size={14} className="mt-0.5 shrink-0" style={{ color: '#C9A84C' }} />
                <span>Lun–Dim : 8h00 – 23h00<br />365 jours par an</span>
              </li>
              <li className="flex gap-3 text-sm text-white/55 font-light">
                <Phone size={14} className="mt-0.5 shrink-0" style={{ color: '#C9A84C' }} />
                <span>+33 (0)1 47 XX XX XX</span>
              </li>
            </ul>

            <div className="mt-6">
              <p className="text-xs text-white/30 mb-3">Newsletter</p>
              <div className="flex">
                <input
                  type="email"
                  placeholder="votre@email.com"
                  className="flex-1 bg-white/5 border border-white/15 px-3 py-2 text-sm text-white placeholder-white/30 focus:outline-none focus:border-white/40 transition-colors"
                />
                <button
                  className="px-3 py-2 flex items-center"
                  style={{ backgroundColor: '#C9A84C' }}
                  aria-label="S'abonner"
                >
                  <ArrowRight size={14} className="text-dark" style={{ color: '#0F1F17' }} />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Ligne de séparation dorée */}
        <div className="gold-line my-10 opacity-20" />

        {/* Copyright */}
        <div className="flex flex-col sm:flex-row justify-between items-center gap-2">
          <p className="text-xs text-white/30 font-light">
            © 2025 Tennis Club de la Châtaigneraie. Tous droits réservés.
          </p>
          <div className="flex gap-6">
            <Link href="#" className="text-xs text-white/30 hover:text-white/60 transition-colors">Mentions légales</Link>
            <Link href="#" className="text-xs text-white/30 hover:text-white/60 transition-colors">Confidentialité</Link>
          </div>
        </div>
      </div>
    </footer>
  )
}
