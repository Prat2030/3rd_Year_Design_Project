import time
from datetime import datetime
import adafruit_dht
import pymongo
from pymongo import MongoClient
import RPi.GPIO as GPIO
from time import strftime
import board
import requests
from dateutil.parser import parse

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)    #4 is the pin number for LDR

#Variables for MongoDB
client = MongoClient("mongodb+srv://admin:li8TXxeO8n416O8t@cluster0.h0ymi0w.mongodb.net/?retryWrites=true&w=majority")
db = client['sensor']
collection = db['sensorData']

def currDate():
    response = requests.get("https://worldtimeapi.org/api/timezone/Asia/Kolkata").json()
    current_date = response["datetime"]
    current_date = parse(current_date)
    current_date_str = current_date.strftime("%Y-%m-%d")
    return current_date_str

def currTime():
    response = requests.get("https://worldtimeapi.org/api/timezone/Asia/Kolkata").json()
    current_time = response["datetime"]
    current_time = parse(current_time)
    current_time_str = current_time.strftime("%H:%M:%S")
    return current_time_str


def tempRead(): #read temperature, return float with 3 decimal places
        sensors = adafruit_dht.DHT11(board.D22)
        temperature = sensors.temperature
        degrees = float('{0:.3f}'.format(temperature))
        return degrees

def humidityRead(): #read humidity, return float with 3 decimal places
        sensors = adafruit_dht.DHT11(board.D22)
        humidity = sensors.humidity
        humidity = float('{0:.3f}'.format(humidity))
        return humidity

def ldrRead(): #read LDR, return 0 or 1
        if GPIO.input(4) == 0:
                #GPIO.output(10, GPIO.LOW)
                return False
        else:

                #GPIO.output(10, GPIO.HIGH)
                return True

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
        # # formatting data
        # data = str.split('\n')
        # sky = data[1]
        return temp

def skyDesc():
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
        return sky


current_time = currTime()
current_date = currDate()
temperature = tempRead()
humidity = humidityRead()
local_tempt = localTempt()
local_sky_dec = skyDesc()
ldr = ldrRead()

# Write data to MongoDB database
def mongoWrite(): 
        temps = local_tempt.replace(u"°C", "")
        tempDiff = abs(temperature - float(temps[:-1]))
        data = {"room":"9001", "date": current_date, "time": current_time,"temperature": temperature, "humidity": humidity, "local weather": local_tempt, "sky description": local_sky_dec,"temperature difference": tempDiff}
        collection.insert_one(data)
        return True

while True:
        print("Writing to the database...")
        try:
                mongoWrite()
                print("Writing completed") 
        # except:
        #         print("We have a problem !!")
        except pymongo.errors.ServerSelectionTimeoutError as err:
                print("pymongo ERROR:", err)
        except RuntimeError as error:
                print(error.args[0])
        time.sleep(5)