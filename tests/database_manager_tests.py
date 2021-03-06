"""Test for 'database_manager' functions."""
import sqlite3
import unittest
from itertools import islice
from src import database_manager

DB_NAME = "tests/testdb.sqlite3"

VAULT_TABLE_SQL = "create table if not exists vault (\
account_id integer primary key,\
name text not null,\
login text not null,\
password text not null,\
note text);"

SHOP_TABLE_SQL = "create table if not exists shop (\
shop_id integer primary key,\
name text not null,\
address text not null);"

DROP_TABLE_VAULT = "drop table if exists vault;"

DROP_TABLE_SHOP = "drop table if exists shop;"

SELECT_SQL = "select * from vault where login= 'user@mail.ru';"
SELECT_SQL_WITHOUT_NOTE = "select * from vault where\
    account_id=2;"

class TestExtraMethods(unittest.TestCase):
    """Testing 'database_manager' functions."""

    def setUp(self):
        """Creating new database with tables."""
        self.database_name = DB_NAME
        self.table_name = "vault"
        self.table_name2 = "shop"
        self.right_insert_dict = {'name': 'mail.ru', 'login': 'user@mail.ru',\
            'password': 'strong password', 'note': 'My note'}
        self.bad_insert_dict = {'name': 'mail.com', 'person': 'Pavel Durov'}
        self.insert_without_note = {'name': 'mail.ru', 'login': 'user2@mail.ru',\
            'password': 'hard psswd'}
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute(VAULT_TABLE_SQL)
        cursor.execute(SHOP_TABLE_SQL)
        connection.commit()
        connection.close()

    def drop_tables(self):
        """Drop tables after tests.
        It method should be called in the last method."""
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute(DROP_TABLE_VAULT)
        cursor.execute(DROP_TABLE_SHOP)
        connection.commit()
        connection.close()

    def test_for_database_existing(self):
        """Checking the existence of a database file."""
        self.assertTrue(database_manager.is_database_exists(self.database_name))
        self.assertFalse(database_manager.is_database_exists("tests/somedb.db"))

    def test_for_table_existing(self):
        """Checking the existence of a table in database.
        Tables 'vault' and 'shop' were created in 'setUp.
        '"""
        self.assertTrue(database_manager.is_table_exists(self.database_name,\
            self.table_name))
        self.assertTrue(database_manager.is_table_exists(self.database_name,\
            self.table_name2))
        self.assertFalse(database_manager.is_table_exists(self.database_name, "big_table"))
        self.assertFalse(database_manager.is_table_exists("tests/somedb.db", "cool_table"))

    def test_table_creating(self):
        """Checking creating of table 'vault'."""
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute(DROP_TABLE_VAULT)
        connection.commit()
        connection.close()
        self.assertFalse(database_manager.is_table_exists(self.database_name,\
            self.table_name))
        database_manager.create_table_if_not_exists(self.database_name)
        self.assertTrue(database_manager.is_table_exists(self.database_name,\
            self.table_name))

    def test_for_insert_into_table(self):
        """Checking that insert into table query completed successfully."""
        # Make a right query
        database_manager.insert_into_table(self.database_name, **self.right_insert_dict)
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute(SELECT_SQL)
        right_query_result = cursor.fetchone()
        # Prepare initial value to tuple for compare
        initial_tuple = (1, ) + tuple(self.right_insert_dict.values())
        # Test it
        self.assertEqual(initial_tuple, right_query_result)
        # Make right query without note
        database_manager.insert_into_table(self.database_name, **self.insert_without_note)
        cursor.execute(SELECT_SQL_WITHOUT_NOTE)
        query_without_note = cursor.fetchone()
        initial_tuple2 = (2, ) + tuple(self.insert_without_note.values()) + (None, )
        # Test it
        self.assertEqual(initial_tuple2, query_without_note)
        # Make a bad query with KeyError Exception
        bad_query_result = database_manager.insert_into_table(self.database_name,\
            **self.bad_insert_dict)
        self.assertEqual(-1, bad_query_result)
        connection.close()

    def test_selecting_rows_by_name(self):
        """Cheking selecting rows by given name."""
        # Make query
        selected_rows = database_manager.select_row_by_name(self.database_name,\
            self.right_insert_dict['name'])
        # Dict from 'right_insert_dict' witout account_id
        first_dict = dict(islice(selected_rows[0].items(), 1, 5))
        second_dict = dict(islice(selected_rows[1].items(), 1, 4))
        # Check it
        self.assertGreater(len(selected_rows), 0)
        self.assertEqual(self.right_insert_dict, first_dict)
        self.assertEqual(self.insert_without_note, second_dict)
        # Try make select without results
        selected_rows = database_manager.select_row_by_name(self.database_name, "vodka")
        self.assertListEqual(selected_rows, [])

    def test_selecting_rows_by_login(self):
        """Checking selecting rows by given login."""
        # Make query
        selected_rows = database_manager.select_row_by_login(self.database_name,\
            self.right_insert_dict['login'])
        result_dict = dict(islice(selected_rows[0].items(), 1, 5))
        # Check it
        self.assertGreater(len(selected_rows), 0)
        self.assertEqual(result_dict, self.right_insert_dict)
        # Try make select without results
        selected_rows = database_manager.select_row_by_login(self.database_name, "dummy")
        self.assertListEqual(selected_rows, [])

def drop_tables():
    """Drop tables after tests.
    It method should be called in the last method."""
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    cursor.execute(DROP_TABLE_VAULT)
    cursor.execute(DROP_TABLE_SHOP)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    unittest.main(exit=False)
    drop_tables()
