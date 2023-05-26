import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup

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
    save_preferences(default_city, default_unit)
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

day1_label = tk.Label(root, text="Gün 1: Veri Bekleniyor...")
day1_label.pack()

day2_label = tk.Label(root, text="Gün 2: Veri Bekleniyor...")
day2_label.pack()

day3_label = tk.Label(root, text="Gün 3: Veri Bekleniyor...")
day3_label.pack()

info_label = tk.Label(root, text="Ayarlar başarıyla yüklendi.", font=("Arial", 10), fg="green")
info_label.pack()

root.mainloop()
