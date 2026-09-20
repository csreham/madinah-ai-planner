from scripts.fetch_places import fetch_places


class PlacesAgent:

    def run(self, city, max_places=200):

        places = fetch_places(
          city=city,
          max_places=max_places
        )
            
        return places


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    city = "Madinah"

    agent = PlacesAgent()

    places = agent.run(
        city=city,
        max_places=200
    )

    print("\nFirst 5 places:\n")

    for place in places[:5]:

        print("-" * 50)

        print(f"Name: {place.get('name')}")
        print(f"Rating: {place.get('rating')}")
        print(f"Reviews: {place.get('reviews')}")
        print(f"Type: {place.get('type')}")
        print(f"Address: {place.get('address')}")
        print(f"Latitude: {place.get('latitude')}")
        print(f"Longitude: {place.get('longitude')}")
        print(f"Hours: {place.get('hours')}")
        print(f"Image: {place.get('image')}")