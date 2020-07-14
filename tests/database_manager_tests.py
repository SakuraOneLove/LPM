"""Test for 'database_manager' functions."""
import os
import sqlite3
import unittest
from src import database_manager

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

class TestExtraMethods(unittest.TestCase):
    """Testing 'database_manager' functions."""

    def setUp(self):
        """Creating new database with tables."""
        self.database_name = "tests/testdb.sqlite3"
        self.table_name = "vault"
        self.table_name2 = "shop"
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute(VAULT_TABLE_SQL)
        cursor.execute(SHOP_TABLE_SQL)
        connection.commit()
        connection.close()

    def tearDown(self):
        """Drop tables after tests."""
        connection = sqlite3.connect(self.database_name)
        cursor = connection.cursor()
        cursor.execute(DROP_TABLE_VAULT)
        cursor.execute(DROP_TABLE_SHOP)
        connection.commit()
        connection.close()

    def test_for_database_existing(self):
        """Checking the existence of a database file."""
        self.assertEqual(True, database_manager.is_database_exists(self.database_name))
        self.assertEqual(False, database_manager.is_database_exists("tests/somedb.db"))
    
    def test_for_table_existing(self):
        """Checking the existence of a table in database.
        Tables 'vault' and 'shop' were created in 'setUp.
        '"""
        self.assertEqual(True, database_manager.is_table_exists(self.database_name, self.table_name))
        self.assertEqual(True, database_manager.is_table_exists(self.database_name, self.table_name2))
        self.assertEqual(False, database_manager.is_table_exists(self.database_name, "big_table"))
        self.assertEqual(False, database_manager.is_table_exists("tests/somedb.db", "cool_table"))

if __name__ == "__main__":
    unittest.main()