// 🌐 translations.js — Sprachumschaltung DE/EN per data-i18n Attribut + localStorage
// 📤 Export: t(key) für andere Module (z.B. kontakt.js)
export function t(key) {
  return translations[currentLang]?.[key] ?? key;
}

const translations = {
  de: {
    'nav-home': 'Home',
    'nav-about': 'Über mich',
    'nav-projects': 'Projekte',
    'nav-contact': 'Kontakt',

    'home-hero': 'Hi, mein Name ist Dennis Poglitsch',
    'home-prefix': 'Ich bin ',
    'home-cta': 'Kontakt zu mir',

    'about-header': 'Über mich',
    'about-text':
      '<span class="first_word">Technik</span> fasziniert mich nicht nur – sie treibt mich an.<br>' +
      'Ich bin eine offene, lernbereite und lösungsorientierte Person mit großer Motivation für die Softwareentwicklung. ' +
      'Ein respektvoller Umgang, ehrliche Kommunikation und gemeinsames Arbeiten an Lösungen sind für mich selbstverständlich.<br><br>' +
      'Durch meine bisherige Berufserfahrung arbeite ich auch in stressigen Situationen ruhig, strukturiert und zuverlässig. ' +
      'Ich übernehme Verantwortung, denke mit und eigne mir neue Themen schnell an.<br><br>' +
      'Mein Interesse an der Anwendungsentwicklung kommt aus echter Begeisterung für Logik, Struktur und kreative Problemlösung. ' +
      'Beim Programmieren analysiere ich Probleme Schritt für Schritt und entwickle praktische Lösungen, ' +
      'Fehler sehe ich dabei als Lernchance.',
    'skills-header': 'Meine Fähigkeiten',

    'lang-en': 'EN',
    'lang-de': 'DE',

    // 🏗️ Projekte
    'projects-header': 'Projekte',
    'project-mailpilot': 'MailPilot (in Entwicklung)',
    'project-crm': 'Werkstatt-CRM (in Entwicklung)',
    'project-weather': 'Live Wetter Widget',
    'project-portfolio': 'Entwickler-Portfolio',
    'project-desc-mailpilot':
      'Multi-Tenant AI-gestütztes E-Mail-Triage- und Reply-Drafting-SaaS.',
    'project-desc-crm':
      'CRM-Lösung für Werkstätten mit Fokus auf digitale Aufträge, mobile Nutzung und saubere Prozesse.',
    'project-desc-weather':
      'API-basiertes Wetter-Widget mit Python im Browser und dynamischer Ortssuche.',
    'project-desc-portfolio':
      'Modernes Portfolio mit Fokus auf Struktur, Performance und professioneller Präsentation.',

    // 💬 Kontakt
    'contact-header': 'Kontakt',
    'contact-intro': 'Schreib mir gerne eine Nachricht – ich freue mich auf den Austausch.',
    'contact-label-name': 'Name',
    'contact-label-email': 'E-Mail',
    'contact-label-message': 'Nachricht',
    'contact-placeholder-name': 'Dein Name',
    'contact-placeholder-email': 'Deine E-Mail',
    'contact-placeholder-message': 'Deine Nachricht...',
    'contact-submit': 'Absenden',
    'contact-sending': 'Sende...',
    'contact-success': 'Danke! Deine Nachricht wurde erfolgreich gesendet.',
    'contact-error': 'Ups! Etwas ist schiefgelaufen. Bitte versuche es später erneut.',

    // 🎭 typing.js Wörter
    'typing-word-0': 'alt aber nicht veraltet',
    'typing-word-1': 'Lösungsorientiert',
    'typing-word-2': 'Analytisch',
    'typing-word-3': 'Strukturiert',

    // 💻 Modal
    'modal-live': 'Live ansehen',
    'modal-close': 'Schließen',
    'modal-title-fallback': 'Titel',
    'modal-desc-fallback': 'Beschreibung',

    // ⚖️ Footer (Rechtsseiten)
    'footer-imprint': 'Impressum',
    'footer-privacy': 'Datenschutz',
  },

  en: {
    'nav-home': 'Home',
    'nav-about': 'About Me',
    'nav-projects': 'Projects',
    'nav-contact': 'Contact',

    'home-hero': "Hi, my name is Dennis Poglitsch",
    'home-prefix': 'I am ',
    'home-cta': 'Contact Me',

    'about-header': 'About Me',
    'about-text':
      '<span class="first_word">Technology</span> doesn\'t just fascinate me — it drives me.<br>' +
      'I am an open, eager-to-learn and solution-oriented person with strong motivation for software development. ' +
      'Respectful interaction, honest communication, and collaborative problem-solving are natural to me.<br><br>' +
      'Through my professional experience, I stay calm, structured, and reliable even in stressful situations. ' +
      'I take responsibility, think proactively, and quickly acquire new skills.<br><br>' +
      'My interest in application development comes from genuine passion for logic, structure, and creative problem-solving. ' +
      'When programming, I analyze problems step by step and develop practical solutions — ' +
      'I see mistakes as learning opportunities.',
    'skills-header': 'My Skills',

    'lang-en': 'EN',
    'lang-de': 'DE',

    // 🏗️ Projects
    'projects-header': 'Projects',
    'project-mailpilot': 'MailPilot (in Development)',
    'project-crm': 'Workshop CRM (in Development)',
    'project-weather': 'Live Weather Widget',
    'project-portfolio': 'Developer Portfolio',
    'project-desc-mailpilot':
      'Multi-Tenant AI-powered Email Triage and Reply Drafting SaaS.',
    'project-desc-crm':
      'Workshop CRM with focus on digital orders, mobile use, and clean processes.',
    'project-desc-weather':
      'API-based weather widget with Python in the browser and dynamic location search.',
    'project-desc-portfolio':
      'Modern portfolio focused on structure, performance, and professional presentation.',

    // 💬 Contact
    'contact-header': 'Contact',
    'contact-intro': 'Feel free to send me a message — I look forward to connecting.',
    'contact-label-name': 'Name',
    'contact-label-email': 'Email',
    'contact-label-message': 'Message',
    'contact-placeholder-name': 'Your Name',
    'contact-placeholder-email': 'Your Email',
    'contact-placeholder-message': 'Your Message...',
    'contact-submit': 'Send',
    'contact-sending': 'Sending...',
    'contact-success': 'Thank you! Your message was sent successfully.',
    'contact-error': 'Oops! Something went wrong. Please try again later.',

    // 🎭 typing.js Words
    'typing-word-0': 'Im old, not obsolete',
    'typing-word-1': 'Solution-Oriented',
    'typing-word-2': 'Analytical',
    'typing-word-3': 'Structured',

    // 💻 Modal
    'modal-live': 'View Live',
    'modal-close': 'Close',
    'modal-title-fallback': 'Title',
    'modal-desc-fallback': 'Description',

    // ⚖️ Footer (legal pages)
    'footer-imprint': 'Imprint',
    'footer-privacy': 'Privacy Policy',
   },
};

