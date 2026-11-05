# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""Deutsche Texte. Ersteinstellung laut Design-Dokument (Entscheidung 7)."""

from __future__ import annotations

TEXTS: dict[str, str] = {
    # Betriebsart (Slice 5): online über einen Schlüssel oder lokal über Ollama.
    "mode_online": "online",
    "mode_lokal": "lokal",
    "invalid_mode": "Unbekannte Betriebsart {value!r}. Bekannt sind: {known}.",
    # Gespräch
    "welcome": "Hallo, ich bin {name}. Frag mich etwas zu deinem Rechner.",
    "model_note": "Antworten kommen von {model} ({mode_name}) über {base_url}.",
    "exit_hint": "Mit /exit beendest du das Gespräch.",
    "memory_hint": (
        "Mit /merken <Tatsache> behalte ich etwas über Sitzungen hinweg, "
        "/gedaechtnis zeigt es im Klartext, /vergessen löscht es."
    ),
    "prompt_user": "Du: ",
    "prompt_assistant": "Helfer [{model}, {mode_name}]: ",
    "farewell": "Bis bald.",
    "interrupted": "Abgebrochen.",
    # Persona (Slice 3): Name und Tonfall. Ein Abschnitt je Charakter, damit
    # eine weitere Sprache nur diese Texte übersetzen muss (Entscheidung 7).
    "persona_system": (
        "Du heißt {name} und bist ein Helfer, der Menschen ohne Technikwissen "
        "bei Fragen zum eigenen Rechner unterstützt.\n"
        "{character}\n"
        "Antworte auf Deutsch, einfach und knapp. Wenn du etwas nicht weißt, "
        "sage das offen, statt zu raten."
    ),
    "persona_memory_header": "Wichtige gemerkte Tatsachen über den Nutzer:",
    "persona_memory": (
        "{header}\n{facts}\n"
        "Stütze dich auf diese Tatsachen, wenn sie zur Frage passen. Was hier "
        "nicht steht, hast du nicht gemerkt."
    ),
    "persona_mira_name": "Mira",
    "persona_mira_character": (
        "Dein Tonfall: ruhig, geduldig und sachlich. Du erklärst in kleinen "
        "Schritten und ohne Fachwörter, die du nicht vorher erklärst, und du "
        "drängst dich nicht auf."
    ),
    "persona_kalle_name": "Kalle",
    "persona_kalle_character": (
        "Dein Tonfall: hemdsärmelig und direkt, wie ein nachbarschaftlicher "
        "Bastler. Du sagst klar, was du tun würdest, und nimmst kein Blatt vor "
        "den Mund."
    ),
    "persona_pico_name": "Pico",
    "persona_pico_character": (
        "Dein Tonfall: neugierig, knapp und nüchtern. Du nennst Zahlen und "
        "gemessene Werte, statt zu vermuten."
    ),
    "invalid_persona": "Unbekannter Charakter {value!r}. Bekannt sind: {known}.",
    # Gedächtnis
    "memory_usage": "So geht es: /merken Dein Drucker heißt Berta",
    "memory_saved": "Gemerkt: {fact}",
    "memory_known": "Das wusste ich schon: {fact}",
    "memory_header": "Gemerkte Tatsachen ({count}):",
    "memory_line": "  - {fact}",
    "memory_empty": "Ich habe mir noch nichts gemerkt.",
    "memory_location": "Gespeichert in: {path}",
    "memory_cleared": "Gedächtnis gelöscht ({count} Einträge).",
    "memory_unavailable": (
        "Das Gedächtnis ist nicht verfügbar; ich merke mir in diesem Gespräch nichts."
    ),
    "memory_unreadable": "Die Gedächtnisdatei {path} lässt sich nicht lesen ({detail}).",
    "memory_corrupt": (
        "Die Gedächtnisdatei {path} ist nicht lesbar ({detail}). Ich starte ohne "
        "Gedächtnis; lösche oder repariere die Datei, dann geht es wieder."
    ),
    "memory_facts_not_list": "Das Feld facts ist keine Liste.",
    "memory_not_writable": "Ich konnte das Gedächtnis nicht speichern ({path}, {detail}).",
    # Beschriftung der Figur, je Zustand ein Text. Der Schlüssel ist
    # "avatar_" + Wert aus ai_helper/avatar/states.py.
    "avatar_neutral": "Ich bin bereit.",
    "avatar_thinking": "Ich denke nach ...",
    "avatar_speaking": "Ich antworte.",
    "avatar_explaining": "Ich erkläre es dir Schritt für Schritt.",
    "avatar_happy": "Schön, dass ich helfen konnte.",
    "avatar_error": "Das hat leider nicht geklappt.",
    # Die Demo (Slice D2): fester Anbieter, fester Messbericht, kein Ausführen.
    # Die Betriebsart der Demo steht wie ``online``/``lokal`` in jeder Zeile.
    "mode_demo": "demo",
    "demo_model_label": "demo-modell",
    "demo_measure_source": "Demo-Bericht (fester Wert, nicht gemessen)",
    "demo_runner_unavailable": (
        "In der Demo wird nichts gemessen; die Werte stammen aus einem festen Bericht."
    ),
    "demo_hint": (
        "Demo: Es werden keine Befehle ausgeführt, und nichts verlässt deinen Browser."
    ),
    "demo_polite_answer": (
        "In dieser Demo antworte ich nur auf die vorbereiteten Fragen — probier einen "
        "der Vorschläge, oder einen Befehl wie /nachschauen, /aktionen, /protokoll oder "
        "/lernen."
    ),
    "demo_answer_abilities": (
        "Ich bin Mira, ein Helfer für deinen Rechner. In dieser Demo beantworte ich ein "
        "paar vorbereitete Fragen, liste mit /aktionen die geprüften Einstellungen auf "
        "und zeige dir Vorschau, Bestätigung und Rücknahme — geändert wird dabei nichts."
    ),
    "demo_answer_setup": (
        "In dieser Demo ist ein Beispielrechner fest eingestellt: Windows 11, ein "
        "Bildschirm mit 1920 x 1080 Pixeln und ein AMD Ryzen 5 7530U. Die Werte sind ein "
        "fester Demo-Bericht, nicht die Messung deines echten Rechners."
    ),
    "demo_answer_cpu": (
        "Der Prozessor in dieser Demo ist ein AMD Ryzen 5 7530U with Radeon Graphics mit "
        "6 Kernen (12 gleichzeitig)."
    ),
    "demo_answer_memory": (
        "In dieser Demo hat der Rechner 15,3 GB Arbeitsspeicher; davon sind gerade 7,1 GB "
        "frei."
    ),
    "demo_answer_actions": (
        "Ja. Mit /aktionen zeige ich dir die geprüften Einstellungen. Bei /aktion "
        "<schlüssel> siehst du zuerst im Klartext, was passieren würde, und erst nach "
        "deinem Ja würde es ausgeführt. In der Demo passiert dabei nichts: der "
        "Demo-Ausführende schreibt nur ins Protokoll — und /rueckgaengig nimmt den "
        "Eintrag trotzdem zurück."
    ),
    "demo_answer_driver": (
        "Ein Gerätetreiber ist ein Programm, das Windows sagt, wie es mit einem Bauteil "
        "wie Drucker, Grafikkarte oder Tastatur reden soll. In dieser Demo habe ich dafür "
        "keine Quelle; im echten Betrieb würde ich in der deutschen Wikipedia nachschlagen."
    ),

    # Nachschauen (Slice 4): Werkzeuge lesen den echten Systemzustand.
    # Je Werkzeug ein Name für die Liste und ein Satz, was es nachschaut.
    "tool_windows_version_name": "Windows-Version",
    "tool_windows_version_description": (
        "Welche Windows-Version und welche Ausgabe installiert ist."
    ),
    "tool_cpu_name": "Prozessor",
    "tool_cpu_description": "Welcher Prozessor im Rechner steckt und wie viele Kerne er hat.",
    "tool_screen_resolution_name": "Bildschirmauflösung",
    "tool_screen_resolution_description": "Wie groß der Bildschirm gerade eingestellt ist.",
    "tool_graphics_name": "Grafik",
    "tool_graphics_description": "Welcher Grafik-Chip im Rechner steckt.",
    "tool_memory_name": "Arbeitsspeicher",
    "tool_memory_description": (
        "Wie viel Arbeitsspeicher vorhanden und wie viel davon gerade frei ist."
    ),
    "tool_drives_name": "Laufwerke",
    "tool_drives_description": (
        "Welche Laufwerke es gibt, wie groß sie sind und wie viel frei ist."
    ),
    # Der Name je gemessenem Wert ("measure_" + Schlüssel des Wertes).
    "measure_windows_version": "Windows-Version",
    "measure_windows_edition": "Windows-Ausgabe",
    "measure_screen_resolution": "Bildschirmauflösung",
    "measure_cpu": "Prozessor",
    "measure_cpu_cores": "Prozessor-Kerne",
    "measure_graphics": "Grafik",
    "measure_memory": "Arbeitsspeicher",
    "measure_memory_total": "Arbeitsspeicher gesamt",
    "measure_memory_free": "Arbeitsspeicher frei",
    "measure_drives": "Laufwerke",
    "measure_drive_total": "Laufwerk {drive} gesamt",
    "measure_drive_free": "Laufwerk {drive} frei",
    "value_pixel": "Pixel",
    # Der Prozessor in einem Satz: die Zahl der gleichzeitig rechenbaren Fäden
    # ist für einen Anfänger das Interessante, „Threads" wäre ein Fachwort.
    "value_cpu_cores": "{cores} Kerne ({threads} gleichzeitig)",
    "value_cpu_cores_single": "1 Kern ({threads} gleichzeitig)",
    "value_gb": "GB",
    "measure_header": "Nachgeschaut ({count} Werte):",
    "measure_line": "  {label}: {value} {unit}",
    "measure_line_plain": "  {label}: {value}",
    "measure_unmeasurable": "  {label}: nicht messbar ({detail})",
    "measure_source": "      Quelle: {source}",
    "measure_no_reason": "kein Grund genannt",
    "looking_around": "Ich schaue kurz nach, wie dein Rechner eingerichtet ist ...",
    "nachschauen_hint": (
        "Mit /nachschauen sehe ich jederzeit nach und zeige dir die gemessenen Werte."
    ),
    # Der Abschnitt, den die Messwerte im Systemtext bekommen.
    "state_tools_header": (
        "Du kannst den Rechner nachschauen. Dafür stehen dir diese Werkzeuge zur Verfügung:"
    ),
    "state_tool_line": "- {name}: {description}",
    "state_values_header": "Das hast du gerade auf diesem Rechner gemessen:",
    "state_value_line": "- {label}: {value} {unit}",
    "state_value_plain": "- {label}: {value}",
    "state_value_missing": "- {label}: nicht gemessen ({detail})",
    "state_rule": (
        "Wenn du über den Rechner sprichst, nenne diese gemessenen Werte und rate "
        "nichts dazu. Was hier nicht steht, hast du nicht gemessen; sage dann "
        "offen, dass du es nicht weißt."
    ),
    # Fehlgeschlagene Messungen: eine Meldung, kein Absturz.
    "tool_command_failed": "Der Befehl {command} ließ sich nicht ausführen ({detail}).",
    "tool_exit_code": "Der Befehl endete mit Code {code}.",
    "tool_unreadable": "Die Ausgabe war nicht lesbar ({output}).",
    "tool_no_output": "Der Befehl lieferte keine verwertbare Ausgabe.",
    "tool_no_value": "Der Befehl lieferte dazu keinen Wert.",
    "tool_no_drives": "Es wurde kein Laufwerk gemeldet.",
    "tool_unexpected": "Unerwarteter Fehler beim Messen ({detail}).",
    # Einstellungen fehlen
    "missing_key": "Kein API-Schlüssel gefunden, deshalb kann ich kein Online-Modell fragen.",
    "missing_key_hint": (
        "Trage ihn in die Datei .env ein: AI_HELPER_API_KEY=dein-schluessel "
        "(Vorlage: .env.example)."
    ),
    "missing_key_hint_env": (
        "Alternativ setzt du die Umgebungsvariable AI_HELPER_API_KEY. Ohne Schlüssel "
        "läuft der Onlinemodus nicht; ohne Schlüssel hilft der lokale Betrieb mit "
        "Ollama weiter (--mode lokal). Den ganzen Weg zeigt: --hilfe"
    ),
    "missing_model": "Es ist kein Modell eingestellt. Trage AI_HELPER_MODEL in .env ein.",
    "invalid_timeout": "AI_HELPER_TIMEOUT_S muss eine Zahl größer als 0 sein, ist aber {value!r}.",
    # Selbstprüfung
    "check_header": "Einstellungen:",
    "check_model": "  Modell:      {model}",
    "check_base_url": "  Basis-URL:   {base_url}",
    "check_persona": "  Charakter:   {name} ({persona_key})",
    "check_memory": "  Gedächtnis:  {path}",
    "check_memory_off": "  Gedächtnis:  aus",
    "check_tools": "  Werkzeuge:   {count} ({names})",
    "check_key": "  Schlüssel:   vorhanden ({source})",
    "check_key_missing": "  Schlüssel:   fehlt",
    "check_ready": "Startklar.",
    "check_not_ready": "Noch nicht startklar.",
    # Fehler im Betrieb
    "error_http": "Der Anbieter hat mit Fehler {status} geantwortet: {detail}",
    "error_network": (
        "Die Verbindung zum Anbieter ist fehlgeschlagen: {detail}. "
        "Prüfe zuerst deine Internetverbindung. Ohne Netz antwortet nur das lokale "
        "Modell auf deinem Rechner (--mode lokal, dann muss Ollama laufen); den "
        "ganzen Weg zeigt --hilfe."
    ),
    "error_response": "Die Antwort des Anbieters war nicht lesbar: {detail}",
    "error_empty_answer": "Der Anbieter hat eine leere Antwort geschickt.",
    # Antwort in Teilstücken (Slice 5b).
    "error_stream_broken": (
        "Die Antwort brach mitten im Strom ab: {detail}. Ich habe die halbe "
        "Antwort nicht ins Gespräch übernommen."
    ),
    "error_stream_unfinished": (
        "Der Anbieter hat den Strom nicht abgeschlossen (das Ende kam nicht an)"
    ),
    "error_local_stream": (
        "Der lokale Dienst hat mitten in der Antwort einen Fehler gemeldet: {detail}"
    ),
    "stream_fallback": (
        "Dieser Anbieter liefert die Antwort nicht in Teilen; ich hole sie "
        "deshalb auf einmal."
    ),
    # Lokaler Betrieb (Slice 5): Ollama auf dem eigenen Rechner.
    "error_local_network": (
        "Der lokale Dienst unter {url} antwortet nicht ({detail})."
    ),
    # Der nächste Schritt dazu steht getrennt: die Selbstprüfung zeigt dieselbe
    # Meldung als Grund (dort wäre der Weg doppelt), die Hülle hängt ihn im
    # lokalen Betrieb an jede gescheiterte Anfrage an.
    "error_local_next_step": (
        "Der nächste Schritt: Ollama starten ('ollama serve') — ist es noch nicht "
        "installiert, von ollama.com herunterladen und entpacken; Rechte braucht es "
        "dafür nicht. Läuft der Dienst, sagt 'ai_helper --check --mode lokal' genau, "
        "ob das Modell schon da ist."
    ),
    "error_local_http": "Der lokale Dienst hat mit Fehler {status} geantwortet: {detail}",
    "error_local_model_missing": (
        "Das lokale Modell {model} ist auf diesem Rechner nicht vorhanden. "
        "Hole es einmalig mit: ollama pull {model}"
    ),
    "error_local_tags": "Die Modellliste des lokalen Dienstes war nicht lesbar ({detail}).",
    # Selbstprüfung: Betriebsart und lokaler Dienst
    "check_mode_online": "  Betriebsart: online (API-Schlüssel nötig)",
    "check_mode_local": "  Betriebsart: lokal (Ollama unter {base_url})",
    "check_local_service": "  Lokaler Dienst: erreichbar ({count} Modelle)",
    "check_local_model_present": "  Modell:      {model} (vorhanden)",
    "check_local_model_missing": "  Modell:      {model} (nicht vorhanden)",
    "check_local_models": "  Vorhandene Modelle: {names}",
    "check_local_unreachable": "  Lokaler Dienst: nicht erreichbar ({detail})",
    "check_local_hint": (
        "Der nächste Schritt: Ollama starten ('ollama serve') — ist es noch nicht "
        "installiert, von ollama.com herunterladen und entpacken; Rechte braucht es "
        "dafür nicht. Danach das Modell einmalig holen: ollama pull {model}"
    ),
    "check_key_not_needed": "  Schlüssel:   nicht nötig (lokaler Betrieb)",
    # Lernmodus (Slice 8): Ansatz C aus Design Kapitel 6.1 — erklären statt
    # ausführen. Der Modus ist im Gespräch umschaltbar (/lernen) und wie die
    # Betriebsart in der Begrüßung, in der Selbstprüfung und im Systemtext
    # sichtbar.
    "learn_on": "Lernmodus an. Ich erkläre dir die Schritte und führe nichts aus.",
    "learn_off": "Lernmodus aus. Ich führe wieder aus, nachdem du bestätigt hast.",
    "learn_usage": "So geht es: /lernen — und mit /lernen aus schalte ich wieder auf Ausführen.",
    "learn_already_on": "Der Lernmodus ist schon an.",
    "learn_already_off": "Der Lernmodus ist schon aus.",
    "learn_hint": (
        "Mit /lernen erkläre ich dir die Schritte, statt etwas auszuführen; "
        "/lernen aus schaltet zurück."
    ),
    "learn_active_note": (
        "Lernmodus: ich erkläre dir die Schritte und ändere nichts. "
        "Mit /lernen aus schalte ich wieder auf Ausführen."
    ),
    # Die Erklärung bei /aktion <schlüssel> im Lernmodus.
    "learn_action_head": "Im Lernmodus ändere ich nichts. Das würde ich sonst tun: {title}",
    "learn_action_steps": (
        "So machst du es selbst in drei Schritten: 1. Öffne die Windows-Einstellungen. "
        "2. Suche dort {title}. 3. Stelle es so ein, wie du es haben willst."
    ),
    "learn_action_rule": (
        "Ich führe in diesem Modus nichts aus — auch ein „ja“ ändert nichts."
    ),
    "learn_undo_blocked": (
        "Im Lernmodus nehme ich nichts zurück und ändere nichts. "
        "Mit /lernen aus geht das wieder."
    ),
    # Der Abschnitt im Systemtext: er sagt dem Modell, dass es gerade erklärt.
    "learn_section": (
        "Du bist gerade im Lernmodus.\n"
        "Erkläre dem Nutzer Schritt für Schritt, wie er es selbst machen kann, "
        "und führe selbst nichts aus: biete keine Aktion an und nenne keinen "
        "Befehl. Die Aktionen aus der Liste darfst du nur als Weg beschreiben "
        "(„so würdest du es machen“), nicht als etwas, das du gleich tust."
    ),
    "invalid_learn": "Unbekannter Wert für den Lernmodus {value!r}. Bekannt sind: {known}.",
    "check_learn": "  Lernmodus:  {state}",
    "learn_state_on": "an (ich erkläre, führe nichts aus)",
    "learn_state_off": "aus (ich führe nach Bestätigung aus)",
    # Recherche (Slice 9): nachschlagen im Netz, mit Quellenangabe. Der Dienst
    # steht in den Einstellungen (AI_HELPER_SEARCH), im Gespräch schlägt
    # /suchen <begriff> nach.
    "search_name_wikipedia": "deutsche Wikipedia",
    "search_name_exa": "Websuche über Exa",
    "search_name_aus": "aus",
    "search_provider_wikipedia": "der deutschen Wikipedia",
    "search_provider_exa": "dem Suchdienst Exa",
    "search_hint": (
        "Mit /suchen <begriff> schaue ich im Netz nach und nenne dir die Quelle."
    ),
    "search_usage": "So geht es: /suchen Wie schalte ich die Bildschirmlupe ein",
    "search_unavailable": (
        "Nachschlagen kann ich gerade nicht: Die Suche ist nicht eingerichtet. "
        "Mit AI_HELPER_SEARCH=wikipedia in der .env schalte ich sie ein "
        "(Vorlage: .env.example)."
    ),
    "search_key_missing": (
        "Für die Websuche fehlt der Schlüssel; ich schicke nichts raus. Trage "
        "AI_HELPER_SEARCH_KEY in die .env ein — oder stelle mit "
        "AI_HELPER_SEARCH=wikipedia auf die Wikipedia um (die braucht keinen Schlüssel)."
    ),
    "search_announce": (
        "Ich schaue nach: „{query}“ — dabei verlässt diese Frage deinen Rechner "
        "und geht an {provider}."
    ),
    "search_sources_header": "Gefundene Quellen ({count}):",
    "search_source_line": "  {number}. {title} — {url}",
    "search_source_snippet": "      {snippet}",
    "search_no_hits": (
        "Zu „{query}“ habe ich nichts gefunden. Etwas zu erfinden, hilft dir nicht weiter."
    ),
    "search_empty_query": "Dazu fehlt mir die Suchanfrage; ich weiß nicht, wonach ich schauen soll.",
    "search_failed": "Die Suche hat nicht geklappt: {detail}",
    "search_http_error": "Der Suchdienst hat mit Fehler {status} geantwortet ({detail}).",
    "search_no_reason": "kein Grund genannt",
    "search_response_unreadable": "Die Antwort des Suchdienstes war nicht lesbar ({detail}).",
    "search_no_results_field": "die erwarteten Felder fehlen",
    # Der Beleg im Auftrag an das Modell: Titel, Adresse und Auszug.
    "search_hit_line": "- {title} ({url}): {snippet}",
    "search_question": (
        "Meine Frage: {query}\n"
        "\n"
        "Ich habe dazu nachgeschlagen. Das sind die gefundenen Quellen:\n"
        "{hits}\n"
        "\n"
        "Beantworte meine Frage und nenne zu jeder Aussage die Quelle (Titel und "
        "Adresse). Was nicht in diesen Quellen steht, hast du nicht nachgeschlagen."
    ),
    # Der Abschnitt im Systemtext: nachschlagen ja, Quelle nennen ja.
    "search_section": (
        "Du kannst im Netz nachschlagen (über {provider}).\n"
        "Sage dem Nutzer, dass er mit /suchen <begriff> nachschlagen kann. Wenn dir "
        "Quellen vorliegen, stütze dich darauf und nenne zu jeder Aussage die Quelle "
        "(Titel und Adresse). Erfinde keine Quelle und keine Adresse."
    ),
    "invalid_search": "Unbekannter Wert für die Suche {value!r}. Bekannt sind: {known}.",
    "check_search": "  Suche:       {name} ({state})",
    "check_search_state_ready": "eingerichtet",
    "check_search_state_key_missing": "Schlüssel fehlt",
    "check_search_state_off": "abgeschaltet",
    # Aktionen (Slice 6): geprüfte Aktionen mit Vorschau, Bestätigung und
    # Rücknahme. Der Platzhalter heißt "schluessel", weil t() selbst einen
    # Parameter "key" hat.
    "action_hint": (
        "Mit /aktionen siehst du, was ich auf diesem Rechner ändern kann; /protokoll "
        "zeigt, was ich getan habe, und /rueckgaengig nimmt das Letzte zurück."
    ),
    "action_list_header": "Aktionen ({count}):",
    "action_list_group": "  {title}",
    "action_list_line": "  {schluessel}: {title} — {description}",
    "action_list_hint": (
        "So geht es: /aktion dateiendungen — ich zeige vorher, was genau passieren "
        "wird, und frage nach."
    ),
    "action_usage": "So geht es: /aktion dateiendungen",
    "action_unknown": (
        "Diese Aktion kenne ich nicht: {schluessel!r}. Bekannt sind: {known}."
    ),
    "action_preview": "Das werde ich tun: {title}",
    "action_now": "Jetzt gerade: {state}",
    "action_already": "Das ist schon so — ich muss nichts ändern.",
    "action_confirm": "Soll ich das tun? (ja/nein) ",
    "action_declined": "Dann nicht. Ich habe nichts geändert.",
    "action_done": "Erledigt: {result}",
    "action_unavailable": (
        "Der Aktionsrahmen ist nicht verfügbar; ich ändere in diesem Gespräch nichts."
    ),
    "action_check_failed": "Das kann ich hier nicht prüfen: {detail}",
    "action_apply_failed": "Das hat nicht geklappt: {detail}",
    "action_undo_failed": "Das Zurücknehmen hat nicht geklappt: {detail}",
    "action_not_logged": (
        "Die Aktion ist ausgeführt, aber ich konnte sie nicht protokollieren ({detail}). "
        "Zurücknehmen kann ich sie deshalb nicht mehr."
    ),
    "undo_nothing": "Es gibt nichts zurückzunehmen.",
    "undo_done": "Rückgängig gemacht: {title} — {result}",
    "undo_unknown": "Zu diesem Eintrag kenne ich keine Aktion mehr ({schluessel!r}).",
    # Das Protokoll: jede ausgeführte Aktion im Klartext.
    "log_header": "Protokoll ({count} Einträge):",
    "log_line": "  {time} — {title}",
    "log_reason": "      Grund: {reason}",
    "log_result": "      Ergebnis: {result}",
    "log_undo_open": "      Rücknahme: mit /rueckgaengig möglich",
    "log_undone": "      Rücknahme: bereits zurückgenommen",
    "log_location": "Gespeichert in: {path}",
    "log_empty": "Ich habe noch nichts ausgeführt.",
    "log_unavailable": (
        "Das Protokoll ist nicht verfügbar; ich führe in diesem Gespräch nichts aus."
    ),
    "log_unreadable": "Die Protokolldatei {path} lässt sich nicht lesen ({detail}).",
    "log_corrupt": (
        "Die Protokolldatei {path} ist nicht lesbar ({detail}). Ich führe deshalb nichts "
        "aus; lösche oder repariere die Datei, dann geht es wieder."
    ),
    "log_actions_not_list": "Das Feld actions ist keine Liste.",
    "log_entry_not_object": "Ein Eintrag des Protokolls ist kein Objekt.",
    "log_entry_incomplete": "Ein Eintrag des Protokolls ist unvollständig ({field}).",
    "log_not_writable": "Ich konnte das Protokoll nicht speichern ({path}, {detail}).",
    # Die drei Aktionen des Katalogs: Titel, Beschreibung, jetziger Zustand,
    # Ergebnistext und Rücknahmetext.
    "action_dateiendungen_title": "Dateiendungen im Explorer anzeigen",
    "action_dateiendungen_description": (
        "Zeigt, was für eine Datei das ist (.txt, .jpg, .exe)."
    ),
    "action_dateiendungen_state_goal": "Die Dateiendungen werden angezeigt.",
    "action_dateiendungen_state_other": "Die Dateiendungen sind versteckt.",
    "action_dateiendungen_state_unset": (
        "Dazu ist nichts eingestellt; Windows versteckt die Dateiendungen standardmäßig."
    ),
    "action_dateiendungen_done": "Die Dateiendungen werden jetzt im Explorer angezeigt.",
    "action_dateiendungen_undone": "Die Dateiendungen sind wieder wie vorher.",
    "action_versteckte_dateien_title": "Versteckte Dateien im Explorer anzeigen",
    "action_versteckte_dateien_description": (
        "Zeigt Dateien und Ordner, die Windows ausblendet."
    ),
    "action_versteckte_dateien_state_goal": "Versteckte Dateien werden angezeigt.",
    "action_versteckte_dateien_state_other": "Versteckte Dateien werden nicht angezeigt.",
    "action_versteckte_dateien_state_unset": (
        "Dazu ist nichts eingestellt; Windows blendet versteckte Dateien standardmäßig aus."
    ),
    "action_versteckte_dateien_done": (
        "Versteckte Dateien werden jetzt im Explorer angezeigt."
    ),
    "action_versteckte_dateien_undone": "Versteckte Dateien sind wieder wie vorher.",
    "action_dunkler_modus_title": "Dunkle Darstellung einschalten",
    "action_dunkler_modus_description": "Stellt Apps und Fenster auf dunkle Farben um.",
    "action_dunkler_modus_state_goal": "Die dunkle Darstellung ist eingeschaltet.",
    "action_dunkler_modus_state_other": "Die helle Darstellung ist eingeschaltet.",
    "action_dunkler_modus_state_unset": (
        "Dazu ist nichts eingestellt; Windows verwendet standardmäßig die helle Darstellung."
    ),
    "action_dunkler_modus_done": "Apps und Fenster werden jetzt dunkel dargestellt.",
    "action_dunkler_modus_undone": "Die Darstellung ist wieder wie vorher.",
    # Die weiteren Aktionen des Katalogs (Slice 7).
    "action_zuletzt_dateien_aus_title": "Zuletzt verwendete Dateien ausblenden",
    "action_zuletzt_dateien_aus_description": (
        "Blendet die Liste der zuletzt geöffneten Dateien im Explorer aus."
    ),
    "action_zuletzt_dateien_aus_state_goal": (
        "Zuletzt verwendete Dateien werden nicht angezeigt."
    ),
    "action_zuletzt_dateien_aus_state_other": "Zuletzt verwendete Dateien werden angezeigt.",
    "action_zuletzt_dateien_aus_state_unset": (
        "Dazu ist nichts eingestellt; Windows zeigt die zuletzt verwendeten Dateien "
        "standardmäßig an."
    ),
    "action_zuletzt_dateien_aus_done": (
        "Die zuletzt verwendeten Dateien werden jetzt nicht mehr angezeigt."
    ),
    "action_zuletzt_dateien_aus_undone": "Die Liste ist wieder wie vorher.",
    "action_uhr_mit_sekunden_title": "Sekunden in der Uhr anzeigen",
    "action_uhr_mit_sekunden_description": (
        "Zeigt in der Uhr der Taskleiste auch die Sekunden."
    ),
    "action_uhr_mit_sekunden_state_goal": "Die Uhr zeigt die Sekunden an.",
    "action_uhr_mit_sekunden_state_other": "Die Uhr zeigt nur Stunden und Minuten.",
    "action_uhr_mit_sekunden_state_unset": (
        "Dazu ist nichts eingestellt; Windows zeigt die Sekunden standardmäßig nicht an."
    ),
    "action_uhr_mit_sekunden_done": "Die Uhr in der Taskleiste zeigt jetzt auch die Sekunden.",
    "action_uhr_mit_sekunden_undone": "Die Uhr ist wieder wie vorher.",
    "action_grosse_schrift_title": "Schrift größer stellen",
    "action_grosse_schrift_description": (
        "Vergrößert die Schrift in Windows auf 125 Prozent — hilfreich, wenn Texte zu "
        "klein sind."
    ),
    "action_grosse_schrift_state_goal": "Die Schrift steht auf 125 Prozent.",
    "action_grosse_schrift_state_other": "Die Schrift steht auf der normalen Größe.",
    "action_grosse_schrift_state_unset": (
        "Dazu ist nichts eingestellt; Windows verwendet 100 Prozent (normale Größe)."
    ),
    "action_grosse_schrift_done": (
        "Die Schrift steht jetzt auf 125 Prozent. Nach dem nächsten Anmelden ist die "
        "Änderung überall zu sehen."
    ),
    "action_grosse_schrift_undone": "Die Schriftgröße ist wieder wie vorher.",
    "action_mausgeschwindigkeit_title": "Maus schneller machen",
    "action_mausgeschwindigkeit_description": (
        "Stellt den Mauszeiger auf die schnellste Stufe."
    ),
    "action_mausgeschwindigkeit_state_goal": "Die Maus steht auf der schnellsten Stufe.",
    "action_mausgeschwindigkeit_state_other": "Die Maus steht nicht auf der schnellsten Stufe.",
    "action_mausgeschwindigkeit_state_unset": (
        "Dazu ist nichts eingestellt; Windows verwendet die mittlere Stufe."
    ),
    "action_mausgeschwindigkeit_done": "Der Mauszeiger ist jetzt auf der schnellsten Stufe.",
    "action_mausgeschwindigkeit_undone": "Die Mausgeschwindigkeit ist wieder wie vorher.",
    "action_menues_sofort_title": "Menüs ohne Verzögerung öffnen",
    "action_menues_sofort_description": (
        "Menüs klappen sofort auf, statt kurz zu warten."
    ),
    "action_menues_sofort_state_goal": "Menüs öffnen sich sofort.",
    "action_menues_sofort_state_other": "Menüs öffnen sich mit Verzögerung.",
    "action_menues_sofort_state_unset": (
        "Dazu ist nichts eingestellt; Windows wartet 400 Tausendstelsekunden, bevor ein "
        "Menü aufklappt."
    ),
    "action_menues_sofort_done": "Menüs öffnen sich jetzt sofort.",
    "action_menues_sofort_undone": "Die Menüverzögerung ist wieder wie vorher.",
    "action_ton_stumm_title": "Ton stumm schalten",
    "action_ton_stumm_description": (
        "Schaltet den Ton stumm, damit nichts mehr zu hören ist."
    ),
    "action_ton_stumm_state_goal": "Der Ton ist stumm.",
    "action_ton_stumm_state_other": "Der Ton ist an.",
    "action_ton_stumm_done": "Der Ton ist jetzt stumm.",
    "action_ton_stumm_undone": "Der Ton ist wieder wie vorher.",
    "action_ton_stumm_unreadable": (
        "Den Ton konnte ich hier nicht ablesen (der Dienst hat {output!r} geantwortet)."
    ),
    "action_windows_tipps_aus_title": "Windows-Tipps und Empfehlungen abschalten",
    "action_windows_tipps_aus_description": (
        "Blendet die Vorschläge aus, die Windows im Startmenü und in den Einstellungen "
        "einblendet."
    ),
    "action_windows_tipps_aus_state_goal": "Die Windows-Tipps sind abgeschaltet.",
    "action_windows_tipps_aus_state_other": "Die Windows-Tipps sind eingeschaltet.",
    "action_windows_tipps_aus_state_unset": (
        "Dazu ist nichts eingestellt; Windows blendet seine Tipps standardmäßig ein."
    ),
    "action_windows_tipps_aus_done": (
        "Windows blendet die Tipps und Empfehlungen jetzt nicht mehr ein."
    ),
    "action_windows_tipps_aus_undone": "Die Windows-Tipps sind wieder wie vorher.",
    # Die zwei Einträge, die nur den Weg zeigen (Administratorrechte,
    # Entscheidung 10): sie haben keinen Zustand, den man ablesen könnte.
    "action_bildschirm_spiegeln_title": "Bildschirm spiegeln",
    "action_bildschirm_spiegeln_description": (
        "Der zweite Bildschirm zeigt dasselbe Bild wie der erste."
    ),
    "action_bildschirm_spiegeln_handover": (
        "Drücke die Windows-Taste zusammen mit P und wähle im Fenster „Duplizieren“ — "
        "dann zeigen beide Bildschirme dasselbe."
    ),
    "action_programm_installieren_title": "Ein Programm installieren",
    "action_programm_installieren_description": (
        "Zeigt den Weg zu einem neuen Programm, ohne selbst etwas zu installieren."
    ),
    "action_programm_installieren_handover": (
        "Öffne im Startmenü den Microsoft Store oder starte die Setup-Datei des "
        "Herstellers im Explorer. Windows fragt dich dann selbst nach der Erlaubnis; "
        "installieren darf ich nichts."
    ),
    # Die Themen, unter denen die Aktionen in der Liste stehen.
    "action_group_explorer": "Explorer und Dateien",
    "action_group_darstellung": "Aussehen und Lesbarkeit",
    "action_group_ton": "Ton",
    "action_group_windows": "Weniger Windows im Weg",
    "action_group_handarbeit": "Das kann nur Windows selbst",
    # Die zwei Einträge mit Administratorrechten: angekündigt, nicht ausgeführt.
    "action_handover_preview": "Das kann ich nicht selbst tun: {title}",
    "action_handover_hint": "So geht es: {hint}",
    "action_handover_rule": (
        "Ich frage dich nie nach dem Windows-Passwort und speichere keine Zugangsdaten."
    ),
    "action_not_self_run": (
        "„{title}“ führe ich nicht selbst aus: Dafür braucht Windows "
        "Administratorrechte. Ich zeige dir, wie du es selbst machst, und ändere nichts."
    ),
    # Der Aktionsabschnitt im Systemtext: was das Modell anbieten darf.
    "actions_header": (
        "Du kannst auf diesem Rechner auch etwas ändern. Dafür stehen dir diese Aktionen "
        "zur Verfügung:"
    ),
    "action_state_line": "- {schluessel}: {title}",
    "action_state_line_admin": "- {schluessel}: {title} (das kann nur Windows selbst)",
    "actions_rule": (
        "Nenne nur Aktionen aus dieser Liste und erfinde weder einen Schlüssel noch einen "
        "eigenen Befehl. Ausgeführt wird eine Aktion erst, wenn der Nutzer sie ausdrücklich "
        "bestätigt; darum kümmert sich das Programm."
    ),
    # Selbstprüfung: Katalog und Protokoll
    "check_actions": "  Aktionen:    {count} ({handover} davon kann nur Windows selbst)",
    "check_log": "  Protokoll:   {path}",
    "check_log_off": "  Protokoll:   aus",

    # --- Erste Schritte (Slice 10): der geführte Weg und der nächste Schritt ---
    # Jede Meldung, die etwas vermisst, nennt den Befehl, der weiterhilft. Der
    # ganze Weg von null bis zum ersten Gespräch steht hinter --hilfe; diese
    # Übersicht ist auch dann erreichbar, wenn die Einstellungen nicht gelesen
    # werden können.
    "check_next_header": "Der nächste Schritt:",
    "next_key": (
        "Schlüssel in die Datei .env eintragen (AI_HELPER_API_KEY=dein-schluessel, "
        "Vorlage: .env.example) — oder den lokalen Betrieb nutzen: --mode lokal"
    ),
    "next_search_key": (
        "Für die Websuche AI_HELPER_SEARCH_KEY in die .env eintragen — oder mit "
        "AI_HELPER_SEARCH=wikipedia auf die Wikipedia umstellen (die braucht keinen "
        "Schlüssel)."
    ),
    "next_help": "Den ganzen Weg von null bis zum ersten Gespräch zeigt: --hilfe",
    "hilfe_header": "AI-Helper — so kommst du von null bis zum ersten Gespräch:",
    "hilfe_system": "  Dein Python: {version}",
    "hilfe_state": "  Dein Stand: {state}",
    "hilfe_state_ready": "startklar — es fehlt nichts",
    "hilfe_state_not_ready": "noch nicht startklar",
    "hilfe_state_unreadable": "die Einstellungen ließen sich nicht lesen (siehe unten)",
    "hilfe_next_header": "Der nächste Schritt:",
    "next_settings": (
        "Zuerst die Einstellungen in Ordnung bringen (die Meldung oben nennt den "
        "Grund); die Vorlage steht in .env.example."
    ),
    "hilfe_ways_header": "Die zwei Wege:",
    "hilfe_way_local": (
        "  A) Ohne Schlüssel, auf deinem eigenen Rechner (lokal):\n"
        "     1. Ollama von ollama.com herunterladen und entpacken — keine "
        "Installation, keine Administratorrechte.\n"
        "     2. Den Dienst starten: ollama serve\n"
        "     3. Das Modell einmalig holen: ollama pull {model}\n"
        "     4. Prüfen, dann starten: --check --mode lokal, danach --mode lokal"
    ),
    "hilfe_way_online": (
        "  B) Über das Netz (online):\n"
        "     1. Die Datei .env.example nach .env kopieren.\n"
        "     2. In .env den Schlüssel eintragen: AI_HELPER_API_KEY=dein-schluessel "
        "(Modell und Adresse stehen schon in der Vorlage: {model} über {base_url}).\n"
        "     3. Prüfen, dann starten: --check, danach ohne weitere Angabe starten"
    ),
    "hilfe_conversation_header": "Im Gespräch:",
    "hilfe_conversation": (
        "  /nachschauen misst deinen Rechner nach\n"
        "  /aktionen zeigt, was ich ändern kann; /aktion <schlüssel> zeigt vorher, "
        "was passiert, und führt erst nach deinem „ja“ aus\n"
        "  /protokoll zeigt, was ich getan habe; /rueckgaengig nimmt das Letzte "
        "zurück\n"
        "  /lernen erklärt die Schritte, statt etwas auszuführen\n"
        "  /suchen <begriff> schlägt im Netz nach und nennt die Quelle\n"
        "  /merken <tatsache> behält etwas über Sitzungen hinweg; /exit beendet"
    ),
    "hilfe_files": (
        "Was auf deinem Rechner liegt: das Gedächtnis ({memory_path}) und das "
        "Aktionsprotokoll ({log_path}) — beide im Klartext und nur für dich."
    ),
    "hilfe_privacy_local": (
        "Was den Rechner verlässt: hier nichts. Das Modell rechnet auf deinem "
        "Rechner. Nur /suchen schickt den Suchbegriff an den Suchdienst — das sagt "
        "dir die Zeile davor an; mit AI_HELPER_SEARCH=aus schaltest du es ab."
    ),
    "hilfe_privacy_online": (
        "Was den Rechner verlässt: deine Frage geht an {base_url}; /suchen schickt "
        "den Suchbegriff an den Suchdienst. Beides wird vorher angesagt. Im lokalen "
        "Betrieb (--mode lokal) bleibt alles auf deinem Rechner."
    ),
    "hilfe_end": "Diese Übersicht bekommst du jederzeit wieder mit: --hilfe",
}

