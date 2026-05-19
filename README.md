# Projekt_Portfolio_CRM

## Überblick
Dieses Projekt ist ein persönliches Entwickler-Portfolio mit Fokus auf:
- klare Struktur
- saubere UI/UX
- modularem JavaScript
- einem Wetter-Widget mit Python im Browser (PyScript)

## Features
- Interaktive Projekt-Modal-Ansicht
- Kontaktformular mit EmailJS (v4 Browser SDK)
- Wetter-Widget über PyScript + Open-Meteo APIs (ohne eigenes Wetter-Backend)
- Scroll-Reveal Animationen
- Canvas-Dotgrid im Hero-Bereich

## Projektstruktur
- `index.html` -> Seitenstruktur
- `style/style.css` -> Styling
- `js/` -> modulare Frontend-Logik
- `python/weather.py` -> Wetter-Logik in Python (PyScript)
- `images/` -> Assets
- `weather-api/` -> optionales/altes Backend (für aktuellen Wetter-Flow nicht nötig)

## Lokal testen
Einfach `index.html` im Browser öffnen.
Hinweis: Für manche Browser-Setups ist ein lokaler Webserver robuster als `file://`.

## Deploy
Das Projekt kann als statische Seite deployed werden (z. B. GitHub Pages oder Hostinger Static Hosting).

## Hinweise zu Secrets
- Keine Secrets im Repo speichern.
- `.env`, Tokens, Recovery-Codes und Passwörter bleiben lokal im Passwortmanager.
- Siehe `.gitignore` im Root.
