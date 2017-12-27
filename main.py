import cryptocurrency


# Currencies to value cryptocurrencies against:
TO_CURRENCIES = ['USD', 'GBP', 'EUR']


# Set up all cryptocurrencies as classes:
bitcoin = cryptocurrency.Cryptocurrency('BTC')
litecoin = cryptocurrency.Cryptocurrency('LTC')
ethereum = cryptocurrency.Cryptocurrency('ETH')

# Creating and populating table for each cryptocurrency class:
for i in TO_CURRENCIES:
    bitcoin.create_table(i)
    bitcoin.populate_table(i)

    litecoin.create_table(i)
    litecoin.populate_table(i)

    ethereum.create_table(i)
    ethereum.populate_table(i)







