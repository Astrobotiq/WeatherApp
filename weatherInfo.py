import requests
from bs4 import BeautifulSoup

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

for i in range(14):
    print(f"{place.text} \n {time.text}")
    print(f'Day:{days[i].text}   {dayTemp[i].text}/{nightTemp[i].text}   Weather:{weather[i].text}   Wind:{wind[i].text}')
    print("****************************************************************************")









