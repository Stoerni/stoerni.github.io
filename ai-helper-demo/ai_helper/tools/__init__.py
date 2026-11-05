# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Werkzeuge, die den echten Systemzustand lesen.

Der Avatar redet nicht über den Rechner, er schaut nach (Entscheidung 9 im
Design-Dokument): Windows-Version, Prozessor, Bildschirmauflösung, Grafik,
Arbeitsspeicher und Laufwerke. Werkzeuge gehören laut Design Kapitel 8.1 in den Kern; deshalb
steht der Werkzeugkasten hier und nicht in einer Hülle.

Der Kern kennt nur die Schnittstelle je Werkzeug (Name, kurze Beschreibung und
eine Funktion, die den Zustand liefert), nicht den Befehl dahinter. Gemessen
wird ausschließlich lesend: kein Netz, keine Administratorenrechte, keine
Änderung am System (Entscheidung 10).

Ein Werkzeug liefert ``Measurement``-Werte; was nicht messbar war, wird als
nicht messbar gemeldet und nicht erfunden.
"""

from __future__ import annotations

from ai_helper.tools.measurement import Measurement
from ai_helper.tools.runner import Runner, SystemRunner, ToolUnavailable
from ai_helper.tools.system import (
    CPU_SOURCE,
    GRAPHICS_SOURCE,
    MEMORY_SOURCE,
    SCREEN_SOURCE,
    DRIVES_SOURCE,
    WINDOWS_EDITION_SOURCE,
    WINDOWS_VERSION_SOURCE,
)
from ai_helper.tools.toolbox import (
    SYSTEM_TOOLS,
    Tool,
    Toolbox,
    build_state_section,
    default_runner,
)

__all__ = [
    "CPU_SOURCE",
    "DRIVES_SOURCE",
    "GRAPHICS_SOURCE",
    "MEMORY_SOURCE",
    "SCREEN_SOURCE",
    "SYSTEM_TOOLS",
    "WINDOWS_EDITION_SOURCE",
    "WINDOWS_VERSION_SOURCE",
    "Measurement",
    "Runner",
    "SystemRunner",
    "Tool",
    "ToolUnavailable",
    "Toolbox",
    "build_state_section",
    "default_runner",
]
