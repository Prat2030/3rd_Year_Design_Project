# Video Link : https://www.youtube.com/watch?v=mvjMmikaDJ0&ab_channel=EC9CLASSES
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)    #8 is the pin number
# GPIO.setup(10, GPIO.OUT)  #10 is the pin number

while True:
    # print(GPIO.input(7))
    if GPIO.input(7) == 0:
        print("No light")
        #print(GPIO.input(7))
        # GPIO.output(10, GPIO.LOW)
    else:
        print("Light")
        #print(GPIO.input(7))
        # GPIO.output(10, GPIO.HIGH)
    time.sleep(3)