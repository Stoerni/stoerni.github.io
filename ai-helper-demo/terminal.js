/* ==========================
   🤖 AI-HELPER: DEMOTERMINAL IM BROWSER
   Das Terminal-Widget der AI-Helper-Projektkarte (Modal) und der
   gleichnamigen Demo-Seite (ai-helper-demo/).

   Aufbau in zwei Teilen:
   - Diese Datei baut und bedient die Oberfläche (Ausgabe, Figur, Chips,
     Eingabefeld, Zustände) und ist überall dieselbe.
   - ai-helper-demo/boot.py bringt den echten Python-Kern zum Laufen und
     schickt seine Zeilen als Ereignisse hierher.

   Geladen wird nichts, solange nicht geklickt wurde: erst auf „Demo starten"
   holt js/pyscript-loader.js PyScript (Version gepinnt) und hängt boot.py an —
   dasselbe Muster wie beim Wetter-Widget.
========================== */

import { t } from '../js/translations.js';
import { loadPyScriptApp } from '../js/pyscript-loader.js';

// Der eigene Ort — daraus entstehen die Pfade, egal ob das Widget im Modal der
// Startseite steckt oder auf der Demo-Seite selbst läuft.
const MODULE_URL = import.meta.url;
const BASE_PATH = new URL('./', MODULE_URL).pathname;   // z. B. /ai-helper-demo/
const BOOT_SRC = new URL('boot.py', MODULE_URL).href;   // absolute Adresse

// Wie lange auf boot.py gewartet wird, bevor der Fehlerzustand kommt.
const READY_TIMEOUT_MS = 40000;
// Wie viele Zeilen das Terminal höchstens behält (sehr lange Sitzungen).
const MAX_LINES = 1500;

/* ================= 🔧 KLEINE HELFER ================= */

