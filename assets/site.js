/* YILGA — script du site : contact du pied, menu mobile, apparition au défilement. */
const TELEPHONE_YILGA = '';   // ex. « +226 70 00 00 00 » ; vide = non affiché
const EMAIL_YILGA = '';       // ex. « contact@yilga.bf » ; vide = non affiché

(function () {
  const contact = document.querySelector('.pied__contact');
  if (contact) {
    if (TELEPHONE_YILGA) {
      const a = document.createElement('a');
      a.href = 'tel:' + TELEPHONE_YILGA.replace(/\s+/g, '');
      a.textContent = TELEPHONE_YILGA;
      contact.appendChild(a);
    }
    if (EMAIL_YILGA) {
      const a = document.createElement('a');
      a.href = 'mailto:' + EMAIL_YILGA;
      a.textContent = EMAIL_YILGA;
      contact.appendChild(a);
    }
  }

  const menu = document.querySelector('.entete__menu');
  const liens = document.querySelector('.entete__liens');
  if (menu && liens) {
    const ouvrir = (etat) => {
      menu.setAttribute('aria-expanded', String(etat));
      document.body.classList.toggle('menu-ouvert', etat);
    };
    menu.addEventListener('click', () => ouvrir(menu.getAttribute('aria-expanded') !== 'true'));
    liens.addEventListener('click', (e) => { if (e.target.closest('a')) ouvrir(false); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') ouvrir(false); });
  }

  const reduit = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const sections = document.querySelectorAll('.reveal');
  if (sections.length && 'IntersectionObserver' in window && !reduit) {
    const obs = new IntersectionObserver((entrees) => {
      entrees.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add('reveal--vu'); obs.unobserve(en.target); }
      });
    }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
    sections.forEach((s) => obs.observe(s));
  } else {
    sections.forEach((s) => s.classList.add('reveal--vu'));
  }
})();
