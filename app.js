/* ── SHARED COMPONENTS ───────────────────────────── */

const TOPBAR = `
<div class="topbar">
  <div class="wrap">
    <div class="tb-l">
      <span>
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0118 0z"/><circle cx="12" cy="10" r="3"/></svg>
        Rueil-Malmaison (92) · 20 min de Paris
      </span>
      <span>
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        Ouvert 7j/7 · 8h – 23h
      </span>
      <span>
        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 01-2.18 2 19.79 19.79 0 01-8.63-3.07A19.5 19.5 0 014.16 12 19.79 19.79 0 011.1 3.38 2 2 0 013.09 1h3a2 2 0 012 1.72c.127.96.361 1.903.7 2.81a2 2 0 01-.45 2.11L7.09 8.91a16 16 0 006 6l1.27-1.27a2 2 0 012.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0122 16.92z"/></svg>
        01 47 51 XX XX
      </span>
    </div>
    <div class="tb-r">
      <a href="https://instagram.com/lachataigneraietennispadel" class="tb-ig" target="_blank" rel="noopener">📸 @lachataigneraietennispadel</a>
    </div>
  </div>
</div>`;

const NAVBAR = `
<nav class="navbar" id="nav">
  <div class="wrap">
    <a href="index.html" class="logo">
      <svg class="logo-mark" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <mask id="lm">
            <rect width="100" height="100" fill="white"/>
            <rect x="17" y="14" width="47" height="68" rx="14" fill="black"/>
            <rect x="64" y="14" width="38" height="44" fill="black"/>
          </mask>
        </defs>
        <rect x="5" y="5" width="90" height="90" rx="16" fill="#475569" mask="url(#lm)"/>
        <circle cx="76" cy="73" r="5.5" fill="white"/>
      </svg>
      <div class="logo-text">
        <div class="logo-name">La Châtaigneraie</div>
        <div class="logo-sub">Tennis &amp; Padel · Rueil-Malmaison</div>
      </div>
    </a>
    <ul class="nav-list">
      <li><a href="index.html" data-nav="accueil">Accueil</a></li>
      <li><a href="tennis.html" data-nav="tennis">Tennis</a></li>
      <li><a href="padel.html" data-nav="padel">Padel</a></li>
      <li><a href="installations.html" data-nav="installations">Installations</a></li>
      <li><a href="evenements.html" data-nav="evenements">Événements</a></li>
      <li><a href="actualites.html" data-nav="actualites">Actualités</a></li>
    </ul>
    <div class="nav-cta">
      <a href="tarifs.html" class="btn btn-outline btn-sm">Tarifs</a>
      <button class="btn btn-clay btn-sm" onclick="mo('booking')">Réserver</button>
    </div>
    <button class="burger" id="brgr" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </div>
  <div class="drawer" id="drwr">
    <a href="index.html" data-nav="accueil">Accueil</a>
    <a href="tennis.html" data-nav="tennis">Tennis</a>
    <a href="padel.html" data-nav="padel">Padel</a>
    <a href="installations.html" data-nav="installations">Toutes nos installations</a>
    <a href="evenements.html" data-nav="evenements">Événements</a>
    <a href="actualites.html" data-nav="actualites">Actualités</a>
    <a href="tarifs.html" data-nav="tarifs">Tarifs &amp; Abonnements</a>
    <button class="btn btn-clay" onclick="mo('booking')" style="margin-top:4px">Réserver un terrain</button>
  </div>
</nav>`;

