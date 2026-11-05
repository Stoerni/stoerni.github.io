# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Einstellungen an einer Stelle gebündelt.

Reihenfolge, in der ein Wert gesucht wird (der erste Treffer gewinnt):
1. ausdrücklich übergebener Wert (Kommandozeile),
2. Umgebungsvariable,
3. ``.env``-Datei,
4. Voreinstellung hier im Modul.

Der Schlüssel kommt zusätzlich aus bekannten Variablennamen anderer
Werkzeuge, damit ein schon vorhandener Schlüssel weiterhilft.
"""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from ai_helper.core.errors import ConfigurationError
from ai_helper.i18n import t
from ai_helper.persona import DEFAULT_PERSONA_KEY

__all__ = [
    "DEFAULT_BASE_URL",
    "DEFAULT_ENV_FILE",
    "DEFAULT_LEARN",
    "DEFAULT_LOCAL_MODEL",
    "DEFAULT_LOCAL_TIMEOUT_S",
    "DEFAULT_LOG_FILE",
    "DEFAULT_MEMORY_FILE",
    "DEFAULT_MODE",
    "DEFAULT_MODEL",
    "DEFAULT_OLLAMA_URL",
    "DEFAULT_SEARCH",
    "DEFAULT_TIMEOUT_S",
    "KEY_ENV_NAMES",
    "LEARN_OFF_VALUES",
    "LEARN_ON_VALUES",
    "LEARN_VALUES",
    "LOG_OFF_VALUES",
    "MEMORY_OFF_VALUES",
    "MODES",
    "MODE_LOCAL",
    "MODE_ONLINE",
    "SEARCH_EXA",
    "SEARCH_KEY_ENV",
    "SEARCH_OFF",
    "SEARCH_VALUES",
    "SEARCH_WIKIPEDIA",
    "Settings",
    "read_env_file",
]

DEFAULT_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-4o-mini"
DEFAULT_TIMEOUT_S = 60.0
DEFAULT_ENV_FILE = Path(".env")

# Betriebsart: online (Voreinstellung, damit sich für Dennis nichts ändert)
# oder lokal über Ollama (Entscheidung 8 und 6).
MODE_ONLINE = "online"
MODE_LOCAL = "lokal"
MODES = (MODE_ONLINE, MODE_LOCAL)
DEFAULT_MODE = MODE_ONLINE

# Der lokale Dienst und sein Modell. Kandidaten laut Design Kapitel 9: kleine
# 2- bis 4-Milliarden-Modelle in 4-Bit-Komprimierung, deutschtauglich.
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434"
DEFAULT_LOCAL_MODEL = "llama3.2:3b"

# Ein lokales Modell lädt erst in den Arbeitsspeicher und antwortet dann auf
# der CPU mit grob 5 bis 15 Wörtern je Sekunde; 60 Sekunden wären dafür knapp.
DEFAULT_LOCAL_TIMEOUT_S = 300.0

# Das Gedächtnis liegt im Benutzerordner, nicht im Projektordner: es gehört dem
# Nutzer, nicht dem Projekt, und überlebt jeden Programmordner. Das Protokoll
# der Aktionen (Slice 6) liegt daneben.
DEFAULT_MEMORY_FILE = Path.home() / ".ai-helper" / "memory.json"
DEFAULT_LOG_FILE = Path.home() / ".ai-helper" / "actions.json"

# So lassen sich das Gedächtnis und das Protokoll ausdrücklich abschalten.
MEMORY_OFF_VALUES = ("aus", "off")
LOG_OFF_VALUES = MEMORY_OFF_VALUES

# Lernmodus (Slice 8, Ansatz C aus Design Kapitel 6.1): ``an`` heißt erklären
# statt ausführen, ``aus`` führt nach Bestätigung aus wie bisher — und bleibt die
# Voreinstellung, damit sich für Dennis ohne Zutun nichts ändert. Im Gespräch
# schaltet ``/lernen`` um; ein unbekannter Wert ist ein Fehler wie bei der
# Betriebsart, damit ein Tippfehler nicht stillschweigend das Falsche tut.
LEARN_ON = "an"
LEARN_OFF = "aus"
# Die Wörter, die als "an" bzw. "aus" gelten (Groß-/Kleinschreibung und
# Leerzeichen sind egal).
LEARN_ON_VALUES = (LEARN_ON, "on", "ein")
LEARN_OFF_VALUES = (LEARN_OFF, "off")
# Die gültigen Werte für die Fehlermeldung.
LEARN_VALUES = (LEARN_ON, LEARN_OFF)
DEFAULT_LEARN = LEARN_OFF

# Recherche (Slice 9): nachschlagen im Netz. Drei Werte:
# * wikipedia — die deutsche Wikipedia (Wikimedia): kostenlos, ohne Schlüssel,
#   ohne Konto, datensparsam; die Voreinstellung, damit Nachschlagen ohne
#   Einrichtung funktioniert (Design Kapitel 5: der Avatar muss auch ohne
#   eigenen Schlüssel brauchbar sein).
# * exa — echte Websuche über einen Schlüssel (AI_HELPER_SEARCH_KEY).
# * aus — kein Nachschlagen; die Hülle meldet es und schickt nichts raus.
SEARCH_WIKIPEDIA = "wikipedia"
SEARCH_EXA = "exa"
SEARCH_OFF = "aus"
SEARCH_VALUES = (SEARCH_WIKIPEDIA, SEARCH_EXA, SEARCH_OFF)
DEFAULT_SEARCH = SEARCH_WIKIPEDIA
# Der Schlüssel für die Websuche. Bewusst ein eigener Name neben dem
# Modell-Schlüssel: wer nur antworten lassen will, soll nicht zwangsläufig auch
# suchen lassen.
SEARCH_KEY_ENV = "AI_HELPER_SEARCH_KEY"

# Der erste gesetzte Name gewinnt. AI_HELPER_API_KEY ist der eigene Name,
# die beiden anderen sind gängige Variablennamen bereits eingerichteter
# Werkzeuge.
KEY_ENV_NAMES = ("AI_HELPER_API_KEY", "OPENROUTER_API_KEY", "OPENAI_API_KEY")


def read_env_file(path: Path) -> dict[str, str]:
    """Liest eine einfache ``KEY=WERT``-Datei.

    Leerzeilen und Zeilen mit ``#`` werden übersprungen, ein führendes
    ``export`` und umschließende Anführungszeichen sind erlaubt.
    Eine fehlende Datei ist kein Fehler, sie liefert eine leere Zuordnung.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return {}
    except OSError:
        return {}

    values: dict[str, str] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        name, _, value = line.partition("=")
        name = name.strip()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        if name:
            values[name] = value
    return values


