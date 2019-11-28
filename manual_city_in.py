#!/usr/bin/python3
"""
Author:     Konstantinos Liosis
File:       manual_city_in.py
Desc:       Manual city insertion due to OpenStreetMaps lack of results
"""

from create_city import city


def manual_city(cursor, db_conn):
    try:
        names = ["Larissa", "Arkadia"]
        args = [(39.5, 22.5, 2, 1), (37.5, 22.5, 2, 1)]

        query = "INSERT INTO geolocation(lat, lon, altitude, ctr_uid)" \
                "VALUES (%s, %s, %s, %s)"
        cursor.executemany(query, args)
        db_conn.commit()

        for idx, ct in enumerate(args):
            # Fetch the UID for possible city creation
            cursor.execute("SELECT geol_uid FROM geolocation WHERE lon = %s AND lat = %s",
                           [ct[1], ct[0]])
            geo_id = cursor.fetchone()[0]
            city(ct[1], ct[0], cursor, db_conn, 2, 1, geo_id, force=names[idx-1])

    except Exception as e:
        print(e)