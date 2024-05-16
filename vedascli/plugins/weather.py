from vedascli.plugins.audio import Vedas
import requests
import json


class Vedas:
    def __init__(self):
        pass

    def match_query(self, query):
        if "weather" in query:
            return query.lower()

    def run(self, *args, **kwargs):
        city = kwargs.get("city", '')
        query = self.match_query(kwargs["city"])
        city += input("Enter the city name: ")
        if city:
            return self.get_weather_data(city)

    dependencies = ["audio"]

    def get_weather_data(self, city):
        api_key = '1b86abaedd0604dce27bfbc2b40ae211'
        base_url = 'http://api.openweathermap.org/data/2.5/weather'
        params = {'q': city, 'appid': api_key, 'units': 'metric'}
        response = requests.get(base_url, params=params)
        data = response.json()
        temperature = str(data['main']['temp'])
        humidity = str(data['main']['humidity'])
        weather_condition = str(data['weather'][0]['description'])
        feels_like = str(data['main']['feels_like'])
        a = f"The weather in {city} is {weather_condition}. The temperature is {temperature} degrees Celsius. " \
            f"The humidity is {humidity}%. The feels like is {feels_like} degrees Celsius."
        print(a)
        Vedas.say(a)
        return a
