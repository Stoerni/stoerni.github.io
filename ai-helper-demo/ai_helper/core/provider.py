# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Die Anbieter-Schnittstelle.

Jeder Anbieter (Online über HTTP, später Ollama oder llama.cpp) erfüllt
dieses Protokoll. Der Kern und die Hüllen kennen nur dieses Protokoll,
nie einen bestimmten Dienst.

Zwei Protokolle, absichtlich getrennt:

* ``Provider`` ist die Pflicht: ``label`` und ``complete``. Wer nur das
  erfüllt, wird weiterhin unterstützt.
* ``StreamingProvider`` ist die Kür: ``stream`` liefert die Antwort in
  Teilstücken. Die Hülle benutzt sie, wenn vorhanden, und fällt sonst
  sichtbar auf ``complete`` zurück (Slice 5b).
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Protocol, runtime_checkable

from ai_helper.core.message import Message

__all__ = ["Provider", "StreamingProvider"]


@runtime_checkable
class Provider(Protocol):
    """Ein Modell, das auf einen Nachrichtenverlauf antwortet."""

    @property
    def label(self) -> str:
        """Kurzer Name für die Anzeige, welches Modell gerade antwortet."""
        ...

    def complete(self, messages: Sequence[Message]) -> str:
        """Holt die Antwort auf den übergebenen Verlauf.

        Der Verlauf bleibt unverändert; die Sitzung kümmert sich darum,
        die Antwort anzuhängen.
        """
        ...


@runtime_checkable
class StreamingProvider(Protocol):
    """Ein Anbieter, der die Antwort schon während des Entstehens liefert.

    ``stream`` gibt die Teilstücke in der Reihenfolge aus, in der sie
    eintreffen. Der Verlauf bleibt unverändert. Fehler unterwegs sind
    ``AIHelperError``: bricht die Leitung mitten in der Antwort ab, kommt eine
    deutsche Meldung statt einer halben Antwort (der Aufrufer hängt dann
    nichts an den Verlauf an).
    """

    def stream(self, messages: Sequence[Message]) -> Iterator[str]:
        """Liefert die Teilstücke der Antwort."""
        ...
