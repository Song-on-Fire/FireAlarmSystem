import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish #publish dependency
from constants import ConfigUtils
import subprocess
import pwa_controller as p_cntr
import sqlite3
import time
from datetime import datetime
import os
import csv

def execute_query_with_retry(conn, query:str, values = None, requires_commit=False, max_retries=3, delay = 0.1, executeMany = False ):
    for i in range(max_retries):
        try: 
            cursor = conn.cursor()
            if values and executeMany:
                cursor.executemany(query, values)
            elif values:
                print(values)
                print(query)
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            if requires_commit:
                conn.commit()
            return cursor.fetchall() # if the command does not return rows, then empty list is returned
        except sqlite3.OperationalError as err:
            if "database is locked" in str(err):
                print(f"Database is locked. Retrying in {delay} seconds...")
                time.sleep(delay)
                continue
            else:
                raise
    raise sqlite3.OperationalError("Max retries exceeded. Unable to execute query.")


def addAlarmToDB(alarmSerial):
    # change this path for where the sqlite db is located in the projectserver
    connection = sqlite3.connect("/home/larnell/Blaze-PWA/BlazeFrontEnd/FireAlarmApp/db.sqlite")
    insertQuery = '''INSERT INTO alarms (alarmSerial, location, createdAt, updatedAt) VALUES (?,?,?,?)'''
    selectQuery = '''SELECT * FROM alarms WHERE alarmSerial = ?'''
    # check if alarmSerial already exists in DB
    if execute_query_with_retry(conn=connection, query=selectQuery, values=(alarmSerial,)):
        # if rows are returned, return success (True)
        connection.close()
        return None
    else:
        execute_query_with_retry(conn=connection,query=insertQuery, values=(alarmSerial,"unknown", datetime.now(), datetime.now()), requires_commit=True)
        connection.close()
        return True
    #
    #  else
        # run Insert query

def getAllAlarmsInDB():
    selectQuery = '''SELECT alarmSerial FROM alarms'''
    connection = sqlite3.connect("/home/larnell/Blaze-PWA/BlazeFrontEnd/FireAlarmApp/db.sqlite")
    alarm_rows = execute_query_with_retry(conn=connection, query=selectQuery)
    return alarm_rows
