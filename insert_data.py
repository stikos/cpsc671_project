#!/usr/bin/python3
"""
Author:     Konstantinos Liosis
File:       insert_data.py
Desc:       Data entry
"""

from cursor import get_cursor
from create_city import city
import os

ALTITUDE = 2  # Fixed value at the moment


def insert(db_name, cursor, db_conn, data_file, datetime_file):
    """
    Inserts data in the database
    :param db_name: The name of the database
    :param data_file: The file containing the measurements
    :param datetime_file: The file containing the measurements' times
    :return: None
    """
    # cursor = get_cursor(db_name)

    # Add weather variable first, only temperature initially
    try:
        query = "INSERT INTO weather_variable(variable, description)" \
                "VALUES (%s, %s)"
        args = ["temperature", "Temperature measurement at a fixed height of 2m above the sea level"]
        cursor.execute(query, args)
        db_conn.commit()
    except Exception as e:
        print(e)

    # Add country, only Greece initially
    try:
        query = "INSERT INTO country(name)" \
                "VALUES (%s)"
        args = ["Greece"]
        cursor.execute(query, args)
        db_conn.commit()
    except Exception as e:
        print(e)

    # Create a list of all datatime objects as tuples in a list, preserving the order
    with open(datetime_file, "r") as dt:
        dt_list = list(map(lambda x: ('-'.join([x[6:8], x[4:6], x[:4]]), x[8:-2]), dt.readlines()))

    # Read the data file line by line and create the respective records.
    # I'll try to parse the data once and create all the records
    data = list(map(lambda x: x.split(","), open(data_file, 'r').readlines()))

    # Fetch the country (Greece) UID to create the geolocations later
    cursor.execute("SELECT ctr_uid FROM country")
    country_id = cursor.fetchall()[0][0]

    # Fetch the weather variable UID (temperature) for later use
    cursor.execute("SELECT wvl_uid FROM weather_variable")
    wv_id = cursor.fetchall()[0][0]

    for idx1, record in enumerate(data):
        entries = []
        print("{} out of {} records inserted".format(idx1, len(data)), end='\r')
        latitude = float(record[0])
        longitude = float(record[1])

        # First create a new geolocation record
        geo_id = None
        try:
            query = "INSERT INTO geolocation(lat, lon, altitude, ctr_uid)" \
                    "VALUES (%s, %s, %s, %s)"
            args = [latitude, longitude, ALTITUDE, country_id]
            cursor.execute(query, args)
            db_conn.commit()

            # Fetch the UID for possible city creation
            cursor.execute("SELECT geol_uid FROM geolocation WHERE lon = %s AND lat = %s",
                           [longitude,
                           latitude])
            geo_id = cursor.fetchall()[0][0]

        except Exception as e:
            print(e)

        # Then create a city record based on that geolocation using geopy
        city(latitude, longitude, cursor, db_conn, ALTITUDE, country_id, geo_id)

        for idx2, measurement in enumerate(record[2:]):
            entries.append((wv_id,
                            dt_list[idx2-1][1],
                            dt_list[idx2-1][0],
                            geo_id,
                            ALTITUDE,
                            float(measurement),
                            "Unspecified"))

        try:
            query = "INSERT INTO raw_measurement(wvl_uid, time, date, geol_uid, height, vector_val, vector_dir)" \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(query, entries)
            db_conn.commit()
        except Exception as e:
            print(e)
