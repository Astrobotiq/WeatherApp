import requests
from bs4 import BeautifulSoup


# Save user preferences to Settings.txt file
def save_preferences(city, unit):
    with open('Settings.txt', 'w') as file:
        file.write(f"{city}, {unit}")


# Function to Load user preferences from Settings.txt file
def load_preferences():
    try:
        with open('Settings.txt', 'r') as file:
            preferences = file.read().split(',')
            city = preferences[0]
            unit = preferences[1]
            return city, unit
    except FileNotFoundError:
        return None, None


# Load user preferences
default_city, default_unit = load_preferences()
if default_city is None or default_unit is None:
    default_city = ''
    default_unit = 'Celsius'

url = 'https://weather.com/weather/tenday/l/780a7c797ce1147202911c273e064fa4e2a0e516a14bb8aeb956331bbad0f637'
x = requests.get(url)

soup = BeautifulSoup(x.content)
time = soup.find('div', class_='DailyForecast--timestamp--22Azh')
place = soup.find('span', class_='LocationPageTitle--PresentationName--1AMA6')
days = soup.find_all('h3', class_='DetailsSummary--daypartName--kbngc')
dayTemp = soup.find_all('span', class_='DetailsSummary--highTempValue--3PjlX')
nightTemp = soup.find_all('span', class_='DetailsSummary--lowTempValue--2tesQ')
weather = soup.find_all('span', class_='DetailsSummary--extendedData--307Ax')
wind = soup.find_all('span', class_='Wind--windWrapper--3Ly7c DailyContent--value--1Jers')

# Test Save user preferences
# selected_city = 'Istanbul'
# selected_unit = 'Fahrenheit'
# save_preferences(selected_city,selected_unit)

##for i in range(14):
##print(f"{place.text} \n {time.text}")
##print(f'Day:{days[i].text}   {dayTemp[i].text}/{nightTemp[i].text}   Weather:{weather[i].text}   Wind:{wind[i].text}')
##print("****************************************************************************")


##To-do:
##Solve how to Calculate C from F
