# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Der Charakter der Figur: Name und Tonfall an einer Stelle.

Eine Persona ist nur ein Schlüssel; die deutschen Texte dazu stehen in der
Sprachdatei (Entscheidung 7 im Design-Dokument), damit weitere Sprachen ohne
Codeänderung nachkommen. Der Kern kennt weder Persona noch Sprachdatei: die
Hülle setzt aus ``build_system_prompt`` den Systemtext zusammen.

Die Auswahl des Charakters ist Entwicklerentscheidung (Design Kapitel 9) und
über die Einstellung ``AI_HELPER_PERSONA`` austauschbar; ``mira`` ist die
Voreinstellung.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from ai_helper.core.errors import ConfigurationError
from ai_helper.i18n import t

__all__ = [
    "DEFAULT_PERSONA",
    "DEFAULT_PERSONA_KEY",
    "PERSONAS",
    "Persona",
    "build_system_prompt",
    "persona_for",
]

DEFAULT_PERSONA_KEY = "mira"


@dataclass(frozen=True, slots=True)
class Persona:
    """Ein Charakter: Name und Tonfall.

    Der Schlüssel bestimmt den Textschlüssel in der Sprachdatei
    (``persona_<schlüssel>_name`` und ``persona_<schlüssel>_character``).
    """

    key: str

    @property
    def name(self) -> str:
        """Der Name der Figur."""
        return t(f"persona_{self.key}_name")

    @property
    def character(self) -> str:
        """Der Tonfall, beschrieben für das Modell."""
        return t(f"persona_{self.key}_character")


# Die Vorschläge aus dieser Slice (Entscheidung bei Dennis): siehe PROGRESS.md.
PERSONAS: dict[str, Persona] = {
    "mira": Persona("mira"),
    "kalle": Persona("kalle"),
    "pico": Persona("pico"),
}

DEFAULT_PERSONA = PERSONAS[DEFAULT_PERSONA_KEY]


def persona_for(key: str) -> Persona:
    """Holt den Charakter zu ``key`` oder meldet verständlich, was fehlt."""
    try:
        return PERSONAS[key]
    except KeyError:
        raise ConfigurationError(
            t("invalid_persona", value=key, known=", ".join(sorted(PERSONAS)))
        ) from None


def build_system_prompt(persona: Persona, facts: Sequence[str] = ()) -> str:
    """Baut den Systemtext aus Charakter und gemerkten Tatsachen.

    Ohne Tatsachen steht keine Gedächtnis-Sektion im Text: eine leere Sitzung
    startet wirklich ohne Gedächtnis. Es wird nichts ergänzt und nichts
    umformuliert; im Text stehen genau die übergebenen Tatsachen.
    """
    text = t("persona_system", name=persona.name, character=persona.character)
    gemerkt = [fact for fact in facts if fact.strip()]
    if not gemerkt:
        return text
    aufzaehlung = "\n".join(f"- {fact}" for fact in gemerkt)
    return f"{text}\n{t('persona_memory', header=t('persona_memory_header'), facts=aufzaehlung)}"
