from scripts.fetch_restaurants import fetch_restaurants


class RestaurantAgent:

    def run(self, city, max_restaurants=200):

        restaurants = fetch_restaurants(
            city=city,
            max_restaurants=max_restaurants
        )

        return restaurants


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    agent = RestaurantAgent()

    restaurants = agent.run(
        city="Madinah",
        max_restaurants=200
    )

    print("\nFirst 5 restaurants:\n")

    for restaurant in restaurants[:5]:

        print("-" * 50)

        print(f"Name: {restaurant['name']}")
        print(f"Rating: {restaurant['rating']}")
        print(f"Reviews: {restaurant['reviews']}")
        print(f"Price: {restaurant['price']}")
        print(f"Type: {restaurant['type']}")
        print(f"Address: {restaurant['address']}")
        print(f"Latitude: {restaurant['latitude']}")
        print(f"Longitude: {restaurant['longitude']}")
        print(f"Image: {restaurant['image']}")