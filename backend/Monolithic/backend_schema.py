import psycopg2
from Monolithic.constants import *
from Monolithic.postgres_utils import *

# connecting flask

def init_pg_tables():
    #initializing postgresql database
    conn = psycopg2.connect(database=DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT)
    cur = conn.cursor()

    cur.execute('''
                  CREATE TABLE users
                  (
                        xqg_user_id                                     SERIAL primary key NOT NULL,
                        xqg_user_name                                   text,
                        xqg_user_mail                                   text,
                        xqg_user_password                               text,
                        xqg_created _timestamp                          timestamp,
                        xqg_status                                      bigint,        
                  );
            ''')
    
    # cur.execute('''
    #                 CREATE TABLE files
    #             ''')




