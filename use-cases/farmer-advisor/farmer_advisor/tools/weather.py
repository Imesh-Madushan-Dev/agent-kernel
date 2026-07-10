"""Weather tools backed by Open-Meteo (no API key required)."""

# WMO weather codes -> farmer-friendly description
_WMO = {0: "clear sky", 1: "mostly clear", 2: "partly cloudy", 3: "overcast", 45: "fog", 48: "fog", 51: "light drizzle", 53: "drizzle", 55: "heavy drizzle", 61: "light rain", 63: "rain", 65: "heavy rain", 80: "rain showers", 81: "rain showers", 82: "violent rain showers", 95: "thunderstorm", 96: "thunderstorm with hail", 99: "thunderstorm with hail"}


def get_forecast(location: str) -> dict:
    """Get a real 3-day weather forecast for a location (Open-Meteo, no API key).

    :param location: town or district name, e.g. "Kandy"
    """
    import httpx

    try:
        geo = httpx.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location.strip(), "count": 1, "language": "en"},
            timeout=10,
        ).json()
        place = geo["results"][0]
        wx = httpx.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max",
                "forecast_days": 3,
                "timezone": "auto",
            },
            timeout=10,
        ).json()["daily"]
        days = [
            {
                "date": wx["time"][i],
                "condition": _WMO.get(wx["weather_code"][i], "unknown"),
                "temp_max_c": wx["temperature_2m_max"][i],
                "temp_min_c": wx["temperature_2m_min"][i],
                "rain_chance_pct": wx["precipitation_probability_max"][i],
                "max_wind_kmh": wx["wind_speed_10m_max"][i],
            }
            for i in range(len(wx["time"]))
        ]
        return {"location": place["name"], "country": place.get("country", ""), "forecast": days, "source": "open-meteo.com"}
    except (KeyError, IndexError):
        return {"error": f"Could not find location '{location}'. Ask the farmer for the nearest town name."}
    except Exception as e:  # network down -> degrade gracefully, don't crash the agent
        return {"error": f"Weather service unavailable ({type(e).__name__}). Ask the farmer to try again later."}
