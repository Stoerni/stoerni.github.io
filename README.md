# Portfolio — Dennis Poglitsch

## Überblick
Persönliches Entwickler-Portfolio — statische Website mit modularer Frontend-Architektur.

## Features
- **DE/EN Sprachumschaltung** per data-i18n + localStorage-Persistenz
- Interaktive Projekt-Modal-Ansicht
- Kontaktformular mit EmailJS (v4 Browser SDK)
- Wetter-Widget über PyScript + Open-Meteo APIs (Python im Browser) — PyScript wird erst nach Klick auf „Wetter laden“ im Wetter-Modal nachgeladen (`js/pyscript-loader.js`), nicht mehr beim Laden der Startseite
- Schreibmaschinen-Effekt im Hero-Bereich
- Scroll-Reveal Animationen
- Canvas-Dotgrid im Hero-Bereich
- Responsive Navigation mit Scroll-Observer

## Technik
- Reines HTML/CSS/JS (kein Framework)
- Module: translations.js, modal.js, pyscript-loader.js, typing.js, kontakt.js, navObserver.js, reveal.js, dotgrid.js
- Python (PyScript/Pyodide) für das Wetter-Widget
- EmailJS für formularlosen E-Mail-Versand
- **Schriften und EmailJS-Bibliothek lokal ausgeliefert**: Inter + JetBrains Mono als `.woff2` in `fonts/` (`@font-face` in `style/style.css`), EmailJS-Browser-SDK in `js/vendor/` — keine Google-Fonts- und keine jsDelivr-Abrufe mehr
- Keine Analytics auf der Seite (GoatCounter entfernt)

## MailPilot-Demo
Der Ordner `mailpilot-demo/` enthält den fertig gebauten Demo-Build des MailPilot-Frontends (`npm run build:demo`) und läuft als statische Seite komplett im Browser — ohne Backend, ohne Netzwerk-Anfragen; der Link „Live ansehen“ in der MailPilot-Projektkarte öffnet ihn. Der Quellcode liegt **nicht** in diesem Repo, sondern im MailPilot-Projekt.