from serpapi import GoogleSearch


def fetch_hotels(city, check_in, check_out, max_hotels=200):

    all_hotels = []
    seen_hotels = set()

    next_page_token = None

    while len(all_hotels) < max_hotels:

        print("=" * 50)

        if next_page_token:
            print("Fetching next page...")
        else:
            print("Fetching first page...")

        params = {
            "engine": "google_hotels",
            "q": f"Hotels in {city}",
            "check_in_date": check_in,
            "check_out_date": check_out,
            "adults": 2,
            "currency": "SAR",
            "gl": "sa",
            "hl": "en",

            # ضعي مفتاحك هنا
            "api_key": "60117fe5faf01fa968183de224efb1721b565f45e2ce2be878c4a4273098b91c",
        }

        # إذا كانت هناك صفحة تالية
        if next_page_token:
            params["next_page_token"] = next_page_token

        search = GoogleSearch(params)

        results = search.get_dict()

        # التحقق من وجود خطأ
        if "error" in results:

            print("SerpApi Error:")
            print(results["error"])

            break

        properties = results.get("properties", [])

        print(f"Hotels received: {len(properties)}")

        if not properties:

            print("No more hotels found.")

            break

        # عدد الفنادق قبل إضافة الصفحة
        old_count = len(all_hotels)

        # إضافة الفنادق الجديدة
        for hotel in properties:

            name = hotel.get("name")

            if not name:
                continue

            # منع التكرار
            if name in seen_hotels:
                continue

            seen_hotels.add(name)

            all_hotels.append(hotel)

            print(f"Added: {name}")

            if len(all_hotels) >= max_hotels:
                break

        print(f"Total unique hotels: {len(all_hotels)}")

        # إذا الصفحة لم تضف أي فندق جديد
        if len(all_hotels) == old_count:

            print("No new hotels found. Stopping.")

            break

        # الحصول على الصفحة التالية
        pagination = results.get("serpapi_pagination", {})

        next_page_token = pagination.get("next_page_token")

        # إذا لم توجد صفحة تالية
        if not next_page_token:

            print("No next page available.")

            break

    print("=" * 50)
    print(f"Total unique hotels collected: {len(all_hotels)}")
    print("=" * 50)

    return all_hotels


# اختبار الملف
if __name__ == "__main__":

    hotels = fetch_hotels(
        city="Madinah",
        check_in="2026-08-10",
        check_out="2026-08-12",
        max_hotels=200
    )

    if not hotels:

        print("No hotels found.")

    else:

        print("\nFirst 5 hotels:\n")

        for hotel in hotels[:5]:

            print("-" * 50)

            print(f"Name: {hotel.get('name')}")

            price = hotel.get("rate_per_night", {})

            print(
                f"Price: {price.get('extracted_lowest')}"
            )

            print(
                f"Rating: {hotel.get('overall_rating')}"
            )

            print(
                f"Reviews: {hotel.get('reviews')}"
            )

            print(
                f"Class: {hotel.get('extracted_hotel_class')}"
            )