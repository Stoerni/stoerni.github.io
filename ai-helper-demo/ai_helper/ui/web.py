# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Browser-Hülle: Eingabe aus einer Warteschlange, Ausgabe Zeile für Zeile.

Der Browser kann nicht blockieren: ``input()`` gibt es dort nicht, und ein
Wartevorgang würde die Seite anhalten. Diese Hülle treibt deshalb **dieselbe**
Gesprächsschleife wie das Terminal (``ai_helper/ui/shell.py``) Schritt für
Schritt: die Seite ruft ``WebShell.feed(<zeile>)`` je Eingabe auf und liest die
fertigen Zeilen aus ``WebShell.ausgabe``. Dieselben Texte, dieselbe
Reihenfolge, derselbe Sicherheitsweg „zeigen, fragen, zurücknehmen können".

Die zwei Nahtstellen sind genau die, die auch die Terminal-Hülle und die Tests
einspeisen:

* ``input_fn`` — hier ``LineQueue``: eine Warteschlange, aus der jede Eingabe
  eine Zeile nimmt; ist sie leer, ergibt sie ``EOFError`` (das ist im Terminal
  das Ende der Eingabe, Strg-D).
* ``out`` — hier ``LineCollector``: ein Objekt mit ``write``/``flush`` wie ein
  Ausgabestrom, das vollständige Zeilen sammelt und jede sofort meldet.

Alles ist **synchron**: PyScript 2024.1.1 führt die Seite mit ``eval_code``
aus, ein ``await`` auf oberster Ebene wäre ein SyntaxError, und ``pyodide.FS``
gibt es in dieser Fassung nicht (beides gemessen in Slice D1). Diese Datei
braucht beides nicht.

