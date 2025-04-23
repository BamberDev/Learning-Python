import requests
import json
from datetime import datetime, timedelta
import os

# Wspolrzedne geograficzne - Katowice
LATITUDE = 50.25
LONGITUDE = 19.02

SAVED_WEATHER_DATA = 'weather_data.json'

class WeatherForecast:
    def __init__(self, filename=SAVED_WEATHER_DATA):
        self.filename = filename
        self._load_data()

    def _load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                self.weather_data = json.load(file)
        else:
            self.weather_data = {}

    def _save_data(self):
        with open(self.filename, 'w') as file:
            json.dump(self.weather_data, file)

    def get_weather_data(self, date):
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={date}&end_date={date}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                rain_sum = data.get('daily', {}).get('rain_sum', [])[0]
                return rain_sum
            else:
                print(f"Error: Cos poszlo nie tak :(\nStatus code: {response.status_code}")
                return None
        except requests.RequestException as error:
            print(f"Error: {error}")
        return None

    def __setitem__(self, date, rain_status):
        self.weather_data[date] = rain_status
        self._save_data()

    def __getitem__(self, date):
        if date not in self.weather_data:
            rain_sum = self.get_weather_data(date)

            if rain_sum is None or rain_sum < 0:
                rain_status = "Nie wiem"
            elif rain_sum > 0:
                rain_status = "Bedzie padac"
            else:
                rain_status = "Nie bedzie padac"
            self[date] = rain_status
            
        return self.weather_data[date]

    def __iter__(self):
        return iter(self.weather_data)

    def items(self):
        return self.weather_data.items()

def main():
    print("\nProgram sprawdzajacy pogode w Katowicach.")
    weather_forecast = WeatherForecast()

    print("\nZapisane daty pogodowe:")
    for date in weather_forecast:
        print(f"Data: {date}")

    print("\nZapisane dane pogodowe:")
    if weather_forecast.items():
        for date, weather in weather_forecast.items():
            print(f"Data: {date}, Pogoda: {weather}")
    else:
        print("Brak zapisanych danych.\n")
    print()
    
    while True:
        print("---Wpisz koniec, aby zakonczyc program---\n")
        user_input = input("Podaj date (YYYY-mm-dd) np. 2024-11-03 lub nacisnij Enter, aby sprawdzic pogode na jutro: ")

        if user_input == "koniec":
            print("Koniec programu.")
            break
        elif not user_input:
            date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            try:
                date = datetime.strptime(user_input, '%Y-%m-%d').strftime('%Y-%m-%d')
            except ValueError:
                print("\nBledny format daty. Uzyj formatu YYYY-mm-dd.\n")
                continue

        weather_status = weather_forecast[date]
        print(f"\nStan pogody w Katowicach na dzien {date}: {weather_status}\n")

if __name__ == "__main__":
    main()