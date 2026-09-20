import re


class BudgetAgent:

    def run(self, schedule_result):

        print("Budget Agent is working...")

        # ==========================================
        # Get schedule
        # ==========================================

        if not schedule_result:
            return {
                "hotel_cost": 0,
                "restaurant_cost": 0,
                "transportation_cost": 0,
                "total_cost": 0
            }
        # إذا ScheduleAgent يرجع:
        #
        # {
        #     "hotel": {...},
        #     "schedule": {...},
        #     "transportation": {...}
        # }
        #
        # نأخذ الجدول

        schedule = schedule_result.get(
            "schedule",
            schedule_result
        )

        # ==========================================
        # HOTEL
        # ==========================================

        hotel = schedule_result.get(
           "hotel"
        )

        hotel_cost = 0
        hotel_price = 0

        if isinstance(
           hotel,
            dict
       ):

         hotel_price = self.extract_number(
         hotel.get("price")
       )

        if hotel_price is not None:

           days = self.get_days(
           schedule
        )

        nights = max(
            days - 1,
            0
        )

        hotel_cost = (
            hotel_price * nights
        )

        # ==========================================
        # RESTAURANTS
        # ==========================================

        restaurant_cost = 0

        # نقرأ المطاعم الموجودة فعليًا
        # داخل ScheduleAgent

        for day, activities in schedule.items():

            if not isinstance(
                activities,
                list
            ):
                continue

            for activity in activities:

                if not isinstance(
                    activity,
                    dict
                ):
                    continue

                restaurant_price = (
                    self.extract_price_range(
                        activity.get("price")
                    )
                )

                if restaurant_price:

                    minimum = restaurant_price[0]
                    maximum = restaurant_price[1]

                    # متوسط السعر الموجود في
                    # بيانات المطعم نفسه

                    average = (
                        minimum + maximum
                    ) / 2

                    restaurant_cost += average

        # ==========================================
        # TRANSPORTATION
        # ==========================================

        transportation_cost = 0

        transportation = (
            schedule_result.get(
                "transportation",
                {}
            )
        )

        if isinstance(
            transportation,
            dict
        ):

            for day, data in transportation.items():

                if not isinstance(
                    data,
                    dict
                ):
                    continue

                cost = data.get(
                    "total_estimated_cost"
                )

                if cost is None:
                    continue

                try:

                    transportation_cost += float(
                        cost
                    )

                except (
                    ValueError,
                    TypeError
                ):

                    pass

        # ==========================================
        # TOTAL
        # ==========================================

        total_cost = (
            hotel_cost
            +
            restaurant_cost
            +
            transportation_cost
        )

        # ==========================================
        # RESULT
        # ==========================================

        return {

            "hotel": {

                "name":
                    hotel.get("name")
                    if hotel
                    else None,

                "cost":
                    round(
                        hotel_cost,
                        2
                    )
            },

            "restaurants": {

                "cost":
                    round(
                        restaurant_cost,
                        2
                    )
            },

            "transportation": {

                "cost":
                    round(
                        transportation_cost,
                        2
                    )
            },

            "total_cost":
                round(
                    total_cost,
                    2
                )
        }

    # ==========================================
    # Get number of days
    # ==========================================

    def get_days(self, schedule):

        if not isinstance(
            schedule,
            dict
        ):
            return 0

        return len(schedule)

    # ==========================================
    # Extract number from price
    # ==========================================

    def extract_number(self, value):

        if value is None:
            return None

        if isinstance(
            value,
            (int, float)
        ):
            return float(value)

        numbers = re.findall(
            r"\d+(?:\.\d+)?",
            str(value).replace(",", "")
        )

        if not numbers:
            return None

        return float(numbers[0])

    # ==========================================
    # Extract restaurant price range
    # ==========================================

    def extract_price_range(self, value):

        if value is None:
            return None

        if isinstance(
            value,
            (int, float)
        ):

            value = float(value)

            return (
                value,
                value
            )

        numbers = re.findall(
            r"\d+(?:\.\d+)?",
            str(value).replace(",", "")
        )

        if not numbers:
            return None

        if len(numbers) == 1:

            value = float(
                numbers[0]
            )

            return (
                value,
                value
            )

        return (
            float(numbers[0]),
            float(numbers[1])
        )