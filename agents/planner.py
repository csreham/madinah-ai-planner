from agents.request_parser import RequestParserAgent
from agents.geocoding import GeocodingAgent
from agents.weather import WeatherAgent
from agents.PlacesAgent import PlacesAgent
from agents.RestaurantsAgent import RestaurantAgent
from agents.HotelAgent import HotelAgent
from agents.scheduleAgent import ScheduleAgent
from agents.TransportationAgent import TransportationAgent
from agents.BudgetAgent import BudgetAgent


class PlannerAgent:

    def run(self, user_request):

        print("===== Planner Agent =====")
        print(f"User Request: {user_request}")

        # ==========================================
        # 1. Parse user request
        # ==========================================

        try:

            parsed_request = RequestParserAgent().run(
                user_request
            )

        except Exception as e:

            print(f"Request Parser Error: {e}")

            return None

        city = parsed_request.get("city")
        days = parsed_request.get("days")

        if not city or not days:

            print("City or days not found.")

            return None

        print(f"City: {city}")
        print(f"Days: {days}")

        # ==========================================
        # 2. Geocoding
        # ==========================================

        coordinates = GeocodingAgent().run(
            city
        )

        if not coordinates:

            print("City not found.")

            return None

        latitude = coordinates["latitude"]
        longitude = coordinates["longitude"]

        # ==========================================
        # 3. Weather
        # ==========================================

        weather = WeatherAgent().run(
            latitude,
            longitude
        )

        # ==========================================
        # 4. Places
        # ==========================================

        places = PlacesAgent().run(
            city=city,
            max_places=200
        )

        # ==========================================
        # 5. Restaurants
        # ==========================================

        restaurants = RestaurantAgent().run(
            city=city,
            max_restaurants=200
        )

        # ==========================================
        # 6. Hotels
        # ==========================================

        hotels = HotelAgent().run(
            city=city,
            check_in="2026-09-05",
            check_out="2026-09-11"
        )

        # ==========================================
        # 7. Schedule
        # ==========================================

        print("Schedule Agent is working...")

        schedule_result = ScheduleAgent().run(
            city=city,
            days=days,
            weather=weather,
            hotels=hotels,
            restaurants=restaurants,
            places=places
        )

        schedule = schedule_result.get(
            "schedule",
            {}
        )

        # ==========================================
        # 8. Transportation
        # ==========================================

        transportation = TransportationAgent().run(
            schedule
        )

       # ==========================================
       # 9. Select Hotel
       # ==========================================

        selected_hotel = hotels[0] if hotels else None


       # ==========================================
       # 10. Budget
       # ==========================================

        budget_data = {
 
         "hotel": selected_hotel,

         "schedule": schedule,

        "transportation": transportation

        }

        budget = BudgetAgent().run(
        budget_data
       )

        # ==========================================
        # 11. Final Result
        # ==========================================

        return {

            "city": city,

            "days": days,

            "weather": weather,

            "hotels": hotels,

            "restaurants": restaurants,

            "places": places,

            "schedule": schedule_result,

            "transportation": transportation,

            "budget": budget

        }