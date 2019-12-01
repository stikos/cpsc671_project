#!/usr/bin/python3
"""
Author:     Konstantinos Liosis
File:       insert_patterns.py
Desc:       Patterns entry
"""

import csv


def patterns(cursor, db_conn, files):
    """

    :param cursor:
    :param files:
    :return:
    """

    # pattern_class tables (only 2 classes)
    try:
        query = "INSERT INTO pattern_class(alphabet, num_classes)" \
                "VALUES (%s, %s)"
        args = [("abcde", "5"), ("abcdefghij", "10")]
        cursor.executemany(query, args)
        db_conn.commit()
    except Exception as e:
        print(e)

    # First insert the patterns, then positions
    for filename in [x for x in files if "positions" not in x]:
        print("Inserting {}".format(filename))
        file_type, city, class_type = filename.split("_")
        class_type = 1 if class_type == '5' else 2

        # Find geolocation uid
        geolocation = 0
        try:
            query = "SELECT geol_uid FROM city WHERE LOWER(name) = %s"
            cursor.execute(query, [city])
            geolocation = cursor.fetchall()[0][0]
        except Exception as e:
            print(e)

        # First count how many are already inserted to
        # make sure primary_key gets properly incremented
        num_of_pat = 0
        try:
            query = "SELECT COUNT(*) FROM pattern"
            cursor.execute(query)
            num_of_pat = int(cursor.fetchone()[0])
        except Exception as e:
            print(e)

        query = "INSERT INTO pattern(ptrn_id, ptrn, length, occurences, geol_uid, ptrn_c_uid)" \
                "VALUES (%s, %s, %s, %s, %s, %s)"

        final_data = []
        with open("pattern_data/"+filename, 'r') as csv_file:
            input_data = csv.reader(csv_file)

            for idx, row in enumerate(input_data):
                if idx > 1:
                    final_data.append((int(row[0]) + num_of_pat, row[1], row[2], row[3],  geolocation, class_type))

        cursor.executemany(query, final_data)
        db_conn.commit()


        # Insert positions
        query = "INSERT INTO result_position(ptrn_id, wvl_uid, position)" \
                "VALUES (%s, %s, %s)"

        for filename in [x for x in files if "positions" in x]:
            final_data = []
            with open("pattern_data/"+filename, 'r') as csv_file:
                input_data = csv.reader(csv_file)

                for idx, row in enumerate(input_data):
                    if idx > 1:
                        final_data.append((int(row[0]) + num_of_pat, row[1], row[2]))

        cursor.executemany(query, final_data)
        db_conn.commit()
