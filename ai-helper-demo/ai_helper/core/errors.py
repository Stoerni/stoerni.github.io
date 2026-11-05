# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Fehlerklassen des Kerns.

Die Meldung (``str(error)``) ist immer schon der fertige Text in der
gewählten Sprache. Die Hülle gibt sie aus, sie muss nichts übersetzen.
"""

from __future__ import annotations


class AIHelperError(Exception):
    """Basisklasse aller Fehler, die dem Nutzer verständlich gemeldet werden."""


class ConfigurationError(AIHelperError):
    """Die Einstellungen reichen nicht aus (z.B. Schlüssel oder Modell fehlt)."""


class ProviderError(AIHelperError):
    """Der Anbieter hat nicht brauchbar geantwortet."""


class MemoryStorageError(AIHelperError):
    """Das Gedächtnis auf der Platte ist kaputt oder nicht beschreibbar.

    Die Meldung nennt den Pfad und den Grund und ist für den Nutzer gedacht;
    ein kaputter Speicher ist ausdrücklich kein Absturz.
    """


class ActionError(AIHelperError):
    """Eine Aktion ließ sich nicht prüfen, ausführen oder zurücknehmen.

    Die Meldung ist fertig deutsch und nennt den Grund; die Hülle gibt sie nur
    aus. Eine gescheiterte Aktion beendet das Gespräch nie.
    """


class LogStorageError(AIHelperError):
    """Das Protokoll auf der Platte ist kaputt oder nicht beschreibbar.

    Wie beim Gedächtnis: die Datei bleibt liegen, das Gespräch läuft weiter,
    aber ohne Protokoll wird nichts ausgeführt (Entscheidung 5).
    """
