# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Die fünf Zustände der Figur (Design-Entscheidung 4).

Die Werte sind gleichzeitig die Endung des Textschlüssels in der Sprachdatei
(``avatar_<wert>``). Ein neuer Zustand braucht deshalb immer beides: einen
Eintrag hier und eine Beschriftung in ``i18n/de.py``.
"""

from __future__ import annotations

from enum import Enum

__all__ = ["AvatarState"]


class AvatarState(str, Enum):
    """Was die Figur gerade tut. Mehr Zustände gibt es in der Alpha nicht."""

    NEUTRAL = "neutral"
    THINKING = "thinking"
    SPEAKING = "speaking"
    # Slice 8: im Lernmodus erklärt die Figur, statt etwas zu tun (Offener
    # Punkt 11 — die Figur hatte bisher keinen Zustand fürs Erklären).
    EXPLAINING = "explaining"
    HAPPY = "happy"
    ERROR = "error"
