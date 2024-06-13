import unittest
from unittest.mock import patch, MagicMock
from backend.db_connector import DBConnector

class DBConnectorTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.db_connector = DBConnector('test_database')

    @patch('backend.db_connector.psycopg2.connect')
    def test_db_connection(self, mock_connect):
        """
        Test database connection.
        """
        mock_connect.return_value.cursor.return_value = MagicMock()
        connection = self.db_connector.connect()
        self.assertIsNotNone(connection)
        mock_connect.assert_called_once_with(database='test_database')

    @patch('backend.db_connector.psycopg2.connect')
    def test_execute_query(self, mock_connect):
        """
        Test executing a query.
        """
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor

        query = "SELECT * FROM test_table"
        self.db_connector.execute_query(query)

        mock_connect.return_value.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(query)
        mock_connect.return_value.commit.assert_called_once()
        mock_cursor.close.assert_called_once()

    @patch('backend.db_connector.psycopg2.connect')
    def test_fetch_results(self, mock_connect):
        """
        Test fetching results from a query.
        """
        mock_cursor = MagicMock()
        mock_connect.return_value.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [(1, 'test'), (2, 'data')]

        query = "SELECT * FROM test_table"
        results = self.db_connector.fetch_results(query)

        mock_connect.return_value.cursor.assert_called_once()
        mock_cursor.execute.assert_called_once_with(query)
        mock_cursor.fetchall.assert_called_once()
        mock_cursor.close.assert_called_once()
        
        self.assertEqual(results, [(1, 'test'), (2, 'data')])

    @patch('backend.db_connector.psycopg2.connect')
    def test_close_connection(self, mock_connect):
        """
        Test closing the database connection.
        """
        mock_connection = mock_connect.return_value
        self.db_connector.close_connection()
        mock_connection.close.assert_called_once()

if __name__ == '__main__':
    unittest.main()
