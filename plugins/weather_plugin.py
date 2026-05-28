from manager.env_manager import (DEFAULT_CITY, OPEN_WEATHER_API_KEY, DEFAULT_WEATHER_UNIT,
                                 DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_LANGUAGE_CODE, GEOCODING_API_KEY)
import requests

class Vedas:
    def __init__(self, config=None, **kwargs):
        self.name = "weather_plugin"
        self.description = ("It provides weather information based on user queries. "
                            "It can fetch current weather, forecasts, and other weather-related data "
                            "for specified locations."
        )

        self.parameters = ["input_data"]

        self.keywords = ["weather", "forecast", "temperature", "humidity", "wind", "rain", "snow"]

        self.dependencies = []
        self.tool_map = {}
        self.config = config or {}
        self.enabled = True
        self.last_query = None

    def matches_query(self, query):
        self.last_query = query
        query_lower = query
        return any(keyword in query_lower for keyword in self.keywords)

    def run(self, *args, **kwargs):
            # For debugging: print received input data and query
            print(f"[{self.name}] received input_data:", args)
            print(f"[{self.name}] last_query:", repr(self.last_query))

            # Call the weather function to get weather data
            weather_data = self.weather()

            return weather_data

    def weather(self, city=DEFAULT_CITY):
        # get the latitude and longitude from the .env file
        latitude, longitude = DEFAULT_LATITUDE, DEFAULT_LONGITUDE

        # get the co-ordinates for the city if not found
        if not latitude or not longitude:
            latitude, longitude = self.get_city_coordinates(city)

        # URL to get the weather data from the OpenWeather API using the latitude and longitude
        BASE_URL = (
            f"https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={OPEN_WEATHER_API_KEY}&units={DEFAULT_WEATHER_UNIT}&lang={DEFAULT_LANGUAGE_CODE}")

        response = requests.get(BASE_URL)
        data = response.json()      # Load data into json form

        # Sort what is needed by the user like temperature, humidity, and other
        temperature = str(data["main"]["temp"])


        return temperature + (" Instruction - The given value is the weather details, "
                              "- add few words don't do much of elaboration combine it and return the response")


    def get_city_coordinates(self, city=DEFAULT_CITY):
        GEO_URL = (
            f"https://geocode.xyz/{city}?json=1&auth={GEOCODING_API_KEY}"
        )
        response = requests.get(GEO_URL)
        data = response.json()

        # returns only the latitude and longitude
        return data['latt'], data['longt']



    def __str__(self):
        return str(self.keywords)


if __name__ == "__main__":
    print(Vedas().run("What's the weather like today?"))
    # print(Vedas().get_city_coordinates("Nagpur"))