# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Die Demo-Fassung des Kerns: feste Antworten, fester Bericht, kein Ausführen.

Diese Demo zeigt den AI-Helper auf einer öffentlichen Seite (Portfolio) ohne
Netz, ohne Schlüssel und ohne einen einzigen Eingriff am Rechner des Besuchers.
``ai_helper/`` bleibt dabei **unverändert**: die Demo ist eine zweite Hülle, die
genau die drei Außenstellen einspeist, die auch die Tests mit Doppelgängern
besetzen — dieselben Nahtstellen, nur mit anderen Doppelgängern:

* **Anbieter** (``provider.py``): fester, geskripteter Anbieter statt Modell
  (``DemoProvider``).
* **Systemabfrage** (``measurements.py``): ein fester, als Demo gekennzeichneter
  Messbericht statt echter Befehle (``DemoToolbox``).
* **Ausführender** (``executor.py``): ein Ausführender, der ins Protokoll
  schreibt und nichts ausführt (``DemoExecutor``).

Der Kern wird nicht umgebaut und bekommt keine ``if browser:``-Zweige; die
Hülle (``ai_helper/ui/web.py``, eigene Slice) und die Demo-Bausteine bleiben
getrennt. Das Drehbuch und die Texte liegen in ``script.py`` bzw. in der
Sprachdatei (Entscheidung 7).
"""

from __future__ import annotations

from ai_helper.demo.executor import DEMO_ANSWERS, DemoExecutor
from ai_helper.demo.measurements import (
    DEMO_MEASUREMENTS,
    DemoRunner,
    DemoToolbox,
    demo_report,
)
from ai_helper.demo.provider import DemoProvider
from ai_helper.demo.script import (
    POLITE_ANSWER_KEY,
    SCRIPT,
    ScriptEntry,
    answer_for,
    polite_answer,
    suggestions,
)

__all__ = [
    "DEMO_ANSWERS",
    "DEMO_MEASUREMENTS",
    "POLITE_ANSWER_KEY",
    "SCRIPT",
    "DemoExecutor",
    "DemoProvider",
    "DemoRunner",
    "DemoToolbox",
    "ScriptEntry",
    "answer_for",
    "demo_report",
    "polite_answer",
    "suggestions",
]
