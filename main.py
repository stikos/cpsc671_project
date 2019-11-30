#!/usr/bin/python3
"""
Author:     Konstantinos Liosis
File:       main.py
Desc:       Database creation
"""

import configparser
import os
import mysql.connector as mysql

from create_db import create
from create_tables import tables
from insert_data import insert
from insert_patterns import patterns
from manual_city_in import manual_city
from queries import box
config = configparser.ConfigParser()
config.read('config.ini')
NAME = config['DB']['name']
TABLES = config['DB']['tables']
HOST = config['HOST']['def']
USER = config['USERS']['1']
PASS = config['PASS']['1']


if __name__ == "__main__":
    try:
        db_conf = {
            "host": HOST,
            "user": USER,
            "password": PASS
        }

        db_conn = mysql.connect(**db_conf)
        cursor = db_conn.cursor()

    except Exception as e:
        print(e)

    create(NAME, cursor, db_conn)
    db_conf["database"] = NAME
    db_conn = mysql.connect(**db_conf)
    # cursor = db_conn.cursor()
    # tables(cursor, db_conn, script_file=TABLES)
    # manual_city(cursor, db_conn)
    # insert(cursor,
    #        db_conn,
    #        data_files=["temperature_data.txt", "pressure_data.txt"],
    #        datetime_file="datetime.txt")
    # files = os.listdir("pattern_data")
    # patterns(cursor, db_conn, files)
    box(db_conn)