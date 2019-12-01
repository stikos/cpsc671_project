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
import queries
config = configparser.ConfigParser()
config.read('config.ini')
NAME = config['DB']['name']
TABLES = config['DB']['tables']
HOST = config['HOST']['def']
USER = config['USERS']['1']
PASS = config['PASS']['1']


if __name__ == "__main__":

    try:
        db_conf = {"host": HOST, "user": USER, "password": PASS, "database": NAME}

        db_conn = mysql.connect(**db_conf)
        cursor = db_conn.cursor()

    except Exception as e:
        print(e)
        exit()

    print("Weather Data Manager PoC")
    choice = int(input("Enter 1 for database creation, 2 for querying: "))

    if choice == 1:
        # Check for pass as a safeguard to mistakenly rebuilding the db
        pass_check = input('Enter db password: ')
        if pass_check != PASS:
            print("Incorrect password.")
            exit()

        create(NAME, cursor, db_conn)
        db_conn = mysql.connect(**db_conf)
        cursor = db_conn.cursor()
        tables(cursor, db_conn, script_file=TABLES)
        manual_city(cursor, db_conn)
        insert(cursor,
               db_conn,
               data_files=["temperature_data.txt", "pressure_data.txt"],
               datetime_file="datetime.txt")
        files = os.listdir("pattern_data")
        patterns(cursor, db_conn, files)

    elif choice == 2:
        while choice not in ["exit", 'e']:
            print("1. Square area of interest",
                   "2. List of cities",
                   "3. Average monthly/yearly temperature charts for Greece", sep="\n")
            choice = int(input("Select a query by number: "))

            if choice == 1:
                points = queries.box(db_conn)
                print("{} points retrieved".format(len(points)))
                print("1. Top 5 patterns for temperature",
                       "2. Top 5 patterns for geopotential height",
                       "3. Average pattern length (among all variables)", sep="\n")
                choice = int(input("Select a query by number: "))

                if choice == 1:
                    queries.top5(db_conn, 1, points)
                if choice == 2:
                    queries.top5(db_conn, 2, points)
                if choice == 3:
                    print("Granularity (in alphabet size):"
                          "1. 5 characters",
                          "2. 10 characters", sep="\n")
                    choice = int(input("Select by number: "))
                    queries.avg_ptrn_len(db_conn, choice)

            if choice == 2:
                queries.cities(db_conn)

            if choice == 3:
                print("1. Monthly",
                       "2. Yearly", sep="\n")
                choice = int(input("Select a query by number: "))