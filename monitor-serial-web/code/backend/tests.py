import time
from datetime import timezone, datetime

date = '2020-11-24 10:55:00'
print(date)
print(datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timestamp())
