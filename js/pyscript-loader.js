/* ==========================
   🐍 PYSCRIPT / PYODIDE NACH LADEN
   PyScript (core.css + core.js) und damit Pyodide sind mehrere MB und
   würden bei jedem Seitenaufruf von pyscript.net und cdn.jsdelivr.net
   geladen - samt IP-Adresse des Besuchers. Deshalb passiert das jetzt
   erst, wenn das Wetter-Widget wirklich benutzt wird (Klick im Modal).
========================== */

const PYSCRIPT_VERSION = '2024.1.1';  // Bewusst gepinnt: gleiche Version wie vorher

const CORE_CSS_URL = `https://pyscript.net/releases/${PYSCRIPT_VERSION}/core.css`;
const CORE_JS_URL = `https://pyscript.net/releases/${PYSCRIPT_VERSION}/core.js`;

// Gespeichertes Promise: die Funktion darf nur einmal laden (auch bei
// mehrfachem Aufruf / mehrfachem Öffnen des Modals).
let loadPromise = null;

// 🔗 1. Stylesheet einhängen und auf 'load' warten
function injectStylesheet(href) {
  return new Promise((resolve, reject) => {
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.href = href;
    link.addEventListener('load', resolve, { once: true });
    link.addEventListener('error', () => reject(new Error(`core.css nicht ladbar: ${href}`)), { once: true });
    document.head.appendChild(link);
  });
}

// 🔗 2. Modul-Script einhängen und auf 'load' warten
function injectModuleScript(src) {
  return new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.type = 'module';
    script.src = src;
    script.addEventListener('load', resolve, { once: true });
    script.addEventListener('error', () => reject(new Error(`core.js nicht ladbar: ${src}`)), { once: true });
    document.head.appendChild(script);
  });
}

/**
 * Lädt PyScript bei Bedarf nach und hängt danach <py-script src="..."> an.
 * Reihenfolge: core.css -> core.js (warten auf 'load') -> py-script.
 * Wiederholte Aufrufe liefern dasselbe Promise.
 * Schlägt das Laden fehl (offline/blockiert), wird der Fehler
 * weitergereicht und ein neuer Versuch ist möglich.
 */
export function loadPyScript(weatherSrc = 'python/weather.py') {
  if (loadPromise) return loadPromise;

  loadPromise = (async () => {
    await injectStylesheet(CORE_CSS_URL);
    await injectModuleScript(CORE_JS_URL);

    // Erst jetzt das Python-File als <py-script> anhängen
    const pyScript = document.createElement('py-script');
    pyScript.setAttribute('src', weatherSrc);
    document.body.appendChild(pyScript);

    return pyScript;
  })().catch(error => {
    // Nach einem Fehlschlag darf erneut geladen werden (Retry-Button im Modal)
    loadPromise = null;
    throw error;
  });

  return loadPromise;
}

/** True, sobald PyScript nachgeladen wurde. */
export function isPyScriptLoaded() {
  return loadPromise !== null;
}
