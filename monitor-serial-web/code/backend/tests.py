from datetime import datetime
from time import sleep

a = datetime.now()
sleep(5)
b = datetime.now()
print(b - a)
print((b - a).seconds)
print(((b - a).microseconds > 106000))