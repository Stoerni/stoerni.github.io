# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Die Gedächtnis-Schnittstelle.

Der Kern merkt sich verdichtete Tatsachen, nicht den Volltext des Verlaufs.
Wie sie aufbewahrt werden (Datei im Benutzerordner, später Datenbank), weiß
der Kern nicht: er kennt nur dieses Protokoll. Die Umsetzung mit Dateizugriff
steht in ``ai_helper/memory/``.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

__all__ = ["Memory"]


@runtime_checkable
class Memory(Protocol):
    """Ein Gedächtnis, das kurze Tatsachen über Sitzungen hinweg behält."""

    def facts(self) -> tuple[str, ...]:
        """Die gemerkten Tatsachen, älteste zuerst."""
        ...

    def remember(self, fact: str) -> bool:
        """Merkt eine verdichtete Tatsache.

        Rückgabe: ``True``, wenn die Tatsache neu war. Eine bereits bekannte
        oder leere Tatsache ändert nichts.
        """
        ...

    def forget_all(self) -> int:
        """Löscht alle gemerkten Tatsachen. Rückgabe: Anzahl der gelöschten."""
        ...
