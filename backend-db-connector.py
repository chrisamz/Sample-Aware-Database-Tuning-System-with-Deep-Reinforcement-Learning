# backend/db_connector.py

import sqlite3
import psycopg2
import mysql.connector

class DBConnector:
    """
    Class to handle database connections and queries.
    """
    
    def __init__(self, db_type, db_config):
        """
        Initializes the DBConnector with the specified database type and configuration.

        Args:
            db_type (str): Type of the database (e.g., 'sqlite', 'postgresql', 'mysql').
            db_config (dict): Database configuration parameters.
        """
        self.db_type = db_type
        self.db_config = db_config
        self.connection = self.connect_to_db()

    def connect_to_db(self):
        """
        Connects to the specified database.

        Returns:
            connection: Database connection object.
        """
        if self.db_type == 'sqlite':
            return sqlite3.connect(self.db_config['database'])
        elif self.db_type == 'postgresql':
            return psycopg2.connect(
                dbname=self.db_config['dbname'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                host=self.db_config['host'],
                port=self.db_config['port']
            )
        elif self.db_type == 'mysql':
            return mysql.connector.connect(
                user=self.db_config['user'],
                password=self.db_config['password'],
                host=self.db_config['host'],
                database=self.db_config['database']
            )
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

    def execute_query(self, query):
        """
        Executes the given SQL query and returns the result.

        Args:
            query (str): SQL query to be executed.

        Returns:
            result: Query result.
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        return result

    def close_connection(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()

    def execute_update(self, query, params):
        """
        Executes an update SQL query with parameters.

        Args:
            query (str): SQL query to be executed.
            params (tuple): Parameters for the SQL query.
        """
        cursor = self.connection.cursor()
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()
