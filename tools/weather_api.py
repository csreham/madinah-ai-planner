import requests


def get_weather(latitude, longitude):

    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={latitude}"
        f"&longitude={longitude}"
        "&current=temperature_2m,weather_code"
    )

    response = requests.get(url)

    data = response.json()

    return data["current"]