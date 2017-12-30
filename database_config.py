import psycopg2
import psycopg2.pool

config = {'user': 'postgres', 'password': 'pass', 'database': 'crypto_project', 'host': 'localhost'}

def connect():
    return psycopg2.connect(**config)

connection_pool = psycopg2.pool.SimpleConnectionPool(minconn=1,  #TODO: consider removing if not used
                                                     maxconn=10,
                                                     **config)

