# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Das Drehbuch der Demo: feste Frage-Antwort-Paare für den geskripteten Anbieter.

Der Demo-Anbieter (``provider.py``) kann nicht wirklich denken: es gibt kein
Modell, keinen Schlüssel und kein Netz. Er antwortet deshalb aus einem
**Drehbuch** — einer kurzen Liste vorbereiteter Fragen mit ihren Antworten.

Zwei Regeln, die diese Datei durchsetzt (und die die Tests festnageln):

* Eine vorbereitete Frage liefert **genau** ihre Drehbuchantwort.
* Alles Unvorbereitete liefert die **Höflichkeitsantwort** — und niemals eine
  erfundene Fachantwort. Eine Demo, die sich eine Antwort ausdenkt, wäre ein
  Versprechen, das das Produkt hier nicht halten kann.

Die Texte stehen wie überall in der Sprachdatei (``i18n/de.py`` und
``i18n/en.py``, Entscheidung 7); hier stehen nur die Verweise darauf und die
Stichwörter, an denen eine Frage erkannt wird — in beiden Sprachen.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from ai_helper.i18n import t

__all__ = [
    "POLITE_ANSWER_KEY",
    "SCRIPT",
    "ScriptEntry",
    "answer_for",
    "polite_answer",
    "suggestions",
]

# Der Text, den jede unvorbereitete Frage bekommt.
POLITE_ANSWER_KEY = "demo_polite_answer"

# Nur Buchstaben (inkl. Umlaute) und Ziffern zählen beim Vergleich: Satzzeichen,
# Groß- und Kleinschreibung und doppelte Leerzeichen sollen eine Frage nicht
# unerkannt lassen.
_WORT_RE = re.compile(r"[0-9a-zäöüß]+")


@dataclass(frozen=True, slots=True)
class ScriptEntry:
    """Eine vorbereitete Frage mit ihrer Antwort.

    ``frage_key`` ist der Textschlüssel der vorgeschlagenen Formulierung (sie
    erscheint als Chip auf der Demo-Seite); ``frage`` gibt sie im Klartext in
    der gerade eingestellten Sprache zurück. ``stichworte`` sind weitere
    Formulierungen oder Begriffe, bei denen dieselbe Antwort gilt — so wird aus
    „Was für eine CPU habe ich?" auch „welchen prozessor?" erkannt, und aus
    „What CPU do I have?" auch „processor". ``antwort_key`` ist der
    Textschlüssel der Antwort in der Sprachdatei.
    """

    frage_key: str
    antwort_key: str
    stichworte: tuple[str, ...] = ()

    @property
    def frage(self) -> str:
        """Die vorgeschlagene Frage im Klartext, in der eingestellten Sprache."""
        return t(self.frage_key)

    @property
    def antwort(self) -> str:
        """Die Antwort im Klartext, aus der Sprachdatei."""
        return t(self.antwort_key)


# Die vorbereiteten Fragen. Reihenfolge = Anzeige-Reihenfolge der Vorschläge.
SCRIPT: tuple[ScriptEntry, ...] = (
    ScriptEntry(
        frage_key="demo_question_abilities",
        antwort_key="demo_answer_abilities",
        stichworte=(
            "was kannst du",
            "was kannst",
            "wer bist du",
            "was machst du",
            "what can you do",
            "what can you",
            "who are you",
            "what do you do",
        ),
    ),
    ScriptEntry(
        frage_key="demo_question_setup",
        antwort_key="demo_answer_setup",
        stichworte=(
            "wie ist mein rechner",
            "rechner eingerichtet",
            "eingerichtet",
            "system",
            "how is my computer set up",
            "computer set up",
        ),
    ),
    ScriptEntry(
        frage_key="demo_question_cpu",
        antwort_key="demo_answer_cpu",
        stichworte=("cpu", "prozessor", "rechenkern", "processor", "cores"),
    ),
    ScriptEntry(
        frage_key="demo_question_memory",
        antwort_key="demo_answer_memory",
        stichworte=("arbeitsspeicher", "ram", "speicher", "memory"),
    ),
    ScriptEntry(
        frage_key="demo_question_actions",
        antwort_key="demo_answer_actions",
        stichworte=(
            "einstellen",
            "einrichten",
            "ändern",
            "etwas tun",
            "change a setting",
            "setting",
        ),
    ),
    ScriptEntry(
        frage_key="demo_question_driver",
        antwort_key="demo_answer_driver",
        stichworte=("gerätetreiber", "treiber", "device driver", "driver"),
    ),
)


def _normalisieren(text: str) -> str:
    """Macht aus einer Frage eine vergleichbare Zeichenkette aus ganzen Wörtern."""
    return " ".join(_WORT_RE.findall(text.lower()))


def _passt(frage: str, stichwort: str) -> bool:
    """Kommt ``stichwort`` als **ganzes Wort** in ``frage`` vor?

    Ganze Wörter, damit „cpu" nicht in „capture" anschlägt: die umgebenden
    Leerzeichen markieren die Wortgrenze.
    """
    return f" {stichwort} " in f" {frage} "


def answer_for(frage: str) -> str:
    """Die Antwort zu einer Frage: Drehbuchantwort oder Höflichkeitsantwort.

    Es gibt keinen dritten Fall. Passt kein Eintrag, kommt die
    Höflichkeitsantwort — nicht eine erfundene Fachantwort.
    """
    normalisiert = _normalisieren(frage)
    for eintrag in SCRIPT:
        if _passt(normalisiert, _normalisieren(t(eintrag.frage_key))):
            return eintrag.antwort
        for stichwort in eintrag.stichworte:
            if _passt(normalisiert, _normalisieren(stichwort)):
                return eintrag.antwort
    return t(POLITE_ANSWER_KEY)


def polite_answer() -> str:
    """Die Höflichkeitsantwort im Klartext."""
    return t(POLITE_ANSWER_KEY)


def suggestions() -> tuple[str, ...]:
    """Die vorgeschlagenen Fragen, in Anzeige-Reihenfolge (die Chips der Demo).

    In der gerade eingestellten Sprache — die Seite holt sie nach einem
    Sprachwechsel erneut, sonst stünden deutsche Chips unter englischem Text.
    """
    return tuple(t(eintrag.frage_key) for eintrag in SCRIPT)
