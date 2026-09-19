"""
Outdoor running weather conditions tool for FitGear Coach agent using Open-Meteo public API.
"""
from typing import Dict, Any
import urllib.request
import urllib.parse
import json


def get_outdoor_running_conditions(city_name: str) -> Dict[str, Any]:
    """
    Fetch real-time outdoor weather and running conditions for a city using Open-Meteo public API.

    Args:
        city_name: Name of the city (e.g. 'Boston', 'New York', 'San Francisco').

    Returns:
        Dictionary with live temperature (°C/°F), wind speed, humidity, precipitation, and summary.
    """
    try:
        encoded_city = urllib.parse.quote(city_name)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1"

        req = urllib.request.Request(geo_url, headers={"User-Agent": "FitGearCoach/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            geo_data = json.loads(resp.read().decode())

        if not geo_data.get("results"):
            return {"error": f"City '{city_name}' not found."}

        location = geo_data["results"][0]
        lat, lon = location["latitude"], location["longitude"]
        found_city = location.get("name", city_name)
        country = location.get("country", "")

        weather_url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,wind_speed_10m"
        )

        req_w = urllib.request.Request(weather_url, headers={"User-Agent": "FitGearCoach/1.0"})
        with urllib.request.urlopen(req_w, timeout=5) as resp_w:
            current = json.loads(resp_w.read().decode()).get("current", {})

        temp_c = current.get("temperature_2m", 0.0)
        temp_f = round((temp_c * 9 / 5) + 32, 1)

        return {
            "city": f"{found_city}, {country}".strip(", "),
            "temperature_celsius": temp_c,
            "temperature_fahrenheit": temp_f,
            "feels_like_celsius": current.get("apparent_temperature"),
            "humidity_percent": current.get("relative_humidity_2m"),
            "wind_speed_kmh": current.get("wind_speed_10m"),
            "precipitation_mm": current.get("precipitation"),
            "conditions_summary": (
                "Ideal outdoor running weather"
                if 40 <= temp_f <= 78 and current.get("precipitation", 0) == 0
                else "Adjust layers/gear for temperature or precipitation"
            ),
        }
    except Exception as e:
        return {"error": f"Failed to fetch weather data: {str(e)}"}
