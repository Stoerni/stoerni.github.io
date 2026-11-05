# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Ein Suchergebnis: Titel, Adresse und ein Auszug.

Entscheidung 9 im Design-Dokument gilt auch beim Nachschlagen: der Avatar redet
mit Beleg statt mit Vermutung. Deshalb trägt ein Treffer nicht nur Text, sondern
auch seine Quelle — Titel und Adresse. Ein Treffer ohne Quelle ist keine Quelle
und wird beim Auswerten weggelassen, statt als eigene Aussage ausgeben zu
werden.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["MAX_RESULTS", "SNIPPET_CHARS", "SearchHit"]

# Wie viele Treffer eine Suche liefert und wie lang ein Auszug höchstens ist.
# Bewusst keine Einstellung: eine Zahl, die niemand einstellen muss, wäre eine
# Entscheidung ohne Nutzer (dieselbe Regel wie beim Aktionsabschnitt in Slice 7).
MAX_RESULTS = 5
SNIPPET_CHARS = 400


@dataclass(frozen=True, slots=True)
class SearchHit:
    """Ein einzelner Treffer: Titel, Adresse und ein Auszug aus der Seite."""

    title: str
    url: str
    snippet: str = ""

    @property
    def complete(self) -> bool:
        """Trägt der Treffer eine Quelle? Ohne Titel und Adresse ist er keine."""
        return bool(self.title.strip()) and bool(self.url.strip())
