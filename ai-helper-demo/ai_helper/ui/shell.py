# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Die Gesprächsschleife ohne Konsole: Eingabe und Ausgabe kommen von außen.

Hier steht alles, was Terminal- und Browser-Hülle **gemeinsam** haben: die
Begrüßung, der Systemtext aus Charakter, Gedächtnis, Messwerten und Aktionen,
die Figur, die Befehle (``/nachschauen``, ``/merken``, ``/aktion`` …) und der
Weg zur Antwort des Anbieters samt Streaming. Diese Datei kennt **keine**
Konsole: sie schreibt über ``show``/``write`` und fordert Eingaben über einen
**Erzeuger** an (``conversation``).

Der Erzeuger ist der Grund für diese Form: ein Browser kann nicht blockieren —
es gibt kein ``input()``, das warten könnte. Im Terminal liest die Hülle
(``ai_helper/ui/terminal.py``) die Zeilen aus der Tastatur und reicht sie in den
Erzeuger hinein; im Browser (``ai_helper/ui/web.py``) treibt die Seite denselben
Erzeuger Zeile für Zeile aus ihrem Eingabefeld. Beide benutzen dieselbe
Schleife, dieselben deutschen Texte und dieselbe Reihenfolge — genau das nagen
die Tests fest.

``conversation`` gibt bei jedem Eingabewunsch eine ``Frage`` aus (der Text der
Aufforderung) und bekommt dafür eine Zeile zurück. Zwei Sonderfälle statt einer
Zeile: ``ENDE`` heißt „die Eingabe ist zu Ende" (Strg-D, leere Warteschlange),
``ABBRUCH`` heißt „hier ist abgebrochen worden" (Strg-C, Escape, Knopf). Was
die beiden an einer Stelle bedeuten, entscheidet die Stelle selbst: am
Haupteingabezeichen heißt beides „verabschieden", bei einer Bestätigungsfrage
heißt ``ENDE`` „nein" und ``ABBRUCH`` „ruhig beenden".

Die Figur wechselt wie bisher: Begrüßung neutral, während der Anfrage „denkt",
nach der Antwort „spricht", bei einem Anbieterfehler „Fehler", Verabschiedung
freudig, im Lernmodus „explaining". Sie kennt weder Terminal noch Browser.

