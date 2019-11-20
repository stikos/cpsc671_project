#!/usr/bin/python3
"""
Author:     Konstantinos Liosis
File:       cursor.py
Desc:       Get a cursor to execute SQL statements
"""

import configparser
import mysql.connector as mysql

config = configparser.ConfigParser()
config.read('config.ini')
HOST = config['HOST']['def']
USER = config['USERS']['1']
PASS = config['PASS']['1']


def get_cursor(db=None):
    """
    Create an instance of 'cursor' class to execute SQL statements
    :param db: Database name (None when creating a DB)
    :return: The cursor object or None
    """
    try:
        db_conf = {
            "host": HOST,
            "user": USER,
            "password": PASS
        }

        if db:
            db_conf["database"] = db

        db_conn = mysql.connect(**db_conf)
        cursor = db_conn.cursor()
        return cursor

    except Exception as e:
        print(e)
        return None

