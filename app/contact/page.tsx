'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowRight, MapPin, Clock, Phone, Mail, Train, Car } from 'lucide-react'
import SectionHeader from '@/components/ui/section-header'

export default function ContactPage() {
  const [formData, setFormData] = useState({ nom: '', email: '', objet: '', message: '' })
  const [sent, setSent] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    setSent(true)
  }

  return (
    <>
      {/* Hero minimal */}
      <section className="pt-36 pb-16 relative" style={{ backgroundColor: '#1B3A2D' }}>
        <div className="container-wide">
          <motion.p className="label-tag text-white/40 mb-3" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.2 }}>
            Parlons
          </motion.p>
          <motion.h1
            className="font-cormorant font-light text-white"
            style={{ fontSize: 'clamp(3rem, 7vw, 6rem)', lineHeight: 0.95 }}
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
          >
            Contactez-nous
          </motion.h1>
          <motion.p
            className="font-cormorant italic text-xl mt-2"
            style={{ color: '#C9A84C' }}
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.5 }}
          >
            Nous répondons sous 24h
          </motion.p>
        </div>
      </section>

      {/* Formulaire + Infos */}
      <section className="section-padding" style={{ backgroundColor: '#F7F4EF' }}>
        <div className="container-wide">
          <div className="grid md:grid-cols-2 gap-16">

            {/* Formulaire */}
            <div>
              <SectionHeader roman="I" label="Formulaire" title="Envoyez-nous un message" />

              {sent ? (
                <motion.div
                  className="p-8 text-center"
                  style={{ backgroundColor: '#1B3A2D' }}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                >
                  <p className="font-cormorant text-3xl font-light text-white mb-3">Message envoyé !</p>
                  <p className="text-sm font-light" style={{ color: 'rgba(255,255,255,0.6)' }}>
                    Nous vous répondrons dans les 24h.
                  </p>
                </motion.div>
              ) : (
                <form onSubmit={handleSubmit} className="space-y-5">
                  {[
                    { name: 'nom', label: 'Nom complet', type: 'text', placeholder: 'Jean Dupont' },
                    { name: 'email', label: 'Adresse email', type: 'email', placeholder: 'jean@exemple.com' },
                    { name: 'objet', label: 'Objet', type: 'text', placeholder: 'Inscription, renseignement...' },
                  ].map((field) => (
                    <div key={field.name}>
                      <label className="label-tag block mb-2" style={{ color: '#7A7A72' }}>{field.label}</label>
                      <input
                        type={field.type}
                        placeholder={field.placeholder}
                        required
                        value={formData[field.name as keyof typeof formData]}
                        onChange={(e) => setFormData({ ...formData, [field.name]: e.target.value })}
                        className="w-full px-4 py-3 text-sm bg-white border focus:outline-none transition-colors font-light"
                        style={{ borderColor: 'rgba(27,58,45,0.15)', color: '#2C2C2C' }}
                        onFocus={(e) => { e.target.style.borderColor = '#1B3A2D' }}
                        onBlur={(e) => { e.target.style.borderColor = 'rgba(27,58,45,0.15)' }}
                      />
                    </div>
                  ))}

                  <div>
                    <label className="label-tag block mb-2" style={{ color: '#7A7A72' }}>Message</label>
                    <textarea
                      rows={5}
                      placeholder="Votre message..."
                      required
                      value={formData.message}
                      onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                      className="w-full px-4 py-3 text-sm bg-white border focus:outline-none transition-colors font-light resize-none"
                      style={{ borderColor: 'rgba(27,58,45,0.15)', color: '#2C2C2C' }}
                      onFocus={(e) => { e.target.style.borderColor = '#1B3A2D' }}
                      onBlur={(e) => { e.target.style.borderColor = 'rgba(27,58,45,0.15)' }}
                    />
                  </div>

                  <button type="submit" className="btn-primary w-full justify-center">
                    Envoyer le message <ArrowRight size={13} />
                  </button>
                </form>
              )}
            </div>

            {/* Infos contact */}
            <div id="acces">
              <SectionHeader roman="II" label="Informations" title="Nous trouver" />

              <div className="space-y-6 mb-10">
                {[
                  {
                    icon: MapPin,
                    title: 'Adresse',
                    lines: ['1 Chemin de la Châtaigneraie', '92500 Rueil-Malmaison'],
                  },
                  {
                    icon: Clock,
                    title: 'Horaires d\'ouverture',
                    lines: ['Lundi – Vendredi : 8h00 – 23h00', 'Samedi – Dimanche : 8h00 – 22h00', 'Jours fériés : 9h00 – 20h00'],
                  },
                  {
                    icon: Phone,
                    title: 'Téléphone',
                    lines: ['+33 (0)1 47 XX XX XX'],
                  },
                  {
                    icon: Mail,
                    title: 'Email',
                    lines: ['contact@tcchataigneraie.fr'],
                  },
                ].map(({ icon: Icon, title, lines }) => (
                  <div key={title} className="flex gap-4">
                    <div className="w-10 h-10 flex items-center justify-center shrink-0" style={{ backgroundColor: 'rgba(201,168,76,0.12)' }}>
                      <Icon size={16} style={{ color: '#C9A84C' }} />
                    </div>
                    <div>
                      <p className="label-tag mb-1" style={{ color: '#7A7A72' }}>{title}</p>
                      {lines.map((line) => (
                        <p key={line} className="text-sm font-light" style={{ color: '#2C2C2C' }}>{line}</p>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              {/* Accès transports */}
              <div className="p-6" style={{ backgroundColor: 'white' }}>
                <p className="label-tag mb-4" style={{ color: '#C9A84C' }}>Accès & Transports</p>
                <div className="space-y-3">
                  <div className="flex gap-3 items-start">
                    <Train size={15} className="mt-0.5 shrink-0" style={{ color: '#1B3A2D' }} />
                    <div>
                      <p className="text-sm font-medium" style={{ color: '#1B3A2D' }}>RER A</p>
                      <p className="text-sm font-light" style={{ color: '#7A7A72' }}>Rueil-Malmaison puis bus 259</p>
                    </div>
                  </div>
                  <div className="flex gap-3 items-start">
                    <Car size={15} className="mt-0.5 shrink-0" style={{ color: '#1B3A2D' }} />
                    <div>
                      <p className="text-sm font-medium" style={{ color: '#1B3A2D' }}>En voiture</p>
                      <p className="text-sm font-light" style={{ color: '#7A7A72' }}>A13 sortie Rueil-Malmaison · Parking gratuit</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Carte embarquée */}
              <div className="mt-4 h-52 overflow-hidden relative" style={{ backgroundColor: '#e8e4df' }}>
                <iframe
                  src="https://maps.google.com/maps?q=Rueil-Malmaison,+France&output=embed&z=14"
                  width="100%"
                  height="100%"
                  style={{ border: 0 }}
                  allowFullScreen
                  loading="lazy"
                  referrerPolicy="no-referrer-when-downgrade"
                  title="Localisation TC Châtaigneraie"
                />
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  )
}
