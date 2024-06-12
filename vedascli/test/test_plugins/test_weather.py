from .test_audio import test_say
import requests
import json


class Test_Vedas:
    def test___init__(self):
        self.dependencies = []
        self.enabled = True

    @staticmethod
    def test_run():
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
        test_say(weather_info)

    def test_matches_query(self, query):
        return 'weather' in query.lower()
