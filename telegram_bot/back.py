from function import *
from database import *
from datetime import datetime
import time

while True:
    numbers = all_phone_numbers()
    for number in numbers:
        print(number)
        try:
            send_health_recommendations(41,61, number)
        except:
            pass
    time.sleep(3600)