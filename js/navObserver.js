/* ======================================
    NAV Active Link per IntersectionObserver
    Diese Datei kümmert sich darum, dass der aktive Navigation-Link
    automatisch rot wird, wenn die dazugehörige Section sichtbar ist
    z.B. "Home" wird rot, wenn Home-Section sichtbar ist
====================================== */

// 📤 EXPORT: Diese Funktion wird von main.js aufgerufen
export function initNavObserver() {

  // 🎯 Alle Links in der Navigation abrufen
  // nav a = alle <a> Elemente in einem <nav> Tag (Home, Über mich, Projekte, Kontakt)
  const navLinks = document.querySelectorAll('nav a');

  // 🎯 Alle Sections mit einer ID holen
  // section[id] = nur Sections, die ein id-Attribute haben (#Home, #Über_mich, #Projekte, #Kontakt)
  const sections = document.querySelectorAll('section[id]');

  // 🛡️ SICHERHEITSCHECK: Falls nichts gefunden wurde, Script abbrechen
  // Das verhindert Fehler, wenn HTML nicht richtig strukturiert ist
  if (!navLinks.length || !sections.length) return;

  // 📋 Funktion: Entfernt die "aktiv"-Markierung bei ALLEN Links
  function clearActive() {
    navLinks.forEach(link => {
      // forEach = für JEDEN Link in der Navigation...
      link.classList.remove('active');          // Klasse "active" entfernen (rot-Färbung)
      link.removeAttribute('aria-current');     // Screenreader-Attribut entfernen
    });
  }

  // 👁️ INTERSECTION OBSERVER = "Beobachter" der prüft, wann Elemente sichtbar werden
  // Das ist besser als Scroll-Events, weil es performanter ist!
  const observer = new IntersectionObserver((entries) => {
    // entries = Array mit allen beobachteten Elementen die gerade etwas Neues machen

    entries.forEach(entry => {
      // entry.target = die aktuelle Section
      // entry.target.id = z.B. "Home", "Über_mich", "Projekte"
      const id = entry.target.id;

      // 🔗 Passenden Navigation-Link für diese Section suchen
      // nav a[href="#${id}"] = Link dessen href auf diese Section zeigt
      // z.B. href="#Home" passt zu Section id="Home"
      const link = document.querySelector(`nav a[href="#${id}"]`);
      
      // 🛡️ Falls kein passender Link gefunden: überspringe diesen
      if (!link) return;

      // 🎯 Wenn Section sichtbar genug ist (55% im Viewport)
      if (entry.isIntersecting) {
        clearActive();                     // Zuerst ALLE Links deaktivieren
        link.classList.add('active');      // Nur DIESER Link wird aktiv (rot)
        link.setAttribute('aria-current', 'page'); // Screenreader-Info: Das ist die aktuelle Seite
      }
    });

  }, {
    // ⚙️ KONFIGURATION:
    threshold: 0.55 // Section gilt als "sichtbar", wenn 55% im Fenster sind
    // 0.55 = 55% der Section müssen sichtbar sein
  });

  // 🔍 Beobachte JEDE Section (der Observer schaut zu)
  sections.forEach(section => observer.observe(section));
  // Das ist die zentrale Schleife die alles startet
}