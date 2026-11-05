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

Die deutschen Texte stehen wie überall in der Sprachdatei (``i18n/de.py``,
Entscheidung 7); hier stehen nur die Verweise darauf und die Stichwörter, an
denen eine Frage erkannt wird.
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

    ``frage`` ist die vorgeschlagene Formulierung (sie erscheint als Chip im
    Terminal). ``stichworte`` sind weitere Formulierungen oder Begriffe, bei
    denen dieselbe Antwort gilt — so wird aus „Was für eine CPU habe ich?"
    auch „welchen prozessor?" erkannt. ``antwort_key`` ist der Textschlüssel in
    der Sprachdatei.
    """

    frage: str
    antwort_key: str
    stichworte: tuple[str, ...] = ()

    @property
    def antwort(self) -> str:
        """Die Antwort im Klartext, aus der Sprachdatei."""
        return t(self.antwort_key)


# Die vorbereiteten Fragen. Reihenfolge = Anzeige-Reihenfolge der Vorschläge.
SCRIPT: tuple[ScriptEntry, ...] = (
    ScriptEntry(
        frage="Was kannst du?",
        antwort_key="demo_answer_abilities",
        stichworte=("was kannst du", "was kannst", "wer bist du", "was machst du"),
    ),
    ScriptEntry(
        frage="Wie ist mein Rechner eingerichtet?",
        antwort_key="demo_answer_setup",
        stichworte=("wie ist mein rechner", "rechner eingerichtet", "eingerichtet", "system"),
    ),
    ScriptEntry(
        frage="Was für eine CPU habe ich?",
        antwort_key="demo_answer_cpu",
        stichworte=("cpu", "prozessor", "rechenkern"),
    ),
    ScriptEntry(
        frage="Wie viel Arbeitsspeicher habe ich?",
        antwort_key="demo_answer_memory",
        stichworte=("arbeitsspeicher", "ram", "speicher"),
    ),
    ScriptEntry(
        frage="Kannst du etwas für mich einstellen?",
        antwort_key="demo_answer_actions",
        stichworte=("einstellen", "einrichten", "ändern", "etwas tun"),
    ),
    ScriptEntry(
        frage="Was ist ein Gerätetreiber?",
        antwort_key="demo_answer_driver",
        stichworte=("gerätetreiber", "treiber"),
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
        if _passt(normalisiert, _normalisieren(eintrag.frage)):
            return eintrag.antwort
        for stichwort in eintrag.stichworte:
            if _passt(normalisiert, _normalisieren(stichwort)):
                return eintrag.antwort
    return t(POLITE_ANSWER_KEY)


def polite_answer() -> str:
    """Die Höflichkeitsantwort im Klartext."""
    return t(POLITE_ANSWER_KEY)


def suggestions() -> tuple[str, ...]:
    """Die vorgeschlagenen Fragen, in Anzeige-Reihenfolge (die Chips der Demo)."""
    return tuple(eintrag.frage for eintrag in SCRIPT)
