import asyncio  # 📦 Asynchrone Programmierung für API-Calls ohne UI-Blockade

# 🛡️ PyScript/Pyodide Imports (im Browser verfügbar)
try:
    import js
    from pyodide.http import pyfetch  # type: ignore
except ImportError:
    js = None
    pyfetch = None


async def _fetch_json(url: str):
    """Hilfsfunktion: URL laden und JSON zurückgeben, mit klarer Fehlerausgabe."""
    response = await pyfetch(url)
    if not response.ok:
        raise OSError(f"HTTP {response.status} bei {url}")
    return await response.json()


async def load_weather(city=None):
    """Lädt Wetterdaten für eine Stadt und rendert das Widget im Modal."""
    city = (city or "Hannover").strip()

    container = js.document.getElementById("weather_container")
    if not container:
        return

    container.innerHTML = "<p>🔄 Wetter wird geladen...</p>"

    try:
        # 1) Geocoding: Stadt -> Koordinaten (Open-Meteo, kein API-Key nötig)
        geo_url = (
            "https://geocoding-api.open-meteo.com/v1/search"
            f"?name={city}&count=1&language=de&format=json"
        )
        geo_data = await _fetch_json(geo_url)

        results = geo_data.get("results") or []
        if not results:
            container.innerHTML = f"<p>⚠️ Stadt nicht gefunden: {city}</p>"
            return

        place = results[0]
        lat = place["latitude"]
        lon = place["longitude"]
        resolved_name = place.get("name", city)

        # 2) Wetterdaten über Koordinaten laden
        weather_url = (
            "https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code"
            "&timezone=auto"
        )
        weather_data = await _fetch_json(weather_url)
        current = weather_data.get("current", {})

        temp = round(current.get("temperature_2m", 0))
        humidity = current.get("relative_humidity_2m", "-")
        wind = current.get("wind_speed_10m", "-")
        weather_code = int(current.get("weather_code", -1))

        # Einfache Code->Text Zuordnung (deutsch)
        weather_map = {
            0: "Klarer Himmel",
            1: "Überwiegend klar",
            2: "Teilweise bewölkt",
            3: "Bedeckt",
            45: "Nebel",
            48: "Reifnebel",
            51: "Leichter Nieselregen",
            53: "Nieselregen",
            55: "Starker Nieselregen",
            61: "Leichter Regen",
            63: "Regen",
            65: "Starker Regen",
            71: "Leichter Schneefall",
            73: "Schneefall",
            75: "Starker Schneefall",
            80: "Regenschauer",
            81: "Starke Regenschauer",
            82: "Heftige Regenschauer",
            95: "Gewitter",
        }
        desc = weather_map.get(weather_code, "Wetterdaten verfügbar")

        container.innerHTML = f"""
        <div class="weather_card">
            <div class="weather_search_inner">
                <input type="text" id="weather_input" placeholder="Stadt eingeben...">
                <button id="weather_search_btn" type="button">Suchen</button>
            </div>
            <div class="weather_header">
                <strong>{resolved_name}</strong>
            </div>
            <div class="weather_temp">{temp}°C</div>
            <div class="weather_desc">{desc}</div>
            <div class="weather_row"><span>Luftfeuchtigkeit</span><span>{humidity}%</span></div>
            <div class="weather_row"><span>Wind</span><span>{wind} km/h</span></div>
        </div>
        """

        from pyodide.ffi import create_proxy  # type: ignore

        btn_el = js.document.getElementById("weather_search_btn")

        async def search_again(event=None):
            if event:
                event.preventDefault()
            city_name = js.document.getElementById("weather_input").value.strip()
            if city_name:
                await load_weather(city_name)

        btn_el.addEventListener("click", create_proxy(search_again))

    except Exception as e:
        container.innerHTML = f"<p>⚠️ Fehler beim Laden: {e}</p>"


# 🌐 Funktion für JavaScript verfügbar machen
if js is not None:
    js.window.loadWeatherFromPython = load_weather
