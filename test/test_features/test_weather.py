import requests
import json
import pytest


@pytest.fixture(autouse=True)
def city():
    return "India"

def test_get_weather_data(city):
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
    return a
