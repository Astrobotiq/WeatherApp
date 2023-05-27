import this
import tkinter as tk
from tkinter import ttk

import requests
from bs4 import BeautifulSoup

def fetchWeather(city):
    global url
    if city == "İzmir":
        url = "https://weather.com/weather/tenday/l/fe1876e1fd0d8cda3894eb7797379983e6591d215dbcd0279bc3181a8cf677f5"
    elif city == "İstanbul":
        url = "https://weather.com/weather/tenday/l/a6ae974ab6d54e31d092094d11d3e04d41a1f81adefe6a49a939c2c1c4bf2696"
    elif city == "Ankara":
        url = "https://weather.com/weather/tenday/l/3660a894e62874de91c47e04d57dc1985920d964073ba2df463f063b4cea26d3"

    fetch = requests.get(url)

    soup = BeautifulSoup(fetch.content,"html.parser")
    time = soup.find('div', class_='DailyForecast--timestamp--22Azh')
    place = soup.find('span', class_='LocationPageTitle--PresentationName--1AMA6')
    days = soup.find_all('h3', class_='DetailsSummary--daypartName--kbngc')
    dayTemp = soup.find_all('span', class_='DetailsSummary--highTempValue--3PjlX')
    nightTemp = soup.find_all('span', class_='DetailsSummary--lowTempValue--2tesQ')
    weather = soup.find_all('span', class_='DetailsSummary--extendedData--307Ax')
    wind = soup.find_all('span', class_='Wind--windWrapper--3Ly7c DailyContent--value--1Jers')

    for i in range (3):
        time_label['text'] = f'Time:{time.text}'
        place_label['text'] = f'Place:{place.text}'
        day_labels[i]['text'] = f'Day: {days[i].text}'
        dayTemp_labels[i]['text'] = f'Day Temperature: {dayTemp[i].text}'
        nightTemp_labels[i]['text'] = f'Night Temperature: {nightTemp[i].text}'
        weather_labels[i]['text'] = f'Weather: {weather[i].text}'
        wind_labels[i]['text'] = f'Wind: {wind[i].text}'



# Save user preferences to Settings.txt file
def save_preferences(city, unit):
    with open('Settings.txt', 'w', encoding='utf-8') as file:
        file.write(f"{city}, {unit}")


# Function to Load user preferences from Settings.txt file
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
    else:
        default_unit = "Celsius"
    switch_button.config(text=f"Switch to °{default_unit}")
    save_preferences(default_city, default_unit)
    # Here, you should update the weather information.


def change_city(event):
    global default_city
    default_city = city.get()
    print(city.get())
    save_preferences(default_city, default_unit)
    fetchWeather(default_city)
    # Here, you should update the weather information.

# Load user preferences
default_city, default_unit = load_preferences()
if default_city is None or default_unit is None:
    default_city = ''
    default_unit = 'Celsius'




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


switch_button = tk.Button(root, text=f"Switch to °{default_unit}", command=switch_unit)
switch_button.pack()

time_label = tk.Label(root,text="")
place_label = tk.Label(root,text="")
time_label.pack()
place_label.pack()
day_labels = []
nightTemp_labels = []
dayTemp_labels = []
weather_labels = []
wind_labels = []
for _ in range(3):
    day_label = tk.Label(root, text="")
    day_label.pack()
    day_labels.append(day_label)

    dayTemp_label = tk.Label(root, text="")
    dayTemp_label.pack()
    dayTemp_labels.append(day_label)

    nightTemp_label = tk.Label(root, text="")
    nightTemp_label.pack()
    nightTemp_labels.append(nightTemp_label)

    weather_label = tk.Label(root, text="")
    weather_label.pack()
    weather_labels.append(weather_label)

    wind_label = tk.Label(root, text="")
    wind_label.pack()
    wind_labels.append(wind_label)


info_label = tk.Label(root, text="Ayarlar başarıyla yüklendi.", font=("Arial", 10), fg="green")
info_label.pack()

root.mainloop()
