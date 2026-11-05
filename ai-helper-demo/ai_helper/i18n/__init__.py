# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Sprachdateien und Textausgabe.

Alle Texte liegen in einer eigenen Datei je Sprache (Entscheidung 7 im
Design-Dokument). Ein neuer Text wird dort ergänzt, nie im Code verstreut.
"""

from __future__ import annotations

from ai_helper.i18n import de

_LANGUAGES: dict[str, dict[str, str]] = {"de": de.TEXTS}
DEFAULT_LANGUAGE = "de"

_current = DEFAULT_LANGUAGE


def available_languages() -> tuple[str, ...]:
    return tuple(sorted(_LANGUAGES))


def set_language(code: str) -> None:
    """Stellt die Sprache ein. Unbekannte Codes werden abgelehnt."""
    global _current
    if code not in _LANGUAGES:
        raise ValueError(
            f"Unbekannte Sprache {code!r}. Bekannt: {', '.join(available_languages())}"
        )
    _current = code


def current_language() -> str:
    return _current


def t(key: str, **values: object) -> str:
    """Holt den Text zu ``key`` und setzt Platzhalter ein."""
    texts = _LANGUAGES[_current]
    try:
        template = texts[key]
    except KeyError:
        raise KeyError(
            f"Text {key!r} fehlt in der Sprachdatei {_current!r}"
        ) from None
    return template.format(**values) if values else template
