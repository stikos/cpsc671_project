#!/usr/bin/python3
"""
Author:     Konstantinos Liosis
File:       main.py
Desc:       Database creation
"""

import configparser
import mysql.connector as mysql

from create_db import create
from create_tables import tables
from insert_data import insert
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
    cursor = db_conn.cursor()
    tables(NAME, cursor, db_conn, script_file=TABLES)
    insert(NAME, cursor, db_conn, data_file="temperature_data.txt", datetime_file="datetime.txt")

