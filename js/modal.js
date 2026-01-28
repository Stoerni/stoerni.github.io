/* ==========================
   Projekt-Modal: Öffnen / Schließen
========================== */
export function initModal() {
  const modal = document.getElementById('projectModal');
  if (!modal) return;

  const modalTitle = document.getElementById('modalTitle');
  const modalImage = document.getElementById('modalImage');
  const modalDesc = document.getElementById('modalDesc');
  const techContainer = document.getElementById('modalTech');
  const linksContainer = document.getElementById('modalLinks');
  const weatherContainer = document.getElementById('weather_container');
  const weatherSearchWrapper = document.getElementById('weather_search_wrapper');
  const weatherInput = document.getElementById('weather_input');
  const weatherSearchBtn = document.getElementById('weather_search_btn');


  function openModal({ title, image1, image2, desc, tech, link, project }) {
    modalTitle.textContent = title || '';
    const gallery = document.getElementById('modalGallery');
    gallery.innerHTML = '';

    const images = [image1, image2].filter(Boolean);

    images.forEach(src => {
      const img = document.createElement('img');
      img.src = src;
      img.alt = title;
      img.className = 'modal_image';
      gallery.appendChild(img);
    });
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
      a.href = link;
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
      a.className = 'btn btn-primary';
      a.textContent = 'Live ansehen';
      linksContainer.appendChild(a);
    } else {
      linksContainer.setAttribute('aria-hidden', 'true');
    }

    // Weather nur für Weather-Projekt
    if (project === "weather") {
      weatherContainer.style.display = "flex";
      weatherSearchWrapper.style.display = "block";

      async function waitForPy() {
        while (!window.loadWeatherFromPython) {
          await new Promise(r => setTimeout(r, 100));
        }
      }

      waitForPy().then(() => {
        window.loadWeatherFromPython("Hannover");
      });

      // Alte Listener entfernen (wichtig!)
      weatherSearchBtn.replaceWith(weatherSearchBtn.cloneNode(true));
      weatherInput.replaceWith(weatherInput.cloneNode(true));

      const newBtn = document.getElementById("weather_search_btn");
      const newInput = document.getElementById("weather_input");

      newBtn.addEventListener("click", () => {
        const city = newInput.value.trim();
        if (city && window.loadWeatherFromPython) {
          window.loadWeatherFromPython(city);
        }
      });

      newInput.addEventListener("keypress", (e) => {
        if (e.key === "Enter") {
          newBtn.click();
        }
      });

    } else {
      weatherContainer.style.display = "none";
      weatherSearchWrapper.style.display = "none";
      weatherContainer.innerHTML = "";
    }
    // Such-Button Event Listener
    weatherSearchBtn.addEventListener('click', () => {
      const city = weatherInput.value.trim();
      if (city && window.loadWeatherFromPython) {
        window.loadWeatherFromPython(city);
      }
    });
    // Enter-Taste im Input-Feld  
    weatherInput.addEventListener('keypress', (e) => {
      if (e.key === "Enter") {
        weatherSearchBtn.click();
      }
    });

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

  // Klick auf Projektkarten
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

  // Close-Buttons & Backdrop
  document.querySelectorAll('[data-modal-close]').forEach(el =>
    el.addEventListener('click', closeModal)
  );
  modal.addEventListener('click', e => {
    if (e.target === modal) closeModal();
  });

  // ESC-Taste schließt Modal
  document.addEventListener('keydown', e => {
    if (e.key === "Escape" && modal.classList.contains('open')) closeModal();
  });
}
