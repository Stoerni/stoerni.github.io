# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Eine echte Websuche über Exa (Schlüssel nötig, Voreinstellung nicht).

Der zweite Suchdienst derselben Naht: er sucht das offene Netz, nicht eine
Enzyklopädie, und ist damit der bessere Dienst für Fragen der Art „wie mache ich
X“. Er braucht dafür ein Konto und einen Schlüssel.

Warum Exa und nicht Brave oder Tavily (Slice 9, Offener Punkt 5, Stand
2026-11-03):
* **Brave** hat seine kostenlose Stufe im Februar 2026 abgeschafft; es gibt nur
  noch ein monatliches Guthaben, für das eine **Bankkarte** hinterlegt werden
  muss.
* **Tavily** hat 1.000 Suchanfragen im Monat gratis, gibt Anfragen aber laut
  eigener Datenschutzerklärung in bestimmten Fällen **an fremde Such-Indizes
  (etwa Google) weiter** — das ist das Gegenteil von datensparsam.
* **Exa** gibt monatlich 10 Dollar Guthaben (rund 2.500 Suchen), **ohne
  Zahlungsmittel**, und arbeitet mit eigenem Index.

**Nicht belegt:** auf diesem Rechner liegt kein Schlüssel, deshalb ist dieser
Weg nur mit Doppelgängern geprüft (Anfrageaufbau, Auswertung, Fehlerfälle). Die
Form stammt aus der offiziellen Schnittstellen-Beschreibung
(``https://docs.exa.ai/reference/search``, am 2026-11-03 gelesen): POST
``https://api.exa.ai/search`` mit der Kopfzeile ``x-api-key`` und dem Rumpf
``{"query": …, "numResults": …, "type": "auto", "contents": {"text": {"maxCharacters": …}}}``;
in der Antwort stehen ``results[]`` mit ``title``, ``url`` und ``text``.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from ai_helper.core.errors import ConfigurationError, ProviderError
from ai_helper.i18n import t
from ai_helper.search.hit import MAX_RESULTS, SNIPPET_CHARS, SearchHit
from ai_helper.search.wikipedia import REQUEST_TIMEOUT_S, USER_AGENT, strip_markup

__all__ = [
    "DEFAULT_SEARCH_URL",
    "ExaSearch",
    "build_search_request",
    "default_search_post",
    "parse_search_response",
]

DEFAULT_SEARCH_URL = "https://api.exa.ai/search"


def build_search_request(
    query: str,
    *,
    api_key: str,
    limit: int = MAX_RESULTS,
    url: str = DEFAULT_SEARCH_URL,
) -> tuple[str, bytes, dict[str, str]]:
    """Adresse, Rumpf und Kopfzeilen der Suchanfrage.

    Der Schlüssel steht in der Kopfzeile ``x-api-key`` (so schreibt es die
    Schnittstelle vor) und nie in der Adresse: eine Adresse landet in
    Fehlermeldungen und Protokollen, eine Kopfzeile nicht.
    """

    body = {
        "query": query,
        "numResults": limit,
        "type": "auto",
        "contents": {"text": {"maxCharacters": SNIPPET_CHARS}},
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
        "x-api-key": api_key,
    }
    return url, json.dumps(body, ensure_ascii=False).encode("utf-8"), headers


def parse_search_response(payload: bytes | str) -> tuple[SearchHit, ...]:
    """Wertet die Antwort aus. Ein Ergebnis ohne Adresse wird weggelassen."""

    text = payload.decode("utf-8", errors="replace") if isinstance(payload, bytes) else payload
    try:
        data = json.loads(text)
    except ValueError as exc:
        raise ProviderError(t("search_response_unreadable", detail=exc)) from exc
    if not isinstance(data, dict) or not isinstance(data.get("results"), list):
        raise ProviderError(t("search_response_unreadable", detail=t("search_no_results_field")))

    hits: list[SearchHit] = []
    for entry in data["results"]:
        if not isinstance(entry, dict):
            continue
        title = str(entry.get("title") or "").strip()
        url = str(entry.get("url") or "").strip()
        if not title or not url:
            # Ein Text ohne Quelle ist keine Quelle (Auftrag dieser Slice).
            continue
        snippet = strip_markup(str(entry.get("text") or ""))[:SNIPPET_CHARS]
        hits.append(SearchHit(title=title, url=url, snippet=snippet))
    return tuple(hits)


def default_search_post(
    url: str,
    body: bytes,
    headers: dict[str, str],
    timeout: float = REQUEST_TIMEOUT_S,
) -> bytes:
    """Die Austauschstelle dieses Dienstes: hier ginge die Anfrage wirklich raus."""

    request = urllib.request.Request(url, data=body, headers=dict(headers), method="POST")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        raise ProviderError(
            t("search_http_error", status=exc.code, detail=exc.reason or t("search_no_reason"))
        ) from exc
    except (urllib.error.URLError, OSError) as exc:
        raise ProviderError(t("search_failed", detail=getattr(exc, "reason", exc))) from exc


class ExaSearch:
    """Die Websuche über Exa. Ohne Schlüssel passiert hier nichts."""

    def __init__(
        self,
        api_key: str | None,
        *,
        limit: int = MAX_RESULTS,
        url: str = DEFAULT_SEARCH_URL,
        timeout: float = REQUEST_TIMEOUT_S,
        post=None,
    ) -> None:
        self._api_key = api_key or ""
        self._limit = limit
        self._url = url
        self._timeout = timeout
        self._post = default_search_post if post is None else post

    @property
    def label(self) -> str:
        return t("search_provider_exa")

    @property
    def url(self) -> str:
        return self._url

    def search(self, query: str) -> tuple[SearchHit, ...]:
        """Sucht im Netz. Ohne Schlüssel geht die Anfrage gar nicht erst raus."""

        if not self._api_key:
            raise ConfigurationError(t("search_key_missing"))
        frage = " ".join(query.split())
        if not frage:
            raise ProviderError(t("search_empty_query"))
        url, body, headers = build_search_request(
            frage, api_key=self._api_key, limit=self._limit, url=self._url
        )
        return parse_search_response(self._post(url, body, headers, self._timeout))
