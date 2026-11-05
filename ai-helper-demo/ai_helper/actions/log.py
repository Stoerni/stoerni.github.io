# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Das Protokoll: was ausgeführt wurde, wann, warum und wie es zurückgeht.

Entscheidung 5 im Design-Dokument: jede ausgeführte Aktion wird mit Zeitpunkt,
Grund, Ergebnis und Rücknahmeweg festgehalten. Die Datei liegt im
Benutzerordner (Pfad über eine Einstellung), ist im Klartext lesbar und wird
atomar geschrieben — genau wie das Gedächtnis (``memory/json_store.py``): erst
in eine Nebendatei, dann an ihren Platz. Ein Absturz lässt damit nie eine halbe
Datei stehen.

Eine kaputte Datei ist kein Absturz, sondern ein ``LogStorageError`` mit
fertiger deutscher Meldung; sie wird nicht überschrieben, damit nichts verloren
geht.

Der Rücknahmeweg ist der vorher festgehaltene Wert (``before``). Ein Eintrag
ohne ``undoable`` (etwa eine Aktion, die sich nicht zurücknehmen lässt) bleibt
im Protokoll stehen, wird aber nie zurückgenommen.
"""

from __future__ import annotations

import json
import os
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ai_helper.core.errors import LogStorageError
from ai_helper.i18n import t

__all__ = ["ActionLog", "LogEntry"]


@dataclass(frozen=True, slots=True)
class LogEntry:
    """Ein Eintrag des Protokolls: eine ausgeführte Aktion."""

    time: str
    key: str
    title: str
    reason: str
    result: str
    before: str | None = None
    undoable: bool = True
    undone: bool = False

    @property
    def time_display(self) -> str:
        """Der Zeitpunkt, wie er angezeigt wird."""
        return self.time.replace("T", " ")[:19]

    def to_json(self) -> dict[str, Any]:
        return {
            "time": self.time,
            "key": self.key,
            "title": self.title,
            "reason": self.reason,
            "result": self.result,
            "before": self.before,
            "undoable": self.undoable,
            "undone": self.undone,
        }

    @classmethod
    def from_json(cls, raw: Any) -> "LogEntry":
        """Liest einen Eintrag. Fehlt etwas, ist die Datei kaputt."""
        if not isinstance(raw, dict):
            raise ValueError(t("log_entry_not_object"))
        try:
            return cls(
                time=str(raw["time"]),
                key=str(raw["key"]),
                title=str(raw["title"]),
                reason=str(raw["reason"]),
                result=str(raw["result"]),
                before=None if raw.get("before") is None else str(raw["before"]),
                undoable=bool(raw.get("undoable", True)),
                undone=bool(raw.get("undone", False)),
            )
        except KeyError as exc:
            raise ValueError(t("log_entry_incomplete", field=exc)) from exc


class ActionLog:
    """Das Protokoll als JSON-Datei im Benutzerordner."""

    def __init__(self, path: Path) -> None:
        self._path = Path(path)

    @property
    def path(self) -> Path:
        """Wo das Protokoll liegt (für die Anzeige, nicht zum Schreiben)."""
        return self._path

    def load(self) -> tuple[LogEntry, ...]:
        """Prüft die Datei beim Start und liefert, was drinsteht.

        Die Prüfung ist der Startpunkt der Hülle: eine kaputte Datei fällt
        dadurch sofort auf, mit deutscher Meldung statt Absturz.
        """
        return self._read()

    def entries(self) -> tuple[LogEntry, ...]:
        """Die Einträge, älteste zuerst."""
        return self._read()

    def append(self, entry: LogEntry) -> None:
        """Hängt einen Eintrag an."""
        self._write((*self._read(), entry))

    def last_undoable_index(self) -> int | None:
        """Der letzte Eintrag, der noch zurückgenommen werden kann."""
        entries = self._read()
        for index in range(len(entries) - 1, -1, -1):
            entry = entries[index]
            if entry.undoable and not entry.undone:
                return index
        return None

    def mark_undone(self, index: int) -> None:
        """Vermerkt, dass der Eintrag zurückgenommen wurde.

        Damit ist eine Rücknahme selbst nicht wieder rücknehmbar: derselbe
        Eintrag wird nie zweimal zurückgenommen.
        """
        entries = list(self._read())
        if not 0 <= index < len(entries):
            return
        entry = entries[index]
        entries[index] = LogEntry(
            time=entry.time,
            key=entry.key,
            title=entry.title,
            reason=entry.reason,
            result=entry.result,
            before=entry.before,
            undoable=entry.undoable,
            undone=True,
        )
        self._write(entries)

    # --- Platte ---------------------------------------------------------

    def _read(self) -> tuple[LogEntry, ...]:
        try:
            text = self._path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return ()
        except OSError as exc:
            raise LogStorageError(t("log_unreadable", path=self._path, detail=exc)) from exc

        try:
            data = json.loads(text)
            raw_entries = data["actions"]
            if not isinstance(raw_entries, list):
                raise TypeError(t("log_actions_not_list"))
            return tuple(LogEntry.from_json(raw) for raw in raw_entries)
        except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            raise LogStorageError(t("log_corrupt", path=self._path, detail=exc)) from exc

    def _write(self, entries: Sequence[LogEntry]) -> None:
        content = (
            json.dumps(
                {"actions": [entry.to_json() for entry in entries]},
                ensure_ascii=False,
                indent=2,
            )
            + "\n"
        )
        neighbour = self._path.with_name(self._path.name + ".tmp")
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            neighbour.write_text(content, encoding="utf-8")
            os.replace(neighbour, self._path)
        except OSError as exc:
            neighbour.unlink(missing_ok=True)
            raise LogStorageError(
                t("log_not_writable", path=self._path, detail=exc)
            ) from exc
