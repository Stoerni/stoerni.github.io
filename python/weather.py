import asyncio  # 📦 Modul für asynchrone Programmierung (wartet auf API-Antwort ohne zu blockieren)

# 🛡️ TRY-EXCEPT: Versucht zu importieren, wenn es nicht funktioniert macht es nichts falsch
try:
    # 🌐 js = Zugang zu JavaScript vom Browser aus (PyScript Bridge)
    # Mit "js" können wir HTML ändern, Buttons klicken, etc. von Python aus
    import js
    
    # 🌐 pyfetch = Python-Version von JavaScript fetch (lädt Daten von APIs)
    # Es ist asynchron, also warten wir mit await darauf
    from pyodide.http import pyfetch    # type: ignore
except ImportError:
    # Falls PyScript nicht verfügbar ist (lädt nur als normales Python Script)
    js = None
    pyfetch = None


# 🌤️ ASYNC FUNKTION: "async" = Diese Funktion kann warten, ohne zu blockieren
# Das ist wichtig, weil API-Anfragen Zeit brauchen
async def load_weather(city=None):
    # 📍 Stadtname setzen: Falls kein Name übergeben, Barcelona als Standard
    # city or "Barcelona" = wenn city=None oder "", nimm Barcelona
    city = city or "Barcelona"

    # 🎯 HTML-Element abrufen, wo das Wetter angezeigt wird
    # js.document = JavaScript document von Browser aus
    container = js.document.getElementById("weather_container")
    
    # 📍 Loader-Text anzeigen (so weiß der Nutzer dass was lädt)
    # innerHTML = HTML-Inhalt des Elements
    # 🔄 = animiertes Ladezeichen (Unicode)
    container.innerHTML = "<p>🔄 Wetter wird geladen...</p>"

    # 🌐 API-REQUEST: Daten vom Wetter-Backend abrufen
    # f""" = f-String (Python kann Variablen direkt einfügen)
    # ${city} wird mit der Stadt ersetzt (z.B. "Berlin")
    # await = Warten bis die Antwort kommt (nicht blockierend!)
    response = await pyfetch(
        f"https://weather-api-b6ta.onrender.com/weather?city={city}"
    )
    
    # 📦 JSON-Daten aus der Antwort extrahieren
    # data = dictionary mit Temperatur, Wetterbeschreibung, etc.
    data = await response.json()

    # 🛡️ FEHLER-ÜBERPRÜFUNG: Wurde die Stadt gefunden?
    # "main" = Temperatur-Daten (muss in der API-Antwort vorhanden sein)
    if "main" not in data:
        # Fehler anzeigen
        # data.get('error', 'Stadt nicht gefunden') = 
        # Wenn es einen error gibt, zeig ihn, sonst Standard-Text
        container.innerHTML = f"<p>⚠️ Fehler: {data.get('error', 'Stadt nicht gefunden')}</p>"
        return  # Funktion beenden, nicht weiter machen

    # 📊 WETTERDATEN AUS API EXTRAHIEREN:
    # data["main"]["temp"] = Temperatur im dictionary
    # round() = Rundet auf nächste ganze Zahl (20.7 → 21)
    temp = round(data["main"]["temp"])
    
    # 📝 Wetterbeschreibung (z.B. "teilweise bewölkt")
    # [0] = erste Wetter-Bedingung (kann mehrere geben)
    # .capitalize() = Großbuchstabe am Anfang (kleinbuchstaben, → Kleinbuchstaben,)
    desc = data["weather"][0]["description"].capitalize()
    
    # 💧 Luftfeuchtigkeit in Prozent
    humidity = data["main"]["humidity"]
    
    # 💨 Windgeschwindigkeit in Meter pro Sekunde
    wind = data["wind"]["speed"]
    
    # 🎨 Wetter-Icon Code von OpenWeather (z.B. "01d" = klarer Tag)
    icon = data["weather"][0]["icon"]
    
    # 🔗 Komplette Icon-URL zusammenbauen
    # f-String wieder: ${icon} wird mit Code ersetzt
    # @2x.png = Version in hoher Qualität (2x Auflösung)
    icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

    # 🎨 WETTERKARTE MIT HTML GENERIEREN
    # f-String mit dreifachen Anführungszeichen = Multi-line String
    # Alle Variablen werden automatisch eingebaut:
    container.innerHTML = f"""
    <div class="weather_card">
        <div class="weather_search_inner">
            <!-- Input-Feld für neue Stadtsuche -->
            <input type="text" id="weather_input" placeholder="Stadt eingeben...">
            <button id="weather_search_btn" type="button">Suchen</button>
        </div>
        <div class="weather_header">
            <!-- Stadtname und Wetter-Icon -->
            <strong>{city}</strong>
            <img src="{icon_url}" class="weather_icon">
        </div>
        <!-- Große Temperatur-Anzeige -->
        <div class="weather_temp">{temp}°C</div>
        <!-- Wetterbeschreibung (z.B. "teilweise bewölkt") -->
        <div class="weather_desc">{desc}</div>
        <!-- Weitere Daten: Luftfeuchtigkeit und Wind -->
        <div class="weather_row"><span>Luftfeuchtigkeit</span><span>{humidity}%</span></div>
        <div class="weather_row"><span>Wind</span><span>{wind} m/s</span></div>
    </div>
    """
    
    # 🔗 BUTTONS MIT EVENT-LISTENERN VERBINDEN
    # create_proxy = konvertiert Python-Funktion zu JavaScript-Funktion
    from pyodide.ffi import create_proxy    # type: ignore

    # Input-Feld abrufen (wo Nutzer neue Stadt eingibt)
    input_el = js.document.getElementById("weather_input")
    # Button abrufen (um neue Wettersuche zu starten)
    btn_el = js.document.getElementById("weather_search_btn")

    # 🔁 ASYNC FUNKTION: Was passiert wenn Button geklickt wird?
    async def search_again(event=None):
        # event = Browser-Event vom Button-Click
        # event.preventDefault() = Standard-Verhalten verhindern (z.B. Form Submit)
        if event:
            event.preventDefault()
        
        # 📝 Neue Stadt aus Input-Feld auslesen
        city_name = js.document.getElementById("weather_input").value
        # .value = Wert des Input-Feldes
        
        # 🎯 Falls Nutzer Text eingegeben hat, neues Wetter laden
        if city_name:
            # Rekursiver Aufruf: load_weather wird mit neuer Stadt aufgerufen
            await load_weather(city_name)

    # 🖱️ Event-Listener am Button attachen
    # addEventListener = Button beobachten auf Clicks
    # create_proxy = damit Browser die Python-Funktion versteht
    btn_el.addEventListener("click", create_proxy(search_again))

# 🌐 DIESE FUNKTION FÜR JAVASCRIPT VERFÜGBAR MACHEN
# Falls PyScript lädt (js ist nicht None):
if js is not None:
    # window.loadWeatherFromPython = diese Python-Funktion im JavaScript verfügbar machen
    # So kann JavaScript die Python-Funktion aufrufen (z.B. von modal.js)
    js.window.loadWeatherFromPython = load_weather