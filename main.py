import requests
from bs4 import BeautifulSoup

url = 'https://weather.com/weather/tenday/l/780a7c797ce1147202911c273e064fa4e2a0e516a14bb8aeb956331bbad0f637'
x = requests.get(url)



soup = BeautifulSoup(x.content)
time = soup.find('div',class_ = 'DailyForecast--timestamp--22Azh')
place = soup.find('span',class_ = 'LocationPageTitle--PresentationName--1AMA6')
days = soup.find_all('h3',class_='DetailsSummary--daypartName--kbngc')
dayTemp = soup.find_all('span',class_='DetailsSummary--highTempValue--3PjlX')
nightTemp = soup.find_all('span',class_='DetailsSummary--lowTempValue--2tesQ')
weather = soup.find_all('span',class_='DetailsSummary--extendedData--307Ax')
wind = soup.find_all('span',class_='Wind--windWrapper--3Ly7c DailyContent--value--1Jers')


##for i in range(14):
  ##print(f"{place.text} \n {time.text}")
  ##print(f'Day:{days[i].text}   {dayTemp[i].text}/{nightTemp[i].text}   Weather:{weather[i].text}   Wind:{wind[i].text}')
  ##print("****************************************************************************")


##To-do:
##Solve how to Calculate C from F