import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import requests


class WeatherFetcher:
    def __init__(self):
        self.url = ""

    def set_url(self, city):
        if city == "İzmir":
            self.url = "https://weather.com/weather/tenday/l/fe1876e1fd0d8cda3894eb7797379983e6591d215dbcd0279bc3181a8cf677f5"
        elif city == "İstanbul":
            self.url = "https://weather.com/weather/tenday/l/a6ae974ab6d54e31d092094d11d3e04d41a1f81adefe6a49a939c2c1c4bf2696"
        elif city == "Ankara":
            self.url = "https://weather.com/weather/tenday/l/3660a894e62874de91c47e04d57dc1985920d964073ba2df463f063b4cea26d3"
        else:
            self.url = ""

    def fetch_weather(self):
        if not self.url:
            return None, None, []

        fetch = requests.get(self.url)
        soup = BeautifulSoup(fetch.content, "html.parser")
        time = soup.find('div', class_='DailyForecast--timestamp--22Azh')
        place = soup.find('span', class_='LocationPageTitle--PresentationName--1AMA6')
        days = soup.find_all('h3', class_='DetailsSummary--daypartName--kbngc')
        day_temp = soup.find_all('span', class_='DetailsSummary--highTempValue--3PjlX')
        night_temp = soup.find_all('span', class_='DetailsSummary--lowTempValue--2tesQ')
        weather_info = soup.find_all('span', class_='DetailsSummary--extendedData--307Ax')
        wind_info = soup.find_all('span', class_='Wind--windWrapper--3Ly7c DailyContent--value--1Jers')

        weather_data = []
        for i in range(min(3, len(days), len(day_temp), len(night_temp), len(weather_info), len(wind_info))):
            day = days[i].text
            day_temperature = day_temp[i].text
            night_temperature = night_temp[i].text
            weather = weather_info[i].text
            wind = wind_info[i].text
            weather_data.append((day, day_temperature, night_temperature, weather, wind))

        return time.text, place.text, weather_data


def convert_temp(unit, temp):
    temp = temp.replace('°', '')  # Remove the degree symbol
    converted_temp = round((float(temp) - 32) * 5 / 9)
    if unit == 'Celsius':
        return str(converted_temp) + '°C'
    elif unit == 'Fahrenheit':
        return str(round((converted_temp * 9 / 5) + 32)) + '°F'



def convert_temp_fahrenheit(temp):
    temp = temp.replace('°', '')  # Remove the degree symbol
    converted_temp = round((float(temp) * 9 / 5) + 32, 2)
    return str(converted_temp)



def save_preferences(city, unit):
    with open('Settings.txt', 'w', encoding='utf-8') as file:
        file.write(f"{city}, {unit}")


def load_preferences():
    try:
        with open('Settings.txt', 'r', encoding='utf-8') as file:
            preferences = file.read().split(',')
            city = preferences[0]
            unit = preferences[1].strip() if len(preferences) > 1 else 'Celsius'
            return city, unit
    except FileNotFoundError:
        return None, None


def switch_unit():
    global default_unit
    if default_unit == "Celsius":
        default_unit = "Fahrenheit"
        for i, data in enumerate(weather_data):
            day, day_temp, night_temp, weather_info, wind_info = data
            if i != 0:
                day_temp = convert_temp_fahrenheit(day_temp)
            night_temp = convert_temp_fahrenheit(night_temp)
            day_labels[i]['text'] = f'Day: {day}'
            day_temp_labels[i]['text'] = f'Day Temperature: {day_temp}°{default_unit}'
            night_temp_labels[i]['text'] = f'Night Temperature: {night_temp}°{default_unit}'
    else:
        default_unit = "Celsius"
        for i, data in enumerate(weather_data):
            day, day_temp, night_temp, weather_info, wind_info = data
            if i != 0 :
                day_temp = convert_temp(default_unit, day_temp)
            night_temp = convert_temp(default_unit, night_temp)
            day_labels[i]['text'] = f'Day: {day}'
            day_temp_labels[i]['text'] = f'Day Temperature: {day_temp}°{default_unit}'
            night_temp_labels[i]['text'] = f'Night Temperature: {night_temp}°{default_unit}'

    switch_button.config(text=f"Switch to °{default_unit}")
    save_preferences(default_city, default_unit)


def change_city(event):
    global default_city
    default_city = city.get()
    fetcher.set_url(default_city)
    time, place, weather_data = fetcher.fetch_weather()
    time_label['text'] = f'Time: {time}' if time else ""
    place_label['text'] = f'Place: {place}' if place else ""

    for i, data in enumerate(weather_data):
        day, day_temp, night_temp, weather_info, wind_info = data
        day_labels[i]['text'] = f'Day: {day}'
        day_temp_labels[i]['text'] = f'Day Temperature: {day_temp}'
        night_temp_labels[i]['text'] = f'Night Temperature: {night_temp}'
        weather_labels[i]['text'] = f'Weather: {weather_info}'
        wind_labels[i]['text'] = f'Wind: {wind_info}'

    save_preferences(default_city, default_unit)


# Load user preferences
default_city, default_unit = load_preferences()
if default_city is None or default_unit is None:
    default_city = ''
    default_unit = 'Fahrenheit'

fetcher = WeatherFetcher()
fetcher.set_url(default_city)
time, place, weather_data = fetcher.fetch_weather()

root = tk.Tk()
root.title("Hava Durumu Uygulaması")

title = tk.Label(root, text="Hava Durumu Uygulaması", font=("Arial", 24), bg="lightblue")
title.pack(fill=tk.X)

city_label = tk.Label(root, text="Şehir")
city_label.pack()

city = ttk.Combobox(root, values=["İstanbul", "Ankara", "İzmir"], state="readonly")
city.set(default_city)
city.bind("<<ComboboxSelected>>", change_city)
city.pack()

switch_button = tk.Button(root, text=f"Switch to °{default_unit}", command=lambda: switch_unit())
switch_button.pack()

time_label = tk.Label(root, text=f"Time: {time}" if time else "")
time_label.pack()

place_label = tk.Label(root, text=f"Place: {place}" if place else "")
place_label.pack()

day_labels = []
night_temp_labels = []
day_temp_labels = []
weather_labels = []
wind_labels = []

for _ in range(3):
    day_label = tk.Label(root, text="")
    day_label.pack()
    day_labels.append(day_label)

    day_temp_label = tk.Label(root, text="")
    day_temp_label.pack()
    day_temp_labels.append(day_temp_label)

    night_temp_label = tk.Label(root, text="")
    night_temp_label.pack()
    night_temp_labels.append(night_temp_label)

    weather_label = tk.Label(root, text="")
    weather_label.pack()
    weather_labels.append(weather_label)

    wind_label = tk.Label(root, text="")
    wind_label.pack()
    wind_labels.append(wind_label)

info_label = tk.Label(root, text="Ayarlar başarıyla yüklendi.", font=("Arial", 10), fg="green")
info_label.pack()

root.mainloop()
