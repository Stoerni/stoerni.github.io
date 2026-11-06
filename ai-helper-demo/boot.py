"""Treiber für das AI-Helper-Demoterminal im Browser (Portfolio, Slice 60).

Diese Datei ist das Bindeglied zwischen der Seite und dem echten Kern des
AI-Helpers (``ai_helper/``, erzeugt von ``scripts/build_demo.py``). Sie wird als
``<py-script src>`` angehängt, sobald der Besucher im Modal auf „Demo starten"
klickt — dasselbe Muster wie beim Wetter-Widget (``js/pyscript-loader.js``).

Was hier passiert
=================

1. **Paket holen:** ``files.json`` lesen, jede der 40 Dateien per
   ``XMLHttpRequest`` holen, ihre SHA-256-Prüfsumme gegen das Manifest prüfen und
   sie ins Dateisystem der Seite legen (``os.makedirs``/``open``). Danach
   ``sys.path.insert`` und importieren.
2. **Demo-Hülle bauen:** ``ai_helper.ui.web.demo_shell`` — dieselbe
   Gesprächsschleife wie im Terminal, mit den drei Doppelgängern aus
   ``ai_helper/demo/`` (fester Anbieter, fester Messbericht, ein Ausführender,
   der nur Buch führt).
3. **Schrittmotor treiben:** ``start``/``feed``/``abort``/``end`` je Eingabe;
   jede fertige Ausgabezeile geht als Ereignis an die Seite.

Zwei gemessene Hürden (Slice D1) werden hier NICHT mehr angefasst:

* Kein ``await`` auf oberster Ebene — PyScript 2024.1.1 führt diese Datei mit
  ``eval_code`` aus. Alles ist **synchron**, Dateien kommen per
  ``XMLHttpRequest`` (drittes Argument ``False``).
* ``pyodide.FS`` gibt es in dieser Fassung nicht — Dateien werden mit
  gewöhnlichem ``os.makedirs``/``open`` abgelegt.

Die Seite ruft: ``window.aiHelperStart()``, ``window.aiHelperFeed(<zeile>)``,
``window.aiHelperAbort()``, ``window.aiHelperEnd()`` und
``window.aiHelperSetLanguage("de"|"en")``. Die Seite hört:
``window.aiHelperEvent(<json>)`` — Ereignisse sind ``line``, ``figure``,
``chips``, ``prompt``, ``language`` und ``fail``.

Die Sprache kommt von der **Seite** (Slice 63): ``window.portfolioLang`` bzw.
``localStorage['portfolio-lang']`` wird gelesen, **bevor** ein Kernmodul
importiert wird — sonst fröre eine beim Import gerechnete Konstante die alte
Sprache ein. Ein Sprachwechsel bei laufender Sitzung baut nichts um (sonst
stünde Englisch mitten in einem deutschen Verlauf); gemerkt wird die Sprache
für den nächsten Start („Neu starten“).

Nichts hier schickt etwas nach außen: geholt werden nur die Dateien des eigenen
Ursprungs (``files.json`` und das Paket), es gibt keinen Schlüssel und kein Netz.
"""

import hashlib
import json
import os
import sys
import traceback

from js import XMLHttpRequest, performance, window

__all__ = [
    "ROOT",
    "abbrechen",
    "beenden",
    "feed",
    "set_language",
    "start",
]

#: Wurzel des Pakets im Dateisystem der Seite.
ROOT = "/ai-helper-demo"
#: Rückfall, falls die Seite ihren Ursprung nicht mitteilt.
FALLBACK_BASE = "ai-helper-demo/"
#: Die Sprachen, die der Kern kennt (``ai_helper.i18n``).
SPRACHEN = ("de", "en")
#: Voreinstellung, wenn die Seite nichts mitteilt — Deutsch bleibt die Vorgabe.
STANDARD_SPRACHE = "de"


# --------------------------------------------------------------- Verbindung
def _basis() -> str:
    """Der Ursprung des Demo-Ordners, wie ihn die Seite gesetzt hat."""
    try:
        wert = str(window.aiHelperBase or "")
    except Exception:  # noqa: BLE001 - die Seite ist hier die einzige Quelle
        wert = ""
    return wert or FALLBACK_BASE


