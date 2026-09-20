from scripts.fetch_hotels import fetch_hotels


class HotelAgent:

    def run(self, city, check_in, check_out, max_hotels=200):

        results = fetch_hotels(
            city,
            check_in,
            check_out,
            max_hotels=max_hotels
        )

        hotels = []

        for hotel in results:

            hotels.append({
                "name": hotel.get("name"),

                "price": hotel.get(
                    "rate_per_night", {}
                ).get("extracted_lowest"),

                "rating": hotel.get("overall_rating"),

                "reviews": hotel.get("reviews"),

                "hotel_class": hotel.get(
                    "extracted_hotel_class"
                ),

                "latitude": hotel.get(
                    "gps_coordinates", {}
                ).get("latitude"),

                "longitude": hotel.get(
                    "gps_coordinates", {}
                ).get("longitude"),

                "amenities": hotel.get(
                    "amenities", []
                )
            })

        return hotels