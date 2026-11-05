# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Die Werkzeuge, die den echten Systemzustand lesen.

Jedes Werkzeug holt seine Rohdaten über die Systemabfrage (``runner.py``) und
übersetzt sie in Messwerte. Der Kern kennt nur diese Funktionen, nicht die
Befehle dahinter: welche Befehle es sind, steht in ``*_COMMAND`` und wird als
Quelle ``*_SOURCE`` mitgeliefert.

Alle Werkzeuge lesen nur. Es gibt hier keinen Befehl, der etwas installiert,
ändert oder löscht, und keinen, der Administratorrechte braucht
(Entscheidung 10).

Die Rohdaten werden nicht geprüft, ob sie plausibel wirken: was der Befehl
ausgibt, wird übernommen; was er nicht ausgibt, wird als nicht messbar
gemeldet. Erfunden wird nichts.
"""

from __future__ import annotations

import re

from ai_helper.i18n import t
from ai_helper.tools.measurement import Measurement
from ai_helper.tools.runner import Runner, ToolUnavailable, command_text

__all__ = [
    "CPU_COMMAND",
    "CPU_SOURCE",
    "DRIVES_COMMAND",
    "DRIVES_SOURCE",
    "GRAPHICS_COMMAND",
    "GRAPHICS_SOURCE",
    "MEMORY_COMMAND",
    "MEMORY_SOURCE",
    "SCREEN_COMMAND",
    "SCREEN_SOURCE",
    "WINDOWS_EDITION_COMMAND",
    "WINDOWS_EDITION_SOURCE",
    "WINDOWS_VERSION_COMMAND",
    "WINDOWS_VERSION_SOURCE",
    "cpu",
    "drives",
    "graphics",
    "memory",
    "screen_resolution",
    "windows_version",
]

# --- Die Befehle ---------------------------------------------------------
# Nur lesende Abfragen. PowerShell wird ohne Profil und ohne Rückfragen
# gestartet; die Eigenschaftsnamen von Get-CimInstance sind englisch und
# damit unabhängig von der Anzeigesprache des Rechners.

WINDOWS_VERSION_COMMAND = ("cmd", "/c", "ver")
WINDOWS_VERSION_SOURCE = command_text(WINDOWS_VERSION_COMMAND)

WINDOWS_EDITION_COMMAND = (
    "powershell",
    "-NoProfile",
    "-NonInteractive",
    "-Command",
    "Get-CimInstance Win32_OperatingSystem | Select-Object -ExpandProperty Caption",
)
# Bewusst nicht die Registry (ProductName): auf einem von Windows 10
# hochgezogenen Windows 11 steht dort bis heute "Windows 10 ...". Am
# Entwicklungsrechner nachgemessen: ProductName sagt "Windows 10 Education",
# während die Build-Nummer 26300 und Caption "Microsoft Windows 11 Education"
# sagen. Gemessen wird deshalb der Caption-Wert.
WINDOWS_EDITION_SOURCE = "PowerShell: Get-CimInstance Win32_OperatingSystem (Caption)"

SCREEN_COMMAND = (
    "powershell",
    "-NoProfile",
    "-NonInteractive",
    "-Command",
    'Get-CimInstance Win32_VideoController | Where-Object { $_.CurrentHorizontalResolution } | '
    'Select-Object -First 1 | ForEach-Object { "$($_.CurrentHorizontalResolution)x$($_.CurrentVerticalResolution)" }',
)
SCREEN_SOURCE = "PowerShell: Get-CimInstance Win32_VideoController"

GRAPHICS_COMMAND = (
    "powershell",
    "-NoProfile",
    "-NonInteractive",
    "-Command",
    "$n = Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name; $n -join '; '",
)
GRAPHICS_SOURCE = "PowerShell: Get-CimInstance Win32_VideoController (Name)"

MEMORY_COMMAND = (
    "powershell",
    "-NoProfile",
    "-NonInteractive",
    "-Command",
    '$cs = Get-CimInstance Win32_ComputerSystem; $os = Get-CimInstance Win32_OperatingSystem; '
    '"$($cs.TotalPhysicalMemory)|$($os.FreePhysicalMemory)"',
)
MEMORY_SOURCE = "PowerShell: Get-CimInstance Win32_ComputerSystem / Win32_OperatingSystem"

# Der Prozessor: Name, Kerne und die Anzahl der gleichzeitig rechenbaren Fäden.
# `MaxClockSpeed` steht bewusst **nicht** im Befehl: das ist der zugesicherte
# Höchstwert, nicht der gerade anliegende Takt — als nackte Zahl wäre „2,0 GHz"
# eine falsche Aussage über den laufenden Rechner (Slice 11, Entscheidung 3).
#
# `-Property` ist hier **kein** Zierrat: `Win32_Processor` hat sehr viele
# Eigenschaften, und sie alle zu holen kostet gemessene 1,32 s statt 0,28 s
# (am 2026-11-03 auf diesem Rechner, je drei Läufe). Die übrigen CIM-Abfragen
# gewinnen damit nichts (0,28–0,34 s vorher wie nachher), dort bleibt es beim
# Vollzugriff.
CPU_COMMAND = (
    "powershell",
    "-NoProfile",
    "-NonInteractive",
    "-Command",
    "$p = Get-CimInstance -ClassName Win32_Processor "
    "-Property Name,NumberOfCores,NumberOfLogicalProcessors | Select-Object -First 1; "
    '"$($p.Name)|$($p.NumberOfCores)|$($p.NumberOfLogicalProcessors)"',
)
CPU_SOURCE = "PowerShell: Get-CimInstance Win32_Processor (Name, Kerne)"

DRIVES_COMMAND = (
    "powershell",
    "-NoProfile",
    "-NonInteractive",
    "-Command",
    'Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | '
    'ForEach-Object { "$($_.DeviceID)|$($_.Size)|$($_.FreeSpace)" }',
)
DRIVES_SOURCE = "PowerShell: Get-CimInstance Win32_LogicalDisk"

# --- Auswertung der Rohdaten ---------------------------------------------

_VERSION_RE = re.compile(r"Version\s+(\d+(?:\.\d+)+)")
_RESOLUTION_RE = re.compile(r"(\d{3,5})\s*x\s*(\d{3,5})")

_BYTES_PER_GIB = 1024**3
_BYTES_PER_KIB = 1024


def _first_line(output: str) -> str:
    """Die erste nicht leere Zeile, gekürzt — für Fehlermeldungen."""
    for line in output.splitlines():
        if line.strip():
            return line.strip()[:120]
    return "-"


def _german(number: float, digits: int = 1) -> str:
    """Eine Zahl mit deutschem Dezimalkomma, so wie sie hier gelesen wird."""
    return f"{number:.{digits}f}".replace(".", ",")


def _gigabytes(raw: str, *, allow_zero: bool, factor: float = 1.0) -> str | None:
    """Einen Rohwert in GB umrechnen. ``None`` heißt: nicht verwertbar.

    ``factor`` rechnet die Einheit des Rohwerts um (Byte = 1, Kilobyte = 1024).
    ``allow_zero`` unterscheidet die beiden Fälle: "0 Byte Größe" ist keine
    Größe (nicht messbar), "0 Byte frei" dagegen eine echte Messung (Laufwerk
    voll).
    """
    try:
        number = float(raw) * factor
    except (TypeError, ValueError):
        return None
    if number < 0 or (number == 0 and not allow_zero):
        return None
    return _german(number / _BYTES_PER_GIB)


def _cpu_cores_line(raw_cores: str, raw_threads: str) -> str | None:
    """„6 Kerne (12 gleichzeitig)" aus den beiden Rohzahlen.

    Beide Zahlen müssen da und größer als null sein: aus einer allein lässt sich
    kein ehrlicher Satz bauen, und „0 Kerne" ist keine Messung, sondern eine
    kaputte Ausgabe. Dann ist der Wert nicht messbar (``None``).
    """
    try:
        cores = int(raw_cores)
        threads = int(raw_threads)
    except (TypeError, ValueError):
        return None
    if cores <= 0 or threads <= 0:
        return None
    if cores == 1:
        return t("value_cpu_cores_single", threads=threads)
    return t("value_cpu_cores", cores=cores, threads=threads)


# --- Die Werkzeuge -------------------------------------------------------


def windows_version(runner: Runner) -> tuple[Measurement, Measurement]:
    """Welche Windows-Version installiert ist und welche Ausgabe."""
    version_output = runner.run(WINDOWS_VERSION_COMMAND)
    version_match = _VERSION_RE.search(version_output)
    version = Measurement(
        "windows_version",
        version_match.group(1) if version_match else None,
        source=WINDOWS_VERSION_SOURCE,
        detail=None if version_match else t("tool_unreadable", output=_first_line(version_output)),
    )

    edition_output = runner.run(WINDOWS_EDITION_COMMAND).strip()
    edition = Measurement(
        "windows_edition",
        edition_output or None,
        source=WINDOWS_EDITION_SOURCE,
        detail=None if edition_output else t("tool_no_output"),
    )
    return (version, edition)


def cpu(runner: Runner) -> tuple[Measurement, Measurement]:
    """Welcher Prozessor im Rechner steckt und wie viele Kerne er hat.

    Zwei Werte aus einem Befehl: der Name (die Antwort auf „was für eine CPU
    habe ich?") und die Kerne in einem Satz, den ein Anfänger versteht. Der Takt
    wird nicht gemessen — siehe ``CPU_COMMAND``.
    """
    output = runner.run(CPU_COMMAND)
    parts = [part.strip() for part in output.strip().split("|")]
    if len(parts) < 3:
        raise ToolUnavailable(t("tool_no_output"))

    name, raw_cores, raw_threads = parts[0], parts[1], parts[2]
    kerne = _cpu_cores_line(raw_cores, raw_threads)
    return (
        Measurement(
            "cpu",
            name or None,
            source=CPU_SOURCE,
            detail=None if name else t("tool_no_value"),
        ),
        Measurement(
            "cpu_cores",
            kerne,
            source=CPU_SOURCE,
            detail=None if kerne else t("tool_no_value"),
        ),
    )


def screen_resolution(runner: Runner) -> Measurement:
    """Wie groß der Bildschirm gerade eingestellt ist."""
    output = runner.run(SCREEN_COMMAND)
    match = _RESOLUTION_RE.search(output)
    if not match:
        return Measurement(
            "screen_resolution",
            None,
            source=SCREEN_SOURCE,
            detail=t("tool_unreadable", output=_first_line(output)),
        )
    return Measurement(
        "screen_resolution",
        f"{match.group(1)} x {match.group(2)}",
        unit=t("value_pixel"),
        source=SCREEN_SOURCE,
    )


def graphics(runner: Runner) -> Measurement:
    """Welcher Grafik-Chip im Rechner steckt."""
    output = runner.run(GRAPHICS_COMMAND).strip()
    if not output:
        return Measurement(
            "graphics", None, source=GRAPHICS_SOURCE, detail=t("tool_no_output")
        )
    return Measurement("graphics", output, source=GRAPHICS_SOURCE)


def memory(runner: Runner) -> tuple[Measurement, Measurement]:
    """Wie viel Arbeitsspeicher vorhanden ist und wie viel gerade frei ist."""
    output = runner.run(MEMORY_COMMAND)
    parts = [part.strip() for part in output.strip().split("|")]
    if len(parts) < 2:
        raise ToolUnavailable(t("tool_no_output"))

    # TotalPhysicalMemory kommt in Byte, FreePhysicalMemory in Kilobyte.
    total = _gigabytes(parts[0], allow_zero=False)
    free = _gigabytes(parts[1], allow_zero=True, factor=_BYTES_PER_KIB)
    return (
        Measurement(
            "memory_total",
            total,
            unit=t("value_gb"),
            source=MEMORY_SOURCE,
            detail=None if total is not None else t("tool_no_value"),
        ),
        Measurement(
            "memory_free",
            free,
            unit=t("value_gb"),
            source=MEMORY_SOURCE,
            detail=None if free is not None else t("tool_no_value"),
        ),
    )


def drives(runner: Runner) -> Measurement | tuple[Measurement, ...]:
    """Welche Laufwerke es gibt, wie groß sie sind und wie viel frei ist."""
    output = runner.run(DRIVES_COMMAND)
    measurements: list[Measurement] = []
    for raw_line in output.splitlines():
        parts = [part.strip() for part in raw_line.strip().split("|")]
        if len(parts) != 3:
            continue
        letter, raw_size, raw_free = parts
        if not letter:
            continue
        size = _gigabytes(raw_size, allow_zero=False)
        free = _gigabytes(raw_free, allow_zero=True)
        for key, value in (("drive_total", size), ("drive_free", free)):
            measurements.append(
                Measurement(
                    key,
                    value,
                    unit=t("value_gb"),
                    source=DRIVES_SOURCE,
                    detail=None if value is not None else t("tool_no_value"),
                    params=(("drive", letter),),
                )
            )

    if not measurements:
        return Measurement(
            "drives", None, source=DRIVES_SOURCE, detail=t("tool_no_drives")
        )
    return tuple(measurements)
