#i have used django
#Create required db setup and django envirnoment
#install psycopg2 before using it
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import select
import threading
import json
import os

#we should be listening the trigger in background continously
#threading used for simplicity

#connect psycopg2 with database
conn = psycopg2.connect(
    host=os.environ.get("SQL_HOST"),
    port=os.environ.get("SQL_PORT"),
    dbname=os.environ.get("SQL_DATABASE"),
    user=os.environ.get("SQL_USER"),
    password=os.environ.get("SQL_PASSWORD"),
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)


curs = conn.cursor()
curs.execute("LISTEN new_id;")


#listening the trigger continously
def listen_callback():
    print("Waiting for notifications on channel 'test'")
    while True:
        if select.select([conn], [], [], 5) == ([], [], []):
            pass
        else:
            conn.poll()
            if conn.notifies:
                # print("Got NOTIFY:", conn.notifies[0].payload)
                notify = conn.notifies.pop(0)
                dict_values = json.loads(notify.payload)
                table = dict_values["table"]
                symbol = dict_values["row"]["symbol"]

                #perform your logic here
                #After trigger

#use threading for parallel task
t1 = threading.Thread(target=listen_callback)
#daemon for background running
t1.daemon = True
t1.start()
