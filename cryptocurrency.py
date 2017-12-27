from database import connection_pool  #TODO: consider removing if unused
import database
import cryptocompare
import datetime

class Cryptocurrency:
    """Represents a particular cryptocurrency."""

    def __init__(self, from_currency_symbol):
        self.symbol = from_currency_symbol

    def __repr__(self):
        return f"Represents cryptocurrency: {self.symbol}"


    def get_data(self, to_currency_symbol):
        """Returns historical data relating to the cryptocurrency against the to_currency_symbol currency."""
        to_currency_symbol = to_currency_symbol
        histo_day_data = cryptocompare.get_histo_day(self.symbol, to_currency_symbol)

        for i in histo_day_data['Data']:
            """Inserts datetime times corresponding to respective timestamps from CryptoCompare"""
            datetime_date = datetime.datetime.fromtimestamp(i['time'])  # datetime.datetime
            ##datetime_date = datetime.datetime.fromtimestamp(i['time']).strftime('%Y-%m-%d %H:%M:%S')  # string in case Postgres processes it better #TODO: consider whether to use this in lieu of above line.
            i['datetime_time'] = datetime_date

        return histo_day_data


    def data_usd(self):
        return self.get_data('USD')

    def data_gbp(self):
        return self.get_data('GBP')

    def data_gbp(self):
        return self.get_data('GBP')


    def create_table(self, to_currency_symbol):
        connection = database.connect()
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS {} (date DATE PRIMARY KEY, timestamp INT, open NUMERIC(8, 2), high NUMERIC(8, 2), low NUMERIC(8, 2), close NUMERIC(8, 2), volumefrom NUMERIC(18, 4), volumeto NUMERIC(18, 4))"
                           .format(self.symbol + '_' + to_currency_symbol))

            ##cursor.execute("CREATE TABLE IF NOT EXISTS {} (date DATE PRIMARY KEY, timestamp INT, open NUMERIC(8, 2), high NUMERIC(8, 2), low NUMERIC(8, 2), close NUMERIC(8, 2), %s NUMERIC(36, 18), %s NUMERIC(36, 18))"
            ##               .format(self.symbol + '_' + to_currency_symbol),
            ##               (psycopg2.extensions.AsIs(self.symbol + '_volume'), psycopg2.extensions.AsIs(to_currency_symbol + '_volume')))
        connection.commit()
        connection.close()

    def populate_table(self, to_currency_symbol):
        connection = database.connect()
        with connection.cursor() as cursor:
            cursor.executemany("INSERT INTO {} (date, timestamp, open, high, low, close, volumefrom, volumeto) VALUES "
                               "(%(datetime_time)s, %(time)s, %(open)s, %(high)s, %(low)s, %(close)s, %(volumefrom)s, %(volumeto)s)"
                               .format(self.symbol + '_' + to_currency_symbol), self.get_data(to_currency_symbol)['Data'])
        connection.commit()
        connection.close()













#    def save_to_db(self):
#        connection = connection_pool.getconn()
#        with connection.cursor() as cursor:
#            cursor.execute('INSERT INTO crypto_project')
#
#        connection_pool.putconn(connection)








##btc = Cryptocurrency('BTC')
##print(btc.symbol)
###print(btc.data_usd())
##btc.create_table('USD')
##
##btc_list = btc.data_gbp()['Data']
##print(btc_list)
##
##new_list = [i for i in btc_list]
##print(new_list)

##for i in new_list:
##    print(i)




