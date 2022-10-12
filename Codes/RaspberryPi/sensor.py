import os
import time
import datetime
import glob
# import MySQLdb // for MySQL database
import adafruit_dht
import pymongo
from pymongo import MongoClient
import RPi.GPIO as GPIO
from time import strftime
import board

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.IN)    #4 is the pin number for LDR
# GPIO.setup(22, GPIO.OUT)  #22 is the pin number for DHT11

#Variables for MySQL
# db = MySQLdb.connect(host="localhost", user="admin", passwd="pass123", db="sensor") # replace password with your password
# cur = db.cursor()

#Variables for MongoDB
client = MongoClient("mongodb+srv://admin:li8TXxeO8n416O8t@cluster0.h0ymi0w.mongodb.net/?retryWrites=true&w=majority")
db = client['sensor']
collection = db['sensorData']

sensors = adafruit_dht.DHT11(board.D22)
# sensor_pin = 22
# humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)

# temperature = sensors.temperature
# humidity = sensors.humidity

# def dateTime(): #get UNIX time
#         secs = float(time.time())
#         secs = secs*1000
#         return secs

def dateTime():
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        datetime = date + " " + time
        return datetime

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



secs = dateTime()
temperatures = tempRead()
humiditys = humidityRead()
lighting = ldrRead()

# Write data to MongoDB database
def mongoWrite(): 
        data = {"room":"9001", "time": secs, "temperature": temperatures, "humidity": humiditys, "ldr": lighting}
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

# write data to MySQL database
# sql = ("""INSERT INTO dhtsensor (datetime,temperature,humidity) VALUES (%s,%s,%s)""", (secs, temperatures, humiditys))

# try:
#     print("Writing to the database...")
#     cur.execute(*sql)
#     db.commit()
#     print ("Writing completed")

# except:
#     db.rollback()
#     print ("We have a problem !!")

# cur.close()
# db.close()
