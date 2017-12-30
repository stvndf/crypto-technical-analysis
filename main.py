import cryptocurrency


# Currencies to value cryptocurrencies against:
TO_CURRENCIES = ['USD', 'GBP', 'EUR']
EXCHANGES = ['CCCAGG', 'Coinbase', 'Bitstamp', 'Poloniex']


# Set up all cryptocurrencies as classes:
bitcoin = cryptocurrency.Cryptocurrency('BTC')
litecoin = cryptocurrency.Cryptocurrency('LTC')
ethereum = cryptocurrency.Cryptocurrency('ETH')

# Creating and populating table for each cryptocurrency class:
for c in TO_CURRENCIES:
    for e in EXCHANGES:
        bitcoin.create_table(c, e)
        bitcoin.populate_table(c, e)

        litecoin.create_table(c, e)
        litecoin.populate_table(c, e)

        ethereum.create_table(c, e)
        ethereum.populate_table(c, e)