const FOOTER_HTML = `
<footer id="contact">
  <div class="wrap">
    <div class="footer-grid">
      <div class="f-brand">
        <div class="f-logo">
          <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <mask id="fm">
                <rect width="100" height="100" fill="white"/>
                <rect x="17" y="14" width="47" height="68" rx="14" fill="black"/>
                <rect x="64" y="14" width="38" height="44" fill="black"/>
              </mask>
            </defs>
            <rect x="5" y="5" width="90" height="90" rx="16" fill="#C06632" mask="url(#fm)"/>
            <circle cx="76" cy="73" r="5.5" fill="white"/>
          </svg>
          <div>
            <strong>La Châtaigneraie</strong>
            <small>Tennis &amp; Padel · Depuis 1963</small>
          </div>
        </div>
        <p class="f-desc">Lieu de vie Sport &amp; Lifestyle premium de l'Ouest Parisien. 7 courts de tennis couverts, 4 pistes de padel indoor, restaurant panoramique, fitness, club house. Ouvert 7j/7 de 8h à 23h.</p>
        <div class="f-soc">
          <a href="https://instagram.com/lachataigneraietennispadel" target="_blank" rel="noopener" title="Instagram">📸</a>
          <a href="#" title="TikTok">🎵</a>
          <a href="#" title="LinkedIn">💼</a>
          <a href="#" title="Facebook">👥</a>
        </div>
      </div>
      <div class="f-col">
        <h5>Navigation</h5>
        <ul>
          <li><a href="index.html">Accueil</a></li>
          <li><a href="tennis.html">Tennis</a></li>
          <li><a href="padel.html">Padel</a></li>
          <li><a href="installations.html">Installations</a></li>
          <li><a href="evenements.html">Événements</a></li>
          <li><a href="actualites.html">Actualités</a></li>
          <li><a href="tarifs.html">Tarifs</a></li>
        </ul>
      </div>
      <div class="f-col">
        <h5>Horaires</h5>
        <div class="f-hours">
          <div><strong>Lundi – Vendredi</strong><br/>8h00 – 23h00</div>
          <br/>
          <div><strong>Samedi – Dimanche</strong><br/>8h00 – 23h00</div>
          <br/>
          <div style="color:rgba(255,255,255,.22);font-size:.73rem">Jours fériés : 9h00 – 21h00</div>
        </div>
      </div>
      <div class="f-col">
        <h5>Accès rapide</h5>
        <ul>
          <li><a href="#" onclick="mo('booking');return false">Réserver un court tennis</a></li>
          <li><a href="#" onclick="mo('booking');return false">Réserver une piste padel</a></li>
          <li><a href="#" onclick="mo('resto');return false">Réserver au restaurant</a></li>
          <li><a href="#" onclick="mo('school');return false">Inscription école tennis</a></li>
          <li><a href="#" onclick="mo('membre');return false">Devenir membre</a></li>
          <li><a href="#" onclick="mo('b2b');return false">Offres entreprises</a></li>
        </ul>
      </div>
      <div class="f-col">
        <h5>Contact</h5>
        <div class="f-contact">
          <a href="#"><span class="f-contact-icon">📍</span>Rueil-Malmaison (92500)<br/>Hauts-de-Seine</a>
          <a href="tel:+33147510000"><span class="f-contact-icon">📞</span>01 47 51 XX XX</a>
          <a href="mailto:contact@lachataigneraietennispadel.com"><span class="f-contact-icon">✉️</span>contact@lachataigneraietennispadel.com</a>
          <a href="https://instagram.com/lachataigneraietennispadel" target="_blank" rel="noopener"><span class="f-contact-icon">📸</span>@lachataigneraietennispadel</a>
        </div>
        <button class="btn btn-clay" style="width:100%;justify-content:center;margin-top:18px;font-size:.82rem" onclick="mo('booking')">Réserver maintenant</button>
      </div>
    </div>
    <div class="f-bot">
      <span>© 2026 Tennis Club de la Châtaigneraie · Tous droits réservés</span>
      <div class="f-bot-links">
        <a href="#">Mentions légales</a>
        <a href="#">Confidentialité</a>
        <a href="#">CGU</a>
      </div>
    </div>
  </div>
</footer>`;

