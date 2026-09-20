class ScheduleAgent:

    def run(
    self,
    city,
    days,
    weather,
    hotels,
    restaurants,
    places
):

        # ------------------------------------------
        # تنظيف البيانات
        # ------------------------------------------

        if not isinstance(hotels, list):
            hotels = []

        if not isinstance(places, list):
            places = []

        if not isinstance(restaurants, list):
            restaurants = []

        # ------------------------------------------
        # اختيار الفندق
        # ------------------------------------------

        hotels_sorted = sorted(
            hotels,
            key=lambda x: x.get("rating") or 0,
            reverse=True
        )

        selected_hotel = None

        if hotels_sorted:
            selected_hotel = hotels_sorted[0]

        # ------------------------------------------
        # ترتيب الأماكن حسب التقييم
        # ------------------------------------------

        places_sorted = sorted(
            places,
            key=lambda x: (
                x.get("rating") or 0,
                x.get("reviews") or 0
            ),
            reverse=True
        )

        # ------------------------------------------
        # ترتيب المطاعم حسب التقييم
        # ------------------------------------------

        restaurants_sorted = sorted(
            restaurants,
            key=lambda x: (
                x.get("rating") or 0,
                x.get("reviews") or 0
            ),
            reverse=True
        )

        # ------------------------------------------
        # إنشاء الجدول
        # ------------------------------------------

        schedule = {}

        # عدد الأنشطة التي نريدها تقريبًا لكل يوم
        places_per_day = 3

        for day in range(1, days + 1):

            day_schedule = []

            # --------------------------------------
            # الصباح
            # --------------------------------------

            place_index = (day - 1) * places_per_day

            morning_place = None

            if place_index < len(places_sorted):
                morning_place = places_sorted[place_index]

            if morning_place:

                day_schedule.append({
                    "time": "09:00 AM",
                    "name": morning_place.get("name"),
                    "type": morning_place.get("type"),
                    "category": "attraction",
                    "rating": morning_place.get("rating"),
                    "address": morning_place.get("address"),
                    "latitude": morning_place.get("latitude"),
                    "longitude": morning_place.get("longitude"),
                    "image": morning_place.get("image")
                })

            # --------------------------------------
            # الغداء
            # --------------------------------------

            restaurant_index = day - 1

            lunch_restaurant = None

            if restaurant_index < len(restaurants_sorted):
                lunch_restaurant = restaurants_sorted[
                    restaurant_index
                ]

            if lunch_restaurant:

                day_schedule.append({
                    "time": "01:00 PM",
                    "name": lunch_restaurant.get("name"),
                    "type": lunch_restaurant.get("type"),
                    "category": "restaurant",
                    "rating": lunch_restaurant.get("rating"),
                    "reviews": lunch_restaurant.get("reviews"),
                    "price": lunch_restaurant.get("price"),
                    "address": lunch_restaurant.get("address"),
                    "latitude": lunch_restaurant.get("latitude"),
                    "longitude": lunch_restaurant.get("longitude"),
                    "image": lunch_restaurant.get("image")
                })

            # --------------------------------------
            # العصر
            # --------------------------------------

            afternoon_index = place_index + 1

            afternoon_place = None

            if afternoon_index < len(places_sorted):
                afternoon_place = places_sorted[
                    afternoon_index
                ]

            if afternoon_place:

                day_schedule.append({
                    "time": "04:00 PM",
                    "name": afternoon_place.get("name"),
                    "type": afternoon_place.get("type"),
                    "category": "attraction",
                    "rating": afternoon_place.get("rating"),
                    "address": afternoon_place.get("address"),
                    "latitude": afternoon_place.get("latitude"),
                    "longitude": afternoon_place.get("longitude"),
                    "image": afternoon_place.get("image")
                })

            # --------------------------------------
            # العشاء
            # --------------------------------------

            dinner_index = day

            dinner_restaurant = None

            if dinner_index < len(restaurants_sorted):
                dinner_restaurant = restaurants_sorted[
                    dinner_index
                ]

            if dinner_restaurant:

                day_schedule.append({
                    "time": "08:00 PM",
                    "name": dinner_restaurant.get("name"),
                    "type": dinner_restaurant.get("type"),
                    "category": "restaurant",
                    "rating": dinner_restaurant.get("rating"),
                    "reviews": dinner_restaurant.get("reviews"),
                    "price": dinner_restaurant.get("price"),
                    "address": dinner_restaurant.get("address"),
                    "latitude": dinner_restaurant.get("latitude"),
                    "longitude": dinner_restaurant.get("longitude"),
                    "image": dinner_restaurant.get("image")
                })

            # --------------------------------------
            # حفظ اليوم
            # --------------------------------------

            schedule[f"Day {day}"] = day_schedule

        # ------------------------------------------
        # النتيجة النهائية
        # ------------------------------------------

        return {
            "city": city,
            "days": days,
            "hotel": selected_hotel,
            "schedule": schedule
        }