// 🌐 translations.js — Sprachumschaltung DE/EN per data-i18n Attribut + localStorage
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