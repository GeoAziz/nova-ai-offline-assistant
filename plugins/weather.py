"""
Example Weather Plugin for Nova
"""
import os
import requests

def run(context):
    api_key = os.environ.get("OPENWEATHER_API_KEY")
    city = os.environ.get("NOVA_WEATHER_CITY", "London")
    if not api_key:
        return "Weather API key not set. Set OPENWEATHER_API_KEY env variable."
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        resp = requests.get(url, timeout=5)
        data = resp.json()
        if resp.status_code == 200:
            desc = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"Weather in {city}: {desc}, {temp}°C."
        else:
            return f"Weather API error: {data.get('message', 'Unknown error')}"
    except Exception as e:
        return f"Weather fetch error: {e}"
