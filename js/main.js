// 🔍 DEBUGGING: Gibt in der Browser-Konsole aus, dass main.js gerade lädt
console.log("main.js lädt");

// 📦 IMPORTS: Lädt verschiedene Module (separate JS-Dateien) ein
// Diese Funktionen sind in anderen Dateien definiert und werden hier importiert
import { initDotGrid } from './dotgrid.js';      // Punkt-Gitter Animation
import { initTyping } from './typing.js';        // Schreibmaschinen-Effekt der Wörter
import { initNavObserver } from './navObserver.js'; // Navigation = aktiver Link beim Scrollen
import { initModal } from './modal.js';          // Popup für Projektdetails
import { initContactForm } from './kontakt.js';  // Kontaktformular mit Email
import { initReveal } from './reveal.js';        // Scroll-Animationen (rote Balken)

// 🎯 WARTE auf DOMContentLoaded Event
// "DOMContentLoaded" = HTML ist vollständig geladen, JavaScript kann jetzt mit DOM arbeiten
// Das ist wichtig, weil HTML-Elemente vorher vielleicht noch nicht existieren
window.addEventListener("DOMContentLoaded", () => {
  // Jetzt starten wir alle Funktionen nacheinander:
  
  initDotGrid();        // Das Punkt-Gitter auf der Startseite wird reaktiv
  initTyping();         // Der Schreibmaschinen-Effekt beginnt
  initNavObserver();    // Der Navigation Observer überwacht das Scrollen
  initModal();          // Projekt-Popups werden klickbar gemacht
  initContactForm();    // Das Kontaktformular wird funktionsfähig
  initReveal();         // Scroll-Animationen werden aktiviert
});

// 🔍 DEBUGGING: Gibt aus, dass main.js erfolgreich geladen wurde
console.log("main.js geladen");