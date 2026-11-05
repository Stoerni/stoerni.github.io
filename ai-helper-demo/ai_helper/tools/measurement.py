# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Ein gemessener Wert: Name, Wert, Einheit und Quelle.

Der Avatar spricht über den Rechner nur mit gemessenen Werten (Entscheidung 9),
nie mit Vermutungen. Deshalb trägt ein Messwert mehr als eine Zahl: seinen
Namen, die Einheit und die Quelle der Messung. Konnte etwas nicht gemessen
werden, steht das da: ``value`` ist dann ``None`` und ``detail`` nennt den
Grund. Geschätzt oder aufgefüllt wird nichts.

Der Name des Wertes ist ein Schlüssel in der Sprachdatei (``measure_<key>``),
damit eine zweite Sprache nur Texte ergänzen muss (Entscheidung 7).
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

from ai_helper.i18n import t

__all__ = ["Measurement", "describe"]


@dataclass(frozen=True, slots=True)
class Measurement:
    """Ein einzelner gemessener Wert."""

    key: str
    value: str | None
    unit: str | None = None
    source: str = ""
    detail: str | None = None
    params: tuple[tuple[str, str], ...] = ()

    @property
    def label(self) -> str:
        """Der Name des Wertes in der eingestellten Sprache."""
        return t(f"measure_{self.key}", **dict(self.params))

    @property
    def measurable(self) -> bool:
        """Wurde wirklich gemessen?"""
        return self.value is not None

    def line(self) -> str:
        """Die eine Zeile, die den Wert im Klartext zeigt."""
        if not self.measurable:
            return t(
                "measure_unmeasurable",
                label=self.label,
                detail=self.detail or t("measure_no_reason"),
            )
        if self.unit:
            return t("measure_line", label=self.label, value=self.value, unit=self.unit)
        return t("measure_line_plain", label=self.label, value=self.value)

    def source_line(self) -> str | None:
        """Woher der Wert kommt, oder ``None``, wenn es nichts zu nennen gibt."""
        return t("measure_source", source=self.source) if self.source else None


def describe(measurements: Sequence[Measurement]) -> tuple[str, ...]:
    """Werte samt Quelle als Zeilen, für die Anzeige im Terminal."""
    lines: list[str] = []
    for measurement in measurements:
        lines.append(measurement.line())
        source = measurement.source_line()
        if source is not None:
            lines.append(source)
    return tuple(lines)
