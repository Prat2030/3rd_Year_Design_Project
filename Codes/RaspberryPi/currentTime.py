import time
import requests
from dateutil.parser import parse

def currTime():
    response = requests.get("https://worldtimeapi.org/api/timezone/Asia/Kolkata").json()
    current_time = response["datetime"]
    current_time = parse(current_time)
    current_time_str = current_time.strftime("%H:%M:%S")
    return current_time_str



while True:
    print(currTime())
    time.sleep(60)
