import requests
import json


class Vedas:
    def __init__(self):
        self.dependencies = []
        self.enabled = True

    def matches_query(self, query):
        return 'weather' in query.lower()

    @staticmethod
    def run():
        city = "Nagpur"
        api_key = '1b86abaedd0604dce27bfbc2b40ae211'
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'appid': api_key, 'units': 'metric'}
        response = requests.get(base_url, params=params)
        data = response.json()

        # Extract weather information
        temperature = str(data['main']['temp'])
        humidity = str(data['main']['humidity'])
        weather_condition = str(data['weather'][0]['description'])
        feels_like = str(data['main']['feels_like'])

        # Create the response string
        weather_info = (f"The weather in {city} is {weather_condition}. "
                        f"The temperature is {temperature} degrees Celsius. "
                        f"The humidity is {humidity}%. "
                        f"The feels like temperature is {feels_like} degrees Celsius.")

        print(weather_info)
        return weather_info

