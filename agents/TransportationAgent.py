import math


class TransportationAgent:

    def run(self, schedule):

        transportation = {}

        # schedule coming directly from ScheduleAgent
        for day, activities in schedule.items():

            routes = []

            total_distance = 0
            total_cost = 0

            # --------------------------------------
            # Calculate transportation between
            # consecutive activities
            # --------------------------------------

            for i in range(len(activities) - 1):

                current = activities[i]
                next_place = activities[i + 1]

                start_lat = current.get("latitude")
                start_lng = current.get("longitude")

                end_lat = next_place.get("latitude")
                end_lng = next_place.get("longitude")

                # Skip if coordinates are missing
                if None in [
                    start_lat,
                    start_lng,
                    end_lat,
                    end_lng
                ]:
                    continue

                # Calculate distance
                distance = self.calculate_distance(
                    start_lat,
                    start_lng,
                    end_lat,
                    end_lng
                )

                # Select transportation
                transport = self.select_transport(
                    distance
                )

                # Calculate estimated cost
                cost = self.calculate_cost(
                    distance,
                    transport
                )

                routes.append({

                    "from": current.get("name"),

                    "to": next_place.get("name"),

                    "distance_km": round(
                        distance,
                        2
                    ),

                    "transport": transport,

                    "estimated_cost": cost
                })

                total_distance += distance
                total_cost += cost

            # --------------------------------------
            # Save result for this day
            # --------------------------------------

            transportation[day] = {

                "number_of_trips": len(routes),

                "routes": routes,

                "total_distance_km": round(
                    total_distance,
                    2
                ),

                "total_estimated_cost": round(
                    total_cost,
                    2
                )
            }

        return transportation

    # ==========================================
    # Calculate geographical distance
    # ==========================================

    def calculate_distance(
        self,
        lat1,
        lon1,
        lat2,
        lon2
    ):

        earth_radius = 6371

        lat1 = math.radians(lat1)
        lon1 = math.radians(lon1)

        lat2 = math.radians(lat2)
        lon2 = math.radians(lon2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = (
            math.sin(dlat / 2) ** 2
            +
            math.cos(lat1)
            * math.cos(lat2)
            * math.sin(dlon / 2) ** 2
        )

        c = 2 * math.atan2(
            math.sqrt(a),
            math.sqrt(1 - a)
        )

        return earth_radius * c

    # ==========================================
    # Transportation type
    # ==========================================

    def select_transport(self, distance):

        if distance <= 1:

            return "Walking"

        return "Taxi"

    # ==========================================
    # Estimated cost
    # ==========================================

    def calculate_cost(
        self,
        distance,
        transport
    ):

        if transport == "Walking":

            return 0

        base_fare = 5
        price_per_km = 2.5

        cost = (
            base_fare
            +
            distance * price_per_km
        )

        # Minimum estimated taxi fare
        cost = max(cost, 10)

        return round(cost, 2)