def _seiten_sprache() -> str:
    """Die Sprache der Seite lesen — ``window.portfolioLang``, sonst localStorage.

    Wird **vor** dem ersten Import eines Kernmoduls aufgerufen: eine Sprache,
    die erst nach dem Import gesetzt wird, kommt für beim Import gerechnete
    Texte (etwa Messberichte) zu spät.
    """
    kandidaten: list[str] = []
    try:
        kandidaten.append(str(window.portfolioLang or ""))
    except Exception:  # noqa: BLE001
        pass
    try:
        kandidaten.append(str(window.localStorage.getItem("portfolio-lang") or ""))
    except Exception:  # noqa: BLE001
        pass
    for wert in kandidaten:
        if wert in SPRACHEN:
            return wert
    return STANDARD_SPRACHE


def sprache_setzen(code: str) -> str:
    """Die Sprache des i18n-Systems setzen (ungültige Codes fallen auf Deutsch)."""
    from ai_helper.i18n import set_language as i18n_set_language

    gewaehlt = code if code in SPRACHEN else STANDARD_SPRACHE
    i18n_set_language(gewaehlt)
    return gewaehlt


def emit(ereignis: dict) -> None:
    """Ein Ereignis an die Seite schicken (das Terminal in JavaScript)."""
    try:
        window.aiHelperEvent(json.dumps(ereignis, ensure_ascii=False))
    except Exception:  # noqa: BLE001 - ein Meldefehler darf nichts abbrechen
        pass


def hole(pfad: str) -> str:
    """Eine Datei synchron vom eigenen Ursprung holen."""
    anfrage = XMLHttpRequest.new()
    anfrage.open("GET", pfad, False)
    anfrage.send()
    if anfrage.status not in (0, 200):
        raise RuntimeError(f"HTTP {anfrage.status} für {pfad}")
    return anfrage.responseText


def schreibe(pfad: str, text: str) -> None:
    """Text als Datei ablegen — Zeilenenden bleiben, wie sie ankommen (LF)."""
    ordner = pfad.rsplit("/", 1)[0]
    if ordner:
        os.makedirs(ordner, exist_ok=True)
    with open(pfad, "w", encoding="utf-8", newline="\n") as datei:
        datei.write(text)


def installiere(basis: str) -> dict:
    """Das Paket aus ``files.json`` holen, prüfen und ablegen.

    Die Prüfsumme ist derselbe Torwächter wie ``--pruefen`` auf der
    Kommandozeile: eine von Hand geänderte Datei hält hier an, mit klarer
    Meldung, statt still etwas anderes auszuführen.
    """
    manifest = json.loads(hole(basis + "files.json"))
    dateien = list(manifest.get("files") or [])
    pruefsummen = dict(manifest.get("checksums") or {})
    falsch: list[str] = []
    bytes_geladen = 0

    for relativ in dateien:
        text = hole(basis + relativ)
        bytes_geladen += len(text.encode("utf-8"))
        ist = "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()
        if pruefsummen.get(relativ) not in (None, ist):
            falsch.append(relativ)
            continue
        schreibe(f"{ROOT}/{relativ}", text)

    if falsch:
        raise RuntimeError(
            "Die Prüfsumme stimmt nicht (das Paket wurde von Hand geändert): "
            + ", ".join(falsch)
        )
    if not dateien:
        raise RuntimeError("Das Manifest nennt keine Dateien.")

    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    return {"dateien": len(dateien), "bytes": bytes_geladen}


# ------------------------------------------------------------ Ausgabe-Weg
def _label_zu_zustand() -> dict:
    """Die Beschriftungen der Figur → ihre Zustände (aus der Sprachdatei)."""
    from ai_helper.avatar import AvatarState
    from ai_helper.i18n import t

    return {t(f"avatar_{zustand.value}"): zustand for zustand in AvatarState}


