import sqlite3
import configuration
from datetime import datetime

import main

# TODO refactor as function or functions called in main
# TODO write docstring

drives: list[main.DriveInfo] = main.drives

# Establish a connection to the database file.
# If it doesn't exist, it will be created.
conn = sqlite3.connect(configuration.db_filename)

# Create a cursor
cur = conn.cursor()

# Create a table if it doesn't already exist.
# Otherwise the SQL command CREATE will be skipped.
try:
    # Construct an SQL command CREATE TABLE  of the following structure:
    # 'CREATE TABLE table_name (column1 COLUMNTYPE, column2 COLUMNTYPE, ...)'
    sql_table_name = configuration.db_table_name  # get the table name

    sql_create_command = "CREATE TABLE "  # start the command
    sql_create_command += f"{sql_table_name} "  # add table name
    sql_create_command += "(id INTEGER, "  # add column for key

    # create list of tuples: (column_name, type)
    sql_columns: list[tuple[str, str]] = [
        ("path", "TEXT"),
        ("used_percent", "REAL"),
        ("free_gb", "REAL"),
        ("total_gb", "REAL"),
        ("snapshot_time", "TEXT"),
        ]

    # 1) Join the tuples pairs in the list to a comma separated string
    # 2) Declare the primary key
    sql_columns_table = [f"{pair[0]} {pair[1]}" for pair in sql_columns]
    sql_columns_table = f"{", ".join(sql_columns_table)}, PRIMARY KEY (id))"

    sql_create_command += sql_columns_table  # join all elements of the command
    # print(sql_create_command)
    cur.execute(sql_create_command)  # execute and commit to database
    conn.commit()
except sqlite3.OperationalError:
    # Do nothing if the table already exists
    pass


# Add rows of data to the table
# example:
# path      free_percent    used_gb     total_gb    snapshot_day    snapshot_time
# path1            25.00     100.00       400.00        20241122           141256
# path2            91.00       0.09         1.00        20241122           141256
for disk in drives:
    # Construct an SQL command INSERT of the following structure:
    # 'INSERT INTO table_name (column1, column2, ...) values ("cell1", "cell2", ...)'

    # Start constucting the command
    sql_insert_command = f"INSERT INTO {configuration.db_table_name} "

    # Join column names into a comma separated string
    sql_column_insert = [pair[0] for pair in sql_columns]
    sql_column_insert = ", ".join(sql_column_insert)

    # Get the data to be written to the cells
    sql_content_insert = [
        disk.path,
        disk.storage.used_percent,
        disk.storage.free_gb,
        disk.storage.total_gb,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ]

    # Join the data entries to a comma separated string
    sql_content_insert = ", ".join(f'"{w}"' for w in sql_content_insert)

    sql_insert_command += f"({sql_column_insert}) "
    sql_insert_command += f"values ({sql_content_insert})"

    # Execute the command and submit to the SQLite database
    cur.execute(sql_insert_command)
    conn.commit()
# Close the connection to the database
conn.close()
