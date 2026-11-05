# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Terminal-Hülle: Figur, Tastatur, Bildschirm, /exit.

Diese Datei ist nur noch der **Antrieb** der Gesprächsschleife: sie liest die
Zeilen aus der Tastatur, schreibt auf den Bildschirm und reicht beides in
``ai_helper/ui/shell.py`` hinein. Die Schleife selbst (Begrüßung, Systemtext,
Figur, Befehle, Antwortweg) steht dort, weil die Browser-Hülle
(``ai_helper/ui/web.py``) dieselbe Schleife benutzt — ein Browser kann nicht
blockieren, deshalb ist sie ein Erzeuger, den jede Hülle auf ihre Art treibt.

Die Hülle setzt die Zustände der Figur: Begrüßung neutral, während der Anfrage
"denkt", nach der Antwort "spricht", bei einem Anbieterfehler "Fehler",
Verabschiedung freudig. Die Figur selbst kennt weder Terminal noch Anbieter
(``ai_helper/avatar/``), und die Schleife enthält keine Modell- und keine
Anbieterlogik.

Der Systemtext wird aus Charakter (``ai_helper/persona/``), Gedächtnis
(``ai_helper/memory/``) und dem Werkzeugabschnitt mit den wirklich gemessenen
Werten (``ai_helper/tools/``) zusammengesetzt. Der Kern kennt weder Persona noch
Dateien noch Befehle, er bekommt nur den fertigen Text.

Der Avatar redet nicht über den Rechner, er schaut nach: beim Start und bei
``/nachschauen`` werden die Werkzeuge befragt, und die gemessenen Werte stehen
im Systemtext jeder Anfrage (Entscheidung 9). Ein Werkzeug, das scheitert,
meldet "nicht messbar" und beendet nichts.

Die Antwort erscheint, während sie entsteht (Slice 5b): jedes Teilstück wird
sofort ausgegeben und die Figur wechselt mit dem ersten Stück auf "spricht".
Der Verlauf bekommt am Ende **eine** vollständige Antwort, nicht die einzelnen
Stücke. Bricht die Leitung mitten in der Antwort ab, kommt eine deutsche
Meldung, das Gespräch läuft weiter, und es landet keine halbe Antwort im
Verlauf.

Die Figur soll das Gespräch nicht zumüllen: höchstens ein Figurenblock je
Zustandswechsel. Es gibt keine Steuerzeichen zum Überschreiben von Zeilen,
damit die Ausgabe auch in eine Datei umgeleitet lesbar bleibt.

Ein Strg-C beendet das Gespräch an jeder Stelle ruhig (Slice 10): beim
Nachschauen, während einer Anfrage, bei der Bestätigungsfrage einer Aktion und
während ``/suchen``. Es gibt dann keinen Traceback, keine halbe Ausgabezeile und
den Exit-Code 0. Nur das Ende der Eingabe (Strg-D) bei einer Rückfrage heißt
weiterhin „nein" und lässt das Gespräch laufen.
"""

from __future__ import annotations

import sys
from collections.abc import Callable
from pathlib import Path
from typing import TextIO

from ai_helper.actions import ActionBox
from ai_helper.core.memory import Memory
from ai_helper.core.provider import Provider
from ai_helper.core.session import Session
from ai_helper.persona import DEFAULT_PERSONA, Persona
from ai_helper.search import SearchProvider
from ai_helper.tools import Toolbox
from ai_helper.ui import shell
from ai_helper.ui.shell import (
    ABBRUCH,
    ACTION_COMMANDS,
    CONFIRM_WORDS,
    ENDE,
    EXIT_COMMANDS,
    LEARN_COMMANDS,
    MEMORY_COMMANDS,
    NACHSEHEN_COMMANDS,
    SEARCH_COMMANDS,
)

__all__ = [
    "ACTION_COMMANDS",
    "CONFIRM_WORDS",
    "EXIT_COMMANDS",
    "LEARN_COMMANDS",
    "MEMORY_COMMANDS",
    "NACHSEHEN_COMMANDS",
    "SEARCH_COMMANDS",
    "run",
]


def _default_input(prompt: str) -> str:
    return input(prompt)


def run(
    *,
    provider: Provider,
    session: Session,
    base_url: str,
    mode_key: str = "online",
    persona: Persona = DEFAULT_PERSONA,
    memory: Memory | None = None,
    memory_path: Path | None = None,
    toolbox: Toolbox | None = None,
    action_box: ActionBox | None = None,
    learn_mode: bool = False,
    search: SearchProvider | None = None,
    input_fn: Callable[[str], str] | None = None,
    out: TextIO | None = None,
) -> int:
    """Führt das Gespräch im Terminal. Rückgabe: Exit-Code.

    ``mode_key`` ist die Betriebsart (``online``, ``lokal`` oder ``demo``); sie
    steht in der Begrüßung und in jeder Antwortzeile, damit erkennbar ist,
    welches Modell geantwortet hat (Entscheidung 8).

    ``learn_mode`` ist der Anfangswert des Lernmodus (Slice 8): ``True`` heißt
    erklären statt ausführen. Umgeschaltet wird im Gespräch mit ``/lernen``.

    ``search`` ist der Suchdienst für ``/suchen`` (Slice 9). Ist er ``None``
    (Suche abgeschaltet oder nicht eingerichtet), meldet das die Hülle und
    schickt nichts raus.

    ``input_fn`` und ``out`` sind die beiden Nahtstellen, die schon vor dieser
    Slice hereingegeben werden konnten; im Testlauf sind sie geskriptet. Die
    Schleife selbst steht in ``ai_helper/ui/shell.py``.
    """
    read_line = _default_input if input_fn is None else input_fn
    stream = sys.stdout if out is None else out

    def show(text: str = "") -> None:
        print(text, file=stream, flush=True)

    def write(text: str) -> None:
        """Gibt Text ohne Zeilenumbruch aus und spült sofort (Teilstücke)."""
        print(text, end="", file=stream, flush=True)

    schleife = shell.conversation(
        provider=provider,
        session=session,
        base_url=base_url,
        mode_key=mode_key,
        persona=persona,
        memory=memory,
        memory_path=memory_path,
        toolbox=toolbox,
        action_box=action_box,
        learn_mode=learn_mode,
        search=search,
        show=show,
        write=write,
    )

    try:
        frage = next(schleife)
        while True:
            try:
                antwort: object = read_line(frage.prompt)
            except EOFError:
                antwort = ENDE
            except KeyboardInterrupt:
                antwort = ABBRUCH
            frage = schleife.send(antwort)
    except StopIteration as ende:
        # Das Gespräch hat sich mit seinem Exit-Code beendet.
        return 0 if ende.value is None else int(ende.value)
