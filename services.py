import requests
import json
import sys
import config


def get_weather_report():
    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat=28.3802&lon=75.6092&appid={config.OPENWEATHER_API_KEY}&units=metric")
    response_json = json.loads(response.text)
    print(response_json, file=sys.stdout)
    return {'description': response_json['weather'][0]['description'], 'temp': response_json['main']['temp'],
            'feels_like': response_json['main']['feels_like'], 'temp_min': response_json['main']['temp_min'],
            'temp_max': response_json['main']['temp_max'], 'pressure': response_json['main']['pressure'],
            'humidity': response_json['main']['humidity'], 'visibility': response_json['visibility'],
            'wind_speed': response_json['wind']['speed'], 'wind_deg': response_json['wind']['deg']}


def check_mess_menu():
    # TODO:
    return

