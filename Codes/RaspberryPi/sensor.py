import os
import time
from datetime import datetime
import glob
# import MySQLdb // for MySQL database
import adafruit_dht
import pymongo
from pymongo import MongoClient
import RPi.GPIO as GPIO
from time import strftime
import board
import requests
from bs4 import BeautifulSoup
import pytz

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)    #4 is the pin number for LDR
# GPIO.setup(22, GPIO.OUT)  #22 is the pin number for DHT11

#Variables for MongoDB
client = MongoClient("mongodb+srv://admin:li8TXxeO8n416O8t@cluster0.h0ymi0w.mongodb.net/?retryWrites=true&w=majority")
db = client['sensor']
collection = db['sensorData']

sensors = adafruit_dht.DHT11(board.D22)

def dateTime():
        # IST = pytz.timezone('Asia/Kolkata')
        # datetime_ist = datetime.now(IST)
        currentDateTime = datetime.now()
        # datetime_ist.strftime('%H:%M:%S')
        # now = datetime.now()
        # date = now.strftime("%Y-%m-%d")
        # times = now.strftime("%H:%M:%S")
        date = currentDateTime.strftime("%Y-%m-%d")
        # times = currentDateTime.strftime("%H:%M:%S")
        # datetimes = date + " " + times
        # datetimes = date
        return date

def tempRead(): #read temperature, return float with 3 decimal places
        temperature = sensors.temperature
        degrees = float('{0:.3f}'.format(temperature))
        return degrees

def humidityRead(): #read humidity, return float with 3 decimal places
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
#time2 = data[0]
sky = data[1]

# getting all div tag
listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
strd = listdiv[5].text

# getting other required data
pos = strd.find('Wind')
other_data = strd[pos:]

# printing all data
# print("Temperature is", temp)
# print("Time: ", time)
# print("Sky Description: ", sky)
# print(other_data)


secs = dateTime()
temperatures = tempRead()
humiditys = humidityRead()
lighting = ldrRead()

# Write data to MongoDB database
def mongoWrite(): 
        temps = temp.replace(u"°C", "")
        tempDiff = abs(temperatures - float(temps[:-1]))
        # data = {"room":"9001", "time": secs, "temperature": temperatures, "humidity": humiditys, "local weather": temps, "sky description": sky,"temperature difference": tempDiff}
        data = {"room":"9001", "date": secs, "time": time2,"temperature": temperatures, "humidity": humiditys, "local weather": temps, "sky description": sky,"temperature difference": tempDiff}
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
