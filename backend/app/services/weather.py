import os
import httpx

OWM_URL = "https://api.openweathermap.org/data/2.5/weather"


async def fetch_weather(query: dict) -> dict:
    """Fetch current weather from OpenWeatherMap.

    `query` may contain `city` or `lat` and `lon`.
    Falls back to mock data when `WEATHER_API_KEY` is not set or on error.
    """
    key = os.getenv("WEATHER_API_KEY")
    if not key:
        # fallback mock
        return {
            "provider": "mock",
            "description": "Cloudy",
            "temp_c": 20.0,
            "raw": {"note": "No WEATHER_API_KEY provided; returning mock data."},
        }

    params = {"appid": key, "units": "metric"}
    if query.get("city"):
        params["q"] = query["city"]
    elif query.get("lat") is not None and query.get("lon") is not None:
        params["lat"] = query["lat"]
        params["lon"] = query["lon"]
    else:
        # default: use a generic location
        params["q"] = "London"

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.get(OWM_URL, params=params)
            resp.raise_for_status()
            data = resp.json()
            weather = data.get("weather", [{}])[0].get("description", "")
            temp = data.get("main", {}).get("temp")
            return {
                "provider": "openweathermap",
                "description": weather.title() if weather else "",
                "temp_c": temp,
                "raw": data,
            }
        except Exception as e:
            return {"provider": "openweathermap", "error": str(e), "raw": {}}
