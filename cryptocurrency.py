from database_config import connection_pool  #TODO: consider removing if unused
import database_config
import cryptocompare
import datetime


class Cryptocurrency:
    """Represents a particular cryptocurrency."""

    def __init__(self, from_currency_symbol):
        self.symbol = from_currency_symbol

    def __repr__(self):
        return f"Represents cryptocurrency: {self.symbol}"


    def get_data(self, to_currency_symbol, exchange):  #TODO: Determine whether the default (CCCAGG) from cryptocompare.py will work without explicitly stating in this parameter.
        """Returns historical data relating to the cryptocurrency against the to_currency_symbol currency."""
        to_currency_symbol = to_currency_symbol
        histo_day_data = cryptocompare.get_histo_day(self.symbol, to_currency_symbol, exchange)  # to_timestamp value is time.time() by default. May set specific time later for consistency.

        for i in histo_day_data['Data']:
            """Inserts datetime times corresponding to respective timestamps from CryptoCompare"""
            datetime_date = datetime.datetime.fromtimestamp(i['time'])  # datetime.datetime
            ##datetime_date = datetime.datetime.fromtimestamp(i['time']).strftime('%Y-%m-%d %H:%M:%S')  # string in case Postgres processes it better #TODO: consider whether to use this in lieu of above line.
            i['datetime_time'] = datetime_date

        return histo_day_data


    def data_usd(self):  #TODO: consider whether these are redundant
        return self.get_data('USD')

    def data_gbp(self):
        return self.get_data('GBP')

    def data_gbp(self):
        return self.get_data('GBP')


    def create_table(self, to_currency_symbol, exchange):
        """ Creates table for each for each cryptocurrency-fiat currency-exchange set.
            Drops table if data is not available from the particular exchange.
        """
        connection = database_config.connect()
        with connection.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS {} (date DATE PRIMARY KEY, timestamp INT, open NUMERIC(8, 2), high NUMERIC(8, 2), low NUMERIC(8, 2), close NUMERIC(8, 2), volumefrom NUMERIC(18, 4), volumeto NUMERIC(18, 4))"
                           .format(self.symbol + '_' + to_currency_symbol + '_' + exchange))
        connection.commit()
        connection.close()


    def populate_table(self, to_currency_symbol, exchange):
        """Populates each table with data from particular exchange.
            Drops table if exchange doesn't have data relating to currency pair.
        """
        connection = database_config.connect()
        data = self.get_data(to_currency_symbol, exchange)

        # Exchange contains data relating to the particular currency pair:
        if data['Response'] == 'Success':
            print("Success populating table:", self.symbol + '_' + to_currency_symbol + '_' + exchange.lower())
            with connection.cursor() as cursor:
                cursor.executemany("INSERT INTO {} (date, timestamp, open, high, low, close, volumefrom, volumeto) VALUES "
                                   "(%(datetime_time)s, %(time)s, %(open)s, %(high)s, %(low)s, %(close)s, %(volumefrom)s, %(volumeto)s)"
                                   .format(self.symbol + '_' + to_currency_symbol + '_' + exchange.lower()), self.get_data(to_currency_symbol, exchange)['Data'])

        # Exchange does not contain data relating to the particular currency pair:
        else:
            print("Error: ", data['Message'], self.symbol + '_' + to_currency_symbol)
            print("Action taken: Dropping table", (self.symbol + '_' + to_currency_symbol + '_' + exchange).lower())
            with connection.cursor() as cursor:
                cursor.execute("DROP TABLE {}".format(self.symbol + '_' + to_currency_symbol + '_' + exchange))

        connection.commit()
        connection.close()






# For module testing:
if __name__ == "__main__":

    btc = Cryptocurrency('BTC')
    print(btc.symbol)
    btc.create_table('GBP', 'Bitstamp')
    btc.populate_table('GBP', 'Bitstamp')





