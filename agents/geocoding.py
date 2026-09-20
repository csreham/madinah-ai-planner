from tools.geocoding_api import get_coordinates


class GeocodingAgent:

    def run(self, city):

        print("Geocoding Agent is working...")

        coordinates = get_coordinates(city)

        return coordinates