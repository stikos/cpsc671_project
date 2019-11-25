#!/usr/bin/python3
"""
Author:     Konstantinos Liosis
File:       create_city.py
Desc:       City creation
"""

import geopy.geocoders
from geopy.geocoders import Nominatim
import certifi
import ssl
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

geolocator = Nominatim(scheme="http")


def city(latitude, longitude, cursor, db_conn, ALTITUDE, country_id, geo_id):
    try:
        city = geolocator.reverse(','.join([str(latitude), str(longitude)]), language='en', timeout=3)
        if "address" in city.raw and "city" in city.raw["address"]:
            city = city.raw["address"]["city"]
        else:
            city = "Undefined"
    except Exception as e:
        print(e)
        return None

    # Create a city record, if it does not exist
    city_id = None
    try:
        cursor.execute("SELECT ct_uid FROM city WHERE name = %s", [city])
        city_id = cursor.fetchall()
        if len(city_id) != 0:
            city_id = city_id[0][0]
        else:
            pass
    except Exception as e:
        print(e)

    if not city_id:
        try:
            query = "INSERT INTO city(name, geol_uid)" \
                    "VALUES (%s, %s)"
            args = [city, geo_id]
            cursor.execute(query, args)
        except Exception as e:
            print(e)

    db_conn.commit()