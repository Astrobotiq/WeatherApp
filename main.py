import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import requests

# This class is used to fetch the weather data of a particular city from weather.com
class WeatherFetcher:
    def __init__(self):
        self.url = ""

    # Set the URL based on the selected city
    def set_url(self, city):
        if city == "Izmir":
            self.url = "https://weather.com/weather/tenday/l/fe1876e1fd0d8cda3894eb7797379983e6591d215dbcd0279bc3181a8cf677f5"
        elif city == "Istanbul":
            self.url = "https://weather.com/weather/tenday/l/a6ae974ab6d54e31d092094d11d3e04d41a1f81adefe6a49a939c2c1c4bf2696"
        elif city == "Ankara":
            self.url = "https://weather.com/weather/tenday/l/3660a894e62874de91c47e04d57dc1985920d964073ba2df463f063b4cea26d3"
        else:
            self.url = ""

    # Fetch the weather data from the website
    def fetch_weather(self):
        try:
            if not self.url:
                return None, None, []
            fetch = requests.get(self.url, timeout=10)
            fetch.raise_for_status()  # Throw an error if the status code is not 200.
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

        except requests.exceptions.RequestException as e:
            print("An error occurred:", str(e))
            return None, None, []

# Function to convert Celsius to Fahrenheit
def celsius_to_fahrenheit(temp):
    temp = temp.replace('°', '')  # Remove the degree symbol
    converted_temp = round((float(temp) * 9 / 5) + 32, 2)
    return str(converted_temp)

# Function to convert Fahrenheit to Celsius
def fahrenheit_to_celsius(temp):
    temp = temp.replace('°', '')  # Remove the degree symbol
    converted_temp = round((float(temp) - 32) * 5 / 9, 2)
    return str(converted_temp)

# Save the user's city and unit preferences
def save_preferences(city, unit):
    with open('Settings.txt', 'w', encoding='utf-8') as file:
        file.write(f"{city}, {unit}")

# Load the user's city and unit preferences
def load_preferences():
    try:
        with open('Settings.txt', 'r', encoding='utf-8') as file:
            preferences = file.read().split(',')
            city = preferences[0]
            unit = preferences[1].strip() if len(preferences) > 1 else 'Celsius'
            return city, unit
    except FileNotFoundError:
        return None, None

# Switch between Celsius and Fahrenheit
def switch_unit():
    global default_unit, weather_data
    if default_unit == "Celsius":
        default_unit = "Fahrenheit"
        for i, data in enumerate(weather_data):
            day, day_temp, night_temp, weather_info, wind_info = data
            day_labels[i]['text'] = f'Day: {day}'
            day_temp_labels[i]['text'] = f'Day Temperature: {day_temp}{default_unit}'
            night_temp_labels[i]['text'] = f'Night Temperature: {night_temp}{default_unit}'
    else:
        default_unit = "Celsius"
        for i, data in enumerate(weather_data):
            day, day_temp, night_temp, weather_info, wind_info = data
            day_temp = fahrenheit_to_celsius(day_temp)
            night_temp = fahrenheit_to_celsius(night_temp)
            day_labels[i]['text'] = f'Day: {day}'
            day_temp_labels[i]['text'] = f'Day Temperature: {day_temp}°{default_unit}'
            night_temp_labels[i]['text'] = f'Night Temperature: {night_temp}°{default_unit}'

    switch_button_text = ''
    if default_unit == 'Fahrenheit':
        switch_button_text = 'Celsius'
    else:
        switch_button_text = 'Fahrenheit'

    switch_button.config(text=f"Switch to °{switch_button_text},")
    save_preferences(default_city, default_unit)

# Change the city and fetch new weather data
def change_city(event):
    global default_city, weather_data
    default_city = city.get()
    fetcher.set_url(default_city)
    time, place, weather_data = fetcher.fetch_weather()
    time_label['text'] = f'Time: {time}' if time else ""
    place_label['text'] = f'Place: {place}' if place else ""

    for i, data in enumerate(weather_data):
        day, day_temp, night_temp, weather_info, wind_info = data
        day_labels[i]['text'] = f'Day: {day}'
        day_temp_labels[i]['text'] = f'Day Temperature: {day_temp} Fahrenheit'
        night_temp_labels[i]['text'] = f'Night Temperature: {night_temp} Fahrenheit'
        weather_labels[i]['text'] = f'Weather: {weather_info}'
        wind_labels[i]['text'] = f'Wind: {wind_info}'

    save_preferences(default_city, default_unit)

# Load user preferences
default_city, default_unit = load_preferences()
if default_city is None or default_unit is None:
    default_city = ''
    default_unit = 'Fahrenheit'

# Create an instance of the WeatherFetcher class
fetcher = WeatherFetcher()
fetcher.set_url(default_city)
time, place, weather_data = fetcher.fetch_weather()

# Start the tkinter GUI
root = tk.Tk()
root.geometry("600x600")  # Set initial size
root.resizable(True, True)  # Allow resizing
root.title("Weather App")

# Create and pack the widgets
title = tk.Label(root, text="Weather App", font=("Arial", 24), bg="lightblue")
title.pack(fill=tk.X)

settings_frame = ttk.Frame(root, padding="10")  # Create a frame for settings
settings_frame.pack(fill=tk.X)

city_label = tk.Label(settings_frame, text="City")
city_label.pack(side=tk.LEFT)

city = ttk.Combobox(settings_frame, values=["Istanbul", "Ankara", "Izmir"], state="readonly")
city.set(default_city)
city.bind("<<ComboboxSelected>>", change_city)
city.pack(side=tk.LEFT)

switch_button = tk.Button(settings_frame, text=f"Switch to °Celsius", command=lambda: switch_unit(),bg="red",fg="white")
switch_button.pack(side=tk.LEFT)

info_frame = ttk.Frame(root, padding="10")  # Create a frame for information
info_frame.pack(fill=tk.X)

time_label = tk.Label(info_frame, text=f"Time: {time}" if time else "", font=("Arial", 16))
time_label.pack()

place_label = tk.Label(info_frame, text=f"Place: {place}" if place else "", font=("Arial", 16))
place_label.pack()

weather_frame = ttk.Frame(root, padding="10")  # Create a frame for weather
weather_frame.pack(fill=tk.X)

day_labels = []
night_temp_labels = []
day_temp_labels = []
weather_labels = []
wind_labels = []

for _ in range(3):
    day_label = tk.Label(weather_frame, text="")
    day_label.pack()
    day_labels.append(day_label)

    day_temp_label = tk.Label(weather_frame, text="")
    day_temp_label.pack()
    day_temp_labels.append(day_temp_label)

    night_temp_label = tk.Label(weather_frame, text="")
    night_temp_label.pack()
    night_temp_labels.append(night_temp_label)

    weather_label = tk.Label(weather_frame, text="")
    weather_label.pack()
    weather_labels.append(weather_label)

    wind_label = tk.Label(weather_frame, text="")
    wind_label.pack()
    wind_labels.append(wind_label)

    if _ < 2:  # We don't need a separator after the last block
        ttk.Separator(weather_frame, orient='horizontal').pack(fill=tk.X)  # Add a separator

info_label = tk.Label(root, text="Settings successfully loaded.", font=("Arial", 10), fg="green")
info_label.pack(pady=(10, 0))  # Decrease the space after the label

status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)  # Create status bar
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()