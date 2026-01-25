/* ==========================
    SCROLL REVEAL OBSERVER
========================== */
// Funktion wird von main.js gestartet
export function initReveal() {

  // Alle Elemente mit Klasse .reveal
  const revealElements = document.querySelectorAll(".reveal");
  if (!revealElements.length) return;

  // Observer prüft, ob Element sichtbar wird
  const revealObserver = new IntersectionObserver((entries, observer) => {

    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("reveal_active"); // CSS Animation starten
        observer.unobserve(entry.target); // nicht nochmal beobachten
      }
    });

  }, { threshold: 0.4 }); // 40% sichtbar = Animation starten

  revealElements.forEach(el => revealObserver.observe(el));
}