function make(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function normalizeFace(face) {
  if (Array.isArray(face)) return face;
  if (typeof face === 'string') {
    // Pyodide gibt eine Python-Liste als Proxy heraus; der sichere Weg ist ein
    // String (durch "\n" getrennt) — beides wird hier angenommen.
    return face.split('\n');
  }
  if (face && typeof face.length === 'number') {
    return Array.from({ length: face.length }, (_, i) => String(face[i]));
  }
  return [];
}

/* ================= 🤖 DAS TERMINAL ================= */

export class AiHelperTerminal {
  /**
   * @param {HTMLElement} container  Der Container (im Modal oder auf der Seite)
   */
  constructor(container) {
    this.container = container;
    this.state = 'notice';       // notice | loading | error | session
    this.errorText = '';
    this.entries = [];           // {kind:'line', text} | {kind:'figure', ...}
    this.chips = [];
    this.figure = null;          // {state, label, face}
    this.promptText = '';
    this.running = false;
    this.finished = false;
    this.ready = false;          // boot.py ist geladen, Funktionen stehen bereit
    this.history = [];           // Eingabeverlauf (Pfeil hoch/runter)
    this.historyIndex = -1;
    this.inputValue = '';
    this.dom = null;
    this.busyPromise = null;
    this.currentLang = 'de';     // aktuelle Sprache der Demo (de/en)
  }

  /* ------------------------- Zustände ------------------------- */

  /** Klick auf „Demo starten": PyScript holen, dann die Sitzung beginnen. */
  async start() {
    if (this.busyPromise) return this.busyPromise;
    this.busyPromise = (async () => {
      this.state = 'loading';
      this.errorText = '';
      this.bootError = null;
      this.render();
      try {
        await this.bootstrap();
      } catch (error) {
        this.state = 'error';
        this.errorText = t('ai-error');
        // Der technische Grund (z. B. "Prüfsumme stimmt nicht: ai_helper/…")
        // steht klein darunter - sonst wäre die Meldung nicht zu deuten.
        this.bootError = String(error && error.message ? error.message : error);
        this.render();
        if (typeof console !== 'undefined' && console.error) {
          console.error('AI-Helper-Demo konnte nicht geladen werden:', error);
        }
        return;
      }
      this.busyPromise = null;
    })();
    try {
      await this.busyPromise;
    } finally {
      this.busyPromise = null;
    }
  }

  /** PyScript + boot.py nachladen und auf die Python-Funktionen warten. */
  async bootstrap() {
    if (!this.ready) {
      // Die Seite weiß, wo der Demo-Ordner liegt (files.json und die 40 Dateien
      // werden relativ dazu geholt).
      window.aiHelperBase = BASE_PATH;
      await loadPyScriptApp(BOOT_SRC);
      await this.waitForBoot();
      this.ready = true;
    }
    if (this.state === 'session' && this.finished) {
      // Die alte Sitzung lief zu Ende: eine frische beginnen.
      this.entries = [];
      this.figure = null;
    }
    this.state = 'session';
    this.finished = false;
    this.running = false;
    this.render();
    window.aiHelperStart();
  }

  /** Warten, bis boot.py seine vier Funktionen bereitgestellt hat. */
  waitForBoot() {
    const deadline = Date.now() + READY_TIMEOUT_MS;
    return new Promise((resolve, reject) => {
      const pruefen = () => {
        if (this.bootError) {
          reject(new Error(this.bootError));
          return;
        }
        if (typeof window.aiHelperStart === 'function') {
          resolve();
          return;
        }
        if (Date.now() > deadline) {
          reject(new Error(`boot.py war nach ${READY_TIMEOUT_MS} ms nicht bereit`));
          return;
        }
        setTimeout(pruefen, 100);
      };
      pruefen();
    });
  }

  /** Ereignis aus boot.py (kommt als JSON-Zeichenkette an). */
  handleEvent(raw) {
    let event;
    try {
      event = typeof raw === 'string' ? JSON.parse(raw) : raw;
    } catch (error) {
      return;
    }
    if (!event || typeof event.t !== 'string') return;

    switch (event.t) {
      case 'line':
        this.addEntry({ kind: 'line', text: String(event.text ?? '') });
        break;
      case 'figure':
        this.figure = {
          state: String(event.state || 'neutral'),
          label: String(event.label || ''),
          face: normalizeFace(event.face)
        };
        this.renderFigure();
        break;
      case 'chips':
        this.chips = normalizeFace(event.items).map(String);
        this.renderChips();
        break;
      case 'prompt':
        this.promptText = String(event.text || '');
        this.running = Boolean(event.running);
        this.finished = !this.running;
        this.renderPrompt();
        this.renderControls();
        this.scrollToEnd();
        break;
      case 'fail':
        this.bootError = String(event.text || 'unbekannter Fehler');
        break;
      case 'ready':
        // Nur für die Prüfung/Diagnose: die Zahl der geholten Dateien.
        this.readyInfo = event;
        break;
      default:
        break;
    }
  }

  /* ------------------------- Bedienung ------------------------- */

  /** Eine Eingabezeile abschicken. */
  send(line) {
    const text = String(line ?? '');
    this.inputValue = '';
    if (this.dom && this.dom.input) this.dom.input.value = '';
    if (text.trim() === '') return;
    this.history.push(text);
    this.historyIndex = this.history.length;
    this.addEntry({ kind: 'line', text: `${this.promptText || 'Du: '}${text}`, echo: true });
    this.scrollToEnd();
    if (typeof window.aiHelperFeed === 'function') window.aiHelperFeed(text);
  }

  /** Abbrechen-Knopf: das Gespräch ruhig beenden. */
  abort() {
    if (this.running && typeof window.aiHelperAbort === 'function') {
      window.aiHelperAbort();
    }
  }

  /** Die letzte Eingabe (Pfeiltaste nach oben). */
  recall(direction) {
    if (!this.dom || this.history.length === 0) return;
    this.historyIndex = Math.min(
      Math.max(this.historyIndex + direction, 0),
      this.history.length
    );
    const value = this.historyIndex < this.history.length
      ? this.history[this.historyIndex]
      : '';
    this.dom.input.value = value;
    this.inputValue = value;
  }

  /** Sprache umschalten (DE ↔ EN). */
  async toggleLanguage() {
    if (typeof window.aiHelperSetLanguage !== 'function') return;
    const newLang = this.currentLang === 'de' ? 'en' : 'de';
    this.currentLang = newLang;
    // Python-Seite umschalten
    window.aiHelperSetLanguage(newLang);
    // UI-Texte sofort aktualisieren (ohne Neuaufbau)
    this.updateLanguageButton();
    // Die Terminal-Texte (Platzhalter, Buttons, etc.) neu rendern
    this.refreshTexts();
  }

  /** Button-Text für Sprachumschalter aktualisieren. */
  updateLanguageButton() {
    if (this.dom && this.dom.langToggle) {
      const langBtn = this.dom.langToggle;
      langBtn.textContent = this.currentLang === 'de' ? 'EN' : 'DE';
      langBtn.title = this.currentLang === 'de' ? 'Switch to English' : 'Auf Deutsch umschalten';
    }
  }

  /**
   * Das Modal wird geschlossen: ein laufendes Gespräch anhalten.
   * Die Ausgabe bleibt im Speicher und steht beim nächsten Öffnen wieder da.
   */
  stop() {
    if (this.running) this.abort();
  }

  /* ------------------------- Aufbau ------------------------- */

  attach() {
    this.render();
  }

  render() {
    if (!this.container) return;
    const focusWarImEingabefeld = Boolean(
      this.dom && this.dom.input && document.activeElement === this.dom.input
    );
    this.container.textContent = '';
    this.dom = null;

    if (this.state === 'notice') {
      this.container.appendChild(this.buildNotice());
      return;
    }
    if (this.state === 'loading') {
      this.container.appendChild(this.buildLoading());
      return;
    }
    if (this.state === 'error') {
      this.container.appendChild(this.buildError());
      return;
    }
    this.container.appendChild(this.buildSession());

    if (focusWarImEingabefeld && this.dom && this.dom.input && !this.finished) {
      this.dom.input.focus();
    }
  }

  buildNotice() {
    const box = make('div', 'ai_notice');
    const note = make('p', 'ai_notice_text', t('ai-consent-note'));
    const button = make('button', 'btn btn-primary ai_start', t('ai-consent-button'));
    button.type = 'button';
    button.addEventListener('click', () => this.start());

    const legal = make('p', 'ai_notice_legal');
    const link = make('a', null, t('ai-consent-privacy'));
    link.href = new URL('../datenschutz.html', MODULE_URL).href;
    legal.appendChild(link);

    box.append(note, button, legal);
    return box;
  }

  buildLoading() {
    const box = make('div', 'ai_notice');
    box.appendChild(make('p', 'ai_loading', t('ai-loading')));
    return box;
  }

  buildError() {
    const box = make('div', 'ai_notice');
    box.appendChild(make('p', 'ai_error', this.errorText || t('ai-error')));
    if (this.bootError) {
      box.appendChild(make('p', 'ai_error_detail', this.bootError));
    }
    const retry = make('button', 'btn btn-primary ai_start', t('ai-retry'));
    retry.type = 'button';
    retry.addEventListener('click', () => this.start());
    box.appendChild(retry);
    return box;
  }

  buildSession() {
    const wrapper = make('div', 'ai_terminal');

    // Kopfzeile: Zustandsanzeiger, Titel, Knöpfe
    const bar = make('div', 'ai_bar');
    bar.appendChild(make('span', 'ai_badge', t('ai-badge')));
    bar.appendChild(make('span', 'ai_bar_title', t('ai-title')));

    const controls = make('div', 'ai_bar_controls');
    const langToggle = make('button', 'ai_btn ai_lang_toggle', t('lang-de'));
    langToggle.type = 'button';
    langToggle.dataset.aiRole = 'lang-toggle';
    langToggle.title = t('ai-lang-tooltip');
    langToggle.addEventListener('click', () => this.toggleLanguage());
    const abort = make('button', 'ai_btn', t('ai-abort'));
    abort.type = 'button';
    abort.dataset.aiRole = 'abort';
    abort.addEventListener('click', () => this.abort());
    const restart = make('button', 'ai_btn', t('ai-restart'));
    restart.type = 'button';
    restart.dataset.aiRole = 'restart';
    restart.addEventListener('click', () => this.start());
    controls.append(langToggle, abort, restart);
    bar.appendChild(controls);
    wrapper.appendChild(bar);

    // Ausgabe + Figur
    const body = make('div', 'ai_body');
    const log = make('div', 'ai_log');
    log.setAttribute('role', 'log');
    log.setAttribute('aria-live', 'polite');
    log.setAttribute('aria-relevant', 'additions text');
    log.setAttribute('aria-label', t('ai-log-label'));
    log.tabIndex = 0;
    this.entries.forEach(entry => log.appendChild(this.buildEntry(entry, false)));
    body.appendChild(log);

    const figure = make('div', 'ai_figure');
    figure.setAttribute('aria-live', 'polite');
    body.appendChild(figure);

    wrapper.appendChild(body);

    // Vorschläge
    const chips = make('div', 'ai_chips');
    wrapper.appendChild(chips);

    // Eingabezeile
    const form = document.createElement('form');
    form.className = 'ai_input_row';
    form.noValidate = true;

    const prompt = make('span', 'ai_prompt', this.promptText || 'Du:');
    const inputId = 'ai_terminal_input';
    const label = make('label', 'ai_visually_hidden', t('ai-input-label'));
    label.htmlFor = inputId;
    const input = document.createElement('input');
    input.type = 'text';
    input.id = inputId;
    input.className = 'ai_input';
    input.autocomplete = 'off';
    input.spellcheck = false;
    input.placeholder = t('ai-placeholder');
    input.value = this.inputValue;
    input.addEventListener('input', () => { this.inputValue = input.value; });
    input.addEventListener('keydown', event => {
      if (event.key === 'ArrowUp') {
        event.preventDefault();
        this.recall(-1);
      } else if (event.key === 'ArrowDown') {
        event.preventDefault();
        this.recall(1);
      }
    });

    const submit = make('button', 'ai_send', t('ai-send'));
    submit.type = 'submit';

    form.append(label, prompt, input, submit);
    form.addEventListener('submit', event => {
      event.preventDefault();
      this.send(input.value);
    });

    wrapper.appendChild(form);

    this.dom = { wrapper, bar, controls, abort, restart, langToggle, log, figure, chips, form, input, submit, prompt };
    this.renderChips();
    this.renderFigure();
    this.renderPrompt();
    this.renderControls();
    this.scrollToEnd();
    return wrapper;
  }

  buildEntry(entry, animate) {
    if (entry.kind === 'figure') {
      const block = make('div', 'ai_entry ai_entry_figure');
      const face = make('pre', 'ai_entry_face');
      face.textContent = entry.face.join('\n');
      const caption = make('span', 'ai_entry_caption', entry.label || '');
      block.append(face, caption);
      if (!animate) block.classList.add('ai_no_animation');
      return block;
    }
    const line = make('div', 'ai_entry ai_entry_line');
    if (entry.echo) line.classList.add('ai_entry_echo');
    if (entry.text === '') {
      line.classList.add('ai_entry_blank');
      line.textContent = '\u00a0';
    } else {
      line.textContent = entry.text;
    }
    if (!animate) line.classList.add('ai_no_animation');
    return line;
  }

  addEntry(entry) {
    this.entries.push(entry);
    if (this.entries.length > MAX_LINES) {
      const ueberzaehlig = this.entries.length - MAX_LINES;
      this.entries.splice(0, ueberzaehlig);
      if (this.dom && this.dom.log) {
        for (let i = 0; i < ueberzaehlig; i += 1) {
          if (this.dom.log.firstChild) this.dom.log.removeChild(this.dom.log.firstChild);
        }
      }
    }
    if (this.dom && this.dom.log) {
      this.dom.log.appendChild(this.buildEntry(entry, true));
    } else {
      // Noch kein Aufbau im DOM (z. B. erstes Ereignis nach dem Öffnen)
      this.render();
    }
  }

  renderChips() {
    if (!this.dom || !this.dom.chips) return;
    const box = this.dom.chips;
    box.textContent = '';
    if (this.chips.length === 0 || this.finished) return;
    box.appendChild(make('span', 'ai_chips_label', t('ai-chips-label')));
    this.chips.forEach(text => {
      const chip = make('button', 'ai_chip', text);
      chip.type = 'button';
      chip.addEventListener('click', () => {
        this.inputValue = text;
        if (this.dom && this.dom.input) {
          this.dom.input.value = text;
          this.dom.input.focus();
        }
      });
      box.appendChild(chip);
    });
  }

  renderFigure() {
    if (!this.dom || !this.dom.figure) return;
    const box = this.dom.figure;
    box.textContent = '';
    if (!this.figure) return;
    const face = make('pre', 'ai_face');
    face.setAttribute('aria-hidden', 'true');
    face.textContent = this.figure.face.join('\n');
    box.appendChild(face);
    box.appendChild(make('span', 'ai_face_label', this.figure.label));
  }

  renderPrompt() {
    if (!this.dom) return;
    if (this.dom.prompt) this.dom.prompt.textContent = this.promptText || 'Du:';
    if (this.dom.input) {
      this.dom.input.disabled = !this.running;
      this.dom.input.placeholder = this.finished
        ? t('ai-placeholder-ended')
        : t('ai-placeholder');
    }
    if (this.dom.submit) this.dom.submit.disabled = !this.running;
  }

  renderControls() {
    if (!this.dom) return;
    if (this.dom.abort) this.dom.abort.hidden = !this.running;
    if (this.dom.wrapper) {
      this.dom.wrapper.classList.toggle('ai_ended', this.finished);
      this.dom.wrapper.classList.toggle('ai_running', this.running);
    }
    if (this.finished) this.renderChips();
  }

  scrollToEnd() {
    if (!this.dom || !this.dom.log) return;
    this.dom.log.scrollTop = this.dom.log.scrollHeight;
  }

  /** Beim Sprachwechsel: die Texte neu setzen (Ereignisse bleiben stehen). */
  refreshTexts() {
    this.render();
    this.updateLanguageButton();
  }
}

/* ================= 🔌 VERBINDUNG ZUR SEITE ================= */

let terminal = null;

/**
 * Holt (oder baut) das Terminal für einen Container.
 * Die Seite bleibt dieselbe: dasselbe Terminal, dieselbe Ausgabe.
 */
export function getAiHelperTerminal(container) {
  if (terminal && terminal.container !== container) {
    // Anderer Container (z. B. die Demo-Seite): Zustand übernehmen.
    const alt = terminal;
    terminal = new AiHelperTerminal(container);
    terminal.entries = alt.entries;
    terminal.chips = alt.chips;
    terminal.figure = alt.figure;
    terminal.promptText = alt.promptText;
    terminal.running = alt.running;
    terminal.finished = alt.finished;
    terminal.ready = alt.ready;
    terminal.state = alt.state === 'notice' && !alt.ready ? 'notice' : alt.state;
  } else if (!terminal) {
    terminal = new AiHelperTerminal(container);
  }

  // Ereignis-Empfänger aus boot.py
  window.aiHelperEvent = raw => terminal.handleEvent(raw);
  // Für den Sprachwechsel (translations.js ruft das auf)
  window.refreshAiHelperTexts = () => terminal.refreshTexts();

  return terminal;
}
