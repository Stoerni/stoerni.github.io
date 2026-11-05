# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Der Aktionskatalog: die Aktionen, die es wirklich gibt.

Entscheidung 6 im Design-Dokument: das Modell wählt ausschließlich aus diesem
Katalog und erfindet nie einen eigenen Befehl. Jeder Eintrag bringt seine
Befehle selbst mit; sie stehen hier im Code, nicht in einer Antwort des Modells
und nicht in einer Einstellung.

Die Aktionen ändern Einstellungen des angemeldeten Nutzers (``HKCU``). Das ist
Absicht:

* **keine Administratorrechte** — alles liegt unter ``HKEY_CURRENT_USER``; was
  Rechte braucht, wird nicht ausgeführt, sondern nur angekündigt
  (Entscheidung 10, siehe ``handover_action``),
* **rücknehmbar** — jede Aktion merkt sich den Wert, der vorher dastand, und
  die Rücknahme schreibt genau diesen Wert zurück. War vorher nichts
  eingestellt, wird der Wert wieder entfernt (statt einen Wert zu schreiben,
  den es nie gab),
* **risikolos** — es sind Darstellungs- und Bedienungseinstellungen; keine
  Datei, kein Programm, kein Netz, kein Laufwerk wird angefasst.

Gelesen wird über PowerShell, geschrieben über ``reg``. Grund: ``reg query``
meldet einen nicht gesetzten Wert als Fehler, und zwar in der Sprache des
Rechners — daraus ließe sich nicht unterscheiden, ob nichts eingestellt ist oder
ob das Lesen nicht erlaubt war. Der Lesebefehl liefert stattdessen einen
Sentinel und endet immer mit Erfolg (am 2026-11-03 auf einem deutschen
Windows 11 nachgemessen).

Der Werttyp steht seit Slice 7 **im Eintrag** und nicht mehr im Befehl
(Offener Punkt 45): ``REG_DWORD`` für Schalter und Zahlen, ``REG_SZ`` für die
Werte, die Windows dort als Zeichenkette führt (etwa die Mausgeschwindigkeit).

