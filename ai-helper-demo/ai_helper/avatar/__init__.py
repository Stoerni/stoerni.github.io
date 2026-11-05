# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Die Figur: Textgrafik mit fünf Zuständen, ohne Animation.

Dieses Paket kennt weder Terminal noch Anbieter und wird vom Kern nicht
benutzt. Es liefert nur das Bild; wann welcher Zustand gezeigt wird, entscheidet
die Hülle (``ui/terminal.py``), und die Beschriftung kommt aus der Sprachdatei.
"""

from __future__ import annotations

from ai_helper.avatar.faces import FACES, FRAME_TOP
from ai_helper.avatar.states import AvatarState

__all__ = ["FACES", "FRAME_TOP", "AvatarState", "render"]


def render(state: AvatarState) -> str:
    """Gibt das Gesicht zu ``state`` als mehrzeiligen Text zurück.

    Reine Funktion: gleicher Zustand, gleicher Text, keine Ausgabe, kein
    Terminal. Unbekannte Zustände sind durch das Enum ausgeschlossen.
    """
    return "\n".join(FACES[state])
