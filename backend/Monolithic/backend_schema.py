import psycopg2
from Monolithic.constants import *

# connecting flask

def init_pg_tables():
    #initializing postgresql database
    conn = psycopg2.connect(database=DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT)
    print("i am here")
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
    
    cur.execute('''
                  CREATE TABLE records
                  (
                        xqg_r_id                                     SERIAL primary key NOT NULL,
                        xqg_r_usecase                                text,
                        xqg_r_input_nl_query                         text,
                        xqg_r_generated_query                        text,
                        xqg_r_created_user_id                        bigint,
                        xqg_r_created _timestamp                     timestamp,
                        xqg_r_last_updated_user_id                   bigint,
                        xqg_r_last_updated_timestamp                 timestamp,
                        xqg_r_status                                   bigint,      
                        CONSTRAINT   records_xqg_r_created_user_id
                        FOREIGN KEY (xqg_r_created_user_id) 
                        REFERENCES users(xqg_user_id) ON DELETE CASCADE  
                  );
            ''')