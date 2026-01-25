// ToDo: Modal per Tastatur (ESC-Taste) schließbar

/* ==========================
    Projekt-Modal: Öffnen / Schließen
    - Bei Klick auf `.projekt` wird das Modal geöffnet
    - Inhalte (Titel, Bild, Beschreibung) werden aus dem Projekt-Element gelesen
========================== */
// Funktion wird von main.js gestartet
export function initModal() {

  // Modal-Element holen
  const modal = document.getElementById('projectModal');
  if (!modal) return; // Falls kein Modal existiert → abbrechen

  // Einzelne Elemente im Modal
  const modalTitle = document.getElementById('modalTitle');
  const modalImage = document.getElementById('modalImage');
  const modalDesc = document.getElementById('modalDesc');
  const techContainer = document.getElementById('modalTech');
  const linksContainer = document.getElementById('modalLinks');

  // Öffnet das Modal mit Daten aus dem Projekt
  function openModal({ title, imageSrc, desc, tech, link }) {

    modalTitle.textContent = title || ''; // Titel setzen

    // Bild anzeigen oder verstecken
    if (imageSrc) {
      modalImage.src = imageSrc;
      modalImage.style.display = 'block';
      modalImage.alt = title || '';
    } else {
      modalImage.style.display = 'none';
    }

    // Beschreibungstext setzen
    modalDesc.textContent = desc || '';

    // Technik-Badges erzeugen
    techContainer.innerHTML = ''; // vorher leeren
    if (tech) {
      techContainer.setAttribute('aria-hidden', 'false');

      tech.split(',').map(t => t.trim()).forEach(t => {
        const span = document.createElement('span');
        span.className = 'tech_badge';
        span.textContent = t;
        techContainer.appendChild(span);
      });
    } else {
      techContainer.setAttribute('aria-hidden', 'true');
    }

    // Links (z.B. Live-Demo)
    linksContainer.innerHTML = '';
    if (link) {
      linksContainer.setAttribute('aria-hidden', 'false');

      const a = document.createElement('a');
      a.href = link;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.className = 'btn btn-primary';
      a.textContent = 'Live ansehen';
      linksContainer.appendChild(a);
    } else {
      linksContainer.setAttribute('aria-hidden', 'true');
    }

    // Modal anzeigen
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden'; // Scrollen deaktivieren
  }

  // Modal schließen
  function closeModal() {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  // Klick auf Projekt-Karten öffnet Modal
  document.querySelectorAll('.projekt').forEach(card => {
    card.style.cursor = 'pointer';

    card.addEventListener('click', () => {
      const title = card.querySelector('h4')?.textContent || '';
      const img = card.querySelector('img')?.src || '';
      const desc = card.dataset.desc || '';
      const tech = card.dataset.tech || '';
      const link = card.dataset.link || '';

      openModal({ title, imageSrc: img, desc, tech, link });
    });
  });

  // Schließen-Buttons & Backdrop
  document.querySelectorAll('[data-modal-close]').forEach(el =>
    el.addEventListener('click', closeModal)
  );

  modal.addEventListener('click', e => {
    if (e.target === modal) closeModal();
  });
}