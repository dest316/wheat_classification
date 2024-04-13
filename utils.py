import sqlite3


PATH_TO_DB = 'wheat_cl.db'


def get_db_connection():
    conn = sqlite3.connect(PATH_TO_DB)
    return conn
