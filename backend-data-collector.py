# backend/data_collector.py

class DataCollector:
    """
    Class to collect performance metrics from the database.
    """
    
    def __init__(self, db_connector):
        """
        Initializes the DataCollector with a database connector.

        Args:
            db_connector (DBConnector): Instance of DBConnector to interact with the database.
        """
        self.db_connector = db_connector

    def collect_data(self):
        """
        Collects performance metrics from the database.

        Returns:
            dict: A dictionary containing various performance metrics.
        """
        metrics = {
            "cpu_usage": self.get_cpu_usage(),
            "memory_usage": self.get_memory_usage(),
            "disk_io": self.get_disk_io(),
            "query_performance": self.get_query_performance(),
            # Add more metrics as needed
        }
        return metrics

    def get_cpu_usage(self):
        """
        Collects CPU usage metrics.

        Returns:
            float: CPU usage percentage.
        """
        # Implement the logic to collect CPU usage from the database
        # Example:
        cpu_usage = self.db_connector.execute_query("SELECT cpu_usage FROM performance_metrics")
        return cpu_usage

    def get_memory_usage(self):
        """
        Collects memory usage metrics.

        Returns:
            float: Memory usage percentage.
        """
        # Implement the logic to collect memory usage from the database
        # Example:
        memory_usage = self.db_connector.execute_query("SELECT memory_usage FROM performance_metrics")
        return memory_usage

    def get_disk_io(self):
        """
        Collects disk I/O metrics.

        Returns:
            float: Disk I/O performance.
        """
        # Implement the logic to collect disk I/O from the database
        # Example:
        disk_io = self.db_connector.execute_query("SELECT disk_io FROM performance_metrics")
        return disk_io

    def get_query_performance(self):
        """
        Collects query performance metrics.

        Returns:
            float: Average query execution time.
        """
        # Implement the logic to collect query performance from the database
        # Example:
        query_performance = self.db_connector.execute_query("SELECT avg_query_time FROM performance_metrics")
        return query_performance
