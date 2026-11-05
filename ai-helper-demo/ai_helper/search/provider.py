# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Die Naht der Suche und die zwei Textabschnitte dazu.

Der Kern kennt nur diese Schnittstelle, nicht den Dienst dahinter
(``wikipedia.py``, ``exa.py``): dieselbe Bauweise wie bei den Anbietern der
Antwort (Slice 5) und beim Werkzeugkasten (Slice 4). Die Hülle hält nur ein
``SearchProvider`` in der Hand.

Zwei Abschnitte gehören hierher, weil sie aus dem Kern kommen und in jeder
Hülle dieselben sind:

* ``build_search_section`` — der Abschnitt im Systemtext: was das Modell über
  die Recherche wissen muss (und dass es die Quelle nennen muss),
* ``build_search_block`` — die gefundenen Quellen als Beleg für den Auftrag an
  das Modell.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from ai_helper.i18n import t
from ai_helper.search.hit import SearchHit

__all__ = ["SearchProvider", "build_search_block", "build_search_section"]


@runtime_checkable
class SearchProvider(Protocol):
    """Ein Suchdienst: er hat einen Namen und beantwortet eine Suchanfrage."""

    @property
    def label(self) -> str:
        """Wie der Dienst im Gespräch genannt wird."""
        ...

    def search(self, query: str) -> tuple[SearchHit, ...]:
        """Sucht ``query`` und liefert die Treffer samt Quelle.

        Wirft ``AIHelperError`` mit fertiger deutscher Meldung, wenn das nicht
        geht; ein fehlgeschlagener Suchdienst beendet nie das Gespräch.
        """
        ...


def build_search_section(provider_label: str) -> str:
    """Der Abschnitt im Systemtext: nachschlagen ja, Quelle nennen ja."""

    return t("search_section", provider=provider_label)


def build_search_block(hits: Sequence[SearchHit]) -> str:
    """Die gefundenen Quellen als Zeilen — Titel, Adresse und Auszug.

    Nur vollständige Treffer kommen hinein: ein Auszug ohne Quelle wäre eine
    Behauptung, die das Modell nicht belegen kann.
    """

    return "\n".join(
        t("search_hit_line", title=hit.title, url=hit.url, snippet=hit.snippet)
        for hit in hits
        if hit.complete
    )
