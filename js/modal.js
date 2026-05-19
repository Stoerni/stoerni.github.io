/* ==========================
   Projekt-Modal: Öffnen / Schließen
   Ein Modal ist ein Popup-Fenster, das Projekt-Details anzeigt
========================== */

// 📤 EXPORT: Diese Funktion wird von main.js aufgerufen
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

  // 📖 Funktion: Modal mit Projektdaten öffnen und füllen
  // Diese Funktion erhält alle Infos über das zu öffnende Projekt
  function openModal({ title, image1, image2, desc, tech, link, project }) {
    
    // 📌 1. TITEL EINTRAGEN
    modalTitle.textContent = title || '';  // textContent setzt den reinen Text

    // 🖼️ 2. BILDER-GALERIE AUFBAUEN
    gallery.innerHTML = '';  // Alte Bilder löschen / html leeren
    
    // filter(Boolean) = nur Bilder, die tatsächlich vorhanden sind (nicht null/undefined)
    // forEach = für JEDES Bild...
    [image1, image2].filter(Boolean).forEach(src => {
      const img = document.createElement('img');  // Neues <img> Element erzeugen
      img.src = src;                              // Bildpfad setzen
      img.alt = title;                            // Alt-Text für Accessibility
      // Performance-Quick-Win: auch im Modal asynchron decodieren + lazy laden
      img.loading = 'lazy';
      img.decoding = 'async';
      img.className = 'modal_image';              // CSS-Klasse hinzufügen
      gallery.appendChild(img);                   // Bild ins Modal einfügen
    });

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
      // Link ist entweder vollständig (http://...) oder ein Domain-Name
      a.href = link.startsWith("http") ? link : `https://${link}`;
      a.target = '_blank';                    // Im neuen Tab öffnen
      a.rel = 'noopener noreferrer';         // Sicherheit für neue Tabs
      a.className = 'btn btn-primary';        // CSS-Button-Klasse
      a.textContent = 'Live ansehen';
      linksContainer.appendChild(a);
    } else {
      // Wenn kein Link: verstecken
      linksContainer.setAttribute('aria-hidden', 'true');
    }

    /* ================= 🌤️ WEATHER WIDGET ================= */
    // Wenn das Projekt "Weather" ist, laden wir Wetter-Daten
    if (project === "weather" && weatherContainer) {
      weatherContainer.style.display = "flex";  // Weather-Container anzeigen
      
      // Warte, bis die Python-Wetter-Funktion verfügbar ist
      // (wird von weather.py geladen)
      async function waitForPy() {
        // Solange waitForPy nicht existiert, alle 100ms prüfen
        while (!window.loadWeatherFromPython) {
          await new Promise(r => setTimeout(r, 100));
        }
      }
      
      // Wenn Funktion ready ist, Wetter laden
      waitForPy().then(() => {
        window.loadWeatherFromPython("Hannover");  // Hannover-Wetter laden
      });
    } else if (weatherContainer) {
      // Wenn NICHT weather-Projekt: Widget verstecken und leeren
      weatherContainer.style.display = "none";
      weatherContainer.innerHTML = "";
    }

    // 🎨 6. MODAL ANZEIGEN
    modal.classList.add('open');              // CSS-Klasse 'open' hinzufügen
    modal.setAttribute('aria-hidden', 'false'); // Screenreader: Modal is sichtbar
    document.body.style.overflow = 'hidden';  // Body Scroll deaktivieren (Modal ist Fokus)
  }

  // 📖 Funktion: Modal wieder schließen
  function closeModal() {
    modal.classList.remove('open');          // CSS Klasse 'open' entfernen
    modal.setAttribute('aria-hidden', 'true'); // Screenreader: Modal ist versteckt
    document.body.style.overflow = '';       // Scroll wieder aktivieren
  }

  // 🖱️ PROJEKT-KARTEN KLICKBAR MACHEN
  // querySelectorAll = alle ".projekt" Elemente finden
  document.querySelectorAll('.projekt').forEach(card => {
    card.style.cursor = 'pointer';  // Maus-Cursor ändert sich zu Hand (Clicker)
    
    // Wenn Projekt geklickt wird:
    card.addEventListener('click', () => {
      openModal({
        // Daten aus HTML-Attributen auslesen:
        // card.querySelector = im Projekt-Card nach Element suchen
        title: card.querySelector('h4')?.textContent || '',  // h4 Text lesen (oder leer)
        image1: card.dataset.modalImg1,    // data-modal-img1 Attribut
        image2: card.dataset.modalImg2,    // data-modal-img2 Attribut
        desc: card.dataset.desc || '',     // data-desc Attribut
        tech: card.dataset.tech || '',     // data-tech Attribut
        link: card.dataset.link || '',     // data-link Attribut
        project: card.dataset.project || '' // data-project Attribut
      });
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