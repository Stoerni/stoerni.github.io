/* ==========================
   Projekt-Modal: Öffnen / Schließen
   Ein Modal ist ein Popup-Fenster, das Projekt-Details anzeigt
========================== */

// 📤 EXPORT: Diese Funktion wird von main.js aufgerufen
import { t } from './translations.js';
import { loadPyScript } from './pyscript-loader.js';

export function initModal() {
  // 🎯 HTML-Elemente für das Modal abrufen
  const modal = document.getElementById('projectModal');  // Das komplette Modal-Container-Element
  if (!modal) return;  // 🛡️ Sicherheitscheck: Wenn kein Modal, beende

  // 🎯 Alle für das Modal wichtigen Container abrufen
  const modalTitle = document.getElementById('modalTitle');          // Überschrift des Modals
  const modalDesc = document.getElementById('modalDesc');            // Beschreibungs-Text
  const techContainer = document.getElementById('modalTech');        // Container für Tech-Badges
  const linksContainer = document.getElementById('modalLinks');      // Container für Links
  const weatherContainer = document.getElementById('weather_container'); // Weather-Widget
  const gallery = document.getElementById('modalGallery');           // Bild-Galerie
  const closeButton = modal.querySelector('.modal_close');           // ×-Button (Fokus-Ziel beim Öffnen)

  /* ================= ⌨️ TASTATUR / FOKUS ================= */

  // Alle fokussierbaren Elemente im Modal (wird bei jedem Tab neu ermittelt,
  // weil das Wetter-Widget seinen Inhalt zur Laufzeit austauscht).
  const FOCUSABLE_SELECTOR = [
    'a[href]',
    'button:not([disabled])',
    'input:not([disabled])',
    'select:not([disabled])',
    'textarea:not([disabled])',
    '[tabindex]:not([tabindex="-1"])'
  ].join(', ');

  // Die Bereiche hinter dem Modal: solange es offen ist, sind sie `inert`
  // (nicht per Tab erreichbar, für Screenreader ausgeblendet).
  // Das Modal selbst liegt außerhalb dieser Elemente.
  const backgroundAreas = ['main', 'nav', 'footer']
    .map(selector => document.querySelector(selector))
    .filter(Boolean);

  // Die Karte, die das Modal geöffnet hat - dorthin kommt der Fokus zurück
  let openerCard = null;

  function getFocusableElements() {
    return [...modal.querySelectorAll(FOCUSABLE_SELECTOR)]
      // Nur tatsächlich sichtbare Elemente (offsetWidth/Height bzw. Client-Rects)
      .filter(el => el.getClientRects().length > 0);
  }

  function setBackgroundInert(isInert) {
    backgroundAreas.forEach(area => {
      if (isInert) area.setAttribute('inert', '');
      else area.removeAttribute('inert');
    });
  }

  // 📖 Funktion: Modal mit Projektdaten öffnen und füllen
  // Diese Funktion erhält alle Infos über das zu öffnende Projekt
  function openModal({ title, image1, image2, desc, tech, link, project }) {
    
    // 📌 1. TITEL EINTRAGEN
    modalTitle.textContent = title || '';  // textContent setzt den reinen Text

    // 🖼️ 2. MEDIEN-BEREICH AUFBAUEN
    gallery.innerHTML = '';     // Alte Bilder löschen / html leeren
    gallery.hidden = false;     // Standard: Medien-Bereich ist sichtbar

    if (project === "weather") {
      // 🌤️ Beim Wetter-Projekt ist das Live-Widget der Medien-Bereich.
      // Das Vorschaubild entfällt, sonst wäre das Modal doppelt so hoch.
      gallery.hidden = true;
    } else {
      // filter(Boolean) = nur Bilder, die tatsächlich vorhanden sind (nicht null/undefined)
      // forEach = für JEDES Bild...
      // Doppelte/falsche Bilder defensiv vermeiden:
      // - nur vorhandene URLs
      // - nur einzigartige URLs
      // - Wetter-Vorschaubild nur außerhalb des Weather-Modals zulassen
      const uniqueImageSources = [...new Set([image1, image2].filter(Boolean))]
        .filter(src => !src.toLowerCase().includes("wetter"));

      uniqueImageSources.forEach(src => {
        const img = document.createElement('img');  // Neues <img> Element erzeugen
        img.src = src;                              // Bildpfad setzen
        img.alt = title;                            // Alt-Text für Accessibility
        // Kein loading="lazy" mehr: Der Medien-Bereich hat eine feste Form
        // (aspect-ratio 16/9), deshalb springt die Modal-Höhe beim Laden nicht.
        img.decoding = 'async';
        img.className = 'modal_image';              // CSS-Klasse hinzufügen
        gallery.appendChild(img);                   // Bild ins Modal einfügen
      });
    }

    // 📝 3. BESCHREIBUNG EINTRAGEN
    modalDesc.textContent = desc || '';  // Text in das Beschreibungs-Element

    // 🏷️ 4. TECH-BADGES (z.B. "HTML", "CSS", "JavaScript")
    techContainer.innerHTML = '';  // Alte Badges löschen
    
    if (tech) {  // Wenn es Tech-Tags gibt
      techContainer.setAttribute('aria-hidden', 'false');  // Für Screenreader sichtbar machen
      
      // split(',') = "HTML, CSS, JS" → ["HTML", " CSS", " JS"]
      // map(t => t.trim()) = Leerzeichen entfernen von jedem
      tech.split(',').map(t => t.trim()).forEach(t => {
        const span = document.createElement('span');      // Neuer <span> für Badge
        span.className = 'tech_badge';                    // CSS-Klasse
        span.textContent = t;                             // Text des Badges
        techContainer.appendChild(span);                  // Ins Modal einfügen
      });
    } else {
      // Wenn keine Tech-Tags: Verstecke den Container
      techContainer.setAttribute('aria-hidden', 'true');  // Für Screenreader verstecken
    }

    // 🔗 5. LINKS (z.B. "Live ansehen" Button)
    linksContainer.innerHTML = '';  // Alte Links löschen
    
    if (link) {  // Falls ein Link vorhanden ist
      linksContainer.setAttribute('aria-hidden', 'false');  // Sichtbar machen
      
      const a = document.createElement('a');  // Neuer <a> Link
      // Link ist eine vollständige URL (http://...), ein relativer Pfad im
      // Portfolio (z. B. "mailpilot-demo/") oder ein Domain-Name ("example.com").
      // Nur der Domain-Name bekommt ein https:// davor – relative Pfade bleiben
      // unverändert, sonst würde "mailpilot-demo/" zu "https://mailpilot-demo/".
      const istDomainName = !link.includes('/') || /^[^/]+\.[^/]+/.test(link);
      a.href = (link.startsWith("http") || !istDomainName) ? link : `https://${link}`;
      a.target = '_blank';                    // Im neuen Tab öffnen
      a.rel = 'noopener noreferrer';         // Sicherheit für neue Tabs
      a.className = 'btn btn-primary';        // CSS-Button-Klasse
      a.textContent = t('modal-live');
      linksContainer.appendChild(a);
    } else {
      // Wenn kein Link: verstecken
      linksContainer.setAttribute('aria-hidden', 'true');
    }

    /* ================= 🌤️ WEATHER WIDGET ================= */
    // Wenn das Projekt "Weather" ist, gibt es zwei Zustände:
    //  - PyScript ist in dieser Sitzung schon geladen -> Wetter direkt laden
    //  - sonst -> Hinweis + Button zeigen (Python erst nach Klick nachladen)
    if (project === "weather" && weatherContainer) {
      weatherContainer.style.display = "flex";  // Weather-Container anzeigen
      weatherContainer.innerHTML = "";          // Alten Inhalt des Containers löschen

      if (window.loadWeatherFromPython) {
        // Funktion ist schon da (Modal war in dieser Sitzung bereits offen)
        window.loadWeatherFromPython("Hannover");
      } else {
        // Nichts laden - der Besucher entscheidet per Klick (Datenschutz)
        showWeatherNotice();
      }
    } else if (weatherContainer) {
      // Wenn NICHT weather-Projekt: Widget verstecken und leeren
      weatherContainer.style.display = "none";
      weatherContainer.innerHTML = "";
    }

    // 🎨 6. MODAL ANZEIGEN
    modal.classList.add('open');              // CSS-Klasse 'open' hinzufügen
    modal.setAttribute('aria-hidden', 'false'); // Screenreader: Modal is sichtbar
    document.body.style.overflow = 'hidden';  // Body Scroll deaktivieren (Modal ist Fokus)

    // ⌨️ Hintergrund inaktiv machen (main/nav/footer) - erst nach dem Öffnen,
    // damit der Fokus beim Setzen von `inert` nicht verloren geht.
    setBackgroundInert(true);

    // ⌨️ Fokus ins Modal: auf den ×-Button (erstes sichtbares Element im Modal
    // und der kürzeste Weg wieder heraus). Erst nach dem Öffnen möglich, ein
    // display:none-Element lässt sich nicht fokussieren.
    if (closeButton) closeButton.focus();
  }

  // 📖 Funktion: Modal wieder schließen
  function closeModal() {
    modal.classList.remove('open');          // CSS Klasse 'open' entfernen
    modal.setAttribute('aria-hidden', 'true'); // Screenreader: Modal ist versteckt
    document.body.style.overflow = '';       // Scroll wieder aktivieren

    // ⌨️ Hintergrund wieder aktiv machen (vor dem Fokus-Wechsel, sonst
    // kann die Karte den Fokus nicht annehmen)
    setBackgroundInert(false);

    // ⌨️ Fokus zurück auf die Karte, die das Modal geöffnet hat
    // (gilt für alle Wege: ESC, Backdrop-Klick, ×-Button)
    if (openerCard && typeof openerCard.focus === 'function') openerCard.focus();
  }

  /* ================= 🌤️ WETTER-WIDGET: HINWEIS UND NACHLADEN ================= */

  // 🔤 Texte des Hinweis-/Fehler-Bereichs neu setzen (für den Sprachwechsel).
  // Es werden nur die Textinhalte getauscht - Aufbau und Klick-Handler bleiben.
  function refreshWeatherTexts() {
    if (!weatherContainer) return;
    weatherContainer.querySelectorAll('[data-weather-notice]').forEach(el => {
      const role = el.dataset.weatherNotice;
      if (role === 'note') el.textContent = t('weather-consent-note');
      else if (role === 'button') el.textContent = t('weather-consent-button');
      else if (role === 'privacy') el.textContent = t('weather-consent-privacy');
      else if (role === 'loading') el.textContent = t('weather-loading');
      else if (role === 'error') el.textContent = t('weather-error');
      else if (role === 'retry') el.textContent = t('weather-retry');
    });
  }

  // 🔘 Kleiner Button im Widget-Bereich (nutzt die vorhandenen Button-Stile)
  function createNoticeButton(text, role, onClick) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'btn btn-primary';       // gleiche Optik wie "Live ansehen"
    button.style.border = 'none';               // <button> bringt sonst einen Rahmen mit
    button.style.cursor = 'pointer';
    button.dataset.weatherNotice = role;
    button.textContent = text;
    button.addEventListener('click', onClick);
    return button;
  }

  // 📄 Hinweis + Button: es wird NICHTS geladen, solange nicht geklickt wurde
  function showWeatherNotice() {
    weatherContainer.innerHTML = '';

    const box = document.createElement('div');
    box.className = 'weather_card';             // vorhandener Karten-Stil

    const note = document.createElement('p');
    note.dataset.weatherNotice = 'note';
    note.textContent = t('weather-consent-note');

    const button = createNoticeButton(t('weather-consent-button'), 'button', startWeatherWidget);

    // Link auf die Datenschutzerklärung
    const legal = document.createElement('p');
    const legalLink = document.createElement('a');
    legalLink.href = 'datenschutz.html';
    legalLink.dataset.weatherNotice = 'privacy';
    legalLink.textContent = t('weather-consent-privacy');
    legal.appendChild(legalLink);

    box.append(note, button, legal);
    weatherContainer.appendChild(box);
  }

  // ⚠️ Fehleranzeige statt endloser Ladeanzeige (offline / blockierter Host)
  function showWeatherError() {
    weatherContainer.innerHTML = '';

    const box = document.createElement('div');
    box.className = 'weather_card';

    const message = document.createElement('p');
    message.dataset.weatherNotice = 'error';
    message.textContent = t('weather-error');

    const retry = createNoticeButton(t('weather-retry'), 'retry', startWeatherWidget);

    box.append(message, retry);
    weatherContainer.appendChild(box);
  }

  // ⏳ Warten, bis weather.py loadWeatherFromPython bereitstellt - höchstens
  // timeoutMs lang, danach bricht der Aufruf mit einem Fehler ab.
  async function waitForPy(timeoutMs = 15000) {
    const deadline = Date.now() + timeoutMs;
    while (!window.loadWeatherFromPython) {
      if (Date.now() > deadline) {
        throw new Error(`loadWeatherFromPython war nach ${timeoutMs} ms nicht verfügbar`);
      }
      await new Promise(r => setTimeout(r, 100));
    }
  }

  // ▶️ Startet den Ablauf nach dem Klick: PyScript/Pyodide nachladen, dann Wetter
  async function startWeatherWidget() {
    // "Lade ..." anzeigen, solange die Dateien geholt werden
    weatherContainer.innerHTML = '';
    const loading = document.createElement('p');
    loading.className = 'weather_loading';      // vorhandener Lade-Stil
    loading.dataset.weatherNotice = 'loading';
    loading.textContent = t('weather-loading');
    weatherContainer.appendChild(loading);

    try {
      await loadPyScript();                     // core.css + core.js + <py-script>
      await waitForPy(15000);                   // warten, bis weather.py die Funktion setzt
      weatherContainer.innerHTML = '';          // Ladeanzeige weg (weather.py füllt neu)
      window.loadWeatherFromPython("Hannover"); // Hannover-Wetter laden
    } catch (e) {
      showWeatherError();                       // verständliche Meldung statt Endlosschleife
      addConsoleError('Wetter-Widget konnte nicht geladen werden:', e);
    }
  }

  // 📝 Fehler nur melden, wenn die Konsole das mitmacht (defensiv)
  function addConsoleError(...args) {
    if (typeof console !== 'undefined' && console.error) console.error(...args);
  }

  // modal.js kennt die Hinweis-Texte -> translations.js ruft das bei Sprachwechsel auf
  window.refreshWeatherNotice = refreshWeatherTexts;

  // 🖱️ PROJEKT-KARTEN KLICKBAR MACHEN
  // querySelectorAll = alle ".projekt" Elemente finden
  // Die Karten sind im HTML role="button" + tabindex="0" (per Tab erreichbar).
  document.querySelectorAll('.projekt').forEach((card, index) => {
    card.style.cursor = 'pointer';  // Maus-Cursor ändert sich zu Hand (Clicker)

    // 📖 Gemeinsamer Weg: Karte öffnet das Modal (Maus-Klick und Tastatur)
    function openFromCard() {
      const descKey = card.dataset.i18nDesc;
      openModal({
        // Daten aus HTML-Attributen auslesen:
        // card.querySelector = im Projekt-Card nach Element suchen
        title: card.querySelector('h4')?.textContent || '',  // h4 Text lesen (oder leer)
        image1: card.dataset.modalImg1,    // data-modal-img1 Attribut
        image2: card.dataset.modalImg2,    // data-modal-img2 Attribut
        desc: descKey ? t(descKey) : (card.dataset.desc || ''),  // Übersetzte Beschreibung via i18n-Key
        tech: card.dataset.tech || '',     // data-tech Attribut
        link: card.dataset.link || '',     // data-link Attribut
        project: card.dataset.project || '' // data-project Attribut
      });
      // Aktuelle Card für Sprachwechsel-Modal-Update speichern
      modal.dataset.activeCardIndex = index;
    }

    // ⌨️ Fokus-Rückgabe: merken, welche Karte das Modal geöffnet hat
    card.addEventListener('click', () => {
      openerCard = card;
      openFromCard();
    });

    // ⌨️ Tastaturbedienung: Enter und Leertaste öffnen das Modal
    card.addEventListener('keydown', (e) => {
      if (e.key !== 'Enter' && e.key !== ' ' && e.key !== 'Spacebar') return;
      e.preventDefault();  // Leertaste darf die Seite nicht scrollen
      openerCard = card;
      openFromCard();
    });
  });

  // ❌ CLOSE BUTTONS
  // data-modal-close = alle Elemente, die das Modal schließen (z.B. Backdrop, X-Button)
  document.querySelectorAll('[data-modal-close]').forEach(el =>
    el.addEventListener('click', closeModal)
  );

  // 🖱️ Wenn auf Modal-Backbone geklickt wird (dunkel), schließen
  modal.addEventListener('click', e => {
    // e.target === modal = Klick auf schwarzen Hintergrund
    if (e.target === modal) closeModal();
  });

  // ⌨️ FOKUSFALLE: Solange das Modal offen ist, bleibt Tab/Shift+Tab im Modal
  // (Schließen-Button, Links, im Wetter-Modal zusätzlich Eingabefeld,
  //  Such-Button und der Hinweis-/Retry-Button).
  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab' || !modal.classList.contains('open')) return;

    const focusable = getFocusableElements();
    if (focusable.length === 0) return;  // nichts fokussierbar: Standardverhalten

    const first = focusable[0];
    const last = focusable[focusable.length - 1];
    const active = document.activeElement;

    // Fokus liegt nicht (mehr) im Modal - z. B. nachdem das Wetter-Widget
    // seinen Inhalt ausgetauscht hat. Dann zurück ins Modal holen.
    if (!modal.contains(active)) {
      e.preventDefault();
      (e.shiftKey ? last : first).focus();
      return;
    }

    // Am Rand angekommen: umlaufen statt aus dem Modal heraus zu tabben
    if (e.shiftKey && active === first) {
      e.preventDefault();
      last.focus();
    } else if (!e.shiftKey && active === last) {
      e.preventDefault();
      first.focus();
    }
  });

  // ⌨️ ESC-Taste schließt Modal
  document.addEventListener('keydown', e => {
    if (e.key === "Escape" && modal.classList.contains('open')) closeModal();
  });

  // ⌨️ ENTER-TASTE in Wetter-Eingabe starten die Wettersuche
  document.addEventListener('keydown', (e) => {
    if (e.key !== "Enter") return;  // Nur Enter-Taste interessiert uns
    
    // Wetter-Input-Feld abrufen
    const input = document.getElementById("weather_input");
    
    // Nur wenn Modal offen UND Fokus im Input:
    if (
      modal.classList.contains('open') &&      // Modal muss offen sein
      input &&                                 // Input muss existieren
      document.activeElement === input         // Fokus muss im Input sein
    ) {
      e.preventDefault();  // Standard Browser-Verhalten (neue Zeile) verhindern
      
      const city = input.value.trim();  // Stadtname auslesen und Leerzeichen trimmen
      
      // Wenn Text da ist und Funktion existiert: Wetter laden
      if (city && window.loadWeatherFromPython) {
        window.loadWeatherFromPython(city);
      }
    }
  });
}