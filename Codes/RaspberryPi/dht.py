import adafruit_dht
import time
import board

# Set sensor type : Options are DHT11,DHT22 or AM2302
# sensor=Adafruit_DHT.DHT11
# sensor_pin = 22

while True:
    # humidity, temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)
    sensors = adafruit_dht.DHT11(board.D22)
    temperature = sensors.temperature
    humidity = sensors.humidity
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))
    else:
        print('Failed to get reading. Try again!')
    time.sleep(5)


import time
import board
import adafruit_dht
#Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT11(board.D17)
while True:
    try:
         # Print the values to the serial port
         temperature_c = dhtDevice.temperature
         temperature_f = temperature_c * (9 / 5) + 32
         humidity = dhtDevice.humidity
         print("Temp: {:.1f} F / {:.1f} C    Humidity: {}% "
               .format(temperature_f, temperature_c, humidity))
    except RuntimeError as error:     # Errors happen fairly often, DHT's are hard to read, just keep going
         print(error.args[0])
    time.sleep(2.0)