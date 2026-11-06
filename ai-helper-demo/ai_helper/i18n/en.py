# erzeugt von scripts/build_demo.py — nicht von Hand ändern
"""English texts. Fallback language, selected via set_language("en")."""

from __future__ import annotations

TEXTS: dict[str, str] = {
    # Operating mode (Slice 5): online via an API key or local via Ollama.
    "mode_online": "online",
    "mode_lokal": "local",
    "invalid_mode": "Unknown mode {value!r}. Known: {known}.",
    # Conversation
    "welcome": "Hello, I am {name}. Ask me something about your computer.",
    "model_note": "Answers come from {model} ({mode_name}) via {base_url}.",
    "exit_hint": "Use /exit to end the conversation.",
    "memory_hint": (
        "Use /merken <fact> to remember something across sessions, "
        "/gedaechtnis shows it in plain text, /vergessen deletes it."
    ),
    "prompt_user": "You: ",
    "prompt_assistant": "Helper [{model}, {mode_name}]: ",
    "farewell": "Goodbye.",
    "interrupted": "Aborted.",
    # Persona (Slice 3): Name and tone. One section per character so a new
    # language only needs to translate these texts (Decision 7).
    "persona_system": (
        "Your name is {name} and you are a helper assisting people without "
        "technical knowledge with questions about their own computer.\n"
        "{character}\n"
        "Answer in English, simply and concisely. If you don't know something, "
        "say so openly instead of guessing."
    ),
    "persona_memory_header": "Important remembered facts about the user:",
    "persona_memory": (
        "{header}\n{facts}\n"
        "Rely on these facts when they fit the question. What is not here, "
        "you have not remembered."
    ),
    "persona_mira_name": "Mira",
    "persona_mira_character": (
        "Your tone: calm, patient, and factual. You explain in small steps "
        "and without jargon you haven't explained before, and you don't push "
        "yourself forward."
    ),
    "persona_kalle_name": "Kalle",
    "persona_kalle_character": (
        "Your tone: down-to-earth and direct, like a neighborly tinkerer. "
        "You say clearly what you would do and don't mince words."
    ),
    "persona_pico_name": "Pico",
    "persona_pico_character": (
        "Your tone: curious, concise, and sober. You name numbers and "
        "measured values instead of guessing."
    ),
    "invalid_persona": "Unknown character {value!r}. Known: {known}.",
    # Memory
    "memory_usage": "Usage: /merken Your printer is called Berta",
    "memory_saved": "Remembered: {fact}",
    "memory_known": "I already knew that: {fact}",
    "memory_header": "Remembered facts ({count}):",
    "memory_line": "  - {fact}",
    "memory_empty": "I haven't remembered anything yet.",
    "memory_location": "Stored in: {path}",
    "memory_cleared": "Memory cleared ({count} entries).",
    "memory_unavailable": (
        "Memory is not available; I won't remember anything in this conversation."
    ),
    "memory_unreadable": "The memory file {path} cannot be read ({detail}).",
    "memory_corrupt": (
        "The memory file {path} is not readable ({detail}). I start without "
        "memory; delete or repair the file, then it works again."
    ),
    "memory_facts_not_list": "The facts field is not a list.",
    "memory_not_writable": "I could not save the memory ({path}, {detail}).",
    # Avatar labels, one text per state. The key is "avatar_" + value from
    # ai_helper/avatar/states.py.
    "avatar_neutral": "I am ready.",
    "avatar_thinking": "I am thinking ...",
    "avatar_speaking": "I am answering.",
    "avatar_explaining": "I am explaining it to you step by step.",
    "avatar_happy": "Glad I could help.",
    "avatar_error": "That didn't work.",
    # The Demo (Slice D2): fixed provider, fixed measurement report, no
    # execution. The demo mode appears like "online"/"local" in every line.
    "mode_demo": "demo",
    "demo_model_label": "demo-model",
    "demo_measure_source": "Demo report (fixed value, not measured)",
    "demo_runner_unavailable": (
        "In the demo nothing is measured; the values come from a fixed report."
    ),
    "demo_hint": (
        "Demo: No commands are executed, and nothing leaves your browser."
    ),
    "demo_polite_answer": (
        "In this demo I only answer the prepared questions — try one of the "
        "suggestions, or a command like /nachschauen, /aktionen, /protokoll, "
        "or /lernen."
    ),
    "demo_answer_abilities": (
        "I am Mira, a helper for your computer. In this demo I answer a few "
        "prepared questions, list the tested settings with /aktionen and show "
        "you preview, confirmation and rollback — nothing is changed in the demo."
    ),
    "demo_answer_setup": (
        "In this demo a sample computer is configured: Windows 11, a screen "
        "with 1920 x 1080 pixels and an AMD Ryzen 5 7530U. The values are a "
        "fixed demo report, not a measurement of your real computer."
    ),
    "demo_answer_cpu": (
        "The processor in this demo is an AMD Ryzen 5 7530U with Radeon "
        "Graphics with 6 cores (12 simultaneously)."
    ),
    "demo_answer_memory": (
        "In this demo the computer has 15.3 GB of RAM; 7.1 GB are currently "
        "free."
    ),
    "demo_answer_actions": (
        "Yes. With /aktionen I show you the tested settings. With /aktion "
        "<key> you first see in plain text what would happen, and only after "
        "your yes would it be executed. In the demo nothing happens: the demo "
        "executor only writes to the log — and /rueckgaengig rolls the entry "
        "back anyway."
    ),
    "demo_answer_driver": (
        "A device driver is a program that tells Windows how to talk to a "
        "component like a printer, graphics card or keyboard. In this demo I "
        "have no source for that; in real operation I would look it up in the "
        "German Wikipedia."
    ),
    # Nachschauen (Slice 4): Tools read the real system state.
    # Per tool a name for the list and a sentence describing what it checks.
    "tool_windows_version_name": "Windows Version",
    "tool_windows_version_description": (
        "Which Windows version and edition are installed."
    ),
    "tool_cpu_name": "Processor",
    "tool_cpu_description": "Which processor is in the computer and how many cores it has.",
    "tool_screen_resolution_name": "Screen Resolution",
    "tool_screen_resolution_description": "How large the screen is currently set.",
    "tool_graphics_name": "Graphics",
    "tool_graphics_description": "Which graphics chip is in the computer.",
    "tool_memory_name": "Memory",
    "tool_memory_description": (
        "How much memory is installed and how much of it is currently free."
    ),
    "tool_drives_name": "Drives",
    "tool_drives_description": (
        "Which drives exist, how large they are and how much is free."
    ),
    # The name per measured value ("measure_" + key of the value).
    "measure_windows_version": "Windows Version",
    "measure_windows_edition": "Windows Edition",
    "measure_screen_resolution": "Screen Resolution",
    "measure_cpu": "Processor",
    "measure_cpu_cores": "Processor Cores",
    "measure_graphics": "Graphics",
    "measure_memory": "Memory",
    "measure_memory_total": "Memory Total",
    "measure_memory_free": "Memory Free",
    "measure_drives": "Drives",
    "measure_drive_total": "Drive {drive} Total",
    "measure_drive_free": "Drive {drive} Free",
    "value_pixel": "px",
    # The processor in one sentence: the number of simultaneously computable
    # threads is the interesting thing for a beginner, "threads" would be jargon.
    "value_cpu_cores": "{cores} cores ({threads} simultaneously)",
    "value_cpu_cores_single": "1 core ({threads} simultaneously)",
    "value_gb": "GB",
    "measure_header": "Checked ({count} values):",
    "measure_line": "  {label}: {value} {unit}",
    "measure_line_plain": "  {label}: {value}",
    "measure_unmeasurable": "  {label}: not measurable ({detail})",
    "measure_source": "      Source: {source}",
    "measure_no_reason": "no reason given",
    "looking_around": "I'll take a quick look at how your computer is set up ...",
    "nachschauen_hint": (
        "With /nachschauen I check anytime and show you the measured values."
    ),
    # The section that the measured values get in the system prompt.
    "state_tools_header": (
        "You can check the computer. For that these tools are available:"
    ),
    "state_tool_line": "- {name}: {description}",
    "state_values_header": "This is what you just measured on this computer:",
    "state_value_line": "- {label}: {value} {unit}",
    "state_value_plain": "- {label}: {value}",
    "state_value_missing": "- {label}: not measured ({detail})",
    "state_rule": (
        "When you talk about the computer, name these measured values and "
        "guess nothing about them. What is not here you have not measured; "
        "then say openly that you don't know it."
    ),
    # Failed measurements: a message, no crash.
    "tool_command_failed": "The command {command} could not be executed ({detail}).",
    "tool_exit_code": "The command ended with code {code}.",
    "tool_unreadable": "The output was not readable ({output}).",
    "tool_no_output": "The command produced no usable output.",
    "tool_no_value": "The command yielded no value for that.",
    "tool_no_drives": "No drive was reported.",
    "tool_unexpected": "Unexpected error during measurement ({detail}).",
    # Missing settings
    "missing_key": "No API key found, so I cannot query an online model.",
    "missing_key_hint": (
        "Enter it in the .env file: AI_HELPER_API_KEY=your-key "
        "(template: .env.example)."
    ),
    "missing_key_hint_env": (
        "Alternatively set the environment variable AI_HELPER_API_KEY. Without "
        "a key the online mode does not work; without a key the local mode with "
        "Ollama still works (--mode lokal). The whole way is shown by: --hilfe"
    ),
    "missing_model": "No model is configured. Enter AI_HELPER_MODEL in .env.",
    "invalid_timeout": "AI_HELPER_TIMEOUT_S must be a number greater than 0, but is {value!r}.",
    # Self-check
    "check_header": "Settings:",
    "check_model": "  Model:      {model}",
    "check_base_url": "  Base URL:   {base_url}",
    "check_persona": "  Character:  {name} ({persona_key})",
    "check_memory": "  Memory:     {path}",
    "check_memory_off": "  Memory:     off",
    "check_tools": "  Tools:      {count} ({names})",
    "check_key": "  Key:        present ({source})",
    "check_key_missing": "  Key:        missing",
    "check_ready": "Ready.",
    "check_not_ready": "Not ready yet.",
    # Runtime errors
    "error_http": "The provider responded with error {status}: {detail}",
    "error_network": (
        "The connection to the provider failed: {detail}. "
        "Check your internet connection first. Without internet only the local "
        "model on your computer answers (--mode lokal, then Ollama must run); "
        "the whole way is shown by --hilfe."
    ),
    "error_response": "The provider's response was not readable: {detail}",
    "error_empty_answer": "The provider sent an empty answer.",
    # Streaming answers (Slice 5b).
    "error_stream_broken": (
        "The answer broke off mid-stream: {detail}. I did not add the partial "
        "answer to the conversation."
    ),
    "error_stream_unfinished": (
        "The provider did not finish the stream (the end did not arrive)."
    ),
    "error_local_stream": (
        "The local service reported an error mid-stream: {detail}"
    ),
    "stream_fallback": (
        "This provider does not deliver the answer in parts; I fetch it all "
        "at once instead."
    ),
    # Local operation (Slice 5): Ollama on your own computer.
    "error_local_network": (
        "The local service at {url} does not respond ({detail})."
    ),
    # The next step is separate: the self-check shows the same message as
    # reason (there it would be duplicate), the shell attaches it to every
    # failed request in local mode.
    "error_local_next_step": (
        "Next step: start Ollama ('ollama serve') — if not installed yet, "
        "download and unpack from ollama.com; it needs no admin rights. Once "
        "the service runs, 'ai_helper --check --mode lokal' tells exactly "
        "whether the model is already present."
    ),
    "error_local_http": "The local service responded with error {status}: {detail}",
    "error_local_model_missing": (
        "The local model {model} is not present on this computer. "
        "Fetch it once with: ollama pull {model}"
    ),
    "error_local_tags": "The model list of the local service was not readable ({detail}).",
    # Self-check: mode and local service
    "check_mode_online": "  Mode:       online (API key required)",
    "check_mode_local": "  Mode:       local (Ollama at {base_url})",
    "check_local_service": "  Local service: reachable ({count} models)",
    "check_local_model_present": "  Model:      {model} (present)",
    "check_local_model_missing": "  Model:      {model} (not present)",
    "check_local_models": "  Available models: {names}",
    "check_local_unreachable": "  Local service: unreachable ({detail})",
    "check_local_hint": (
        "Next step: start Ollama ('ollama serve') — if not installed yet, "
        "download and unpack from ollama.com; it needs no admin rights. Then "
        "fetch the model once: ollama pull {model}"
    ),
    "check_key_not_needed": "  Key:        not needed (local mode)",
    # Learn mode (Slice 8): Approach C from Design Chapter 6.1 — explain
    # instead of execute. The mode is switchable in conversation (/lernen) and
    # visible like the mode in the greeting, self-check and system prompt.
    "learn_on": "Learn mode on. I explain the steps and do not execute.",
    "learn_off": "Learn mode off. I execute again after your confirmation.",
    "learn_usage": "Usage: /lernen — and /lernen aus switches back to execute.",
    "learn_already_on": "Learn mode is already on.",
    "learn_already_off": "Learn mode is already off.",
    "learn_hint": (
        "With /lernen I explain the steps instead of executing; "
        "/lernen aus switches back."
    ),
    "learn_active_note": (
        "Learn mode: I explain the steps and change nothing. "
        "With /lernen aus I switch back to execute."
    ),
    # The explanation for /aktion <key> in learn mode.
    "learn_action_head": "In learn mode I change nothing. What I would do otherwise: {title}",
    "learn_action_steps": (
        "Here is how you do it yourself in three steps: 1. Open Windows Settings. "
        "2. Search for {title} there. 3. Set it the way you want."
    ),
    "learn_action_rule": (
        "I do not execute anything in this mode — not even a \"yes\" changes anything."
    ),
    "learn_undo_blocked": (
        "In learn mode I roll back nothing and change nothing. "
        "With /lernen aus it works again."
    ),
    # The section in the system prompt: tells the model it is explaining now.
    "learn_section": (
        "You are currently in learn mode.\n"
        "Explain to the user step by step how they can do it themselves, "
        "and do not execute anything yourself: offer no action and name no "
        "command. The actions from the list you may only describe as a way "
        "(\"that's how you would do it\"), not as something you are about to do."
    ),
    "invalid_learn": "Unknown value for learn mode {value!r}. Known: {known}.",
    "check_learn": "  Learn mode: {state}",
    "learn_state_on": "on (I explain, do not execute)",
    "learn_state_off": "off (I execute after confirmation)",
    # Search (Slice 9): look up on the net, with source citation. The service
    # is in settings (AI_HELPER_SEARCH), in conversation /suchen <term> triggers it.
    "search_name_wikipedia": "German Wikipedia",
    "search_name_exa": "Web search via Exa",
    "search_name_aus": "off",
    "search_provider_wikipedia": "the German Wikipedia",
    "search_provider_exa": "the search service Exa",
    "search_hint": (
        "With /suchen <term> I look up on the net and give you the source."
    ),
    "search_usage": "Usage: /suchen How do I turn on the magnifier",
    "search_unavailable": (
        "I cannot look up right now: Search is not configured. "
        "With AI_HELPER_SEARCH=wikipedia in .env I enable it "
        "(template: .env.example) — it needs no key."
    ),
    "search_key_missing": (
        "The web search key is missing; I send nothing. Enter "
        "AI_HELPER_SEARCH_KEY in .env — or switch to Wikipedia with "
        "AI_HELPER_SEARCH=wikipedia (that needs no key)."
    ),
    "search_announce": (
        "I look up: \"{query}\" — this question leaves your computer "
        "and goes to {provider}."
    ),
    "search_sources_header": "Found sources ({count}):",
    "search_source_line": "  {number}. {title} — {url}",
    "search_source_snippet": "      {snippet}",
    "search_no_hits": (
        "For \"{query}\" I found nothing. Making something up doesn't help you."
    ),
    "search_empty_query": "The search query is missing; I don't know what to look for.",
    "search_failed": "The search failed: {detail}",
    "search_http_error": "The search service responded with error {status} ({detail}).",
    "search_no_reason": "no reason given",
    "search_response_unreadable": "The search service's response was not readable ({detail}).",
    "search_no_results_field": "the expected fields are missing",
    # The evidence in the prompt to the model: title, URL and snippet.
    "search_hit_line": "- {title} ({url}): {snippet}",
    "search_question": (
        "My question: {query}\n"
        "\n"
        "I looked it up. These are the found sources:\n"
        "{hits}\n"
        "\n"
        "Answer my question and name the source (title and URL) for every "
        "statement. What is not in these sources you have not looked up."
    ),
    # The section in the system prompt: search yes, cite source yes.
    "search_section": (
        "You can look up on the net (via {provider}).\n"
        "Tell the user they can use /suchen <term> to look up. When sources "
        "are available, rely on them and name the source (title and URL) for "
        "every statement. Invent no source and no URL."
    ),
    "invalid_search": "Unknown value for search {value!r}. Known: {known}.",
    "check_search": "  Search:     {name} ({state})",
    "check_search_state_ready": "configured",
    "check_search_state_key_missing": "key missing",
    "check_search_state_off": "off",
    # Actions (Slice 6): tested actions with preview, confirmation and
    # rollback. The placeholder is called "schluessel" because t() itself has
    # a parameter "key".
    "action_hint": (
        "With /aktionen you see what I can change on this computer; /protokoll "
        "shows what I have done, and /rueckgaengig rolls back the last one."
    ),
    "action_list_header": "Actions ({count}):",
    "action_list_group": "  {title}",
    "action_list_line": "  {schluessel}: {title} — {description}",
    "action_list_hint": (
        "Usage: /aktion dateiendungen — I show beforehand what exactly will "
        "happen and ask."
    ),
    "action_usage": "Usage: /aktion dateiendungen",
    "action_unknown": "I don't know this action: {schluessel!r}. Known: {known}.",
    "action_preview": "I will do: {title}",
    "action_now": "Currently: {state}",
    "action_already": "That is already the case — I don't need to change anything.",
    "action_confirm": "Shall I do it? (yes/no) ",
    "action_declined": "Then not. I changed nothing.",
    "action_done": "Done: {result}",
    "action_unavailable": (
        "The action framework is not available; I change nothing in this conversation."
    ),
    "action_check_failed": "I cannot check that here: {detail}",
    "action_apply_failed": "That didn't work: {detail}",
    "action_undo_failed": "Rolling back didn't work: {detail}",
    "action_not_logged": (
        "The action was executed but I could not log it ({detail}). "
        "I can no longer roll it back."
    ),
    "undo_nothing": "There is nothing to roll back.",
    "undo_done": "Rolled back: {title} — {result}",
    "undo_unknown": "I no longer know an action for this entry ({schluessel!r}).",
    # The log: every executed action in plain text.
    "log_header": "Log ({count} entries):",
    "log_line": "  {time} — {title}",
    "log_reason": "      Reason: {reason}",
    "log_result": "      Result: {result}",
    "log_undo_open": "      Rollback: with /rueckgaengig possible",
    "log_undone": "      Rollback: already rolled back",
    "log_location": "Stored in: {path}",
    "log_empty": "I haven't executed anything yet.",
    "log_unavailable": (
        "The log is not available; I execute nothing in this conversation."
    ),
    "log_unreadable": "The log file {path} cannot be read ({detail}).",
    "log_corrupt": (
        "The log file {path} is not readable ({detail}). I therefore execute "
        "nothing; delete or repair the file, then it works again."
    ),
    "log_actions_not_list": "The actions field is not a list.",
    "log_entry_not_object": "An entry in the log is not an object.",
    "log_entry_incomplete": "An entry in the log is incomplete ({field}).",
    "log_not_writable": "I could not save the log ({path}, {detail}).",
    # The three actions of the catalog: title, description, current state,
    # result text and rollback text.
    "action_dateiendungen_title": "Show file extensions in Explorer",
    "action_dateiendungen_description": (
        "Shows what kind of file it is (.txt, .jpg, .exe)."
    ),
    "action_dateiendungen_state_goal": "File extensions are shown.",
    "action_dateiendungen_state_other": "File extensions are hidden.",
    "action_dateiendungen_state_unset": (
        "Nothing is set for this; Windows hides file extensions by default."
    ),
    "action_dateiendungen_done": "File extensions are now shown in Explorer.",
    "action_dateiendungen_undone": "File extensions are back as before.",
    "action_versteckte_dateien_title": "Show hidden files in Explorer",
    "action_versteckte_dateien_description": (
        "Shows files and folders that Windows hides."
    ),
    "action_versteckte_dateien_state_goal": "Hidden files are shown.",
    "action_versteckte_dateien_state_other": "Hidden files are not shown.",
    "action_versteckte_dateien_state_unset": (
        "Nothing is set for this; Windows hides hidden files by default."
    ),
    "action_versteckte_dateien_done": "Hidden files are now shown in Explorer.",
    "action_versteckte_dateien_undone": "Hidden files are back as before.",
    "action_dunkler_modus_title": "Enable dark mode",
    "action_dunkler_modus_description": "Switches apps and windows to dark colors.",
    "action_dunkler_modus_state_goal": "Dark mode is enabled.",
    "action_dunkler_modus_state_other": "Light mode is enabled.",
    "action_dunkler_modus_state_unset": (
        "Nothing is set for this; Windows uses light mode by default."
    ),
    "action_dunkler_modus_done": "Apps and windows are now displayed in dark mode.",
    "action_dunkler_modus_undone": "Display is back as before.",
    # The further actions of the catalog (Slice 7).
    "action_zuletzt_dateien_aus_title": "Hide recently used files",
    "action_zuletzt_dateien_aus_description": (
        "Hides the list of recently opened files in Explorer."
    ),
    "action_zuletzt_dateien_aus_state_goal": "Recently used files are not shown.",
    "action_zuletzt_dateien_aus_state_other": "Recently used files are shown.",
    "action_zuletzt_dateien_aus_state_unset": (
        "Nothing is set for this; Windows shows recently used files by default."
    ),
    "action_zuletzt_dateien_aus_done": "Recently used files are no longer shown.",
    "action_zuletzt_dateien_aus_undone": "The list is back as before.",
    "action_uhr_mit_sekunden_title": "Show seconds in clock",
    "action_uhr_mit_sekunden_description": (
        "Shows seconds in the taskbar clock."
    ),
    "action_uhr_mit_sekunden_state_goal": "The clock shows seconds.",
    "action_uhr_mit_sekunden_state_other": "The clock shows only hours and minutes.",
    "action_uhr_mit_sekunden_state_unset": (
        "Nothing is set for this; Windows does not show seconds by default."
    ),
    "action_uhr_mit_sekunden_done": "The taskbar clock now also shows seconds.",
    "action_uhr_mit_sekunden_undone": "The clock is back as before.",
    "action_grosse_schrift_title": "Increase text size",
    "action_grosse_schrift_description": (
        "Increases text size in Windows to 125 percent — helpful if texts are "
        "too small."
    ),
    "action_grosse_schrift_state_goal": "Text size is at 125 percent.",
    "action_grosse_schrift_state_other": "Text size is at normal size.",
    "action_grosse_schrift_state_unset": (
        "Nothing is set for this; Windows uses 100 percent (normal size)."
    ),
    "action_grosse_schrift_done": (
        "Text size is now at 125 percent. After the next sign-in the change "
        "is visible everywhere."
    ),
    "action_grosse_schrift_undone": "Text size is back as before.",
    "action_mausgeschwindigkeit_title": "Make mouse faster",
    "action_mausgeschwindigkeit_description": (
        "Sets the mouse pointer to the fastest speed."
    ),
    "action_mausgeschwindigkeit_state_goal": "Mouse is at the fastest speed.",
    "action_mausgeschwindigkeit_state_other": "Mouse is not at the fastest speed.",
    "action_mausgeschwindigkeit_state_unset": (
        "Nothing is set for this; Windows uses the middle speed."
    ),
    "action_mausgeschwindigkeit_done": "The mouse pointer is now at the fastest speed.",
    "action_mausgeschwindigkeit_undone": "Mouse speed is back as before.",
    "action_menues_sofort_title": "Open menus without delay",
    "action_menues_sofort_description": (
        "Menus open immediately instead of waiting briefly."
    ),
    "action_menues_sofort_state_goal": "Menus open instantly.",
    "action_menues_sofort_state_other": "Menus open with delay.",
    "action_menues_sofort_state_unset": (
        "Nothing is set for this; Windows waits 400 milliseconds before a "
        "menu opens."
    ),
    "action_menues_sofort_done": "Menus now open instantly.",
    "action_menues_sofort_undone": "Menu delay is back as before.",
    "action_ton_stumm_title": "Mute sound",
    "action_ton_stumm_description": (
        "Mutes the sound so nothing is heard."
    ),
    "action_ton_stumm_state_goal": "Sound is muted.",
    "action_ton_stumm_state_other": "Sound is on.",
    "action_ton_stumm_done": "Sound is now muted.",
    "action_ton_stumm_undone": "Sound is back as before.",
    "action_ton_stumm_unreadable": (
        "I could not read the sound state here (the service responded with {output!r})."
    ),
    "action_windows_tipps_aus_title": "Turn off Windows tips",
    "action_windows_tipps_aus_description": (
        "Hides the suggestions that Windows shows in the Start menu and Settings."
    ),
    "action_windows_tipps_aus_state_goal": "Windows tips are turned off.",
    "action_windows_tipps_aus_state_other": "Windows tips are turned on.",
    "action_windows_tipps_aus_state_unset": (
        "Nothing is set for this; Windows shows its tips by default."
    ),
    "action_windows_tipps_aus_done": "Windows no longer shows tips and recommendations.",
    "action_windows_tipps_aus_undone": "Windows tips are back as before.",
    # The two entries that only show the way (admin rights, Decision 10):
    # they have no state that can be read.
    "action_bildschirm_spiegeln_title": "Mirror screen",
    "action_bildschirm_spiegeln_description": (
        "The second screen shows the same image as the first."
    ),
    "action_bildschirm_spiegeln_handover": (
        "Press the Windows key together with P and choose \"Duplicate\" in the "
        "window — then both screens show the same."
    ),
    "action_programm_installieren_title": "Install a program",
    "action_programm_installieren_description": (
        "Shows the way to a new program without installing anything myself."
    ),
    "action_programm_installieren_handover": (
        "Open the Microsoft Store in the Start menu or run the manufacturer's "
        "setup file in Explorer. Windows will then ask you for permission; "
        "I may not install anything."
    ),
    # The themes under which the actions are listed.
    "action_group_explorer": "Explorer and Files",
    "action_group_darstellung": "Appearance and Readability",
    "action_group_ton": "Sound",
    "action_group_windows": "Less Windows in the Way",
    "action_group_handarbeit": "Only Windows Can Do This",
    # The two entries with admin rights: announced, not executed.
    "action_handover_preview": "I cannot do this myself: {title}",
    "action_handover_hint": "Here is how: {hint}",
    "action_handover_rule": (
        "I never ask for the Windows password and do not store credentials."
    ),
    "action_not_self_run": (
        "\"{title}\" I do not execute myself: Windows needs "
        "admin rights for that. I show you how to do it yourself and change nothing."
    ),
    # The action section in the system prompt: what the model may offer.
    "actions_header": (
        "You can also change something on this computer. For that these actions "
        "are available:"
    ),
    "action_state_line": "- {schluessel}: {title}",
    "action_state_line_admin": "- {schluessel}: {title} (only Windows can do this)",
    "actions_rule": (
        "Name only actions from this list and invent neither a key nor a "
        "command of your own. An action is executed only when the user "
        "explicitly confirms it; the program takes care of that."
    ),
    # Self-check: Catalog and Log
    "check_actions": "  Actions:    {count} ({handover} of which only Windows can do)",
    "check_log": "  Log:        {path}",
    "check_log_off": "  Log:        off",
    # --- First steps (Slice 10): the guided way and the next step ---
    # Every message that misses something names the command that helps. The
    # whole way from zero to the first conversation is behind --hilfe; this
    # overview is also reachable when settings cannot be read.
    "check_next_header": "Next step:",
    "next_key": (
        "Enter the key in the .env file (AI_HELPER_API_KEY=your-key, "
        "template: .env.example) — or use local mode: --mode lokal"
    ),
    "next_search_key": (
        "For web search enter AI_HELPER_SEARCH_KEY in .env — or switch to "
        "Wikipedia with AI_HELPER_SEARCH=wikipedia (that needs no key)."
    ),
    "next_help": "The whole way from zero to the first conversation is shown by: --hilfe",
    "hilfe_header": "AI-Helper — how to get from zero to the first conversation:",
    "hilfe_system": "  Your Python: {version}",
    "hilfe_state": "  Your status: {state}",
    "hilfe_state_ready": "ready — nothing is missing",
    "hilfe_state_not_ready": "not ready yet",
    "hilfe_state_unreadable": "settings could not be read (see below)",
    "hilfe_next_header": "Next step:",
    "next_settings": (
        "First fix the settings (the message above names the reason); the "
        "template is in .env.example."
    ),
    "hilfe_ways_header": "The two ways:",
    "hilfe_way_local": (
        "  A) Without key, on your own computer (local):\n"
        "     1. Download and unpack Ollama from ollama.com — no installation, "
        "no admin rights.\n"
        "     2. Start the service: ollama serve\n"
        "     3. Fetch the model once: ollama pull {model}\n"
        "     4. Check, then start: --check --mode lokal, then --mode lokal"
    ),
    "hilfe_way_online": (
        "  B) Over the net (online):\n"
        "     1. Copy .env.example to .env.\n"
        "     2. In .env enter the key: AI_HELPER_API_KEY=your-key "
        "(model and address are already in the template: {model} via {base_url}).\n"
        "     3. Check, then start: --check, then start without further args"
    ),
    "hilfe_conversation_header": "In conversation:",
    "hilfe_conversation": (
        "  /nachschauen measures your computer\n"
        "  /aktionen shows what I can change; /aktion <key> shows beforehand "
        "what happens and executes only after your \"yes\"\n"
        "  /protokoll shows what I did; /rueckgaengig rolls back the last one\n"
        "  /lernen explains the steps instead of executing\n"
        "  /suchen <term> looks up on the net and names the source\n"
        "  /merken <fact> remembers something across sessions; /exit ends it"
    ),
    "hilfe_files": (
        "What lies on your computer: the memory ({memory_path}) and the "
        "action log ({log_path}) — both in plain text and only for you."
    ),
    "hilfe_privacy_local": (
        "What leaves the computer: nothing here. The model computes on your "
        "computer. Only /suchen sends the search term to the search service — "
        "the line before tells you that; with AI_HELPER_SEARCH=aus you turn it off."
    ),
    "hilfe_privacy_online": (
        "What leaves the computer: your question goes to {base_url}; /suchen "
        "sends the search term to the search service. Both are announced "
        "beforehand. In local mode (--mode lokal) everything stays on your computer."
    ),
    "hilfe_end": "You get this overview anytime with: --hilfe",
}
