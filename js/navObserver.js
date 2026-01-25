/* ======================================
    NAV Active Link per IntersectionObserver
    - setzt automatisch die Klasse `active` auf den Nav-Link,
      dessen Section momentan sichtbar ist
====================================== */
// Funktion wird von main.js gestartet
export function initNavObserver() {

  // Alle Links in der Navigation holen
  const navLinks = document.querySelectorAll('nav a');

  // Alle Sections, die eine ID haben (z.B. #Home, #Kontakt)
  const sections = document.querySelectorAll('section[id]');

  // Falls nichts gefunden wurde → Script abbrechen (Sicherheitscheck)
  if (!navLinks.length || !sections.length) return;

  // Entfernt bei ALLEN Links die aktive Markierung
  function clearActive() {
    navLinks.forEach(link => {
      link.classList.remove('active');          // CSS-Klasse entfernen
      link.removeAttribute('aria-current');     // Screenreader-Hilfe entfernen
    });
  }

  // Beobachtet, wann Sections in den sichtbaren Bereich kommen
  const observer = new IntersectionObserver((entries) => {

    entries.forEach(entry => {
      const id = entry.target.id; // ID der Section (z.B. "Home")

      // passenden Navigationslink suchen
      const link = document.querySelector(`nav a[href="#${id}"]`);
      if (!link) return;

      // Wenn Section sichtbar genug ist
      if (entry.isIntersecting) {
        clearActive();                     // erst alles deaktivieren
        link.classList.add('active');      // aktuellen Link aktiv machen
        link.setAttribute('aria-current', 'page'); // Screenreader-Info
      }
    });

  }, {
    threshold: 0.55 // Section gilt als "aktiv", wenn 55% sichtbar sind
  });

  // Jede Section wird vom Observer überwacht
  sections.forEach(section => observer.observe(section));
}