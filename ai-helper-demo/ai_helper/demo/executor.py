# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Der Demo-Ausführende: schreibt ins Protokoll, führt nichts aus.

Aktionen dürfen in der Demo **sichtbar** sein — Vorschau, Rückfrage, ja/nein,
Protokoll und Rücknahme sollen genau wie im echten Betrieb ablaufen. Nur eines
darf nicht passieren: dass wirklich etwas am Rechner des Besuchers geändert
wird. Im Browser gäbe es ohnehin keine Registry und keinen Prozessstart.

``DemoExecutor`` sitzt an derselben Naht wie der echte ``SystemExecutor``
(``ai_helper/actions/executor.py``): er hat ein ``run(command)``. Er **merkt
sich** den Befehl (damit ``/protokoll`` und die Prüfung so tun können, als sei
etwas geschehen) und **antwortet** mit einem festen Demo-Wert — doch er ruft
nichts auf. Kein ``subprocess``, kein Netz, keine Datei.

Ein Test weist das nach: mit einem Wächter auf ``subprocess.run`` läuft ein
ganzer Aktionsweg (prüfen, anwenden, zurücknehmen) durch, ohne dass der Wächter
je auslöst.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence

from ai_helper.actions.catalog import NOT_SET

__all__ = ["DEMO_ANSWERS", "DemoExecutor"]


# Der Zustand des Demo-Rechners, wie ihn eine Abfrage liefern würde. Die
# Stichwörter entsprechen den Wertnamen aus dem Katalog (``catalog.py``): die
# Lesebefehle tragen ``-Name <Wert>``, der Ton ``Stumm()``, Schreibbefehle
# ``/v `` (reg) bzw. ``SetzeStumm``. Die Werte sind so gewählt, dass die
# meisten Aktionen noch etwas zu tun haben — eine Demo, in der alles schon
# eingestellt ist, zeigt den Weg nicht.
DEMO_ANSWERS: dict[str, str] = {
    "-Name HideFileExt": "1",
    "-Name Hidden": "2",
    "-Name ShowRecent": NOT_SET,
    "-Name ShowSecondsInSystemClock": NOT_SET,
    "-Name AppsUseLightTheme": "1",
    "-Name TextScaleFactor": NOT_SET,
    "-Name MouseSensitivity": "10",
    "-Name MenuShowDelay": "400",
    "-Name SubscribedContent-338388Enabled": NOT_SET,
    "Stumm()": "0",
    "SetzeStumm": "",
    "/v ": "",
}


class DemoExecutor:
    """Führt nichts aus: merkt sich den Befehl und antwortet mit einem Demo-Wert."""

    def __init__(self, answers: Mapping[str, str] | None = None) -> None:
        self.answers: dict[str, str] = dict(DEMO_ANSWERS if answers is None else answers)
        # Jeder Befehl wird mitgeschrieben — damit lässt sich belegen, dass der
        # Demo-Ausführende gar nichts anderes tut, als Buch zu führen.
        self.commands: list[list[str]] = []

    def run(self, command: Sequence[str]) -> str:
        """Merkt sich den Befehl und liefert einen festen Demo-Wert.

        Es wird **nichts** aufgerufen. Ein unbekannter Befehl ergibt den leeren
        Text (die Demo tut so, als sei dazu nichts eingestellt) — statt zu
        scheitern, damit das Gespräch im Portfolio nie stockt.
        """
        argv = [str(teil) for teil in command]
        self.commands.append(argv)
        joined = " ".join(argv)
        for needle, output in self.answers.items():
            if needle in joined:
                return output
        return ""

    def schreibbefehle(self) -> list[str]:
        """Die Befehle, die **etwas ändern würden** — hier nur Buchführung.

        Für Tests und die Anzeige: ``reg add``/``reg delete`` und das Stumm-
        Schalten des Tons. Am Rechner des Besuchers passiert dabei nichts.
        """
        return [
            " ".join(argv)
            for argv in self.commands
            if argv and (argv[0] == "reg" or any("SetzeStumm" in teil for teil in argv))
        ]
