# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Eine Aktion: Schlüssel, Prüfung, Anwendung und Rücknahme.

Entscheidung 6 im Design-Dokument: Aktionen sind deklarative Katalog-Einträge
mit drei Teilen. Ein Eintrag besteht aus seinem Schlüssel, den Texten dazu in
der Sprachdatei (Entscheidung 7) und drei Funktionen:

* ``check``  — geht das hier überhaupt, und was ist der jetzige Zustand?
* ``apply``  — führt die Änderung aus.
* ``undo``   — stellt den vorher festgehaltenen Zustand wieder her.

Ein Eintrag führt nie einen freien Befehl aus und übernimmt nie einen Befehl aus
der Antwort des Modells: die Befehle stehen im Katalog selbst (``catalog.py``),
das Modell darf nur einen Schlüssel nennen.

Neben den drei Teilen trägt ein Eintrag drei Angaben über sich selbst, die die
Hülle und die Tests brauchen (Slice 7, als der Katalog wuchs):

* ``group``  — das Thema, unter dem er in ``/aktionen`` steht,
* ``needs_admin`` — ob die Änderung Administratorrechte braucht. Solche Einträge
  werden angekündigt und an Windows übergeben, nie selbst ausgeführt
  (Entscheidung 10); ``ActionBox`` verweigert die Ausführung.
* ``texts``  — welche Texte der Eintrag in der Sprachdatei hat. Ein Schalter mit
  Systemvorgabe hat zusätzlich ``state_unset``, ein Eintrag, der nur den Weg
  zeigt, hat stattdessen ``handover``. Ein Test prüft für jeden Eintrag genau
  diese Liste; ein fehlender Text fällt damit sofort auf.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

from ai_helper.actions.executor import Executor
from ai_helper.i18n import t

__all__ = ["BASE_TEXTS", "HANDOVER_TEXTS", "UNSET_TEXT", "Action", "ActionState"]

# Die Texte, die jeder Eintrag hat.
BASE_TEXTS: tuple[str, ...] = (
    "title",
    "description",
    "state_goal",
    "state_other",
    "done",
    "undone",
)
# Zusätzlich, wenn das System eine Vorgabe hat (etwa ein Registry-Schalter).
UNSET_TEXT = "state_unset"
# Stattdessen, wenn der Eintrag nur den Weg zeigt (Administratorrechte).
HANDOVER_TEXTS: tuple[str, ...] = ("title", "description", "handover")


@dataclass(frozen=True, slots=True)
class ActionState:
    """Der jetzige Zustand, wie ihn die Prüfung gefunden hat.

    ``raw`` ist der Wert, wie er auf dem Rechner steht — genau das, was die
    Rücknahme später wiederherstellt. ``raw=None`` heißt: dazu ist nichts
    eingestellt, es gilt die Voreinstellung des Systems; die Rücknahme entfernt
    den Wert dann wieder, statt einen Wert zu schreiben, den es nie gab.
    ``at_goal`` sagt, ob die Aktion überhaupt etwas zu tun hätte.
    """

    raw: str | None
    description: str
    at_goal: bool


@dataclass(frozen=True, slots=True)
class Action:
    """Ein Eintrag des Aktionskatalogs."""

    key: str
    check: Callable[[Executor], ActionState]
    apply: Callable[[Executor], str]
    undo: Callable[[Executor, "str | None"], str]
    group: str = "sonstiges"
    needs_admin: bool = False
    texts: tuple[str, ...] = BASE_TEXTS

    @property
    def title(self) -> str:
        """Was die Aktion tut, als kurzer Satz („Das werde ich tun: …")."""
        return t(f"action_{self.key}_title")

    @property
    def description(self) -> str:
        """Ein Satz, was die Aktion bedeutet — für die Liste und das Modell."""
        return t(f"action_{self.key}_description")

    @property
    def group_title(self) -> str:
        """Das Thema, unter dem der Eintrag in der Liste steht."""
        return t(f"action_group_{self.group}")

    @property
    def handover(self) -> str:
        """Wie der Nutzer es selbst macht — nur für Einträge, die Rechte brauchen."""
        return t(f"action_{self.key}_handover")
