import psycopg2
import psycopg2.pool

db_details = {'user': 'postgres', 'password': 'pass', 'database': 'crypto_project', 'host': 'localhost'}

def connect():
    return psycopg2.connect(**db_details)

connection_pool = psycopg2.pool.SimpleConnectionPool(minconn=1,  #TODO: consider removing if not used
                                                     maxconn=10,
                                                     **db_details)