Der Ton-Eintrag ist der einzige, der nicht in der Registry steht: die
Lautstärke liegt in der Audio-Schnittstelle von Windows, nicht in einem
Schlüssel. Er liest und schreibt sie über PowerShell mit einem kleinen
C#-Block (``Add-Type``), also **ohne Zusatzpaket** — am 2026-11-03 auf diesem
Rechner gemessen: 0,33 bis 0,36 s je Aufruf, Lesen und Schreiben belegt.
"""

from __future__ import annotations

from collections.abc import Sequence

from ai_helper.actions.action import BASE_TEXTS, HANDOVER_TEXTS, UNSET_TEXT, Action, ActionState
from ai_helper.actions.executor import Executor
from ai_helper.core.errors import ActionError
from ai_helper.i18n import t

__all__ = [
    "ACCESSIBILITY",
    "CONTENT_DELIVERY",
    "CONTROL_PANEL_DESKTOP",
    "CONTROL_PANEL_MOUSE",
    "DWORD",
    "EXPLORER_ADVANCED",
    "MUTED",
    "NOT_SET",
    "SZ",
    "SYSTEM_ACTIONS",
    "THEMES_PERSONALIZE",
    "UNMUTED",
    "build_actions_section",
    "build_learn_section",
    "delete_command",
    "grouped_actions",
    "handover_action",
    "read_command",
    "read_value",
    "registry_action",
    "restore_value",
    "sound_action",
    "sound_read_command",
    "sound_write_command",
    "write_command",
    "write_value",
]

# Die Einstellungen liegen unter dem angemeldeten Nutzer — deshalb braucht keine
# Aktion Administratorrechte.
HIVE = "HKCU"
EXPLORER_ADVANCED = r"Software\Microsoft\Windows\CurrentVersion\Explorer\Advanced"
THEMES_PERSONALIZE = r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize"
ACCESSIBILITY = r"Software\Microsoft\Accessibility"
CONTENT_DELIVERY = r"Software\Microsoft\Windows\CurrentVersion\ContentDeliveryManager"
CONTROL_PANEL_DESKTOP = r"Control Panel\Desktop"
CONTROL_PANEL_MOUSE = r"Control Panel\Mouse"

# Was der Lesebefehl ausgibt, wenn der Wert gar nicht gesetzt ist.
NOT_SET = "__NICHT_GESETZT__"

# Die beiden Registry-Werttypen, die der Katalog benutzt.
DWORD = "REG_DWORD"
SZ = "REG_SZ"

# Der Ton kennt nur zwei Zustände.
MUTED = "1"
UNMUTED = "0"


def read_command(path: str, name: str) -> tuple[str, ...]:
    """Der Befehl, der einen Wert liest (und nie fehlschlägt).

    Der Name steht beim Auslesen in einfachen Anführungszeichen
    (``.'SubscribedContent-338388Enabled'``). Ohne sie liest PowerShell einen
    Namen mit Bindestrich als Subtraktion und bricht mit einem Parser-Fehler ab —
    am 2026-11-03 in der Außenprobe gefunden (der Doppelgänger im Testlauf hatte
    das nicht gezeigt, weil er nur Stichwörter im Befehl vergleicht).
    """
    script = (
        f"$v = (Get-ItemProperty -Path '{HIVE}:\\{path}' -Name {name} "
        f"-ErrorAction SilentlyContinue).'{name}'; "
        f"if ($null -eq $v) {{ '{NOT_SET}' }} else {{ $v }}"
    )
    return ("powershell", "-NoProfile", "-NonInteractive", "-Command", script)


def write_command(
    path: str, name: str, value: str, value_type: str = DWORD
) -> tuple[str, ...]:
    """Der Befehl, der einen Wert setzt (ohne Rückfrage, ohne Rechte).

    ``value_type`` ist der Registry-Typ (``REG_DWORD`` oder ``REG_SZ``). Er
    gehört zum Eintrag, nicht hierher — diese Funktion bekommt ihn nur
    durchgereicht (Offener Punkt 45).
    """
    return (
        "reg",
        "add",
        f"{HIVE}\\{path}",
        "/v",
        name,
        "/t",
        value_type,
        "/d",
        value,
        "/f",
    )


def delete_command(path: str, name: str) -> tuple[str, ...]:
    """Der Befehl, der einen Wert wieder entfernt."""
    return ("reg", "delete", f"{HIVE}\\{path}", "/v", name, "/f")


def read_value(executor: Executor, path: str, name: str) -> str | None:
    """Liest einen Wert. ``None`` heißt: es ist nichts eingestellt."""
    output = executor.run(read_command(path, name)).strip()
    if not output or output == NOT_SET:
        return None
    return output


def write_value(
    executor: Executor, path: str, name: str, value: str, value_type: str = DWORD
) -> None:
    """Setzt einen Wert."""
    executor.run(write_command(path, name, value, value_type))


def restore_value(
    executor: Executor,
    path: str,
    name: str,
    raw: str | None,
    value_type: str = DWORD,
) -> None:
    """Stellt den vorher festgehaltenen Zustand her.

    War vorher nichts gesetzt, wird der Wert entfernt: die Voreinstellung des
    Systems gilt dann wieder, statt eines Wertes, den es nie gab.
    """
    if raw is None:
        executor.run(delete_command(path, name))
    else:
        executor.run(write_command(path, name, raw, value_type))


def registry_action(
    *,
    key: str,
    path: str,
    name: str,
    goal: str,
    default: str,
    value_type: str = DWORD,
    group: str = "sonstiges",
) -> Action:
    """Baut einen Katalogeintrag für einen Wert in der Registry.

    ``goal`` ist der Wert, den die Aktion herstellt, ``default`` der Wert, den
    Windows verwendet, wenn nichts eingestellt ist. Mit ``default`` lässt sich
    auch ohne gesetzten Wert ehrlich sagen, ob das Ziel schon erreicht ist.
    ``value_type`` und ``group`` gehören zum Eintrag: der Typ, weil eine
    ``REG_SZ``-Einstellung anders geschrieben wird als ein Schalter, die Gruppe,
    weil ``/aktionen`` nach Themen sortiert bleibt, wenn der Katalog wächst.
    """

    def check(executor: Executor) -> ActionState:
        raw = read_value(executor, path, name)
        if raw is None:
            return ActionState(
                raw=None,
                description=t(f"action_{key}_state_unset"),
                at_goal=default == goal,
            )
        return ActionState(
            raw=raw,
            description=t(
                f"action_{key}_state_goal" if raw == goal else f"action_{key}_state_other"
            ),
            at_goal=raw == goal,
        )

    def apply(executor: Executor) -> str:
        write_value(executor, path, name, goal, value_type)
        return t(f"action_{key}_done")

    def undo(executor: Executor, raw: str | None) -> str:
        restore_value(executor, path, name, raw, value_type)
        return t(f"action_{key}_undone")

    return Action(
        key=key,
        check=check,
        apply=apply,
        undo=undo,
        group=group,
        texts=(*BASE_TEXTS, UNSET_TEXT),
    )


# --- Der Ton (der einzige Eintrag außerhalb der Registry) -----------------
#
# Die Lautstärke steht nicht in der Registry, sondern in der Audio-Schnittstelle
# von Windows (``IAudioEndpointVolume``). PowerShell kann sie nicht von sich aus
# ansprechen; deshalb wird die Schnittstelle in einem kleinen C#-Block bekannt
# gemacht (``Add-Type``). Das ist **kein Zusatzpaket**: der Übersetzer steckt in
# Windows. Am 2026-11-03 auf diesem Rechner gemessen: 0,33 bis 0,36 s je Aufruf,
# Stumm-Schalten und Zurücknehmen wirklich belegt (getrennte Prozesse, wie im
# Betrieb).
SOUND_SCRIPT = r"""
using System;
using System.Runtime.InteropServices;

