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

// Gespeichertes Promise: die Laufzeit (core.css + core.js) darf nur einmal
// geladen werden - auch bei mehrfachem Aufruf, mehrfachem Öffnen des Modals
// und auch dann, wenn zwei Widgets (Wetter und AI-Helper) dieselbe Laufzeit
// benutzen.
let runtimePromise = null;

// Die bereits angehängten <py-script>-Quellen: jede genau einmal.
const attachedScripts = new Set();

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
 * Sorgt dafür, dass die PyScript-Laufzeit da ist (core.css -> core.js,
 * warten auf 'load'). Wiederholte Aufrufe liefern dasselbe Promise; schlägt
 * das Laden fehl (offline/blockiert), wird der Fehler weitergereicht und ein
 * neuer Versuch ist möglich (Retry-Button im Modal).
 */
export function ensurePyScriptRuntime() {
  if (runtimePromise) return runtimePromise;

  runtimePromise = (async () => {
    await injectStylesheet(CORE_CSS_URL);
    await injectModuleScript(CORE_JS_URL);
  })().catch(error => {
    // Nach einem Fehlschlag darf erneut geladen werden (Retry-Button im Modal)
    runtimePromise = null;
    throw error;
  });

  return runtimePromise;
}

/** Hängt ein <py-script src="..."> an - jede Quelle genau einmal. */
function attachPyScript(src) {
  if (attachedScripts.has(src)) return;
  attachedScripts.add(src);

  const pyScript = document.createElement('py-script');
  pyScript.setAttribute('src', src);
  document.body.appendChild(pyScript);
}

/**
 * Lädt PyScript bei Bedarf nach und hängt danach <py-script src="..."> an.
 * Reihenfolge: core.css -> core.js (warten auf 'load') -> py-script.
 */
export async function loadPyScript(weatherSrc = 'python/weather.py') {
  await ensurePyScriptRuntime();
  attachPyScript(weatherSrc);
}

/**
 * Dasselbe für ein zweites Widget (AI-Helper-Demoterminal): die Laufzeit wird
 * geteilt, jede Python-Datei aber nur einmal angehängt.
 */
export async function loadPyScriptApp(src) {
  await ensurePyScriptRuntime();
  attachPyScript(src);
}

/** True, sobald PyScript nachgeladen wurde (bzw. gerade wird). */
export function isPyScriptLoaded() {
  return runtimePromise !== null;
}
