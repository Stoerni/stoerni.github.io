# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Der Werkzeugkasten: welche Werkzeuge es gibt und was sie gemessen haben.

Ein Werkzeug ist ein Eintrag mit Schlüssel, kurzer Beschreibung (in der
Sprachdatei) und einer Funktion, die den Zustand liefert. Der Kern kennt nur
diese Schnittstelle, nicht den Befehl dahinter (``system.py``).

Ein fehlschlagendes Werkzeug beendet nichts: es wird als "nicht messbar"
gemeldet, und die übrigen Werkzeuge messen weiter. Ein Werkzeugauftrag ist
damit nie ein Grund, das Gespräch abzubrechen.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass

from ai_helper.core.errors import AIHelperError
from ai_helper.i18n import t
from ai_helper.tools import system
from ai_helper.tools.measurement import Measurement
from ai_helper.tools.runner import Runner, SystemRunner

__all__ = [
    "SYSTEM_TOOLS",
    "Tool",
    "Toolbox",
    "build_state_section",
    "default_runner",
]


def default_runner() -> Runner:
    """Die Systemabfrage der echten Maschine.

    Diese eine Stelle tauschen die Tests aus, damit kein Testlauf echte
    Befehle ausführt: sie speisen dann bekannte Rohdaten ein.
    """
    return SystemRunner()


@dataclass(frozen=True, slots=True)
class Tool:
    """Ein Werkzeug: Schlüssel, Beschreibung in der Sprachdatei, Messfunktion."""

    key: str
    measure: Callable[[Runner], Measurement | tuple[Measurement, ...]]

    @property
    def name(self) -> str:
        """Kurzer Name des Werkzeugs."""
        return t(f"tool_{self.key}_name")

    @property
    def description(self) -> str:
        """Was das Werkzeug nachschaut, in einem Satz."""
        return t(f"tool_{self.key}_description")


# Die Werkzeuge dieser Slice: lesen den echten Systemzustand, ändern nichts.
SYSTEM_TOOLS: tuple[Tool, ...] = (
    Tool("windows_version", system.windows_version),
    Tool("cpu", system.cpu),
    Tool("screen_resolution", system.screen_resolution),
    Tool("graphics", system.graphics),
    Tool("memory", system.memory),
    Tool("drives", system.drives),
)


class Toolbox:
    """Die Werkzeuge des Kerns, über eine gemeinsame Systemabfrage verbunden."""

    def __init__(
        self,
        runner: Runner | None = None,
        tools: Sequence[Tool] = SYSTEM_TOOLS,
    ) -> None:
        self._runner = default_runner() if runner is None else runner
        self._tools = tuple(tools)

    @property
    def tools(self) -> tuple[Tool, ...]:
        """Die Werkzeuge in der Reihenfolge, in der sie angezeigt werden."""
        return self._tools

    @property
    def runner(self) -> Runner:
        """Die benutzte Systemabfrage (für Tests und für die Quelle der Werte)."""
        return self._runner

    def measure_all(self) -> tuple[Measurement, ...]:
        """Misst alle Werkzeuge.

        Ein Werkzeug, das scheitert, liefert genau einen Messwert mit
        ``value=None`` und dem Grund; gemessen wird trotzdem weiter. Es gibt
        keinen Pfad, auf dem eine fehlgeschlagene Messung das Gespräch beendet.
        """
        results: list[Measurement] = []
        for tool in self._tools:
            try:
                outcome = tool.measure(self._runner)
            except AIHelperError as exc:
                results.append(Measurement(tool.key, None, detail=str(exc)))
                continue
            except Exception as exc:  # noqa: BLE001 - ein Werkzeug darf nie durchschlagen
                results.append(
                    Measurement(tool.key, None, detail=t("tool_unexpected", detail=repr(exc)))
                )
                continue
            results.extend(outcome if isinstance(outcome, tuple) else (outcome,))
        return tuple(results)


def build_state_section(
    measurements: Sequence[Measurement],
    tools: Sequence[Tool] = SYSTEM_TOOLS,
) -> str:
    """Der Abschnitt im Systemtext: Werkzeugliste und gemessene Werte.

    Hier stehen die Werte, aber nicht ihre Quelle: ein Anfänger muss keine
    Befehle lesen, und das Modell soll keine vorlesen. Die Quelle steht bei
    ``/nachschauen``.
    """
    lines = [t("state_tools_header")]
    for tool in tools:
        lines.append(t("state_tool_line", name=tool.name, description=tool.description))

    lines.append(t("state_values_header"))
    for measurement in measurements:
        if measurement.measurable:
            if measurement.unit:
                lines.append(
                    t(
                        "state_value_line",
                        label=measurement.label,
                        value=measurement.value,
                        unit=measurement.unit,
                    )
                )
            else:
                lines.append(
                    t(
                        "state_value_plain",
                        label=measurement.label,
                        value=measurement.value,
                    )
                )
        else:
            lines.append(
                t(
                    "state_value_missing",
                    label=measurement.label,
                    detail=measurement.detail or t("measure_no_reason"),
                )
            )

    lines.append(t("state_rule"))
    return "\n".join(lines)