class Ausgabe:
    """Macht aus den Zeilen der Schleife Ereignisse für die Seite.

    Zwei Sorten kommen getrennt an:

    * gewöhnliche Zeilen → ``{"t": "line", "text": …}``
    * die Figur — Beschriftung **und** vier Zeilen Textgrafik — → die
      Beschriftung bleibt eine Zeile, die vier Zeichenzeilen werden zu
      ``{"t": "figure", …}`` (die Figur steht auf der Seite neben der Ausgabe).

    Die Erkennung ist streng: die vier folgenden Zeilen müssen **zeichengleich**
    das Gesicht dieses Zustands sein (``ai_helper.avatar.render``). Passt die
    Annahme nicht, bleiben die Zeilen gewöhnliche Ausgabezeilen — es geht keine
    Zeile verloren.
    """

    def __init__(self) -> None:
        from ai_helper.avatar import FACES

        self._gesichter = {zustand: tuple(FACES[zustand]) for zustand in FACES}
        # Zwei Richtungen: Beschriftung → Zustand (Erkennung) und
        # Zustand → Beschriftung (für das Ereignis an die Seite).
        self._labels = _label_zu_zustand()
        self._texte = {zustand: text for text, zustand in self._labels.items()}
        self._kandidat = None
        self._puffer: list[str] = []

    def zeile(self, text: str) -> None:
        """Eine fertige Zeile der Schleife annehmen."""
        if self._kandidat is None:
            zustand = self._labels.get(text)
            if zustand is None:
                emit({"t": "line", "text": text})
            else:
                # Beschriftung zeigen und auf das Gesicht warten.
                self._kandidat = zustand
                self._puffer = []
                emit({"t": "line", "text": text})
            return

        self._puffer.append(text)
        if len(self._puffer) < len(self._gesichter[self._kandidat]):
            return

        zustand = self._kandidat
        zeilen = tuple(self._puffer)
        self._kandidat = None
        self._puffer = []
        if zeilen == self._gesichter[zustand]:
            aufruf = self._texte[zustand]
            emit(
                {
                    "t": "figure",
                    "state": zustand.value,
                    "label": aufruf,
                    "face": list(zeilen),
                }
            )
        else:
            for zeile in zeilen:
                emit({"t": "line", "text": zeile})

    def flush(self) -> None:
        """Angefangene Zeilen ausgeben — es darf nichts im Puffer hängen bleiben."""
        if self._kandidat is None:
            return
        zeilen = self._puffer
        self._kandidat = None
        self._puffer = []
        for zeile in zeilen:
            emit({"t": "line", "text": zeile})


# ----------------------------------------------------------------- Treiber
_ausgabe: Ausgabe | None = None
_schleife = None
#: Die Sprache, in der die nächste Sitzung aufgebaut wird (von der Seite).
_sprache = STANDARD_SPRACHE


def _neu() -> None:
    """Eine frische Demo-Sitzung aufbauen (Anbieter, Bericht, Ausführender).

    Die Sprache wird **vor** dem Bauen gesetzt: ``demo_shell`` rechnet die
    Beschriftungen der Figur und den Demo-Bericht mit ``t()``, und die
    Schleife soll in genau der Sprache starten, die die Seite zeigt.
    """
    global _ausgabe, _schleife

    sprache_setzen(_sprache)
    from ai_helper.ui.web import LineCollector, demo_shell

    _ausgabe = Ausgabe()
    _schleife = demo_shell(
        collector=LineCollector(on_line=_ausgabe.zeile),
        language=_sprache,
    )


def _lage() -> None:
    """Der Seite sagen, wo das Gespräch steht (Aufforderung, läuft es noch?)."""
    if _schleife is None:
        return
    laeuft = bool(_schleife.laeuft)
    frage = getattr(_schleife, "frage", None)
    emit(
        {
            "t": "prompt",
            "text": str(frage.prompt) if (laeuft and frage is not None) else "",
            "running": laeuft,
            "code": _schleife.exit_code,
        }
    )


