from tools.maps_api import get_places


class PlacesAgent:

    def run(self, latitude, longitude):

        print("Places Agent is working...")

        return get_places(latitude, longitude)