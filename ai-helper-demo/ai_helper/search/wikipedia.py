# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Nachschlagen in der deutschen Wikipedia (Wikimedia).

Warum dieser Dienst (Slice 9, Offener Punkt 5): er ist **kostenlos**, braucht
**keinen Schlüssel** und **kein Konto**, und es verlässt nur die Suchanfrage den
Rechner — kein Nutzerprofil, keine Werbe-Kennung. Damit funktioniert das
Nachschlagen auch auf Rechnern von Lernenden, die keinen eigenen API-Schlüssel
haben (Design Kapitel 5, „Vertrieb an Bildungseinrichtungen“).

Der Dienst verlangt eine beschreibende ``User-Agent``-Kopfzeile: am 2026-11-03
gemessen antwortet Wikimedia ohne diese Kopfzeile mit **HTTP 403**, mit ihr mit
**HTTP 200** (0,38 s). Genau solche Funde macht nur die Außenprobe — der
Doppelgänger im Testlauf hätte den 403 nie gezeigt.

Grenze: Wikipedia ist eine Enzyklopädie, kein Erklärbuch. Für Fragen der Art
„wie schalte ich X ein“ ist der Ertrag dünn; das ist im Bericht als Offener
Punkt notiert, nicht verschwiegen.
"""

from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request
from html import unescape

from ai_helper.core.errors import ProviderError
from ai_helper.i18n import t
from ai_helper.search.hit import MAX_RESULTS, SNIPPET_CHARS, SearchHit

__all__ = [
    "DEFAULT_SEARCH_URL",
    "REQUEST_TIMEOUT_S",
    "USER_AGENT",
    "WikipediaSearch",
    "build_search_url",
    "default_search_get",
    "page_url",
    "parse_search_response",
    "strip_markup",
]

DEFAULT_SEARCH_URL = "https://de.wikipedia.org/w/api.php"
REQUEST_TIMEOUT_S = 15.0

# Wikimedia weist Anfragen ohne beschreibenden User-Agent ab (am 2026-11-03
# gemessen: ohne Kopfzeile HTTP 403, mit Kopfzeile HTTP 200). Die Vorgabe von
# ``urllib`` genügt dafür nicht.
USER_AGENT = "ai-helper/0.1 (privater Terminal-Helfer; kein oeffentlicher Dienst)"

_TAG = re.compile(r"<[^>]+>")


def strip_markup(text: str) -> str:
    """Entfernt Auszeichnung aus einem Auszug: Wikipedia schickt HTML.

    Die Treffer-Auszüge der Schnittstelle enthalten ``<span class="searchmatch">``
    um die gesuchten Wörter. Für die Anzeige und für den Auftrag an das Modell
    wird daraus reiner Text.
    """

    return " ".join(unescape(_TAG.sub("", text)).split())


def build_search_url(
    query: str,
    *,
    limit: int = MAX_RESULTS,
    url: str = DEFAULT_SEARCH_URL,
) -> str:
    """Die fertige Adresse der Suchanfrage, mit Kodierung."""

    params = {
        "action": "query",
        "list": "search",
        "srsearch": query,
        "format": "json",
        "srlimit": limit,
        "utf8": 1,
    }
    return f"{url}?{urllib.parse.urlencode(params)}"


def page_url(title: str, *, base: str = "https://de.wikipedia.org") -> str:
    """Die Adresse der gefundenen Seite, aus dem Titel gebaut.

    Klammern bleiben stehen (``Lupe (Software)``), weil die Adresse im Gespräch
    und im Auftrag an das Modell gelesen wird; Umlaute und Leerzeichen werden
    kodiert, ein ``#`` ebenfalls — sonst würde daraus ein Sprungmarken-Anhang.
    """

    return f"{base}/wiki/{urllib.parse.quote(title.replace(' ', '_'), safe='()')}"


def parse_search_response(payload: bytes | str) -> tuple[SearchHit, ...]:
    """Wertet die Antwort aus. Ohne Quelle wird kein Treffer daraus.

    Eine Suche ohne Treffer ist kein Fehler, sondern eine leere Liste; eine
    unlesbare Antwort ist ein deutscher Fehler. Ein Eintrag ohne Titel wird
    weggelassen, weil daraus keine Adresse gebaut werden kann.
    """

    text = payload.decode("utf-8", errors="replace") if isinstance(payload, bytes) else payload
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise ProviderError(t("search_response_unreadable", detail=exc)) from exc
    if not isinstance(data, dict) or not isinstance(data.get("query"), dict):
        raise ProviderError(t("search_response_unreadable", detail=t("search_no_results_field")))

    hits: list[SearchHit] = []
    for entry in data["query"].get("search") or ():
        if not isinstance(entry, dict):
            continue
        title = str(entry.get("title") or "").strip()
        if not title:
            continue
        snippet = strip_markup(str(entry.get("snippet") or ""))[:SNIPPET_CHARS]
        hits.append(SearchHit(title=title, url=page_url(title), snippet=snippet))
    return tuple(hits)


def default_search_get(url: str, timeout: float = REQUEST_TIMEOUT_S) -> bytes:
    """Die eine Stelle, an der wirklich gesucht wird.

    Diese Austauschstelle ersetzen die Tests (``tests/conftest.py``) durch einen
    blinden Doppelgänger, damit kein Testlauf ins Netz greift. Ein Fehler wird zu
    einer fertigen deutschen Meldung, nie zu einem Absturz.
    """

    request = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        raise ProviderError(
            t("search_http_error", status=exc.code, detail=exc.reason or t("search_no_reason"))
        ) from exc
    except (urllib.error.URLError, OSError) as exc:
        raise ProviderError(t("search_failed", detail=getattr(exc, "reason", exc))) from exc


class WikipediaSearch:
    """Die deutsche Wikipedia über die MediaWiki-Schnittstelle."""

    def __init__(
        self,
        *,
        limit: int = MAX_RESULTS,
        url: str = DEFAULT_SEARCH_URL,
        timeout: float = REQUEST_TIMEOUT_S,
        get=None,
    ) -> None:
        self._limit = limit
        self._url = url
        self._timeout = timeout
        # Die Voreinstellung ist ein Aufruf, keine feste Bindung: nur so lässt
        # sich die Naht im Testlauf ersetzen (Lehre aus Slice 5).
        self._get = default_search_get if get is None else get

    @property
    def label(self) -> str:
        return t("search_provider_wikipedia")

    @property
    def url(self) -> str:
        """Die Adresse des Dienstes (für die Selbstprüfung und Meldungen)."""
        return self._url

    def search(self, query: str) -> tuple[SearchHit, ...]:
        """Sucht in der Wikipedia und liefert die Treffer mit Quelle."""

        frage = " ".join(query.split())
        if not frage:
            raise ProviderError(t("search_empty_query"))
        payload = self._get(build_search_url(frage, limit=self._limit, url=self._url), self._timeout)
        return parse_search_response(payload)
