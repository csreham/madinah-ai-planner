from tools.weather_api import get_weather


class WeatherAgent:

    def run(self, latitude, longitude):

        print("Weather Agent is working...")

        return get_weather(latitude, longitude)