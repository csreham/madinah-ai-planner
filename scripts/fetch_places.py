from serpapi import GoogleSearch


def fetch_places(city, max_places=200):

    all_places = []
    seen_places = set()

    # عمليات البحث المتخصصة
    queries = [
        f"tourist attractions in {city}",
        f"museums in {city}",
        f"historical sites in {city}",
        f"parks in {city}",
        f"cultural attractions in {city}"
    ]

    for query in queries:

        start = 0

        print("\n")
        print("#" * 60)
        print(f"Starting query: {query}")
        print("#" * 60)

        while len(all_places) < max_places:

            print("=" * 50)
            print(f"Query: {query}")
            print(f"Start: {start}")

            params = {
                "engine": "google_maps",
                "q": query,
                "type": "search",
                "google_domain": "google.com",
                "gl": "sa",
                "hl": "en",

                # ضعي مفتاح SerpApi الخاص بك
                "api_key": "60117fe5faf01fa968183de224efb1721b565f45e2ce2be878c4a4273098b91c",

                "start": start
            }

            search = GoogleSearch(params)

            results = search.get_dict()

            # -----------------------------
            # التحقق من الأخطاء
            # -----------------------------

            if "error" in results:

                print("SerpApi Error:")
                print(results["error"])

                break

            # -----------------------------
            # الحصول على النتائج
            # -----------------------------

            places = results.get(
                "local_results",
                []
            )

            print(
                f"Places received: "
                f"{len(places)}"
            )

            # لا توجد نتائج
            if not places:

                print(
                    "No more places found "
                    "for this query."
                )

                break

            old_count = len(all_places)

            # -----------------------------
            # معالجة الأماكن
            # -----------------------------

            for place in places:

                name = place.get("title")

                if not name:
                    continue

                # إزالة التكرار
                if name in seen_places:
                    continue

                seen_places.add(name)

                place_data = {

                    "name": name,

                    "rating": place.get(
                        "rating"
                    ),

                    "reviews": place.get(
                        "reviews"
                    ),

                    "type": place.get(
                        "type"
                    ),

                    "address": place.get(
                        "address"
                    ),

                    "latitude": place.get(
                        "gps_coordinates", {}
                    ).get("latitude"),

                    "longitude": place.get(
                        "gps_coordinates", {}
                    ).get("longitude"),

                    "website": place.get(
                        "website"
                    ),

                    "phone": place.get(
                        "phone"
                    ),

                    "hours": place.get(
                        "hours"
                    )
                }

                all_places.append(place_data)

                print(
                    f"Added: {name} | "
                    f"Rating: {place.get('rating')} | "
                    f"Type: {place.get('type')}"
                )

                # الوصول للحد الأقصى
                if len(all_places) >= max_places:
                    break

            # -----------------------------
            # العدد الإجمالي
            # -----------------------------

            print(
                f"Total unique places: "
                f"{len(all_places)}"
            )

            # -----------------------------
            # إذا لم تتم إضافة أي نتيجة جديدة
            # -----------------------------

            if len(all_places) == old_count:

                print(
                    "No new places found "
                    "for this query."
                )

                break

            # -----------------------------
            # Pagination
            # -----------------------------

            pagination = results.get(
                "serpapi_pagination",
                {}
            )

            next_url = pagination.get(
                "next"
            )

            if not next_url:

                print(
                    "No next page available "
                    "for this query."
                )

                break

            # الصفحة التالية
            start += len(places)

    # -----------------------------
    # النتيجة النهائية
    # -----------------------------

    print("\n")
    print("=" * 60)

    print(
        f"Total unique places collected: "
        f"{len(all_places)}"
    )

    print("=" * 60)

    return all_places


# ==================================================
# TEST
# ==================================================

if __name__ == "__main__":

    places = fetch_places(
        city="Madinah",
        max_places=200
    )

    if not places:

        print("No places found.")

    else:

        print("\nFirst 5 places:\n")

        for place in places[:5]:

            print("-" * 50)

            print(
                f"Name: {place['name']}"
            )

            print(
                f"Rating: {place['rating']}"
            )

            print(
                f"Reviews: {place['reviews']}"
            )

            print(
                f"Type: {place['type']}"
            )

            print(
                f"Address: {place['address']}"
            )

            print(
                f"Latitude: {place['latitude']}"
            )

            print(
                f"Longitude: {place['longitude']}"
            )

            print(
                f"Hours: {place['hours']}"
            )
            print(f"Image: {places['image']}")