let currentLang = localStorage.getItem('portfolio-lang') || 'de';

function applyLanguage(lang) {
  const t = translations[lang];
  if (!t) return;

  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    if (t[key] !== undefined) {
      el.innerHTML = t[key];
    }
  });

  // data-i18n-placeholder für input/textarea placeholder-Texte
  document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (t[key] !== undefined) {
      el.placeholder = t[key];
    }
  });

  // data-i18n-aria-label für aria-label Attribute (z.B. Modal-Schließen-Button)
  document.querySelectorAll('[data-i18n-aria-label]').forEach((el) => {
    const key = el.getAttribute('data-i18n-aria-label');
    if (t[key] !== undefined) {
      el.setAttribute('aria-label', t[key]);
    }
  });

  // data-i18n-desc für Projekt-Beschreibungen (data-desc wird aktualisiert)
  document.querySelectorAll('[data-i18n-desc]').forEach((el) => {
    const key = el.getAttribute('data-i18n-desc');
    if (t[key] !== undefined) {
      el.dataset.desc = t[key];
    }
  });

  // Update <html lang> Attribute für SEO / Screenreader
  document.documentElement.lang = lang;

  currentLang = lang;
  localStorage.setItem('portfolio-lang', lang);

  // Toggle-Button-Text aktualisieren
  const toggle = document.getElementById('lang-toggle');
  if (toggle) {
    const target = lang === 'de' ? 'lang-en' : 'lang-de';
    // Button zeigt die SPRACHE an, in die gewechselt wird
    toggle.textContent = translations[lang][target];
  }

  // Modal-Inhalt aktualisieren, falls gerade geöffnet
  const modal = document.getElementById('projectModal');
  if (modal && modal.classList.contains('open') && modal.dataset.activeCardIndex !== undefined) {
    const cards = document.querySelectorAll('.projekt');
    const card = cards[parseInt(modal.dataset.activeCardIndex)];
    if (card) {
      const modalTitle = document.getElementById('modalTitle');
      const modalDesc = document.getElementById('modalDesc');
      if (modalTitle) modalTitle.textContent = card.querySelector('h4')?.textContent || '';
      if (modalDesc) {
        const descKey = card.dataset.i18nDesc;
        modalDesc.textContent = descKey ? (translations[lang][descKey] || card.dataset.desc || '') : (card.dataset.desc || '');
      }
    }
  }
}

function initLanguageSwitcher() {
  const toggle = document.getElementById('lang-toggle');
  if (toggle) {
    toggle.addEventListener('click', () => {
      const newLang = currentLang === 'de' ? 'en' : 'de';
      applyLanguage(newLang);
    });
  }

  // Gespeicherte Sprache anwenden
  applyLanguage(currentLang);
}

export { initLanguageSwitcher, applyLanguage };