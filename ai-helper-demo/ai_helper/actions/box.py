# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Der Aktionsrahmen: prüfen, anwenden, protokollieren, zurücknehmen.

Der Rahmen hält Katalog, Ausführenden und Protokoll zusammen und ist die eine
Stelle, an der eine Aktion wirklich läuft. Die Hülle fragt ihn; sie kennt weder
Befehle noch Dateien.

Zwei Regeln, die hier durchgesetzt werden:

* **Ohne Protokoll wird nichts ausgeführt.** Entscheidung 5 verlangt, dass jede
  Aktion mit Zeitpunkt, Grund, Ergebnis und Rücknahmeweg festgehalten wird; eine
  Aktion ohne Protokoll wäre nicht mehr nachvollziehbar.
* **Die Rücknahme ist selbst nicht rücknehmbar.** Der Eintrag wird als
  zurückgenommen vermerkt; derselbe Eintrag geht kein zweites Mal zurück.

Jeder Fehler ist eine fertige deutsche Meldung (``ActionError`` bzw.
``LogStorageError``) und beendet nie das Gespräch.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from datetime import datetime

from ai_helper.actions.action import Action, ActionState
from ai_helper.actions.catalog import SYSTEM_ACTIONS
from ai_helper.actions.executor import Executor, default_executor
from ai_helper.actions.log import ActionLog, LogEntry
from ai_helper.core.errors import ActionError, LogStorageError
from ai_helper.i18n import t

__all__ = ["ActionBox"]


class ActionBox:
    """Katalog, Ausführender und Protokoll an einer Stelle."""

    def __init__(
        self,
        *,
        log: ActionLog,
        executor: Executor | None = None,
        actions: Sequence[Action] = SYSTEM_ACTIONS,
        clock: Callable[[], datetime] = datetime.now,
    ) -> None:
        # Die Voreinstellung des Ausführenden steht in ``executor.py`` und wird
        # von den Tests durch einen blinden Doppelgänger ersetzt; wer einen
        # eigenen mitgibt, bekommt genau diesen.
        self._executor = default_executor() if executor is None else executor
        self._log = log
        self._actions = tuple(actions)
        self._clock = clock

    @property
    def actions(self) -> tuple[Action, ...]:
        """Der Katalog in der Reihenfolge, in der er angezeigt wird."""
        return self._actions

    @property
    def log(self) -> ActionLog:
        """Das Protokoll (für die Anzeige)."""
        return self._log

    @property
    def executor(self) -> Executor:
        """Der benutzte Ausführende (für Tests und zum Nachprüfen)."""
        return self._executor

    def find(self, key: str) -> Action | None:
        """Die Aktion zu einem Schlüssel, oder ``None``.

        Ein Schlüssel außerhalb des Katalogs führt nie zu einem Befehl: das ist
        die Stelle, an der Entscheidung 6 durchgesetzt wird.
        """
        wanted = key.strip().lower()
        for action in self._actions:
            if action.key == wanted:
                return action
        return None

    def check(self, action: Action) -> ActionState:
        """Fragt den jetzigen Zustand ab. Scheitert das, gibt es eine Meldung."""
        try:
            return action.check(self._executor)
        except ActionError as exc:
            raise ActionError(t("action_check_failed", detail=exc)) from exc

    def execute(self, action: Action, *, reason: str, state: ActionState) -> LogEntry:
        """Führt die Aktion aus und schreibt sie ins Protokoll.

        Rückgabe: der Protokolleintrag mit dem Ergebnistext. Die Prüfung ist
        hier schon geschehen (``state``), damit zwischen Vorschau und Ausführung
        nichts zweimal gemessen wird.

        Ein Eintrag mit Administratorrechten wird hier verweigert (Slice 7,
        Entscheidung 10): es geht kein Befehl über die Naht. Angekündigt wird
        das in der Hülle; diese Sperre ist die zweite, unabhängige Sicherung.
        """
        if action.needs_admin:
            raise ActionError(t("action_not_self_run", title=action.title))

        try:
            result = action.apply(self._executor)
        except ActionError as exc:
            raise ActionError(t("action_apply_failed", detail=exc)) from exc

        entry = LogEntry(
            time=self._clock().isoformat(timespec="seconds"),
            key=action.key,
            title=action.title,
            reason=reason,
            result=result,
            before=state.raw,
            undoable=True,
            undone=False,
        )
        try:
            self._log.append(entry)
        except LogStorageError as exc:
            # Die Änderung ist passiert — das ehrlich sagen, statt "nicht
            # ausgeführt" zu behaupten.
            raise LogStorageError(t("action_not_logged", detail=exc)) from exc
        return entry

    def undo_last(self) -> tuple[LogEntry, str] | None:
        """Nimmt die letzte Aktion zurück.

        Rückgabe: der Eintrag und der Text der Rücknahme, oder ``None``, wenn es
        nichts zurückzunehmen gibt.
        """
        index = self._log.last_undoable_index()
        if index is None:
            return None
        entry = self._log.entries()[index]
        action = self.find(entry.key)
        if action is None:
            raise ActionError(t("undo_unknown", schluessel=entry.key))
        try:
            text = action.undo(self._executor, entry.before)
        except ActionError as exc:
            raise ActionError(t("action_undo_failed", detail=exc)) from exc
        self._log.mark_undone(index)
        return entry, text