const MODALS_HTML = `
<!-- Réservation -->
<div class="ov" id="m-booking" onclick="oc(event,'booking')">
  <div class="modal">
    <button class="modal-x" onclick="mc('booking')">✕</button>
    <div class="modal-emo">⚡</div>
    <h2>Réserver un terrain</h2>
    <p class="sub">Confirmation instantanée par SMS &amp; e-mail. Annulation gratuite jusqu'à 24h avant.</p>
    <div class="fg-row">
      <div class="fg"><label>Activité</label><select><option>🎾 Tennis</option><option>🏓 Padel</option><option>👨‍🏫 Cours collectif</option></select></div>
      <div class="fg"><label>Joueurs</label><select><option>2 joueurs</option><option>3 joueurs</option><option>4 joueurs</option></select></div>
    </div>
    <div class="fg-row">
      <div class="fg"><label>Date</label><input type="date"/></div>
      <div class="fg"><label>Créneau</label><select><option>08:00</option><option>09:30</option><option>11:00</option><option>12:30</option><option>14:00</option><option>15:30</option><option>17:00</option><option>18:30</option><option>20:00</option><option>21:30</option></select></div>
    </div>
    <div class="fg"><label>E-mail</label><input type="email" placeholder="prenom.nom@email.com"/></div>
    <button class="btn btn-clay" style="width:100%;justify-content:center;padding:14px;margin-top:4px">Vérifier les disponibilités →</button>
    <p class="modal-note">Paiement sécurisé · CB, PayPal, Chèques vacances</p>
  </div>
</div>

<!-- B2B -->
<div class="ov" id="m-b2b" onclick="oc(event,'b2b')">
  <div class="modal">
    <button class="modal-x" onclick="mc('b2b')">✕</button>
    <div class="modal-emo">🏢</div>
    <h2>Offre entreprise</h2>
    <p class="sub">Notre équipe vous rappelle sous 24h avec une offre personnalisée.</p>
    <div class="fg"><label>Société</label><input type="text" placeholder="Votre entreprise"/></div>
    <div class="fg-row">
      <div class="fg"><label>Contact</label><input type="text" placeholder="Prénom Nom"/></div>
      <div class="fg"><label>Email pro</label><input type="email" placeholder="contact@societe.com"/></div>
    </div>
    <div class="fg-row">
      <div class="fg"><label>Type d'événement</label><select><option>Tournoi Padel entreprise</option><option>Séminaire</option><option>Team Building</option><option>Privatisation restaurant</option><option>Abonnement Corporate</option></select></div>
      <div class="fg"><label>Participants</label><select><option>Moins de 20</option><option>20 – 50</option><option>50 – 100</option><option>+ de 100</option></select></div>
    </div>
    <div class="fg"><label>Précisez votre projet</label><textarea placeholder="Dates souhaitées, besoins spécifiques..."></textarea></div>
    <button class="btn btn-clay" style="width:100%;justify-content:center;padding:14px">Envoyer ma demande →</button>
  </div>
</div>

<!-- Restaurant -->
<div class="ov" id="m-resto" onclick="oc(event,'resto')">
  <div class="modal">
    <button class="modal-x" onclick="mc('resto')">✕</button>
    <div class="modal-emo">🍽️</div>
    <h2>Réserver une table</h2>
    <p class="sub">Restaurant panoramique ouvert 7j/7. Vue sur les courts, déjeuner et dîner.</p>
    <div class="fg-row">
      <div class="fg"><label>Date</label><input type="date"/></div>
      <div class="fg"><label>Couverts</label><select><option>1 – 2</option><option>3 – 4</option><option>5 – 8</option><option>Groupe (+8)</option></select></div>
    </div>
    <div class="fg-row">
      <div class="fg"><label>Service</label><select><option>Déjeuner (12h–14h30)</option><option>Dîner (19h–22h30)</option><option>Brunch week-end (11h–15h)</option></select></div>
      <div class="fg"><label>Téléphone</label><input type="tel" placeholder="06 XX XX XX XX"/></div>
    </div>
    <button class="btn btn-clay" style="width:100%;justify-content:center;padding:14px">Confirmer →</button>
  </div>
</div>

<!-- École tennis -->
<div class="ov" id="m-school" onclick="oc(event,'school')">
  <div class="modal">
    <button class="modal-x" onclick="mc('school')">✕</button>
    <div class="modal-emo">👨‍🏫</div>
    <h2>École de Tennis &amp; Padel</h2>
    <p class="sub">Cours individuels, collectifs, stages vacances. Tous âges, tous niveaux.</p>
    <div class="fg-row">
      <div class="fg"><label>Prénom</label><input type="text"/></div>
      <div class="fg"><label>Âge / Niveau</label><select><option>Enfant – Débutant</option><option>Enfant – Intermédiaire</option><option>Adulte – Débutant</option><option>Adulte – Intermédiaire</option><option>Adulte – Avancé</option></select></div>
    </div>
    <div class="fg"><label>Type de cours</label><select><option>Cours individuel</option><option>Cours collectif</option><option>Stage vacances</option><option>Préparation compétition</option></select></div>
    <div class="fg"><label>E-mail</label><input type="email" placeholder="prenom.nom@email.com"/></div>
    <button class="btn btn-clay" style="width:100%;justify-content:center;padding:14px">M'inscrire →</button>
  </div>
</div>

<!-- Membre -->
<div class="ov" id="m-membre" onclick="oc(event,'membre')">
  <div class="modal">
    <button class="modal-x" onclick="mc('membre')">✕</button>
    <div class="modal-emo">🌳</div>
    <h2>Devenir membre</h2>
    <p class="sub">Rejoignez plus de 1 000 membres et profitez de tout le club sans restriction.</p>
    <div class="fg-row">
      <div class="fg"><label>Prénom</label><input type="text"/></div>
      <div class="fg"><label>Nom</label><input type="text"/></div>
    </div>
    <div class="fg"><label>E-mail</label><input type="email" placeholder="prenom.nom@email.com"/></div>
    <div class="fg"><label>Formule</label><select><option>Essential — 420 €/an</option><option>Premium — 780 €/an ⭐</option><option>Corporate — Sur devis</option></select></div>
    <div class="fg"><label>Activité principale</label><select><option>Tennis</option><option>Padel</option><option>Tennis &amp; Padel</option><option>Fitness uniquement</option></select></div>
    <button class="btn btn-clay" style="width:100%;justify-content:center;padding:14px">Commencer mon inscription →</button>
    <p class="modal-note">Notre équipe vous contactera sous 48h pour finaliser votre adhésion.</p>
  </div>
</div>`;

