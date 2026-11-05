# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Die Gesichter als Textgrafik.

Reine Zeichen, keine Sprache: Beschriftungen stehen in der Sprachdatei
(Entscheidung 7), hier steht nur das Bild. Alle Gesichter sind gleich breit und
gleich hoch, damit ein Figurenblock im Terminal nicht springt.

``FRAME_TOP`` ist die oberste Zeile jedes Gesichts. Tests zählen damit die
Figurenblöcke in der Ausgabe, ohne die Zeichenkunst nachzubauen.
"""

from __future__ import annotations

from ai_helper.avatar.states import AvatarState

__all__ = ["FACES", "FRAME_TOP"]

FRAME_TOP = "  .----."
_FRAME_BOTTOM = "  '----'"

FACES: dict[AvatarState, tuple[str, ...]] = {
    # Ruhig, Augen offen, gerader Mund.
    AvatarState.NEUTRAL: (
        FRAME_TOP,
        "  | oo |",
        "  | -- |",
        _FRAME_BOTTOM,
    ),
    # Augen zugekniffen, kleiner Mund: angestrengt.
    AvatarState.THINKING: (
        FRAME_TOP,
        "  | ^^ |",
        "  | .. |",
        _FRAME_BOTTOM,
    ),
    # Augen offen, Mund auf: er redet.
    AvatarState.SPEAKING: (
        FRAME_TOP,
        "  | oo |",
        "  | () |",
        _FRAME_BOTTOM,
    ),
    # Augen offen, gerader Mund: er erklärt etwas in Schritten, ohne es zu tun.
    AvatarState.EXPLAINING: (
        FRAME_TOP,
        "  | oo |",
        "  | == |",
        _FRAME_BOTTOM,
    ),
    # Augen zugekniffen, Mund breit: freut sich.
    AvatarState.HAPPY: (
        FRAME_TOP,
        "  | ^^ |",
        "  | \\/ |",
        _FRAME_BOTTOM,
    ),
    # Augen zu, Mund schief: etwas ist schiefgegangen.
    AvatarState.ERROR: (
        FRAME_TOP,
        "  | xx |",
        "  | ~~ |",
        _FRAME_BOTTOM,
    ),
}
