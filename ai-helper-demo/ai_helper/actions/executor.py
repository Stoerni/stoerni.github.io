# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Der Ausführende: der eine Ort, an dem eine Aktion wirklich etwas tut.

Eine Aktion liest ihren jetzigen Zustand und ändert ihn über dieses Protokoll.
Der Aktionskatalog (``catalog.py``) kennt nur diese Schnittstelle, nicht den
Befehl dahinter — genau wie die Werkzeuge nur die Systemabfrage kennen
(``tools/runner.py``). Die Tests setzen einen Doppelgänger ein, damit kein
Testlauf etwas am System ändert.

Der echte Ausführende führt ausschließlich Befehle aus, die im Katalog
festgeschrieben sind: kein Netz, keine Administratorrechte, kein Passwort,
keine Zugangsdaten (Entscheidung 10). Was Rechte braucht, scheitert mit einer
deutschen Meldung, statt nach ihnen zu fragen. Schlägt ein Befehl fehl, ist das
kein Absturz, sondern ein ``ActionError``.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from ai_helper.core.errors import ActionError
from ai_helper.tools.runner import DEFAULT_TIMEOUT_S, SystemRunner, ToolUnavailable

__all__ = ["Executor", "SystemExecutor", "default_executor"]


@runtime_checkable
class Executor(Protocol):
    """Führt einen Befehl aus — anders als die Systemabfrage darf er ändern."""

    def run(self, command: Sequence[str]) -> str:
        """Führt ``command`` aus und liefert seine Ausgabe.

        Wirft ``ActionError``, wenn das nicht geht (Befehl fehlt, Rechte fehlen,
        Zeitablauf).
        """
        ...


class SystemExecutor:
    """Der echte Ausführende.

    Er benutzt denselben Mechanismus wie die Systemabfrage der Werkzeuge
    (``SystemRunner``: ``subprocess``, ohne Konsolenfenster), ist aber
    ausdrücklich auch für ändernde Befehle da. Ein fehlgeschlagener Befehl wird
    von ``ToolUnavailable`` in ``ActionError`` übersetzt, damit der Aktionsrahmen
    nur eine Fehlerart kennen muss.
    """

    def __init__(self, timeout_s: float = DEFAULT_TIMEOUT_S) -> None:
        self._runner = SystemRunner(timeout_s)

    def run(self, command: Sequence[str]) -> str:
        try:
            return self._runner.run(command)
        except ToolUnavailable as exc:
            raise ActionError(str(exc)) from exc


def default_executor() -> Executor:
    """Der voreingestellte Ausführende.

    Diese eine Stelle tauschen die Tests aus (``tests/conftest.py`` ersetzt
    ``ai_helper.actions.box.default_executor`` durch einen blinden Doppelgänger),
    damit kein Testlauf etwas am System ändert. Neue Naht nach außen, blinder
    Vorgabe-Doppelgänger im selben Schritt — die Regel aus Offener Punkt 30.
    """
    return SystemExecutor()
