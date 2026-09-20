from serpapi import GoogleSearch


def fetch_restaurants(city, max_restaurants=200):

    all_restaurants = []
    seen_restaurants = set()

    start = 0

    while len(all_restaurants) < max_restaurants:

        print("=" * 50)
        print(f"Fetching restaurants... start={start}")

        params = {
            "engine": "google_maps",
            "q": f"restaurants in {city}",
            "type": "search",
            "google_domain": "google.com",
            "gl": "sa",
            "hl": "en",

            # ضعي مفتاح SerpApi هنا
            "api_key":"60117fe5faf01fa968183de224efb1721b565f45e2ce2be878c4a4273098b91c",

            # Pagination
            "start": start
        }

        search = GoogleSearch(params)

        results = search.get_dict()
        print(results["local_results"][0])
        
        # التحقق من وجود خطأ
        if "error" in results:

            print("SerpApi Error:")
            print(results["error"])

            break

        restaurants = results.get(
            "local_results", []
        )

        print(
            f"Restaurants received: "
            f"{len(restaurants)}"
        )
        
        # لا توجد نتائج
        if not restaurants:

            print("No more restaurants found.")

            break

        old_count = len(all_restaurants)

        # معالجة النتائج
        for restaurant in restaurants:

            name = restaurant.get("title")

            if not name:
                continue
            price = restaurant.get("price")
            if not price:
                continue
            # منع التكرار
            if name in seen_restaurants:
                continue

            seen_restaurants.add(name)

            all_restaurants.append({
                  "name": name,
                 "rating": restaurant.get("rating"),
                 "reviews": restaurant.get("reviews"),
                 "price": restaurant.get("price"),
                 "type": restaurant.get("type"),
                 "address": restaurant.get("address"),

                "latitude": restaurant.get(
                "gps_coordinates", {}
                ).get("latitude"),

               "longitude": restaurant.get(
               "gps_coordinates", {}
              ).get("longitude"),

               "image": restaurant.get("thumbnail"),

              "website": restaurant.get("website"),
              "phone": restaurant.get("phone"),
              "hours": restaurant.get("hours")
})

                
        print(
        f"Added: {name} | "
        f"Rating: {restaurant.get('rating')} | "
        f"Price: {restaurant.get('price')}"
        )
        if len(all_restaurants) >= max_restaurants:

              break
        print(
            f"Total unique restaurants: "
            f"{len(all_restaurants)}"
        )

        # إذا لم تتم إضافة أي مطعم جديد
        if len(all_restaurants) == old_count:

            print(
                "No new restaurants found. "
                "Stopping."
            )

            break

        # التأكد من وجود صفحة تالية
        pagination = results.get(
            "serpapi_pagination",
            {}
        )

        next_url = pagination.get("next")

        if not next_url:

            print(
                "No next page available."
            )

            break

        # الانتقال للصفحة التالية
        start += len(restaurants)
        # بعد انتهاء while

    with_price = sum(
        1 for restaurant in all_restaurants
        if restaurant.get("price")
    )

    without_price = (
        len(all_restaurants) - with_price
    )

    print("=" * 50)

    print(
        f"Total unique restaurants collected: "
        f"{len(all_restaurants)}"
    )

    print(
        f"Restaurants with price: "
        f"{with_price}"
    )

    print(
        f"Restaurants without price: "
        f"{without_price}"
    )

    print("=" * 50)

    return all_restaurants
    print("=" * 50)

    print(
        f"Total unique restaurants collected: "
        f"{len(all_restaurants)}"
    )

    print("=" * 50)

    return all_restaurants


# اختبار
if __name__ == "__main__":

    restaurants = fetch_restaurants(
        city="Madinah",
        max_restaurants=200
    )

    print("\nFirst 5 restaurants:\n")

    for restaurant in restaurants[:5]:

        print("-" * 50)

        print(
            f"Name: {restaurant['name']}"
        )

        print(
            f"Rating: {restaurant['rating']}"
        )

        print(
            f"Reviews: {restaurant['reviews']}"
        )

        print(
            f"Price: {restaurant['price']}"
        )

        print(
            f"Type: {restaurant['type']}"
        )

        print(
            f"Address: {restaurant['address']}"
        )

        print(
            f"Latitude: {restaurant['latitude']}"
        )

        print(
            f"Longitude: {restaurant['longitude']}"
        )
        print(f"Image: {restaurant['image']}")
