"""Executing manipulations with sqlite 3 database like the:
* checking for exists database,
* creating new schema of database,
* make insert, update, searching and remove from database,
* managment database log file with all manipulations.
"""
import datetime
import sqlite3
import os
import pytz

STORAGE_TABLE_SQL = "create table if not exists vault (\
account_id integer primary key,\
name text not null,\
login text not null,\
password text not null,\
note text);"

LOG_NAME = "log/dbmanager.log"

def is_database_exists(database_name: str) -> bool:
    """Checking for the existence of a database with name 'database_name'."""
    result = os.path.isfile(database_name)
    if not result:
        database_logger(LOG_NAME, "Warning: Database '{}' doesn't exists".format(database_name))
    return result

def is_table_exists(database_name: str, table_name: str) -> bool:
    """Checking for the existence of a table with name 'table_name' in the database
    with name 'database_name'.
    """
    # If database doesn't exist skip the next operations
    if is_database_exists(database_name):
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor.execute("select name from sqlite_master where type=\
            'table' and name='{}';".format(table_name))
        expected_name = cursor.fetchone()
        connection.close()
        try:
            result = expected_name[0] == table_name
        except TypeError:
            result = False
            database_logger(LOG_NAME, "Warning: Table '{}' doesn't exists".format(table_name))
    else:
        result = False
    return result

def create_table_if_not_exists(database_name: str):
    """Creating in database 'database_name' table with name 'vault' if this table not exists."""
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute(STORAGE_TABLE_SQL)
    connection.commit()
    connection.close()
    database_logger(LOG_NAME, "Informing: Create table 'vault'")

def insert_into_table(database_name: str, **query_params) -> int:
    """Insert row with name of record, login, password and notice for record.
    Where '**query_params' consit of: record, login, password and optional note.
    """
    exit_code = 0
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    try:
        # Where name, login and password arguments from **query_params
        name = query_params.pop('name')
        login = query_params.pop('login')
        password = query_params.pop('password')
        if 'note' in query_params:
            note = query_params.pop('note')
            sql_requst = "insert into vault (name, login, password, note)\
                values ('{}', '{}', '{}', '{}');".format(name, login, password, note)
        else:
            sql_requst = "insert into vault (name, login, password)\
                values ('{}', '{}', '{}');".format(name, login, password)
        database_logger(LOG_NAME, "SQL: {}".format(sql_requst))
        cursor.execute(sql_requst)
        connection.commit()
    except KeyError:
        database_logger(LOG_NAME, "Error: No arguments were passed")
        exit_code = -1
    connection.close()
    return exit_code

def database_logger(file_name: str, message: str):
    """Logging database operations with time of executing operation to log file."""
    tzmsk = pytz.timezone("Europe/Moscow")
    time_now = datetime.datetime.now(tz=tzmsk).strftime("[%Y-%m-%dT%H:%M:%S]")
    with open(file_name, "a") as log_file:
        log_file.write("{} {}\n".format(time_now, message))
