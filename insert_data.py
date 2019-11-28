#!/usr/bin/python3
"""
Author:     Konstantinos Liosis
File:       insert_data.py
Desc:       Data entry
"""

from create_city import city

ALTITUDE = 2  # Fixed value at the moment


def insert(cursor, db_conn, data_files, datetime_file):
    """
    Inserts data in the database
    :param db_name: The name of the database
    :param data_file: The file containing the measurements
    :param datetime_file: The file containing the measurements' times
    :return: None
    """

    # Temperature variable
    try:
        query = "INSERT INTO weather_variable(variable, description)" \
                "VALUES (%s, %s)"
        args = ["temperature", "Temperature measurement at a fixed height of 2m above the sea level"]
        cursor.execute(query, args)
        db_conn.commit()
    except Exception as e:
        print(e)

    # Pressure-height variable
    try:
        query = "INSERT INTO weather_variable(variable, description)" \
                "VALUES (%s, %s)"
        args = ["pressure_height", "Height at which the pressure is 500mbar"]
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
        dt_list = list(map(lambda x: ('-'.join([x[:4], x[4:6], x[6:8]]), ':'.join([x[8:].strip('\n'), "00:00"])), dt.readlines()))

    # Read the data file line by line and create the respective records.
    # I'll try to parse the data once and create all the records
    t_data = list(map(lambda x: x.split(","), open(data_files[0], 'r').readlines()))
    p_data = list(map(lambda x: x.split(","), open(data_files[1], 'r').readlines()))

    # Fetch the country (Greece) UID to create the geolocations later
    cursor.execute("SELECT ctr_uid FROM country")
    country_id = cursor.fetchall()[0][0]

    # Fetch the weather variable UID (temperature) for later use
    cursor.execute("SELECT wvl_uid FROM weather_variable")
    res = cursor.fetchall()
    t_id = res[0][0]
    p_id = res[1][0]

    for idx1, record in enumerate(t_data):
        t_entries = []  # temperature data
        p_entries = []  # pressure data
        print("{} out of {} records inserted".format(idx1, len(t_data)), end='\r')
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
            geo_id = cursor.fetchone[0]

        except Exception as e:
            print(e)

        # Then create a city record based on that geolocation using geopy
        city(latitude, longitude, cursor, db_conn, ALTITUDE, country_id, geo_id)

        for idx2, measurement in enumerate(record[2:]):
            t_entries.append((t_id,
                              dt_list[idx2 - 1][0],
                              dt_list[idx2 - 1][1],
                              geo_id,
                              ALTITUDE,
                              float(measurement),
                              "Unspecified"))

            p_entries.append((p_id,
                              dt_list[idx2 - 1][0],
                              dt_list[idx2 - 1][1],
                              geo_id,
                              ALTITUDE,
                              float(p_data[idx1][idx2 - 1]),
                              "Unspecified"))

        try:
            query = "INSERT INTO raw_measurement(wvl_uid, date, time, geol_uid, height, vector_val, vector_dir)" \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(query, t_entries)
            db_conn.commit()
        except Exception as e:
            print(e)
