/* ==========================
   Projekt-Modal: Öffnen / Schließen
========================== */
export function initModal() {
  const modal = document.getElementById('projectModal');
  if (!modal) return;

  const modalTitle = document.getElementById('modalTitle');
  const modalDesc = document.getElementById('modalDesc');
  const techContainer = document.getElementById('modalTech');
  const linksContainer = document.getElementById('modalLinks');
  const weatherContainer = document.getElementById('weather_container');
  const gallery = document.getElementById('modalGallery');

  function openModal({ title, image1, image2, desc, tech, link, project }) {
    // Titel
    modalTitle.textContent = title || '';

    // Bilder-Galerie
    gallery.innerHTML = '';
    [image1, image2].filter(Boolean).forEach(src => {
      const img = document.createElement('img');
      img.src = src;
      img.alt = title;
      img.className = 'modal_image';
      gallery.appendChild(img);
    });

    // Beschreibung
    modalDesc.textContent = desc || '';

    // Tech Badges
    techContainer.innerHTML = '';
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

    // Links
    linksContainer.innerHTML = '';
    if (link) {
      linksContainer.setAttribute('aria-hidden', 'false');
      const a = document.createElement('a');
      a.href = link.startsWith("http") ? link : `https://${link}`;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.className = 'btn btn-primary';
      a.textContent = 'Live ansehen';
      linksContainer.appendChild(a);
    } else {
      linksContainer.setAttribute('aria-hidden', 'true');
    }

    /* ================= WEATHER ================= */
    if (project === "weather" && weatherContainer) {
      weatherContainer.style.display = "flex";
      async function waitForPy() {
        while (!window.loadWeatherFromPython) {
          await new Promise(r => setTimeout(r, 100));
        }
      }
      waitForPy().then(() => {
        window.loadWeatherFromPython("Hannover");
      });
    } else if (weatherContainer) {
      weatherContainer.style.display = "none";
      weatherContainer.innerHTML = "";
    }


    // Modal anzeigen
    modal.classList.add('open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    modal.classList.remove('open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  // Projektkarten klickbar machen
  document.querySelectorAll('.projekt').forEach(card => {
    card.style.cursor = 'pointer';
    card.addEventListener('click', () => {
      openModal({
        title: card.querySelector('h4')?.textContent || '',
        image1: card.dataset.modalImg1,
        image2: card.dataset.modalImg2,
        desc: card.dataset.desc || '',
        tech: card.dataset.tech || '',
        link: card.dataset.link || '',
        project: card.dataset.project || ''
      });
    });
  });

  // Close Buttons
  document.querySelectorAll('[data-modal-close]').forEach(el =>
    el.addEventListener('click', closeModal)
  );

  modal.addEventListener('click', e => {
    if (e.target === modal) closeModal();
  });

  document.addEventListener('keydown', e => {
    if (e.key === "Escape" && modal.classList.contains('open')) closeModal();
  });
}
