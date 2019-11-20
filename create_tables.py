#!/usr/bin/python3
"""
Author:     Konstantinos Liosis
File:       create_tables.py
Desc:       Create database tables
"""

from cursor import get_cursor


def tables(db_name, cursor, db_conn, script_file=None):
    """
    Creation of database tables with both manual and script options
    :param db_name: The name of the database
    :param script_file: Filename of external SQL script
    :return: None
    """
    # cursor = get_cursor(db_name)

    if script_file is not None:
        create = open(script_file, 'r').read().replace('\n', '').split(';')

    else:
        create = list(input("Enter table name and fields, comma separated: "))
    try:
        for query in create:
            cursor.execute(query)
            db_conn.commit()

    except Exception as e:
        print(e)