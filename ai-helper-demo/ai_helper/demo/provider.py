# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Der Demo-Anbieter: antwortet aus dem Drehbuch statt aus einem Modell.

Er sitzt an **derselben Naht** wie jeder echte Anbieter
(``ai_helper/core/provider.py``): er hat ``label``, ``complete`` und ``stream``.
Die Hülle merkt keinen Unterschied — sie spricht ihn genau so an wie einen
Ollama- oder Online-Anbieter. Deshalb braucht der Kern für die Demo **keine**
Änderung.

Eigenschaften, die die Demo versprochen hat:

* **Kein Netz, kein Schlüssel.** Es gibt keine Leitung, keine Adresse, keinen
  ``Authorization``-Kopf — nur einen Wörterbuchvergleich mit dem Drehbuch.
* **Keine erfundenen Antworten.** Alles Unvorbereitete bekommt die
  Höflichkeitsantwort (``script.answer_for``).
* **Teilstücke wie ein echter Anbieter.** ``stream`` liefert die Antwort in
  Wörtern, damit die Figur mit dem ersten Wort auf „spricht" geht — die Demo
  sieht genauso lebendig aus wie der echte Betrieb, ohne einen einzigen
  Netzaufruf.
"""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from ai_helper.core.message import Message, Role
from ai_helper.demo.script import answer_for
from ai_helper.i18n import t

__all__ = ["DemoProvider"]

# Der Name, unter dem der Demo-Anbieter in jeder Antwortzeile steht.
DEMO_MODEL_LABEL_KEY = "demo_model_label"


class DemoProvider:
    """Ein Anbieter mit festen Antworten aus dem Drehbuch."""

    def __init__(self, antwort_fuer=answer_for, label_key: str = DEMO_MODEL_LABEL_KEY) -> None:
        # ``antwort_fuer`` ist eine Austauschstelle (wie die Transporte der
        # echten Anbieter): ein Test kann eine eigene Funktion einspeisen, ohne
        # das Drehbuch zu ändern.
        self._antwort_fuer = antwort_fuer
        self._label_key = label_key

    @property
    def label(self) -> str:
        """Kurzer Name für die Anzeige („welches Modell antwortet")."""
        return t(self._label_key)

    def complete(self, messages: Sequence[Message]) -> str:
        """Die fertige Antwort auf die letzte Frage im Verlauf."""
        return self._antwort_fuer(self._frage(messages))

    def stream(self, messages: Sequence[Message]) -> Iterator[str]:
        """Dieselbe Antwort, Wort für Wort — wie ein streamender Anbieter.

        Zusammengesetzt ergibt die Teilstückfolge **genau** den Text von
        ``complete``: die letzte Lücke steckt nicht am Ende, damit die Hülle
        keine überzähligen Leerzeichen in den Verlauf schreibt.
        """
        antwort = self._antwort_fuer(self._frage(messages))
        teile = antwort.split(" ")
        letzter = len(teile) - 1
        for index, wort in enumerate(teile):
            yield wort if index == letzter else f"{wort} "

    @staticmethod
    def _frage(messages: Sequence[Message]) -> str:
        """Die letzte Frage (die Rolle ``user``) aus dem Verlauf, sonst leer."""
        for message in reversed(messages):
            if message.role == Role.USER:
                return message.content
        return ""
