/* ==========================
    SCROLL REVEAL OBSERVER
    Diese Datei zeigt Animationen, wenn der Nutzer scrollt
    z.B. Texte mit rotem Balken-Effekt fahren rein

    Wie das funktioniert:
    - Alle Elemente mit .reveal Klasse werden beobachtet
    - Wenn sie 40% sichtbar werden, wird die CSS-Animation gestartet
    - Der rote Balken fährt von links nach rechts, dann der Text
========================== */

// 📤 EXPORT: Diese Funktion wird von main.js aufgerufen
export function initReveal() {

  // 🎯 Alle Elemente mit der Klasse .reveal abrufen
  // Das sind normalerweise Text-Elemente, die animiert reinkommen sollen
  // z.B. <h1 class="reveal">...
  const revealElements = document.querySelectorAll(".reveal");
  
  // 🛡️ Sicherheitscheck: Wenn keine Elemente gefunden, Script beenden
  if (!revealElements.length) return;

  // 👁️ INTERSECTION OBSERVER = "Beobachter" der prüft, wann Elemente sichtbar werden
  // Dieser Observer ist ähnlich wie in navObserver.js
  const revealObserver = new IntersectionObserver((entries, observer) => {
    // entries = alle beobachteten Elemente die gerade etwas Neues machen
    // observer = der Beobachter selbst (um Elements wieder abzumelden)

    entries.forEach(entry => {
      // 🎯 Wenn Element momentan sichtbar ist (40%+ im Viewport)
      if (entry.isIntersecting) {
        // 🎨 Klasse "reveal_active" hinzufügen = CSS Animation starten
        // Die CSS definiert dann:
        // - Roter Balken fährt von links nach rechts (0.8 Sekunden)
        // - Text wird dann sichtbar und kommt nach oben (0.6 Sekunden, später startend)
        entry.target.classList.add("reveal_active");
        
        // 🛑 Element abmelden vom Observer (Optimierung)
        // Es macht keinen Sinn das Element weiter zu beobachten,
        // da die Animation nur einmal spielen soll
        observer.unobserve(entry.target);
      }
    });

  }, { 
    // ⚙️ KONFIGURATION:
    threshold: 0.4  // Element wird als "sichtbar" registriert, wenn 40% im Fenster sind
    // threshold = 0.4 bedeutet: 40% des Elements müssen sichtbar sein
  });

  // 🔍 Beobachte JEDES Element mit .reveal Klasse
  revealElements.forEach(el => revealObserver.observe(el));
  // Jedes Element wird vom Observer überwacht
}