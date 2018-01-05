import database
import datetime
import numpy

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

def macd(pair,shorter,longer,start_date):
    mac = mavg(pair,longer,start_date)
    start_date += datetime.timedelta(days=(longer-shorter))
    mic = mavg(pair,shorter,start_date)

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

def stoch_osc_mavg(pair,num_of_days,window,date):
    avg_stoch = []
    for i in range(num_of_days):
       avg_stoch.append(stoch_osc(pair,window,date))
       date -= datetime.timedelta(days=1)
    return sum(avg_stoch)/len(avg_stoch)
