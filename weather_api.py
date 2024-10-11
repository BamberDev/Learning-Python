import requests
import json
from datetime import datetime, timedelta
import os

# Wspolrzedne geograficzne - Katowice
LATITUDE = 50.25
LONGITUDE = 19.02

SAVED_WEATHER_DATA = 'weather_data.json'

def get_weather_data(date):
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

def save_weather_data(date, rain_status):
    if os.path.exists(SAVED_WEATHER_DATA):
        with open(SAVED_WEATHER_DATA, 'r') as file:
            weather_data = json.load(file)
    else:
        weather_data = {}

    weather_data[date] = rain_status

    with open(SAVED_WEATHER_DATA, 'w') as file:
        json.dump(weather_data, file)

def load_weather_data():
    if os.path.exists(SAVED_WEATHER_DATA):
        with open(SAVED_WEATHER_DATA, 'r') as file:
            return json.load(file)
    return {}

def check_weather(date):
    weather_data = load_weather_data()

    if date in weather_data:
        return weather_data[date]
    
    rain_sum = get_weather_data(date)

    if rain_sum is None or rain_sum < 0:
        rain_status = "Nie wiem"
    elif rain_sum > 0:
        rain_status = "Bedzie padac"
    else:
        rain_status = "Nie bedzie padac"
    
    save_weather_data(date, rain_status)
    return rain_status

def main():
    print("Program sprawdzajacy pogode w Katowicach.")
    
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

        weather_status = check_weather(date)
        print(f"\nStan pogody w Katowicach na dzien {date}: {weather_status}\n")

if __name__ == "__main__":
    main()