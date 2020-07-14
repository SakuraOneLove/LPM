"""Executing manipulations with sqlite 3 database like the:
* checking for exists database,
* creating new schema of database,
* make insert, update, searching and remove from database,
* managment database log file with all manipulations.
"""
import os
import pytz
import sqlite3
import datetime

STORAGE_TABLE_SQL = "create table if not exists vault (\
account_id integer primary key,\
name text not null,\
login text not null,\
password text not null,\
note text);"

def is_database_exists(database_name: str) -> bool:
    """Checking for the existence of a database with name 'database_name'."""
    return os.path.isfile(database_name)

def is_table_exists(database_name: str, table_name: str) -> bool:
    """Checking for the existence of a table with name 'table_name' in the database with name 'database_name'."""
    # If database doesn't exist skip the next operations
    if is_database_exists(database_name):
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("select name from sqlite_master where type= 'table' and name='{}';".format(table_name))
        expected_name = cursor.fetchone()
        try:
            result = expected_name[0] == table_name
        except TypeError:
            result = False
    else:
        result = False
    return result

def create_table_if_not_exists(database_name: str):
    """Creating in database 'database_name' table with name 'vault' if this table not exists."""
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute(STORAGE_TABLE_SQL)
    connection.commit()
    

def database_logger(file_name: str, message: str):
    """Logging database operations with time of executing operation to log file."""
    tzmsk = pytz.timezone("Europe/Moscow")
    time_now = datetime.datetime.now(tz=tzmsk).strftime("[%Y-%m-%dT%H:%M:%S]")
    with open(file_name, "a") as log_file:
        log_file.write("{} {}\n".format(time_now, message))
