# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Die Systemabfrage: der eine Ort, an dem wirklich gemessen wird.

Jedes Werkzeug holt seine Rohdaten über dieses Protokoll. Die Tests setzen
einen Doppelgänger ein und speisen bekannte Rohdaten ein, statt Interna zu
patchen.

Der echte Runner führt ausschließlich lesende Befehle aus: kein Netz, keine
Administratorenrechte, keine Änderung am System (Entscheidung 10). Schlägt ein
Befehl fehl, ist das kein Absturz, sondern ein ``ToolUnavailable`` mit fertiger
deutscher Meldung — das Werkzeug meldet dann "nicht messbar".
"""

from __future__ import annotations

import locale
import os
import subprocess
from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from ai_helper.core.errors import AIHelperError
from ai_helper.i18n import t

__all__ = ["Runner", "SystemRunner", "ToolUnavailable", "command_text"]

# Ein sichtbar aufblitzendes Konsolenfenster wäre auf einem Anfänger-Rechner
# beunruhigend; auf Windows wird es deshalb unterdrückt.
_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0) if os.name == "nt" else 0

DEFAULT_TIMEOUT_S = 15.0


class ToolUnavailable(AIHelperError):
    """Eine Messung war nicht möglich: Befehl fehlgeschlagen, Zeitablauf, kein Gerät."""


@runtime_checkable
class Runner(Protocol):
    """Führt eine Systemabfrage aus und liefert die rohe Ausgabe."""

    def run(self, command: Sequence[str]) -> str:
        """Führt ``command`` aus und liefert seine Ausgabe.

        Wirft ``ToolUnavailable``, wenn das nicht geht.
        """
        ...


def command_text(command: Sequence[str]) -> str:
    """Der Befehl als lesbare Zeile, für Meldungen und die Quellenangabe."""
    return " ".join(command)


def _encoding() -> str:
    """Die Kodierung, in der die Ausgabe eines Konsolenbefehls ankommt."""
    return locale.getpreferredencoding(False) or "utf-8"


class SystemRunner:
    """Der echte Runner: führt den Befehl aus und gibt seine Ausgabe zurück."""

    def __init__(self, timeout_s: float = DEFAULT_TIMEOUT_S) -> None:
        self._timeout_s = timeout_s

    def run(self, command: Sequence[str]) -> str:
        argv = list(command)
        try:
            completed = subprocess.run(
                argv,
                capture_output=True,
                timeout=self._timeout_s,
                check=False,
                creationflags=_NO_WINDOW,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise ToolUnavailable(
                t("tool_command_failed", command=command_text(argv), detail=exc)
            ) from exc

        if completed.returncode != 0:
            detail = completed.stderr.decode(_encoding(), errors="replace").strip()
            raise ToolUnavailable(
                t(
                    "tool_command_failed",
                    command=command_text(argv),
                    detail=detail or t("tool_exit_code", code=completed.returncode),
                )
            )
        return completed.stdout.decode(_encoding(), errors="replace")
