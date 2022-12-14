# importing library
import requests
import re
from bs4 import BeautifulSoup

# # enter city name
# city = "gandhinagar"

# # creating url and requests instance
# url = "https://www.google.com/search?q="+"weather"+city
# html = requests.get(url).content

# # getting raw data
# soup = BeautifulSoup(html, 'html.parser')
# temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
# str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text

# # formatting data
# data = str.split('\n')
# time_pattern = re.compile(r'\d.+')
# time = time_pattern.search(data[0]).group().strip()
# sky = data[1]

# # getting all div tag
# listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
# strd = listdiv[5].text

# # getting other required data
# pos = strd.find('Wind')
# other_data = strd[pos:]

# # printing all data
# print("Temperature is", temp)
# temps = temp.replace(u"°C", "")
# a = 10
# diff = a - int(temps)
# print(diff)
# print("Time:", time)
# print("Sky Description:", sky)
# sky = chr(sky)
# print(type(sky))
# print(other_data)

def localTempt():
        # enter city name
        city = "gandhinagar"
        # creating url and requests instance
        url = "https://www.google.com/search?q="+"weather"+city
        html = requests.get(url).content
        # getting raw data
        soup = BeautifulSoup(html, 'html.parser')
        temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
        str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text
        # formatting data
        data = str.split('\n')
        sky = data[1]
        # getting all div tag   
        listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
        strd = listdiv[5].text
        # getting other required data
        pos = strd.find('Wind')
        other_data = strd[pos:]
        return temp, sky

