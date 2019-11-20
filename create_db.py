#!/usr/bin/python3
"""
Author:     Konstantinos Liosis
File:       create_db.py
Desc:       Initial creation of database
"""

from cursor import get_cursor


def create(db_name, cursor, db_conn):
    """
    Create a new database
    :param name: Name of the new database
    :return: None
    """
    try:
        # cursor = get_cursor()
        cursor.execute("CREATE DATABASE " + db_name)
        db_conn.commit()
    except Exception as e:
        print(e)
