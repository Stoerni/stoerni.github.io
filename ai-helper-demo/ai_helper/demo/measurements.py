# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Der feste Messbericht der Demo — ausdrücklich als Demo gekennzeichnet.

Im Browser läuft kein Windows: es gibt keine Registry, kein CIM, keinen
Prozessstart. Die Demo misst deshalb **nichts**. Sie zeigt dem Besucher einen
**festen Bericht**, und jeder Wert trägt als Quelle den Hinweis, dass er nicht
gemessen, sondern festgelegt ist (``demo_measure_source``). Ein festgelegter
Wert, der sich als Messung ausgäbe, wäre gegen Entscheidung 9 („gemessene Werte
statt Vermutungen") — deshalb steht der Hinweis an jedem Wert.

``DemoToolbox`` sitzt an derselben Naht wie ``Toolbox``: die Hülle ruft
``measure_all()`` und bekommt Werte; woher sie kommen, weiß sie nicht. Der
``DemoRunner`` dahinter führt nichts aus (er scheitert wie ein blinder
Doppelgänger) — so kann auch versehentlich kein echter Befehl laufen.
"""

from __future__ import annotations

from collections.abc import Sequence

from ai_helper.i18n import t
from ai_helper.tools import SYSTEM_TOOLS, Toolbox, ToolUnavailable
from ai_helper.tools.measurement import Measurement

__all__ = [
    "DEMO_MEASUREMENTS",
    "DemoRunner",
    "DemoToolbox",
    "demo_report",
]


def _quelle() -> str:
    """Die Quelle jedes Demo-Wertes — deutlich als „nicht gemessen" erkennbar."""
    return t("demo_measure_source")


# Der feste Bericht der Demo. Ein einziger, plausibler Beispielrechner; die
# Namen (``windows_version`` …) sind dieselben wie bei den echten Werkzeugen,
# damit Beschriftung und Anzeige unverändert aus der Sprachdatei kommen.
DEMO_MEASUREMENTS: tuple[Measurement, ...] = (
    Measurement("windows_version", "10.0.26100.1742", source=_quelle()),
    Measurement("windows_edition", "Microsoft Windows 11 Pro", source=_quelle()),
    Measurement("cpu", "AMD Ryzen 5 7530U with Radeon Graphics", source=_quelle()),
    Measurement("cpu_cores", t("value_cpu_cores", cores=6, threads=12), source=_quelle()),
    Measurement("screen_resolution", "1920 x 1080", unit=t("value_pixel"), source=_quelle()),
    Measurement("graphics", "AMD Radeon (TM) Graphics", source=_quelle()),
    Measurement("memory_total", "15,3", unit=t("value_gb"), source=_quelle()),
    Measurement("memory_free", "7,1", unit=t("value_gb"), source=_quelle()),
    Measurement("drive_total", "475,9", unit=t("value_gb"), source=_quelle(), params=(("drive", "C:"),)),
    Measurement("drive_free", "312,4", unit=t("value_gb"), source=_quelle(), params=(("drive", "C:"),)),
)


def demo_report() -> tuple[Measurement, ...]:
    """Der feste Messbericht der Demo (eine Kopie, damit niemand ihn verändert)."""
    return DEMO_MEASUREMENTS


class DemoRunner:
    """Eine Systemabfrage, die nichts kann — wie ein blinder Doppelgänger.

    Er liegt unter der ``DemoToolbox``, damit gar kein echter Befehl möglich
    ist. Er wird im Betrieb nie aufgerufen (die Toolbox liefert den festen
    Bericht), aber wenn, dann scheitert er mit einer deutschen Meldung statt
    etwas auszuführen.
    """

    def __init__(self) -> None:
        self.commands: list[list[str]] = []

    def run(self, command: Sequence[str]) -> str:
        self.commands.append([str(teil) for teil in command])
        raise ToolUnavailable(t("demo_runner_unavailable"))


class DemoToolbox(Toolbox):
    """Die Werkzeugliste der Demo mit festem Bericht statt echter Messung.

    Sie benutzt dieselben Werkzeug-Namen wie der echte Betrieb (für den
    Werkzeugabschnitt im Systemtext), misst aber nichts: ``measure_all``
    liefert den festen Bericht aus ``DEMO_MEASUREMENTS``.
    """

    def __init__(self, tools: Sequence = SYSTEM_TOOLS) -> None:
        # ``runner=DemoRunner()`` statt der Voreinstellung: so wird **kein**
        # ``SystemRunner`` erzeugt und der voreingestellte Tauschpunkt
        # (``default_runner``) gar nicht erst angefasst.
        super().__init__(runner=DemoRunner(), tools=tools)

    def measure_all(self) -> tuple[Measurement, ...]:
        """Der feste Bericht — unabhängig davon, wie oft nachgeschaut wird."""
        return DEMO_MEASUREMENTS
