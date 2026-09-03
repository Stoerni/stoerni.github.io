# Portfolio — Dennis Poglitsch

## Überblick
Persönliches Entwickler-Portfolio — statische Website mit modularer Frontend-Architektur.

## Features
- **DE/EN Sprachumschaltung** per data-i18n + localStorage-Persistenz
- Interaktive Projekt-Modal-Ansicht
- Kontaktformular mit EmailJS (v4 Browser SDK)
- Wetter-Widget über PyScript + Open-Meteo APIs (Python im Browser)
- Schreibmaschinen-Effekt im Hero-Bereich
- Scroll-Reveal Animationen
- Canvas-Dotgrid im Hero-Bereich
- Responsive Navigation mit Scroll-Observer

## Technik
- Reines HTML/CSS/JS (kein Framework)
- Module: translations.js, modal.js, typing.js, kontakt.js, navObserver.js, reveal.js, dotgrid.js
- Python (PyScript/Pyodide) für das Wetter-Widget
- EmailJS für formularlosen E-Mail-Versand
- Goatcounter für datenschutzfreundliche Analytics