console.log("main.js lädt");

import { initDotGrid } from './dotgrid.js';
import { initTyping } from './typing.js';
import { initNavObserver } from './navObserver.js';
import { initModal } from './modal.js';
import { initContactForm } from './kontakt.js';
import { initReveal } from './reveal.js';

window.addEventListener("DOMContentLoaded", () => {
  initDotGrid();
  initTyping();
  initNavObserver();
  initModal();
  initContactForm();
  initReveal();
});

console.log("main.js geladen");