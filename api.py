# api.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
API_KEY = os.getenv("API_KEY")

def get_weather(city=None, state=None, zip_code=None):
    """
    Fetch current weather data from OpenWeatherMap API.
    Returns:
        (dict, None) on success
        (None, str) on error
    """
    if not API_KEY:
        return None, "API key not found. Check your .env file."

    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "appid": API_KEY,
        "units": "imperial"
    }

    # Build location query
    if zip_code:
        params["zip"] = f"{zip_code},US"
    elif city:
        q = city
        if state:
            q += f",{state},US"
        else:
            q += ",US"
        params["q"] = q
    else:
        return None, "No location provided", "Please enter a city, state, or zip code."

    try:
        response = requests.get(base_url, params=params, timeout=5)
        data = response.json()

        if response.status_code != 200:
            return None, data.get("message", "Error fetching weather")

        return {
            "city": data.get("name"),
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"].capitalize()
        }, None

    except requests.exceptions.RequestException as e:
        return None, f"Network error: {e}"
    except KeyError:
        return None, "Unexpected API response format"

