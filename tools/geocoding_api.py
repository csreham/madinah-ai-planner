import requests


def get_coordinates(city):

    url = "https://nominatim.openstreetmap.org/search"

    headers = {
        "User-Agent": "AI-Agent-Tourism/1.0 (learning project)"
    }

    params = {
        "q": city,
        "format": "json",
        "limit": 1
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        return None

    return {
        "latitude": float(data[0]["lat"]),
        "longitude": float(data[0]["lon"])
    }