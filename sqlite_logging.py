from dataclasses import dataclass
from datetime import datetime

# TODO write module docstring
# TODO update readme, including example sql tables (get them from old commits, in code comments)

def sql_command_create_table(
    table_name:str,
    sql_columns:list[tuple],
    ) -> str:
    """Construct an SQL command CREATE TABLE.

    The command has the following structure:
    'CREATE TABLE table_name (id INTEGER, column1 COLUMNTYPE, column2 COLUMNTYPE, ..., PRIMARY KEY (id))'
    """
    sql_create_command = "CREATE TABLE "  # start the command
    sql_create_command += f"{table_name} "  # add table name
    sql_create_command += "(id INTEGER, "  # add column for key

    # 1) Join the tuples pairs in the list to a comma separated string
    # 2) Declare the primary key
    sql_columns_table = [f"{pair[0]} {pair[1]}" for pair in sql_columns]
    sql_columns_table = f"{", ".join(sql_columns_table)}, PRIMARY KEY (id))"

    sql_create_command += sql_columns_table  # join all elements of the command

    return sql_create_command

def sql_create_row(
    table_name:str, 
    disk:dataclass,
    sql_columns:list[tuple],
    ) -> str:
    """Construct an SQL command to  INSERT values from input sql_columns.

    Command structure:
    'INSERT INTO table_name (column1, column2, ...) values ("cell1", "cell2", ...)'
    """
    # Start constucting the command
    sql_insert_command = f"INSERT INTO {table_name} "

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

    # Assemble the entire INSERT command
    sql_insert_command += f"({sql_column_insert}) "
    sql_insert_command += f"values ({sql_content_insert})"

    return sql_insert_command