def _schritt(aktion) -> None:
    """Einen Schritt der Schleife fahren und danach die Lage melden."""
    if _ausgabe is None:
        return
    try:
        aktion()
    except BaseException as fehler:  # noqa: BLE001 - der Fehler ist der Befund
        _ausgabe.flush()
        kurz = traceback.format_exc().splitlines()[-1]
        emit({"t": "line", "text": f"⚠️ {kurz}"})
        try:
            window.console.error(f"AI-Helper-Demo: {kurz}")
        except Exception:  # noqa: BLE001
            pass
    finally:
        _ausgabe.flush()
        _lage()


def start() -> None:
    """Die Sitzung beginnen: Demo-Hinweis, Begrüßung, erste Aufforderung."""
    if _schleife is None or not _schleife.laeuft:
        _neu()

    from ai_helper.i18n import t

    emit({"t": "line", "text": t("demo_hint")})
    emit({"t": "line", "text": ""})
    _schritt(_schleife.start)
    _vorschlaege()


def _vorschlaege() -> None:
    """Die sprachabhängigen Vorschläge (Chips) neu an die Seite schicken."""
    try:
        from ai_helper.demo import suggestions

        emit({"t": "chips", "items": list(suggestions())})
    except Exception:  # noqa: BLE001 - Vorschläge sind Beiwerk, kein Fehler
        pass


def feed(zeile) -> None:
    """Eine Eingabezeile des Besuchers verarbeiten."""
    if _schleife is None or not _schleife.laeuft:
        return
    _schritt(lambda: _schleife.feed(str(zeile)))


def abbrechen() -> None:
    """Escape bzw. der Abbrechen-Knopf: das Gespräch ruhig beenden."""
    if _schleife is None or not _schleife.laeuft:
        return
    _schritt(_schleife.abort)


def beenden() -> None:
    """Das Ende der Eingabe (wie Strg-D): verabschieden und beenden."""
    if _schleife is None or not _schleife.laeuft:
        return
    _schritt(_schleife.end)


def set_language(language: str) -> None:
    """Die Sprache der Seite übernehmen und der Seite melden, wie es steht.

    Zwei Lagen (Slice 63):

    * **Keine laufende Sitzung** — die Sprache wird gesetzt und die
      Vorschläge neu geschickt; der nächste Start läuft in der neuen Sprache.
    * **Laufende Sitzung** — es wird **nichts** umgebaut: das i18n-System
      bleibt, wie es ist, sonst stünden englische Antworten in einem deutschen
      Verlauf. Die Sprache wird nur für den nächsten Start gemerkt; die Seite
      zeigt dazu einen Hinweis („Neu starten“).

    Die Seite erfährt das Ergebnis über das Ereignis ``language``
    (``code`` und ``running``).
    """
    global _sprache

    gewaehlt = language if language in SPRACHEN else STANDARD_SPRACHE
    _sprache = gewaehlt
    laeuft = bool(_schleife is not None and _schleife.laeuft)
    if not laeuft:
        sprache_setzen(gewaehlt)
        _vorschlaege()
    emit({"t": "language", "code": gewaehlt, "running": laeuft})


# ------------------------------------------------------------------- Start
def _vorbereiten() -> None:
    """Paket installieren und die Funktionen für die Seite bereitstellen.

    Die Sprache wird **vor** dem ersten Kernimport gesetzt (Slice 63): Texte,
    die beim Import gerechnet werden, stünden sonst dauerhaft in der alten
    Sprache.
    """
    global _sprache

    beginn = performance.now()
    basis = _basis()
    bericht = installiere(basis)

    _sprache = sprache_setzen(_seiten_sprache())

    window.aiHelperStart = start
    window.aiHelperFeed = feed
    window.aiHelperAbort = abbrechen
    window.aiHelperEnd = beenden
    window.aiHelperSetLanguage = set_language

    emit(
        {
            "t": "ready",
            "files": bericht["dateien"],
            "bytes": bericht["bytes"],
            "seconds": round((performance.now() - beginn) / 1000.0, 2),
            "language": _sprache,
        }
    )


try:
    _vorbereiten()
except BaseException as _fehler:  # noqa: BLE001 - jeder Fehler ist hier ein Befund
    emit(
        {
            "t": "fail",
            "text": f"{type(_fehler).__name__}: {_fehler}",
        }
    )
