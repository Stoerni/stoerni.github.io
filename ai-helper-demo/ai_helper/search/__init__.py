# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Nachschlagen: eine Suche als Werkzeug des Kerns (Slice 9).

Der Avatar kann recherchieren: ``/suchen <begriff>`` schickt die Frage an einen
Suchdienst, und das Ergebnis kommt **mit Quellenangabe** in die Antwort
(Design Kapitel 2, „erklärt und recherchiert“; Kapitel 3 verbietet nur das freie
Ausführen, nicht das Lesen).

Der Kern kennt nur die Naht (``SearchProvider``), nicht den Dienst dahinter.
Gemessen statt angenommen wurde die Wahl des Dienstes: siehe ``wikipedia.py``
und ``exa.py``. Das Ergebnis trägt immer Titel und Adresse — was keine Quelle
hat, wird nicht als eigene Aussage ausgegeben.
"""

from __future__ import annotations

from ai_helper.search.exa import DEFAULT_SEARCH_URL as EXA_SEARCH_URL
from ai_helper.search.exa import ExaSearch, build_search_request, default_search_post
from ai_helper.search.exa import parse_search_response as parse_exa_response
from ai_helper.search.hit import MAX_RESULTS, SNIPPET_CHARS, SearchHit
from ai_helper.search.provider import (
    SearchProvider,
    build_search_block,
    build_search_section,
)
from ai_helper.search.wikipedia import (
    DEFAULT_SEARCH_URL as WIKIPEDIA_SEARCH_URL,
)
from ai_helper.search.wikipedia import (
    WikipediaSearch,
    build_search_url,
    default_search_get,
    page_url,
    strip_markup,
)
from ai_helper.search.wikipedia import parse_search_response as parse_wikipedia_response

__all__ = [
    "EXA_SEARCH_URL",
    "MAX_RESULTS",
    "SNIPPET_CHARS",
    "WIKIPEDIA_SEARCH_URL",
    "ExaSearch",
    "SearchHit",
    "SearchProvider",
    "WikipediaSearch",
    "build_search_block",
    "build_search_request",
    "build_search_section",
    "build_search_url",
    "default_search_get",
    "default_search_post",
    "page_url",
    "parse_exa_response",
    "parse_wikipedia_response",
    "strip_markup",
]