[Guid("5CDF2C82-841E-4546-9722-0CF74078229A"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
public interface IAudioEndpointVolume {
  int NotImpl1();
  int NotImpl2();
  int GetChannelCount(out uint c);
  int SetMasterVolumeLevel(float level, ref Guid ctx);
  int SetMasterVolumeLevelScalar(float level, ref Guid ctx);
  int GetMasterVolumeLevel(out float level);
  int GetMasterVolumeLevelScalar(out float level);
  int SetChannelVolumeLevel(uint ch, float level, ref Guid ctx);
  int SetChannelVolumeLevelScalar(uint ch, float level, ref Guid ctx);
  int GetChannelVolumeLevel(uint ch, out float level);
  int GetChannelVolumeLevelScalar(uint ch, out float level);
  int SetMute([MarshalAs(UnmanagedType.Bool)] bool mute, ref Guid ctx);
  int GetMute([MarshalAs(UnmanagedType.Bool)] out bool mute);
}

[Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
public interface IMMDevice {
  int Activate(ref Guid iid, int clsCtx, IntPtr activationParams, [MarshalAs(UnmanagedType.IUnknown)] out object iface);
  int OpenPropertyStore(int access, out IntPtr props);
  int GetId([MarshalAs(UnmanagedType.LPWStr)] out string id);
  int GetState(out int state);
}

[Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
public interface IMMDeviceEnumerator {
  int NotImpl1();
  int GetDefaultAudioEndpoint(int dataFlow, int role, out IMMDevice endpoint);
}

[ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")]
class MMDeviceEnumeratorComObject { }

public class Ton {
  private static IAudioEndpointVolume Geraet() {
    var enumerator = (IMMDeviceEnumerator)(new MMDeviceEnumeratorComObject());
    IMMDevice dev;
    enumerator.GetDefaultAudioEndpoint(0, 1, out dev);
    Guid iid = typeof(IAudioEndpointVolume).GUID;
    object o;
    dev.Activate(ref iid, 23, IntPtr.Zero, out o);
    return (IAudioEndpointVolume)o;
  }
  public static bool Stumm() { bool m; Geraet().GetMute(out m); return m; }
  public static void SetzeStumm(bool m) { Guid g = Guid.Empty; Geraet().SetMute(m, ref g); }
}
"""


def _sound_script(aktion: str) -> str:
    """Erst die Audio-Schnittstelle bekannt machen, dann ``aktion`` ausführen."""
    return (
        "$ErrorActionPreference = 'Stop'; "
        f"Add-Type -TypeDefinition @'\n{SOUND_SCRIPT}\n'@ -Language CSharp | Out-Null; "
        f"{aktion}"
    )


def sound_read_command() -> tuple[str, ...]:
    """Der Befehl, der liest, ob der Ton stumm ist (``1``) oder nicht (``0``)."""
    return (
        "powershell",
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        _sound_script("if ([Ton]::Stumm()) { '1' } else { '0' }"),
    )


def sound_write_command(muted: str) -> tuple[str, ...]:
    """Der Befehl, der den Ton stumm schaltet (``1``) oder wieder anschaltet (``0``)."""
    wahr = "true" if muted == MUTED else "false"
    return (
        "powershell",
        "-NoProfile",
        "-NonInteractive",
        "-Command",
        _sound_script(f"[Ton]::SetzeStumm(${wahr})"),
    )


def sound_action() -> Action:
    """Der Ton-Eintrag: prüfen, stumm schalten, den vorherigen Zustand herstellen.

    Die Rücknahme stellt genau den Zustand her, der vorher dastand — war der Ton
    schon stumm, bleibt er stumm. Das Ziel ist immer dasselbe („stumm"), damit
    die Vorschau nicht raten muss (Entscheidung 2 aus Slice 6).
    """

    def check(executor: Executor) -> ActionState:
        raw = executor.run(sound_read_command()).strip()
        if raw not in (MUTED, UNMUTED):
            raise ActionError(t("action_ton_stumm_unreadable", output=raw))
        return ActionState(
            raw=raw,
            description=t(
                "action_ton_stumm_state_goal" if raw == MUTED else "action_ton_stumm_state_other"
            ),
            at_goal=raw == MUTED,
        )

    def apply(executor: Executor) -> str:
        executor.run(sound_write_command(MUTED))
        return t("action_ton_stumm_done")

    def undo(executor: Executor, raw: str | None) -> str:
        # ``None`` kann hier nicht vorkommen (der Ton hat immer einen Zustand);
        # falls doch, wird angeschaltet statt stumm geschaltet.
        executor.run(sound_write_command(MUTED if raw == MUTED else UNMUTED))
        return t("action_ton_stumm_undone")

    return Action(
        key="ton_stumm",
        check=check,
        apply=apply,
        undo=undo,
        group="ton",
    )


def handover_action(*, key: str, group: str = "handarbeit") -> Action:
    """Ein Eintrag, den der Avatar nicht selbst ausführt (Administratorrechte).

    Entscheidung 10: „Aktionen, die Administratorrechte brauchen, werden
    angekündigt und an Windows übergeben, nicht selbst durchgeführt." Deshalb
    geht hier **kein** Befehl über die Naht: alle drei Teile verweigern mit
    einer deutschen Meldung, und die Hülle zeigt stattdessen den Weg
    (``Action.handover``).
    """

    def refuse() -> str:
        raise ActionError(t("action_not_self_run", title=t(f"action_{key}_title")))

    def check(executor: Executor) -> ActionState:
        refuse()

    def apply(executor: Executor) -> str:
        refuse()

    def undo(executor: Executor, raw: str | None) -> str:
        refuse()

    return Action(
        key=key,
        check=check,
        apply=apply,
        undo=undo,
        group=group,
        needs_admin=True,
        texts=HANDOVER_TEXTS,
    )


# --- Der Katalog (Slice 7: 12 Aktionen in 5 Gruppen) ----------------------
#
# Auswahl (Entwicklerentscheidung, Design Kapitel 9: „10 bis 15 Anfängerfälle"):
# häufige Anfängerfragen, die sich ohne Administratorrechte, ohne Datei, ohne
# Netz und ohne Laufwerk beantworten lassen — und deren Wirkung man sieht. Alle
# Werte sind am 2026-11-03 auf diesem Rechner gelesen worden; sie stehen als
# Kommentar dahinter. Was Rechte braucht, steht in der Gruppe „handarbeit" und
# wird nur angekündigt.

SYSTEM_ACTIONS: tuple[Action, ...] = (
    # --- Explorer und Dateien ---------------------------------------------
    # Windows blendet Dateiendungen aus; dann sieht man nicht, ob eine Datei
    # ein Bild, ein Text oder ein Programm ist. 0 = anzeigen (Voreinstellung 1;
    # gelesen: 0).
    registry_action(
        key="dateiendungen",
        path=EXPLORER_ADVANCED,
        name="HideFileExt",
        goal="0",
        default="1",
        group="explorer",
    ),
    # Versteckte Dateien und Ordner: 1 = anzeigen, 2 = nicht anzeigen
    # (gelesen: 2).
    registry_action(
        key="versteckte_dateien",
        path=EXPLORER_ADVANCED,
        name="Hidden",
        goal="1",
        default="2",
        group="explorer",
    ),
    # Die Liste der zuletzt geöffneten Dateien im Explorer: 1 = zeigen
    # (Voreinstellung), 0 = nicht zeigen (gelesen: nicht gesetzt).
    registry_action(
        key="zuletzt_dateien_aus",
        path=EXPLORER_ADVANCED,
        name="ShowRecent",
        goal="0",
        default="1",
        group="explorer",
    ),
    # Sekunden in der Uhr der Taskleiste: 1 = zeigen, 0 = nicht zeigen
    # (Voreinstellung; gelesen: nicht gesetzt).
    registry_action(
        key="uhr_mit_sekunden",
        path=EXPLORER_ADVANCED,
        name="ShowSecondsInSystemClock",
        goal="1",
        default="0",
        group="explorer",
    ),
    # --- Aussehen und Lesbarkeit -----------------------------------------
    # Helle oder dunkle Darstellung für Apps und Fenster: 0 = dunkel,
    # 1 = hell (Voreinstellung 1; gelesen: 0).
    registry_action(
        key="dunkler_modus",
        path=THEMES_PERSONALIZE,
        name="AppsUseLightTheme",
        goal="0",
        default="1",
        group="darstellung",
    ),
    # Schriftgröße in Prozent: 100 = normal (Voreinstellung; gelesen: nicht
    # gesetzt), 125 = deutlich größer. Mehr als 225 nimmt Windows nicht an.
    registry_action(
        key="grosse_schrift",
        path=ACCESSIBILITY,
        name="TextScaleFactor",
        goal="125",
        default="100",
        group="darstellung",
    ),
    # Mausgeschwindigkeit, von Windows als Zeichenkette geführt (REG_SZ):
    # 1 bis 20, 10 ist die mittlere Stufe (gelesen: 10).
    registry_action(
        key="mausgeschwindigkeit",
        path=CONTROL_PANEL_MOUSE,
        name="MouseSensitivity",
        goal="20",
        default="10",
        value_type=SZ,
        group="darstellung",
    ),
    # Wartezeit, bis ein Menü aufklappt, in Tausendstelsekunden, ebenfalls
    # REG_SZ: 400 ist die Voreinstellung (gelesen: 400), 0 lässt Menüs sofort
    # aufgehen.
    registry_action(
        key="menues_sofort",
        path=CONTROL_PANEL_DESKTOP,
        name="MenuShowDelay",
        goal="0",
        default="400",
        value_type=SZ,
        group="darstellung",
    ),
    # --- Ton --------------------------------------------------------------
    sound_action(),
    # --- Weniger Windows im Weg -------------------------------------------
    # Die Tipps und Empfehlungen, die Windows im Startmenü und in den
    # Einstellungen einblendet: 0 = aus, 1 = an (Voreinstellung; gelesen: nicht
    # gesetzt).
    registry_action(
        key="windows_tipps_aus",
        path=CONTENT_DELIVERY,
        name="SubscribedContent-338388Enabled",
        goal="0",
        default="1",
        group="windows",
    ),
    # --- Das kann nur Windows selbst --------------------------------------
    # Beides braucht Rechte, die der Avatar nie anfordert (Entscheidung 10);
    # er zeigt nur den Weg.
    handover_action(key="bildschirm_spiegeln"),
    handover_action(key="programm_installieren"),
)


def grouped_actions(
    actions: Sequence[Action] = SYSTEM_ACTIONS,
) -> tuple[tuple[Action, ...], ...]:
    """Die Einträge nach Themen, in der Reihenfolge des Katalogs.

    ``/aktionen`` bleibt damit lesbar, wenn der Katalog wächst (Slice 7): die
    Gruppen kommen in der Reihenfolge, in der ihr erster Eintrag steht.
    """
    gruppen: dict[str, list[Action]] = {}
    for action in actions:
        gruppen.setdefault(action.group, []).append(action)
    return tuple(tuple(entries) for entries in gruppen.values())


def build_actions_section(actions: Sequence[Action] = SYSTEM_ACTIONS) -> str:
    """Der Abschnitt im Systemtext: welche Aktionen es gibt und wer sie auslöst.

    Das Modell erfährt damit, was es anbieten darf — und dass es selbst nichts
    ausführt. Die Ausführung hängt an der Bestätigung des Nutzers, nicht an der
    Antwort des Modells (Entscheidung 5 und 6).

    Seit Slice 7 stehen hier nur Schlüssel und Kurztitel, nicht mehr die
    Langbeschreibung: bei einem wachsenden Katalog wächst dieser Abschnitt sonst
    in **jede** Anfrage hinein (Offene Punkte 35 und 46). Die genauen Zahlen
    stehen in PROGRESS.md; die Beschreibungen sieht man mit ``/aktionen``.
    """
    lines = [t("actions_header")]
    for action in actions:
        schluessel = "action_state_line_admin" if action.needs_admin else "action_state_line"
        lines.append(t(schluessel, schluessel=action.key, title=action.title))
    lines.append(t("actions_rule"))
    return "\n".join(lines)


def build_learn_section(active: bool = True) -> str:
    """Der Abschnitt im Systemtext für den Lernmodus (Ansatz C, Kapitel 6.1).

    Er sagt dem Modell, dass es gerade erklärt statt auszuführen — damit es
    nichts anbietet, was es in diesem Modus nicht tun darf. Der Katalog bleibt
    dabei unverändert und steht weiter im Systemtext: im Lernmodus sind seine
    Einträge Wissen („so würde ich es machen"), kein Angebot.

    Im gewöhnlichen Betrieb kommt der Abschnitt nicht vor (leerer Text): dann
    gilt die Regel aus ``build_actions_section`` (ausführen nach Bestätigung).
    """
    if not active:
        return ""
    return t("learn_section")
