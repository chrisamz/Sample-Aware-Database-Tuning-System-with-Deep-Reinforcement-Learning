import unittest
from unittest.mock import patch, MagicMock
from backend.data_collector import DataCollector

class DataCollectorTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.data_collector = DataCollector()

    @patch('backend.data_collector.psutil')
    def test_collect_cpu_usage(self, mock_psutil):
        """
        Test collecting CPU usage.
        """
        mock_psutil.cpu_percent.return_value = 55.0
        cpu_usage = self.data_collector.collect_cpu_usage()
        self.assertEqual(cpu_usage, 55.0)
        mock_psutil.cpu_percent.assert_called_once()

    @patch('backend.data_collector.psutil')
    def test_collect_memory_usage(self, mock_psutil):
        """
        Test collecting memory usage.
        """
        mock_psutil.virtual_memory.return_value.percent = 70.0
        memory_usage = self.data_collector.collect_memory_usage()
        self.assertEqual(memory_usage, 70.0)
        mock_psutil.virtual_memory.assert_called_once()

    @patch('backend.data_collector.time')
    def test_collect_disk_io(self, mock_time):
        """
        Test collecting disk I/O.
        """
        with patch('backend.data_collector.psutil.disk_io_counters') as mock_disk_io:
            mock_disk_io.return_value.read_bytes = 1000
            mock_disk_io.return_value.write_bytes = 2000

            self.data_collector.previous_disk_io = None
            disk_io = self.data_collector.collect_disk_io()

            self.assertEqual(disk_io['read_bytes'], 1000)
            self.assertEqual(disk_io['write_bytes'], 2000)

            self.data_collector.previous_disk_io = MagicMock()
            self.data_collector.previous_disk_io.read_bytes = 500
            self.data_collector.previous_disk_io.write_bytes = 1000
            disk_io = self.data_collector.collect_disk_io()

            self.assertEqual(disk_io['read_bytes'], 500)
            self.assertEqual(disk_io['write_bytes'], 1000)
            self.assertEqual(self.data_collector.previous_disk_io.read_bytes, 1000)
            self.assertEqual(self.data_collector.previous_disk_io.write_bytes, 2000)

    def test_collect_data(self):
        """
        Test collecting all performance metrics.
        """
        with patch.object(self.data_collector, 'collect_cpu_usage', return_value=55.0):
            with patch.object(self.data_collector, 'collect_memory_usage', return_value=70.0):
                with patch.object(self.data_collector, 'collect_disk_io', return_value={'read_bytes': 500, 'write_bytes': 1000}):
                    data = self.data_collector.collect_data()
                    self.assertEqual(data['cpu_usage'], 55.0)
                    self.assertEqual(data['memory_usage'], 70.0)
                    self.assertEqual(data['disk_io']['read_bytes'], 500)
                    self.assertEqual(data['disk_io']['write_bytes'], 1000)

if __name__ == '__main__':
    unittest.main()
