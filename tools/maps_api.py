import requests


def get_places(latitude, longitude):

    query = f"""
    [out:json];

    node
      ["tourism"="attraction"]
      (around:5000,{latitude},{longitude});

    out;
    """

    url = "https://overpass-api.de/api/interpreter"

    headers = {
        "User-Agent": "AI-Agent-Tourism/1.0 (learning project)"
    }

    response = requests.post(
     url,
     data={"data": query},
     headers=headers,
     timeout=30
    )
    response = requests.get(...)

    print("Status Code:", response.status_code)
    print("Response:")
    print(response.text)

    data = response.json()

    places = []

    for place in data["elements"]:

        tags = place.get("tags", {})

        name = (
        tags.get("name")
        or tags.get("name:en")
    )
        if name:
            places.append({
                "name": name,
                "latitude": place["lat"],
                "longitude": place["lon"]
            })

    return places


# هذا الجزء للاختبار فقط
if __name__ == "__main__":

    places = get_places(24.4709, 39.6122)

    print(places)