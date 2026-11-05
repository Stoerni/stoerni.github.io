# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Der Aktionsrahmen: geprüfte Aktionen mit Vorschau, Bestätigung, Protokoll.

Entscheidungen 5 und 6 im Design-Dokument: Aktionen sind deklarative
Katalog-Einträge mit drei Teilen (prüfen, anwenden, rücknehmen); vor jeder
Ausführung gibt es eine Vorschau in Klartext und eine Bestätigung, und jede
ausgeführte Aktion wird mit Zeitpunkt, Grund, Ergebnis und Rücknahmeweg
protokolliert.

Der Rahmen gehört laut Design Kapitel 8.1 in den Kern: die Terminal-Hülle kennt
nur ``ActionBox`` und die Anzeigetexte, die Desktop-Hülle soll denselben Rahmen
benutzen.

Ein Eintrag führt nie einen freien Befehl aus und übernimmt nie einen Befehl aus
der Antwort des Modells — die Befehle stehen im Katalog selbst.
"""

from __future__ import annotations

from ai_helper.actions.action import (
    BASE_TEXTS,
    HANDOVER_TEXTS,
    UNSET_TEXT,
    Action,
    ActionState,
)
from ai_helper.actions.box import ActionBox
from ai_helper.actions.catalog import (
    ACCESSIBILITY,
    CONTENT_DELIVERY,
    CONTROL_PANEL_DESKTOP,
    CONTROL_PANEL_MOUSE,
    DWORD,
    MUTED,
    NOT_SET,
    SZ,
    SYSTEM_ACTIONS,
    UNMUTED,
    build_actions_section,
    build_learn_section,
    delete_command,
    grouped_actions,
    handover_action,
    read_command,
    read_value,
    registry_action,
    restore_value,
    sound_action,
    sound_read_command,
    sound_write_command,
    write_command,
    write_value,
)
from ai_helper.actions.executor import Executor, SystemExecutor, default_executor
from ai_helper.actions.log import ActionLog, LogEntry
from ai_helper.core.errors import ActionError, LogStorageError

__all__ = [
    "ACCESSIBILITY",
    "BASE_TEXTS",
    "CONTENT_DELIVERY",
    "CONTROL_PANEL_DESKTOP",
    "CONTROL_PANEL_MOUSE",
    "DWORD",
    "HANDOVER_TEXTS",
    "MUTED",
    "NOT_SET",
    "SZ",
    "SYSTEM_ACTIONS",
    "UNMUTED",
    "UNSET_TEXT",
    "Action",
    "ActionBox",
    "ActionError",
    "ActionLog",
    "ActionState",
    "Executor",
    "LogEntry",
    "LogStorageError",
    "SystemExecutor",
    "build_actions_section",
    "build_learn_section",
    "default_executor",
    "delete_command",
    "grouped_actions",
    "handover_action",
    "read_command",
    "read_value",
    "registry_action",
    "restore_value",
    "sound_action",
    "sound_read_command",
    "sound_write_command",
    "write_command",
    "write_value",
]
