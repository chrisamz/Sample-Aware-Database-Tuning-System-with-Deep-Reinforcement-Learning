# backend/parameter_adjuster.py

import psycopg2
import logging

class ParameterAdjuster:
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None
        self._connect()

    def _connect(self):
        try:
            self.conn = psycopg2.connect(**self.db_config)
        except Exception as e:
            logging.error(f"Error connecting to the database: {e}")
            raise

    def _execute_query(self, query):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query)
                self.conn.commit()
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            self.conn.rollback()
            raise

    def adjust_parameter(self, parameter, value):
        query = f"ALTER SYSTEM SET {parameter} = '{value}';"
        self._execute_query(query)
        logging.info(f"Parameter {parameter} adjusted to {value}")

    def reload_configuration(self):
        query = "SELECT pg_reload_conf();"
        self._execute_query(query)
        logging.info("Database configuration reloaded")

    def close(self):
        if self.conn:
            self.conn.close()

# Example usage
if __name__ == "__main__":
    db_config = {
        'dbname': 'your_database',
        'user': 'your_username',
        'password': 'your_password',
        'host': 'localhost',
        'port': 5432
    }

    adjuster = ParameterAdjuster(db_config)
    adjuster.adjust_parameter('work_mem', '64MB')
    adjuster.reload_configuration()
    adjuster.close()