@dataclass(frozen=True, slots=True)
class Settings:
    """Alles, was der Start braucht."""

    model: str
    base_url: str
    api_key: str | None = field(repr=False)  # niemals in Ausgaben zeigen
    key_source: str | None
    timeout_s: float
    env_file: Path | None = None
    persona_key: str = DEFAULT_PERSONA_KEY
    memory_file: Path | None = None
    log_file: Path | None = None
    mode: str = DEFAULT_MODE
    # Lernmodus (Slice 8): an = erklären statt ausführen. Voreinstellung aus.
    learn_mode: bool = False
    # Recherche (Slice 9): welcher Suchdienst nachschlägt und sein Schlüssel.
    search: str = DEFAULT_SEARCH
    # Auch der Suchschlüssel steht nie in Ausgaben.
    search_key: str | None = field(repr=False, default=None)
    search_key_source: str | None = None

    @property
    def has_key(self) -> bool:
        return bool(self.api_key)

    @property
    def has_search_key(self) -> bool:
        return bool(self.search_key)

    @property
    def search_off(self) -> bool:
        """Ist das Nachschlagen abgeschaltet?"""
        return self.search == SEARCH_OFF

    @property
    def search_name(self) -> str:
        """Der Suchdienst als Anzeigetext."""
        return t(f"search_name_{self.search}")

    @property
    def is_local(self) -> bool:
        """Läuft das Gespräch über das lokale Modell?"""
        return self.mode == MODE_LOCAL

    @property
    def mode_name(self) -> str:
        """Die Betriebsart als Anzeigetext."""
        return t(f"mode_{self.mode}")

    @classmethod
    def load(
        cls,
        *,
        env: Mapping[str, str] | None = None,
        env_file: Path | None = None,
        model: str | None = None,
        base_url: str | None = None,
        persona: str | None = None,
        memory_file: str | None = None,
        log_file: str | None = None,
        mode: str | None = None,
        learn: str | None = None,
        search: str | None = None,
        ollama_url: str | None = None,
        local_model: str | None = None,
    ) -> "Settings":
        """Baut die Einstellungen aus Umgebung, Datei, Übergabe und Voreinstellung."""
        environment = os.environ if env is None else env
        path = DEFAULT_ENV_FILE if env_file is None else env_file
        from_file = read_env_file(path)

        def pick(name: str, override: str | None = None) -> str | None:
            if override:
                return override
            value = environment.get(name)
            if value:
                return value
            value = from_file.get(name)
            if value:
                return value
            return None

        # Die Betriebsart steht zuerst fest: sie entscheidet, welches Modell und
        # welche Adresse gelten und welches Zeitlimit voreingestellt ist.
        chosen_mode = (pick("AI_HELPER_MODE", mode) or DEFAULT_MODE).strip().lower()
        if chosen_mode not in MODES:
            raise ConfigurationError(
                t("invalid_mode", value=chosen_mode, known=", ".join(MODES))
            )

        chosen_persona = pick("AI_HELPER_PERSONA", persona) or DEFAULT_PERSONA_KEY

        # Der Lernmodus: an oder aus, streng geprüft wie die Betriebsart.
        raw_learn = (pick("AI_HELPER_LEARN", learn) or DEFAULT_LEARN).strip().lower()
        if raw_learn in LEARN_ON_VALUES:
            learn_mode = True
        elif raw_learn in LEARN_OFF_VALUES:
            learn_mode = False
        else:
            raise ConfigurationError(
                t("invalid_learn", value=raw_learn, known=", ".join(LEARN_VALUES))
            )

        # Der Suchdienst (Slice 9): wikipedia, exa oder aus — streng geprüft wie
        # die Betriebsart und der Lernmodus.
        raw_search = (pick("AI_HELPER_SEARCH", search) or DEFAULT_SEARCH).strip().lower()
        if raw_search not in SEARCH_VALUES:
            raise ConfigurationError(
                t("invalid_search", value=raw_search, known=", ".join(SEARCH_VALUES))
            )

        if chosen_mode == MODE_LOCAL:
            # Im lokalen Betrieb ist keine Basis-URL und kein Schlüssel nötig;
            # gebraucht wird die Adresse des lokalen Dienstes und sein Modell.
            chosen_model = (
                pick("AI_HELPER_LOCAL_MODEL", local_model or model) or DEFAULT_LOCAL_MODEL
            )
            chosen_base_url = (
                pick("AI_HELPER_OLLAMA_URL", ollama_url) or DEFAULT_OLLAMA_URL
            ).rstrip("/")
        else:
            chosen_model = pick("AI_HELPER_MODEL", model) or DEFAULT_MODEL
            chosen_base_url = (
                pick("AI_HELPER_BASE_URL", base_url) or DEFAULT_BASE_URL
            ).rstrip("/")

        # Der Gedächtnispfad ist die eine Einstellung, bei der ein ausdrücklich
        # leerer Wert nicht "nimm die Voreinstellung" heißt, sondern "kein
        # Gedächtnis". Deshalb steht die Prüfung hier und nicht in pick().
        raw_memory = pick("AI_HELPER_MEMORY_FILE", memory_file)
        memory_path: Path | None = DEFAULT_MEMORY_FILE
        if raw_memory:
            memory_path = (
                None
                if raw_memory.strip().lower() in MEMORY_OFF_VALUES
                else Path(raw_memory).expanduser()
            )

        # Dasselbe für das Protokoll der Aktionen: leer heißt Voreinstellung,
        # "aus" heißt kein Protokoll (und damit keine Aktionen).
        raw_log = pick("AI_HELPER_LOG_FILE", log_file)
        log_path: Path | None = DEFAULT_LOG_FILE
        if raw_log:
            log_path = (
                None
                if raw_log.strip().lower() in LOG_OFF_VALUES
                else Path(raw_log).expanduser()
            )

        api_key: str | None = None
        key_source: str | None = None
        for name in KEY_ENV_NAMES:
            value = environment.get(name) or from_file.get(name)
            if value:
                api_key = value
                key_source = f"Variable {name}" if environment.get(name) else f"{path.name}: {name}"
                break

        # Der Suchschlüssel (Slice 9) hat einen eigenen Namen; er ist nur für
        # die Websuche nötig, nicht für das Antworten.
        search_key: str | None = environment.get(SEARCH_KEY_ENV) or from_file.get(SEARCH_KEY_ENV)
        search_key_source: str | None = None
        if search_key:
            search_key_source = (
                f"Variable {SEARCH_KEY_ENV}"
                if environment.get(SEARCH_KEY_ENV)
                else f"{path.name}: {SEARCH_KEY_ENV}"
            )
        else:
            search_key = None

        raw_timeout = pick("AI_HELPER_TIMEOUT_S")
        timeout_s = DEFAULT_LOCAL_TIMEOUT_S if chosen_mode == MODE_LOCAL else DEFAULT_TIMEOUT_S
        if raw_timeout:
            try:
                timeout_s = float(raw_timeout)
            except ValueError:
                raise ConfigurationError(t("invalid_timeout", value=raw_timeout)) from None
            if timeout_s <= 0:
                raise ConfigurationError(t("invalid_timeout", value=raw_timeout)) from None

        return cls(
            model=chosen_model,
            base_url=chosen_base_url,
            api_key=api_key,
            key_source=key_source,
            timeout_s=timeout_s,
            env_file=path,
            persona_key=chosen_persona,
            memory_file=memory_path,
            log_file=log_path,
            mode=chosen_mode,
            learn_mode=learn_mode,
            search=raw_search,
            search_key=search_key,
            search_key_source=search_key_source,
        )

    def require_key(self) -> str:
        """Gibt den Schlüssel zurück oder meldet verständlich, was fehlt.

        Nur der Onlinemodus braucht einen Schlüssel; im lokalen Betrieb wird
        diese Prüfung nie aufgerufen (Entscheidung 8: Onlinemodus nur mit
        hinterlegtem Schlüssel, lokaler Betrieb ohne).
        """
        if not self.api_key:
            raise ConfigurationError(f"{t('missing_key')} {t('missing_key_hint')} {t('missing_key_hint_env')}")
        return self.api_key