Aktionen (Slice 6): ``/aktionen`` listet den Katalog, ``/aktion <schlüssel>``
zeigt vorher in Klartext, was passieren wird, und führt erst nach einer
Bestätigung aus — ohne Bestätigung passiert nichts. ``/rueckgaengig`` nimmt die
letzte Aktion zurück, ``/protokoll`` zeigt, was ausgeführt wurde. Diese Datei
kennt nur ``ActionBox``; welche Befehle dahinterstehen, weiß der Kern
(``ai_helper/actions/``).
"""

from __future__ import annotations

from collections.abc import Callable, Generator, Sequence
from dataclasses import dataclass
from pathlib import Path

from ai_helper.actions import (
    ActionBox,
    build_actions_section,
    build_learn_section,
    grouped_actions,
)
from ai_helper.avatar import AvatarState, render
from ai_helper.config.settings import LEARN_OFF_VALUES, LEARN_ON_VALUES, MODE_LOCAL
from ai_helper.core.errors import AIHelperError, ProviderError
from ai_helper.core.memory import Memory
from ai_helper.core.message import Message
from ai_helper.core.provider import Provider, StreamingProvider
from ai_helper.core.session import Session
from ai_helper.i18n import t
from ai_helper.persona import DEFAULT_PERSONA, Persona, build_system_prompt
from ai_helper.search import (
    SearchHit,
    SearchProvider,
    build_search_block,
    build_search_section,
)
from ai_helper.tools import Measurement, Toolbox, build_state_section
from ai_helper.tools.measurement import describe

__all__ = [
    "ABBRUCH",
    "ACTION_COMMANDS",
    "CONFIRM_WORDS",
    "ENDE",
    "EXIT_COMMANDS",
    "Frage",
    "LEARN_COMMANDS",
    "MEMORY_COMMANDS",
    "NACHSEHEN_COMMANDS",
    "QuietExit",
    "SEARCH_COMMANDS",
    "conversation",
]

EXIT_COMMANDS = ("/exit", "/quit", "/ende")
MEMORY_COMMANDS = ("/merken", "/gedaechtnis", "/vergessen")
NACHSEHEN_COMMANDS = ("/nachschauen",)
ACTION_COMMANDS = ("/aktionen", "/aktion", "/rueckgaengig", "/protokoll")
# Der Lernmodus (Slice 8): /lernen schaltet an, /lernen aus zurück.
LEARN_COMMANDS = ("/lernen",)
# Die Recherche (Slice 9): /suchen <begriff> schlägt nach und nennt die Quelle.
SEARCH_COMMANDS = ("/suchen",)

# Was als Bestätigung gilt. Alles andere — auch eine leere Zeile, ein Abbruch
# oder eine Antwort wie "vielleicht" — heißt: nicht ausführen.
CONFIRM_WORDS = ("ja", "j", "jawohl", "yes", "y", "ok", "okay")


class _Sonderfall:
    """Ein Sonderfall der Eingabe — kein Text, sondern ein Ereignis.

    Zwei gibt es: ``ENDE`` (die Eingabe ist zu Ende) und ``ABBRUCH`` (es ist
    abgebrochen worden). Beide werden als **dieselbe** Art Objekt durch den
    Erzeuger gereicht, damit der Treiber sie kennt; was sie bedeuten, entscheidet
    die Stelle, die gerade gelesen hat.
    """

    __slots__ = ("_name",)

    def __init__(self, name: str) -> None:
        self._name = name

    def __repr__(self) -> str:
        return self._name


#: Die Eingabe ist zu Ende (Strg-D bzw. leere Warteschlange).
ENDE = _Sonderfall("ENDE")
#: Es ist abgebrochen worden (Strg-C, Escape bzw. ein Knopf).
ABBRUCH = _Sonderfall("ABBRUCH")


class QuietExit(Exception):
    """Ein Abbruch mitten in einer Hilfsfunktion: das Gespräch ruhig beenden.

    Nicht zu verwechseln mit dem Ende der Eingabe (``ENDE``): das heißt bei
    einer Rückfrage „nein" und lässt das Gespräch weiterlaufen.
    """


@dataclass(frozen=True, slots=True)
class Frage:
    """Ein Eingabewunsch: der Text, mit dem um die Eingabe gebeten wird.

    Der Text ist derselbe wie bisher: die Hülle übergibt ihn ihrer Eingabe
    (``input(prompt)`` in der Tastatur, das Eingabefeld im Browser), damit die
    Aufforderung dort steht, wo bisher auch.
    """

    prompt: str


class _Figure:
    """Zeigt die Figur höchstens einmal je Zustandswechsel.

    Der zuletzt gezeigte Zustand bleibt stehen: ändert er sich nicht, kommt
    kein zweiter Block. ``last_state`` ist nur zum Prüfen da.
    """

    def __init__(self, show: Callable[[str], None]) -> None:
        self._show = show
        self.last_state: AvatarState | None = None

    def switch(self, state: AvatarState) -> None:
        """Wechselt den Zustand und gibt den Block nur beim echten Wechsel aus."""
        if state is self.last_state:
            return
        self.last_state = state
        self._show(t(f"avatar_{state.value}"))
        self._show(render(state))


def _show_measurements(measurements: Sequence[Measurement], show: Callable[[str], None]) -> None:
    """Zeigt die gemessenen Werte im Klartext, jeden mit seiner Quelle."""
    if not measurements:
        show(t("measure_empty"))
        return
    show(t("measure_header", count=len(measurements)))
    for line in describe(measurements):
        show(line)


def _show_sources(hits: Sequence[SearchHit], show: Callable[[str], None]) -> None:
    """Zeigt die gefundenen Quellen im Klartext: Titel, Adresse und Auszug.

    Die Quelle steht **immer** in der Ausgabe, nicht nur in der Antwort des
    Modells: ein Beleg, den das Modell hätte weglassen können, wäre keiner
    (Entscheidung 9).
    """
    show(t("search_sources_header", count=len(hits)))
    for number, hit in enumerate(hits, start=1):
        show(t("search_source_line", number=number, title=hit.title, url=hit.url))
        if hit.snippet:
            show(t("search_source_snippet", snippet=hit.snippet))


def _show_memory(memory: Memory, memory_path: Path | None, show: Callable[[str], None]) -> None:
    """Zeigt die gemerkten Tatsachen im Klartext, genauso wie sie gespeichert sind."""
    facts = memory.facts()
    if facts:
        show(t("memory_header", count=len(facts)))
        for fact in facts:
            show(t("memory_line", fact=fact))
    else:
        show(t("memory_empty"))
    if memory_path is not None:
        show(t("memory_location", path=memory_path))


def _memory_command(
    line: str,
    *,
    memory: Memory | None,
    memory_path: Path | None,
    show: Callable[[str], None],
    refresh: Callable[[], None],
) -> bool:
    """Behandelt /merken, /gedaechtnis und /vergessen.

    Rückgabe: ``True``, wenn die Zeile ein Gedächtnisbefehl war. Ein Fehler des
    Speichers wird als deutsche Meldung ausgegeben, nicht geworfen.
    """
    command = line.partition(" ")[0].lower()
    if command not in MEMORY_COMMANDS:
        return False

    if memory is None:
        # Ohne Gedächtnis wird nichts vorgetäuscht: lieber eine klare Meldung.
        show(t("memory_unavailable"))
        return True

    try:
        if command == "/merken":
            fact = " ".join(line.partition(" ")[2].split())
            if not fact:
                show(t("memory_usage"))
            elif memory.remember(fact):
                refresh()
                show(t("memory_saved", fact=fact))
            else:
                show(t("memory_known", fact=fact))
        elif command == "/gedaechtnis":
            _show_memory(memory, memory_path, show)
        else:  # /vergessen
            count = memory.forget_all()
            refresh()
            show(t("memory_cleared", count=count))
    except AIHelperError as exc:
        show(str(exc))
    return True


def _show_actions(box: ActionBox, show: Callable[[str], None]) -> None:
    """Listet den Katalog nach Themen: was es gibt, nicht was passieren würde.

    Seit Slice 7 stehen die Einträge in Gruppen — bei zwölf Aktionen wäre eine
    flache Liste unübersichtlich. Die Gruppe wird einmal genannt, dann ihre
    Einträge.
    """
    show(t("action_list_header", count=len(box.actions)))
    for gruppe in grouped_actions(box.actions):
        show(t("action_list_group", title=gruppe[0].group_title))
        for action in gruppe:
            show(
                t(
                    "action_list_line",
                    schluessel=action.key,
                    title=action.title,
                    description=action.description,
                )
            )
    show(t("action_list_hint"))


def _show_log(box: ActionBox, show: Callable[[str], None]) -> None:
    """Zeigt das Protokoll im Klartext: Zeitpunkt, Grund, Ergebnis, Rücknahme."""
    entries = box.log.entries()
    if not entries:
        show(t("log_empty"))
    else:
        show(t("log_header", count=len(entries)))
        for entry in entries:
            show(t("log_line", time=entry.time_display, title=entry.title))
            show(t("log_reason", reason=entry.reason))
            show(t("log_result", result=entry.result))
            show(t("log_undone") if entry.undone else t("log_undo_open"))
    show(t("log_location", path=box.log.path))


def _undo(box: ActionBox, show: Callable[[str], None]) -> None:
    """Nimmt die letzte Aktion zurück. Ein Fehler ist eine Meldung, kein Abbruch."""
    try:
        outcome = box.undo_last()
    except AIHelperError as exc:
        show(str(exc))
        return
    if outcome is None:
        show(t("undo_nothing"))
        return
    entry, text = outcome
    show(t("undo_done", title=entry.title, result=text))


def _run_action(
    key: str,
    *,
    box: ActionBox,
    show: Callable[[str], None],
    learn: bool = False,
    figure: "_Figure | None" = None,
) -> Generator[Frage, object, None]:
    """Vorschau, Bestätigung, Ausführung — in genau dieser Reihenfolge.

    Ohne Bestätigung passiert nichts: es geht kein Befehl über die Naht und es
    entsteht kein Protokolleintrag. Ist das Ziel schon erreicht, wird ebenfalls
    nichts ausgeführt und nichts protokolliert — sonst stünde im Protokoll eine
    Aktion, die nichts getan hat.

    Ein Eintrag, der Administratorrechte braucht, wird **angekündigt und nicht
    ausgeführt** (Slice 7, Entscheidung 10): es gibt keine Rückfrage, keinen
    Befehl und keinen Protokolleintrag, sondern den Weg, den der Nutzer selbst
    gehen kann.

    Im Lernmodus (Slice 8) wird **gar nichts** ausgeführt, auch nicht nach
    einem „ja": die Hülle zeigt den jetzigen Zustand, den Weg und die Schritte,
    und das war es. Es geht kein Befehl über die Naht und es entsteht kein
    Protokolleintrag.

    Die Bestätigung wird **erfragt** (``yield``): ob sie aus der Tastatur, aus
    dem Eingabefeld des Browsers oder aus einer Warteschlange kommt, entscheidet
    die Hülle, die diesen Erzeuger treibt.
    """
    action = box.find(key)
    if action is None:
        show(
            t(
                "action_unknown",
                schluessel=key,
                known=", ".join(entry.key for entry in box.actions),
            )
        )
        return

    if action.needs_admin:
        if figure is not None:
            figure.switch(AvatarState.EXPLAINING)
        show(t("action_handover_preview", title=action.title))
        show(t("action_handover_hint", hint=action.handover))
        show(t("action_handover_rule"))
        return

    try:
        state = box.check(action)
    except AIHelperError as exc:
        show(str(exc))
        return

    if learn:
        # Lernmodus: nur erklären — nicht fragen, nichts schreiben.
        if figure is not None:
            figure.switch(AvatarState.EXPLAINING)
        show(t("learn_action_head", title=action.title))
        show(t("action_now", state=state.description))
        show(t("learn_action_steps", title=action.title))
        show(t("learn_action_rule"))
        return

    show(t("action_preview", title=action.title))
    show(t("action_now", state=state.description))
    if state.at_goal:
        show(t("action_already"))
        return

    answer: object = yield Frage(t("action_confirm"))
    if answer is ABBRUCH:
        # Ein Abbruch bei der Rückfrage beendet das Gespräch ruhig — wie an
        # jeder anderen Stelle (Slice 10). Die Aktion selbst läuft dabei nicht:
        # es geht kein Befehl über die Naht und es entsteht kein Protokolleintrag.
        raise QuietExit
    if answer is ENDE:
        # Kein Lesen der Bestätigung möglich heißt: keine Bestätigung.
        show("")
        show(t("action_declined"))
        return
    if str(answer).strip().lower() not in CONFIRM_WORDS:
        show(t("action_declined"))
        return

    try:
        entry = box.execute(action, reason=f"/aktion {action.key}", state=state)
    except AIHelperError as exc:
        show(str(exc))
        return
    show(t("action_done", result=entry.result))


def _action_command(
    line: str,
    *,
    box: ActionBox | None,
    show: Callable[[str], None],
    learn: bool = False,
    figure: "_Figure | None" = None,
) -> Generator[Frage, object, bool]:
    """Behandelt /aktionen, /aktion, /rueckgaengig und /protokoll.

    Rückgabe: ``True``, wenn die Zeile ein Aktionsbefehl war. Ohne
    Aktionsrahmen (kein Protokoll) wird nichts ausgeführt, sondern gemeldet.

    Im Lernmodus (Slice 8) sind ``/aktionen`` und ``/protokoll`` unverändert
    (sie zeigen nur), ``/aktion <schlüssel>`` erklärt statt auszuführen, und
    ``/rueckgaengig`` wird abgelehnt: der Modus verspricht, nichts zu ändern.
    """
    command = line.partition(" ")[0].lower()
    if command not in ACTION_COMMANDS:
        return False

    if box is None:
        show(t("action_unavailable") if command != "/protokoll" else t("log_unavailable"))
        return True

    if command == "/aktionen":
        _show_actions(box, show)
    elif command == "/protokoll":
        _show_log(box, show)
    elif command == "/rueckgaengig":
        if learn:
            show(t("learn_undo_blocked"))
        else:
            _undo(box, show)
    else:  # /aktion <schlüssel>
        key = " ".join(line.partition(" ")[2].split()).lower()
        if not key:
            show(t("action_usage"))
        else:
            yield from _run_action(key, box=box, show=show, learn=learn, figure=figure)
    return True


def conversation(
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
    show: Callable[[str], None],
    write: Callable[[str], None],
) -> Generator[Frage, object, int]:
    """Führt das Gespräch und gibt bei jeder Eingabe eine ``Frage`` aus.

    ``show`` schreibt eine ganze Zeile (mit Umbruch), ``write`` gibt Text ohne
    Umbruch aus — das braucht der gestreamte Antwortweg (Slice 5b). Beide
    Hüllen setzen das auf ihre Art um: das Terminal auf ``sys.stdout``, der
    Browser in einen Zeilensammler.

    Zweimal im Gespräch wird eine Zeile gebraucht (Haupteingabe und
    Bestätigungsfrage); an beiden Stellen wird der Erzeuger unterbrochen.
    Rückgabe (über ``StopIteration``): der Exit-Code.

    ``mode_key`` ist die Betriebsart (``online``, ``lokal`` oder ``demo``); sie
    steht in der Begrüßung und in jeder Antwortzeile, damit erkennbar ist,
    welches Modell geantwortet hat (Entscheidung 8).
    """
    box = Toolbox() if toolbox is None else toolbox
    mode_name = t(f"mode_{mode_key}")
    # Der Lernmodus (Slice 8): erklären statt ausführen. Der Anfangswert kommt
    # aus den Einstellungen, /lernen schaltet zur Laufzeit um.
    lernen = learn_mode
    # Die zuletzt gemessenen Werte: sie stehen im Systemtext, damit der Avatar
    # mit gemessenen Werten antwortet statt mit Vermutungen.
    gemessen: list[Measurement] = []
    # Der Hinweis auf den Rückfall (Anbieter ohne Teilstücke) kommt einmal.
    hinweis_gezeigt = False

    def refresh_system_prompt() -> None:
        """Setzt den Systemtext aus Charakter, Gedächtnis, Messwerten und Aktionen neu."""
        try:
            facts = memory.facts() if memory is not None else ()
        except AIHelperError as exc:
            # Der Speicher ist kaputt geworden: melden und ohne Gedächtnis weiter.
            show(str(exc))
            facts = ()
        teile = [
            build_system_prompt(persona, facts),
            build_state_section(gemessen, box.tools),
        ]
        if action_box is not None:
            teile.append(build_actions_section(action_box.actions))
        if search is not None:
            # Die Recherche steht hinter den Aktionen: sie sagt, dass es
            # Nachschlagen gibt und dass die Quelle genannt werden muss.
            teile.append(build_search_section(search.label))
        if lernen:
            # Der Lernmodus steht hinter dem Aktionsabschnitt: er sagt, dass die
            # Einträge gerade Wissen sind und nichts davon ausgeführt wird.
            teile.append(build_learn_section(True))
        session.set_system_prompt("\n".join(teile))

    show(t("welcome", name=persona.name))
    show(t("model_note", model=provider.label, mode_name=mode_name, base_url=base_url))
    show(t("exit_hint"))
    show(t("memory_hint") if memory is not None else t("memory_unavailable"))
    show(t("nachschauen_hint"))
    show(t("action_hint"))
    if search is not None:
        # Die Recherche steht wie die Aktionen in der Begrüßung (Slice 9).
        show(t("search_hint"))
    # Der Lernmodus steht wie die Betriebsart in der Begrüßung (Entscheidung 8).
    show(t("learn_active_note") if lernen else t("learn_hint"))
    show("")

    figure = _Figure(show)

    def abbruch() -> int:
        """Ein Strg-C: ruhig beenden, ohne Traceback und ohne halbe Zeile (Slice 10).

        Die Figur geht auf neutral — ein Abbruch ist kein Fehler (Slice 2) —, es
        kommt genau eine deutsche Zeile, und der Exit-Code ist 0.
        """
        show("")
        figure.switch(AvatarState.NEUTRAL)
        show(t("interrupted"))
        return 0

    figure.switch(AvatarState.NEUTRAL)

    # Nachschauen beim Start: ab hier steht der echte Systemzustand im
    # Systemtext jeder Anfrage. Ein Strg-C währenddessen beendet ruhig.
    show(t("looking_around"))
    try:
        gemessen.extend(box.measure_all())
    except KeyboardInterrupt:
        return abbruch()
    refresh_system_prompt()

    while True:
        raw: object = yield Frage(t("prompt_user"))
        if raw is ENDE or raw is ABBRUCH:
            # Ende der Eingabe oder Abbruch: das Gespräch endet ruhig (Slice 10).
            show("")
            figure.switch(AvatarState.HAPPY)
            show(t("farewell"))
            return 0

        line = str(raw).strip()
        if not line:
            continue
        if line.lower() in EXIT_COMMANDS:
            figure.switch(AvatarState.HAPPY)
            show(t("farewell"))
            return 0
        if line.lower() in NACHSEHEN_COMMANDS:
            # Frisch nachschauen; die neuen Werte kommen auch in den Systemtext.
            # Ein Strg-C währenddessen beendet ruhig (Slice 10).
            try:
                frisch = box.measure_all()
            except KeyboardInterrupt:
                return abbruch()
            gemessen.clear()
            gemessen.extend(frisch)
            refresh_system_prompt()
            _show_measurements(gemessen, show)
            continue
        if line.partition(" ")[0].lower() in LEARN_COMMANDS:
            # /lernen schaltet an, /lernen aus zurück (Slice 8). Die Umschaltung
            # wirkt sofort auf den Systemtext der nächsten Anfrage.
            argument = line.partition(" ")[2].strip().lower()
            if argument in LEARN_OFF_VALUES:
                if lernen:
                    lernen = False
                    refresh_system_prompt()
                    show(t("learn_off"))
                else:
                    show(t("learn_already_off"))
            elif not argument or argument in LEARN_ON_VALUES:
                if lernen:
                    show(t("learn_already_on"))
                else:
                    lernen = True
                    refresh_system_prompt()
                    show(t("learn_on"))
            else:
                show(t("learn_usage"))
            continue
        if line.partition(" ")[0].lower() in SEARCH_COMMANDS:
            # Die Recherche (Slice 9): erst ansagen, dass eine Frage den Rechner
            # verlässt, dann nachschlagen, dann die Quellen zeigen. Dieselben
            # Quellen gehen mit der Frage an das Modell, damit die Antwort sich
            # belegen lässt; sie stehen damit im Verlauf und bleiben für
            # Rückfragen erhalten.
            frage = " ".join(line.partition(" ")[2].split())
            if not frage:
                show(t("search_usage"))
                continue
            if search is None:
                show(t("search_unavailable"))
                continue
            figure.switch(AvatarState.THINKING)
            show(t("search_announce", query=frage, provider=search.label))
            try:
                treffer = search.search(frage)
            except AIHelperError as exc:
                figure.switch(AvatarState.ERROR)
                show(str(exc))
                continue
            except KeyboardInterrupt:
                # Strg-C während des Nachschlagens beendet das Gespräch ruhig
                # (Slice 10); es kommt keine halbe Quellenliste.
                return abbruch()
            if not treffer:
                show(t("search_no_hits", query=frage))
                continue
            _show_sources(treffer, show)
            line = t("search_question", query=frage, hits=build_search_block(treffer))
        if _memory_command(
            line,
            memory=memory,
            memory_path=memory_path,
            show=show,
            refresh=refresh_system_prompt,
        ):
            continue
        try:
            aktion_bearbeitet = yield from _action_command(
                line,
                box=action_box,
                show=show,
                learn=lernen,
                figure=figure,
            )
        except QuietExit:
            # Strg-C bei der Bestätigungsfrage (Slice 10): ruhig beenden.
            return abbruch()
        if aktion_bearbeitet:
            continue

        history = [*session.messages, Message.user(line)]
        # Die Figur denkt, bevor die Anfrage rausgeht.
        figure.switch(AvatarState.THINKING)
        kopf = t("prompt_assistant", model=provider.label, mode_name=mode_name)
        stuecke: list[str] = []
        begonnen = False

        def stueck_zeigen(teil: str) -> None:
            """Gibt ein Teilstück sofort aus (ohne Zeilenumbruch, mit flush).

            Mit dem ersten Stück wechselt die Figur auf "spricht" und die
            Antwortzeile beginnt: der Nutzer sieht das erste Wort nach rund
            einer Zehntelsekunde statt erst nach der ganzen Antwort.
            """
            nonlocal begonnen
            if not begonnen:
                begonnen = True
                figure.switch(AvatarState.SPEAKING)
                write(kopf)
            stuecke.append(teil)
            write(teil)

        antwort = ""
        try:
            if isinstance(provider, StreamingProvider):
                for teil in provider.stream(history):
                    if teil:
                        stueck_zeigen(teil)
                if not stuecke:
                    # Ein Strom ohne ein einziges Stück ist eine leere Antwort
                    # und gehört nicht in den Verlauf.
                    raise ProviderError(t("error_empty_answer"))
                antwort = "".join(stuecke)
            else:
                # Rückfall: dieser Anbieter kann keine Teilstücke liefern.
                # Einmal ansagen, dann wie bisher die fertige Antwort holen.
                if not hinweis_gezeigt:
                    show(t("stream_fallback"))
                    hinweis_gezeigt = True
                antwort = provider.complete(history)
        except AIHelperError as exc:
            figure.switch(AvatarState.ERROR)
            if begonnen:
                # Die halbe Antwort steht schon auf dem Schirm; der Rest kommt
                # als Meldung, und der Verlauf bleibt unverändert.
                write("\n")
            show(f"{kopf}{exc}")
            if mode_key == MODE_LOCAL:
                # Im lokalen Betrieb hängt die Hülle den nächsten Schritt an
                # (Slice 10): die Meldung des Anbieters bleibt kurz, damit die
                # Selbstprüfung sie als Grund zeigen kann, ohne den Weg doppelt
                # zu nennen.
                show(t("error_local_next_step"))
            continue
        except KeyboardInterrupt:
            if begonnen:
                write("\n")
            show("")
            figure.switch(AvatarState.NEUTRAL)
            show(t("interrupted"))
            return 0

        session.add_user(line)
        session.add_assistant(antwort)
        if begonnen:
            write("\n")
        else:
            figure.switch(AvatarState.SPEAKING)
            show(f"{kopf}{antwort}")
        show("")