Die Demo-Bausteine aus Slice D2 (``ai_helper/demo/``) setzt ``demo_shell``
zusammen: fester Anbieter, fester Messbericht, ein Ausführender, der nur Buch
führt. Ohne diese drei Ersatzteile stünden die echten Befehle samt Fehlertext
im Bild des Besuchers (gemessen in Slice D1, Frage 4).
"""

from __future__ import annotations

from collections import deque
from collections.abc import Callable, Generator, Iterable
from pathlib import Path

from ai_helper.actions import ActionBox, ActionLog, Executor
from ai_helper.core.memory import Memory
from ai_helper.core.provider import Provider
from ai_helper.core.session import Session
from ai_helper.demo import DemoExecutor, DemoProvider, DemoToolbox
from ai_helper.i18n import t, set_language, current_language
from ai_helper.persona import DEFAULT_PERSONA, Persona
from ai_helper.search import SearchProvider
from ai_helper.tools import Toolbox
from ai_helper.ui import shell
from ai_helper.ui.shell import ABBRUCH, ENDE, Frage

__all__ = [
    "DEMO_BASE_URL",
    "DEMO_LOG_FILE",
    "DEMO_MODE_KEY",
    "LineCollector",
    "LineQueue",
    "WebShell",
    "demo_notice",
    "demo_shell",
]

#: Die Betriebsart der Demo: sie steht in jeder Antwortzeile (Entscheidung 8).
DEMO_MODE_KEY = "demo"
#: Die Adresse, die in der Begrüßung genannt wird — eine Demo, kein Dienst.
DEMO_BASE_URL = "demo://browser"
#: Das Protokoll der Demo: es liegt im Dateisystem der Seite, nicht auf der Platte.
DEMO_LOG_FILE = Path("/ai-helper-demo/actions.json")


class LineQueue:
    """Eingabe aus einer Warteschlange — das Eingabefeld der Browser-Hülle.

    Sie ist als ``input_fn`` einsetzbar: jeder Aufruf gibt die nächste Zeile
    zurück, und eine **leere** Warteschlange ergibt ``EOFError``. Genau das
    bedeutet im Terminal das Ende der Eingabe (Strg-D) — hier also die leere
    Eingabe. ``prompts`` hält fest, mit welchem Text um welche Zeile gebeten
    wurde (``Du: `` bzw. die Bestätigungsfrage).
    """

    def __init__(self, lines: Iterable[str] = ()) -> None:
        self._lines: deque[str] = deque(lines)
        self.prompts: list[str] = []

    def push(self, line: str) -> None:
        """Legt eine Zeile bereit (etwa die aus dem Eingabefeld)."""
        self._lines.append(line)

    def __call__(self, prompt: str) -> str:
        """Die nächste bereitliegende Zeile. Leer ⇒ ``EOFError``."""
        self.prompts.append(prompt)
        if not self._lines:
            raise EOFError
        return self._lines.popleft()

    def __len__(self) -> int:
        return len(self._lines)


class LineCollector:
    """Ausgabe der Browser-Hülle: sammelt vollständige Zeilen.

    Sie ist als ``out`` einsetzbar (``write``/``flush`` wie ein Ausgabestrom,
    also auch für ``print(..., file=...)``). Vollständige Zeilen stehen in
    ``lines``, was noch ohne Umbruch dasteht — ein Teilstück der gestreamten
    Antwort, die Aufforderung ``Du: `` — steht in ``pending``. ``text`` ist
    alles Geschriebene unverändert und deshalb Zeichen für Zeichen mit einer
    Konsole vergleichbar.

    ``on_line`` meldet jede fertige Zeile sofort, damit die Seite den Text
    anhängen kann, während die Schleife noch läuft.
    """

    def __init__(self, on_line: Callable[[str], None] | None = None) -> None:
        self._lines: list[str] = []
        self._pending = ""
        self._raw: list[str] = []
        self._on_line = on_line

    def write(self, text: str) -> None:
        """Nimmt Text an und teilt ihn an den Zeilenenden in Zeilen."""
        if not text:
            return
        self._raw.append(text)
        self._pending += text
        while "\n" in self._pending:
            zeile, self._pending = self._pending.split("\n", 1)
            self._lines.append(zeile)
            if self._on_line is not None:
                self._on_line(zeile)

    def flush(self) -> None:
        """Nichts zu tun: jede vollständige Zeile steht sofort bereit."""

    @property
    def lines(self) -> list[str]:
        """Die vollständigen Zeilen in der Reihenfolge der Ausgabe."""
        return list(self._lines)

    @property
    def pending(self) -> str:
        """Die angefangene Zeile (noch ohne Umbruch)."""
        return self._pending

    @property
    def text(self) -> str:
        """Alles Geschriebene, unverändert — zum Vergleichen mit einer Konsole."""
        return "".join(self._raw)


class WebShell:
    """Die Hülle für den Browser: eine Zeile hinein, Zeilen heraus.

    Der Browser kann nicht blockieren, deshalb ist die Schleife ein
    Schrittmotor über denselben Erzeuger wie im Terminal
    (``ai_helper/ui/shell.py``). Der Ablauf auf der Seite:

    1. ``start()`` — Begrüßung, fester Messbericht, erste Aufforderung.
    2. Je Eingabe des Besuchers ``feed(zeile)`` (Rückgabe: läuft es noch?).
    3. ``abort()`` für Escape bzw. den Abbrechen-Knopf, ``end()`` für das Ende
       der Eingabe. Beides endet ruhig mit Exit-Code 0.

    ``frage`` ist die gerade offene Aufforderung (``Frage.prompt`` ist der Text,
    den das Eingabefeld zeigen kann), ``exit_code`` bleibt ``None``, solange das
    Gespräch läuft.

    Die Sprache kann per ``set_language`` umgeschaltet werden — die Sitzung wird
    neu gestartet und alle Texte werden in der neuen Sprache gerendert.
    """

    def __init__(
        self,
        *,
        provider: Provider,
        lines: Iterable[str] = (),
        collector: LineCollector | None = None,
        session: Session | None = None,
        base_url: str = DEMO_BASE_URL,
        mode_key: str = DEMO_MODE_KEY,
        persona: Persona = DEFAULT_PERSONA,
        memory: Memory | None = None,
        memory_path: Path | None = None,
        toolbox: Toolbox | None = None,
        action_box: ActionBox | None = None,
        learn_mode: bool = False,
        search: SearchProvider | None = None,
        language: str = "de",
    ) -> None:
        self._provider = provider
        self._action_box = action_box
        self._language = language
        set_language(language)
        self.eingabe = LineQueue(lines)
        self.ausgabe = LineCollector() if collector is None else collector
        self.frage: Frage | None = None
        self.exit_code: int | None = None
        self._schleife: Generator[Frage, object, int] | None = shell.conversation(
            provider=provider,
            session=Session() if session is None else session,
            base_url=base_url,
            mode_key=mode_key,
            persona=persona,
            memory=memory,
            memory_path=memory_path,
            toolbox=toolbox,
            action_box=action_box,
            learn_mode=learn_mode,
            search=search,
            show=self._zeile,
            write=self.ausgabe.write,
        )

    # --- Zustand -----------------------------------------------------
    @property
    def laeuft(self) -> bool:
        """Läuft das Gespräch noch?"""
        return self.exit_code is None

    @property
    def zeilen(self) -> list[str]:
        """Die bisher vollständigen Ausgabezeilen (Kurzform für die Seite)."""
        return self.ausgabe.lines

    @property
    def language(self) -> str:
        """Aktuelle Sprache (de/en)."""
        return self._language

    # --- Antrieb -----------------------------------------------------
    def start(self) -> None:
        """Gibt die Begrüßung aus und läuft bis zur ersten Aufforderung."""
        self._weiter(None, senden=False)

    def feed(self, line: str) -> bool:
        """Verarbeitet **eine** Eingabezeile. Rückgabe: läuft es noch?"""
        self._weiter(line, senden=True)
        return self.laeuft

    def end(self) -> bool:
        """Die Eingabe endet: wie ``EOFError`` (am Hauptzeichen: verabschieden)."""
        self._weiter(ENDE, senden=True)
        return self.laeuft

    def abort(self) -> bool:
        """Escape bzw. Abbrechen-Knopf: das Gespräch ruhig beenden (Slice 10)."""
        self._weiter(ABBRUCH, senden=True)
        return self.laeuft

    def set_language(self, language: str) -> None:
        """Schaltet die Sprache um und startet die Sitzung neu.

        Alle Texte (Begrüßung, Demo-Antworten, Messbericht, Hilfetexte) werden
        in der neuen Sprache gerendert.
        """
        if language not in ("de", "en"):
            raise ValueError(f"Unsupported language: {language!r}. Use 'de' or 'en'.")
        if language == self._language:
            return
        self._language = language
        set_language(language)
        # Sitzung neu aufbauen mit der neuen Sprache
        self._schleife = shell.conversation(
            provider=self._provider,
            session=Session(),
            base_url=DEMO_BASE_URL,
            mode_key=DEMO_MODE_KEY,
            persona=DEFAULT_PERSONA,
            memory=None,
            memory_path=None,
            toolbox=DemoToolbox(),
            action_box=self._action_box,
            learn_mode=False,
            search=None,
            show=self._zeile,
            write=self.ausgabe.write,
        )
        self.eingabe = LineQueue()
        self.ausgabe = LineCollector()
        self.frage = None
        self.exit_code = None
        self.start()

    # --- Innen -------------------------------------------------------
    def _zeile(self, text: str = "") -> None:
        """Eine ganze Zeile ausgeben (das ``show`` der gemeinsamen Schleife)."""
        self.ausgabe.write(f"{text}\n")

    def _weiter(self, wert: object, *, senden: bool) -> None:
        """Einen Schritt der Schleife fahren: hineinreichen oder anfangen."""
        if self._schleife is None:
            return
        try:
            if senden:
                self.frage = self._schleife.send(wert)
            else:
                self.frage = next(self._schleife)
        except StopIteration as ende:
            # Das Gespräch ist zu Ende und nennt seinen Exit-Code.
            self.frage = None
            self.exit_code = 0 if ende.value is None else int(ende.value)
            self._schleife = None


def demo_shell(
    *,
    lines: Iterable[str] = (),
    collector: LineCollector | None = None,
    executor: Executor | None = None,
    log_path: Path | None = DEMO_LOG_FILE,
    session: Session | None = None,
    persona: Persona = DEFAULT_PERSONA,
    language: str = "de",
) -> WebShell:
    """Die Demo-Hülle für den Browser: alle drei Außenstellen aus ``ai_helper/demo``.

    Eingespeist werden Anbieter (``DemoProvider``), Werkzeugliste
    (``DemoToolbox`` mit festem Bericht) und Ausführender (``DemoExecutor``, der
    nur Buch führt) — dieselben drei Nahtstellen, die auch die Tests mit
    Doppelgängern besetzen. Damit misst die Demo nichts, führt nichts aus und
    schickt nichts nach außen; der Sicherheitsweg bleibt trotzdem vollständig
    sichtbar.

    ``log_path=None`` schaltet die Aktionen ab (kein Protokoll, keine Aktion) —
    im Browser liegt das Protokoll im Dateisystem der Seite.
    """
    ausfuehrer: Executor = DemoExecutor() if executor is None else executor
    box = None if log_path is None else ActionBox(log=ActionLog(log_path), executor=ausfuehrer)
    return WebShell(
        provider=DemoProvider(),
        lines=lines,
        collector=collector,
        session=session,
        base_url=DEMO_BASE_URL,
        mode_key=DEMO_MODE_KEY,
        persona=persona,
        memory=None,
        memory_path=None,
        toolbox=DemoToolbox(),
        action_box=box,
        learn_mode=False,
        search=None,
        language=language,
    )


def demo_notice() -> str:
    """Die Zeile, die über der Demo stehen muss: was hier nicht passiert."""
    return t("demo_hint")
