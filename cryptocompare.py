import datetime
import time
import requests


URL_HISTO_DAY = "https://min-api.cryptocompare.com/data/histoday?fsym={}&tsym={}&toTs={}&e={}&allData=true"


def request_cryptocompare(url, error_check=False):
    """Makes request to CryptoCompare URL"""
    try:
        response = requests.get(url).json()
    except Exception as e:
        print(f'Error obtaining data: {str(e)}')
        return None
    if error_check and 'Response' in response.keys():
        print('[ERROR] %s' % response['Response'])
        return None
    return response

def get_histo_day(from_currency_symbol, to_currency_symbol, exchange, to_timestamp=time.time()):
    """Adjusts URL to contain given parameters before running request"""
    if isinstance(to_timestamp, datetime.datetime):
        to_timestamp = time.mktime(to_timestamp.timetuple())  # converts datetime.datetime to timestamp
    return request_cryptocompare(url=URL_HISTO_DAY.format(from_currency_symbol,
                                                          to_currency_symbol,
                                                          int(to_timestamp),
                                                          exchange))





# For module testing:
if __name__ == "__main__":

    var = get_histo_day('BTC', 'GBP', 'Bitstamp')
    print(var)
    print(var['Response'])

