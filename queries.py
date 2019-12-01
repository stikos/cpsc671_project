#!/usr/bin/python3
"""
Author:     Konstantinos Liosis
File:       queries.py
Desc:       Queries processing & execution
"""


from calc_dist import dist


def quarter(val):
    """
    Turn coordinate values into multiples of a quarter of a degree (dataset limitation)
    :param val: Lat or Lon in string format
    :return: An acceptable value
    """
    remainder = float(val) % 25
    if remainder >= 13:
        return val + (25 - remainder)
    else:
        return val - remainder


def box(db_conn):
    """
    Executes the necessary operations and queries to return a set of geolocation UIDs representing the points
    in the desired square shaped area
    :param db_conn: The db connection object
    :return: The set of points UIDs
    """

    cursor = db_conn.cursor()

    user_in = input("Enter either a city name or a pair of coordinates (lat, lon): ")
    radius = float(input("Enter radius (>= 30km): "))

    # Check if input is a pair of coords. If it is, convert to quarters of a degree
    if ',' in user_in:
        user_in = list(map(quarter, user_in.replace(' ', '').split(',')))
    else:
        cursor.callproc("get_coords_by_name", [str.lower(user_in)])
        for res in cursor.stored_results():
            user_in = res.fetchall()[0]

    args = list(dist(user_in, radius))
    cursor.callproc("get_box", args)
    points = [x[0] for x in [res.fetchall() for res in cursor.stored_results()][0]]

    return points


def top5(db_conn, wvl, points):
#     docstring
    cursor = db_conn.cursor()
    cursor.callproc("get_top_5", [wvl, ','.join(list(map(str, points)))])
    resu = [res.fetchall() for res in cursor.stored_results()]
    print(resu)


def avg_ptrn_len(db_conn, num_class):
#     docstring
    cursor = db_conn.cursor()
    cursor.callproc("get_patterns", [num_class])
    ptrn_len = [res.fetchall()[0][0] for res in cursor.stored_results()][0]
    print("Average pattern length")


def cities(db_conn):
#     docstring
    cursor = db_conn.cursor()
    cursor.callproc("get_cities")
    cities = [x[0] for x in [res.fetchall() for res in cursor.stored_results()][0]]
    print(*cities, sep="\n")


def