/* ── INJECT ──────────────────────────────────────── */
document.getElementById('header').innerHTML = TOPBAR + NAVBAR;
document.getElementById('footer').innerHTML = FOOTER_HTML;
document.getElementById('modals').innerHTML = MODALS_HTML;

/* ── ACTIVE NAV ──────────────────────────────────── */
const page = document.body.dataset.page || 'accueil';
document.querySelectorAll('[data-nav]').forEach(a =>
  a.classList.toggle('on', a.dataset.nav === page)
);

/* ── SCROLL SHADOW ───────────────────────────────── */
const nav = document.getElementById('nav');
window.addEventListener('scroll', () =>
  nav?.classList.toggle('scrolled', scrollY > 24)
, {passive:true});

/* ── BURGER ──────────────────────────────────────── */
const brgr = document.getElementById('brgr');
const drwr = document.getElementById('drwr');
brgr?.addEventListener('click', () => drwr?.classList.toggle('open'));
drwr?.querySelectorAll('a').forEach(a =>
  a.addEventListener('click', () => drwr.classList.remove('open'))
);

/* ── MODALS ──────────────────────────────────────── */
function mo(id){ document.getElementById('m-'+id)?.classList.add('on'); document.body.style.overflow='hidden' }
function mc(id){ document.getElementById('m-'+id)?.classList.remove('on'); document.body.style.overflow='' }
function oc(e,id){ if(e.target===document.getElementById('m-'+id)) mc(id) }
document.addEventListener('keydown', e => {
  if(e.key==='Escape'){
    document.querySelectorAll('.ov.on').forEach(el=>el.classList.remove('on'));
    document.body.style.overflow='';
  }
});

/* ── DATE INPUTS ─────────────────────────────────── */
const today = new Date().toISOString().split('T')[0];
document.querySelectorAll('input[type=date]').forEach(el => {
  el.value = today;
  el.min = today;
});

/* ── FAQ ACCORDION ───────────────────────────────── */
document.querySelectorAll('.faq-item').forEach(item => {
  item.querySelector('.faq-q')?.addEventListener('click', () => {
    const wasOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item.open').forEach(i => i.classList.remove('open'));
    if(!wasOpen) item.classList.add('open');
  });
});
