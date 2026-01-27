import asyncio

try:
    import js
    from pyodide.http import pyfetch    # type: ignore
except ImportError:
    js = None
    pyfetch = None


API_KEY = "514f4f54ee8cf357fe02bfce06d18e60"
CITY = "Barcelona"

URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric&lang=de"


async def load_weather(city=None):
    if js is None or pyfetch is None:
        print("Dieses Skript läuft nur im Browser mit PyScript.")
        return

    container = js.document.getElementById("weather_container")

    # Wenn keine Stadt übergeben, default = Barcelona
    city = city or "Barcelona"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=de"

    try:
        response = await pyfetch(url)
        data = await response.json()

        if data.get("cod") != 200:
            container.innerHTML = f"<p>⚠️ Stadt '{city}' nicht gefunden.</p>"
            return

        temp = round(data["main"]["temp"])
        desc = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]
        icon = data["weather"][0]["icon"]

        icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"

        container.innerHTML = f"""
        <div class="weather_card">
            <div class="weather_header">
                <strong>{city}</strong>
                <img src="{icon_url}" class="weather_icon">
            </div>

            <div class="weather_temp">{temp}°C</div>
            <div class="weather_desc">{desc}</div>

            <div class="weather_row">
                <span>Luftfeuchtigkeit</span><span>{humidity}%</span>
            </div>
            <div class="weather_row">
                <span>Wind</span><span>{wind} m/s</span>
            </div>
        </div>
        """
    except Exception as e:
        js.console.error(e)
        container.innerHTML = "<p>⚠️ Wetterdaten konnten nicht geladen werden</p>"


if js is not None:
    # Funktion für JavaScript verfügbar machen
    js.window.loadWeatherFromPython = load_weather
