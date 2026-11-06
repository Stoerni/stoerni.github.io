# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""The fixed measurement report of the demo — explicitly marked as demo.

In the browser there is no Windows: no registry, no CIM, no process
start. The demo therefore measures **nothing**. It shows the visitor a
**fixed report**, and every value carries as source the notice that it is
not measured but fixed (``demo_measure_source``). A fixed value pretending
to be a measurement would violate Decision 9 ("measured values instead of
guesses") — hence the notice on every value.

``DemoToolbox`` sits at the same seam as ``Toolbox``: the shell calls
``measure_all()`` and gets values; it doesn't know where they come from.
The ``DemoRunner`` behind it executes nothing (it fails like a blind
doubleganger) — so no real command can run even by accident.
"""

from __future__ import annotations

from collections.abc import Sequence

from ai_helper.i18n import format_number, t
from ai_helper.tools import SYSTEM_TOOLS, Toolbox, ToolUnavailable
from ai_helper.tools.measurement import Measurement

__all__ = [
    "DEMO_MEASUREMENTS",
    "DemoRunner",
    "DemoToolbox",
    "demo_report",
]


def _build_demo_measurements() -> tuple[Measurement, ...]:
    """Build the fixed demo report fresh on each call.

    Decimal values are stored as floats; formatting with the correct decimal
    separator (comma for German, dot for English) is done via the i18n
    system using the ``value_gb`` and ``value_pixel`` keys.
    """
    return (
        Measurement("windows_version", "10.0.26100.1742", source=t("demo_measure_source")),
        Measurement("windows_edition", "Microsoft Windows 11 Pro", source=t("demo_measure_source")),
        Measurement("cpu", "AMD Ryzen 5 7530U with Radeon Graphics", source=t("demo_measure_source")),
        Measurement(
            "cpu_cores",
            t("value_cpu_cores", cores=6, threads=12),
            source=t("demo_measure_source"),
        ),
        Measurement(
            "screen_resolution",
            "1920 x 1080",
            unit=t("value_pixel"),
            source=t("demo_measure_source"),
        ),
        Measurement("graphics", "AMD Radeon (TM) Graphics", source=t("demo_measure_source")),
        Measurement(
            "memory_total",
            format_number(15.3),
            unit=t("value_gb"),
            source=t("demo_measure_source"),
        ),
        Measurement(
            "memory_free",
            format_number(7.1),
            unit=t("value_gb"),
            source=t("demo_measure_source"),
        ),
        Measurement(
            "drive_total",
            format_number(475.9),
            unit=t("value_gb"),
            source=t("demo_measure_source"),
            params=(("drive", "C:"),),
        ),
        Measurement(
            "drive_free",
            format_number(312.4),
            unit=t("value_gb"),
            source=t("demo_measure_source"),
            params=(("drive", "C:"),),
        ),
    )


# Backwards-compatible constant — a tuple built once at import time.
DEMO_MEASUREMENTS: tuple[Measurement, ...] = _build_demo_measurements()


def demo_report() -> tuple[Measurement, ...]:
    """The fixed demo measurement report (a fresh copy on every call)."""
    return _build_demo_measurements()


class DemoRunner:
    """A system query that can do nothing — like a blind doubleganger.

    It sits under the ``DemoToolbox`` so that no real command is possible.
    It is never called in operation (the toolbox delivers the fixed report),
    but if it were, it fails with a German message instead of executing
    anything.
    """

    def __init__(self) -> None:
        self.commands: list[list[str]] = []

    def run(self, command: Sequence[str]) -> str:
        self.commands.append([str(part) for part in command])
        raise ToolUnavailable(t("demo_runner_unavailable"))


class DemoToolbox(Toolbox):
    """The demo toolbox with a fixed report instead of real measurement.

    It uses the same tool names as real operation (for the tool section in
    the system prompt), but measures nothing: ``measure_all`` delivers the
    fixed report from ``demo_report()`` (built fresh with current language).
    """

    def __init__(self, tools: Sequence = SYSTEM_TOOLS) -> None:
        # ``runner=DemoRunner()`` instead of the default: this way **no**
        # ``SystemRunner`` is created and the default swap point
        # (``default_runner``) is never touched.
        super().__init__(runner=DemoRunner(), tools=tools)

    def measure_all(self) -> tuple[Measurement, ...]:
        """The fixed report — built fresh on each call with current language."""
        return demo_report()
