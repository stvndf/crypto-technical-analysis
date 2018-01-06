import database
import datetime
import numpy
from decimal import Decimal

def mavg(pair, num_of_days, start_date):
    connection = database.connect()
    cursor = connection.cursor()
    rows = []
    avg_prices = []

    for i in range(num_of_days):
       cursor.execute("SELECT * FROM " + pair + " WHERE date = '" + str(start_date) + "';")
       rows.append(cursor.fetchone())
       start_date += datetime.timedelta(days=1)
    rows = filter(None,rows)

    for row in rows:
       avg = row[5]
       avg_prices.append(avg)
    if len(avg_prices) == 0:
       return 0
    return sum(avg_prices)/len(avg_prices)
    
    connection.commit()
    connection.close()

def ema(pair,num_of_days,start_date):
    connection = database.connect()
    cursor = connection.cursor()
    rows = []
    first_day = mavg(pair,num_of_days,start_date-datetime.timedelta(days=1))
    for i in range(num_of_days):
       cursor.execute("SELECT * FROM " + pair + " WHERE date = '" + str(start_date) + "';")
       rows.append(cursor.fetchone())
       start_date += datetime.timedelta(days=1)
    #rows = filter(None,rows)
    check = 0
    ema = 0
    multiplier = str((2.0/(float(num_of_days)+1.0)))
    for row in rows:
       if row is None:
           pass
       else:
           if check == 0:
               ema = (row[5] - first_day) * Decimal(multiplier) + first_day
           else:
               ema = (row[5] - ema) * Decimal(multiplier) + ema

    return ema
    
    connection.commit()
    connection.close()
    
def macd(pair,shorter,longer,start_date):
    mac = ema(pair,longer,start_date)
    start_date += datetime.timedelta(days=(longer-shorter))
    mic = ema(pair,shorter,start_date)

    if mic < mac:
        return 0
    elif mic > mac:
        return 1
    elif mic == mac:
        return 2

def stoch_osc(pair,window,date):
    connection = database.connect()
    cursor = connection.cursor()
    date_hold = date
    rows = []
    for i in range(window):
       cursor.execute("SELECT * FROM " + pair + " WHERE date = '" + str(date) + "';")
       rows.append(cursor.fetchone())
       date -= datetime.timedelta(days=1)
    rows = list(filter(None,rows))
    check = 0
    low = 0
    high = 0
    for row in rows:
       if check == 0:
           low = row[4]
           high = row[3]
           check = 1
       else:
           if row[4] < low:
              low = row[4]
           if row[3] > high:
              high = row[3]
    return 100*(rows[len(rows)-1][5]-low)/(high-low)

    connection.commit()
    connection.close()
    
def stoch_osc_mavg(pair,num_of_days,window,date):
    avg_stoch = []
    for i in range(num_of_days):
       avg_stoch.append(stoch_osc(pair,window,date))
       date -= datetime.timedelta(days=1)
    return sum(avg_stoch)/len(avg_stoch)
