from time import ctime
from datetime import date, datetime, timedelta


DATE_TODAY = date.today()
d = timedelta(days=-1)
d = DATE_TODAY + d
Y = d
d = str(d).split(' ')
YESTERDAY = d[0]

DAY_NAME = DATE_TODAY.strftime('%A')

def previous_month():
    year, month, _ = f'{DATE_TODAY}'.split('-')
    month = int(month) - 1
    if month < 1:
        month = 12
        year = int(year) - 1 
    return f'{year}-{month}'

PREVIOUS_MONTH = previous_month()