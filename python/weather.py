import asyncio

try:
    import js
    from pyodide.http import pyfetch    # type: ignore
except ImportError:
    js = None
    pyfetch = None


async def load_weather(city=None):
    city = city or "Barcelona"

    container = js.document.getElementById("weather_container")
    # 🔄 Loader anzeigen, solange wir auf die API warten
    container.innerHTML = "<p>🔄 Wetter wird geladen...</p>"

    # API Request
    response = await pyfetch(
        f"https://weather-api-b6ta.onrender.com/weather?city={city}"
    )
    data = await response.json()

    # Fehlerabfrage
    if "main" not in data:
        container.innerHTML = f"<p>⚠️ Fehler: {data.get('error', 'Stadt nicht gefunden')}</p>"
        return

    temp = round(data["main"]["temp"])
    desc = data["weather"][0]["description"].capitalize()
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]
    icon = data["weather"][0]["icon"]
    icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

    # Wetterkarte anzeigen
    container.innerHTML = f"""
    <div class="weather_card">
        <div class="weather_search_inner">
            <input type="text" id="weather_input" placeholder="Stadt eingeben...">
            <button id="weather_search_btn" type="button">Suchen</button>
        </div>
        <div class="weather_header">
            <strong>{city}</strong>
            <img src="{icon_url}" class="weather_icon">
        </div>
        <div class="weather_temp">{temp}°C</div>
        <div class="weather_desc">{desc}</div>
        <div class="weather_row"><span>Luftfeuchtigkeit</span><span>{humidity}%</span></div>
        <div class="weather_row"><span>Wind</span><span>{wind} m/s</span></div>
    </div>
    """
    
    from pyodide.ffi import create_proxy    # type: ignore

    input_el = js.document.getElementById("weather_input")
    btn_el = js.document.getElementById("weather_search_btn")

    async def search_again(event=None):
        if event:
            event.preventDefault()  # verhindert Scroll/Reload
        city_name = input_el.value
        if city_name:
            await load_weather(city_name)

    btn_el.addEventListener("click", create_proxy(search_again))

    def handle_key(e):
        key = e.get("key", None)  # <-- sicher auf key zugreifen
        if key == "Enter":
            asyncio.ensure_future(search_again())


    input_el.addEventListener("keydown", create_proxy(handle_key))

if js is not None:

    js.window.loadWeatherFromPython = load_weather
