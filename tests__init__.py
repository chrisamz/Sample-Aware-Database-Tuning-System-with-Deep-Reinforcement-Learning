"""
This module contains the test suite for the Sample-Aware Database Tuning System with Deep Reinforcement Learning project.

The test suite includes unit tests, integration tests, and system tests to ensure the functionality and reliability of the project components.

Modules:
    - test_data_collector.py: Tests for the DataCollector class and related functions.
    - test_db_collector.py: Tests for the DBCollector class and related functions.
    - test_rl_agent.py: Tests for the RLAgent class and reinforcement learning logic.
    - test_parameter_adjuster.py: Tests for the ParameterAdjuster class and parameter adjustment logic.
    - test_dashboard.py: Tests for the Dashboard component and its web interface.
    - test_utils.py: Tests for utility functions and helpers.
"""

import unittest

# Import test modules
from .test_data_collector import DataCollectorTestCase
from .test_db_collector import DBCollectorTestCase
from .test_rl_agent import RLAgentTestCase
from .test_parameter_adjuster import ParameterAdjusterTestCase
from .test_dashboard import DashboardTestCase
from .test_utils import UtilsTestCase

def load_tests(loader, tests, pattern):
    """
    This function is used to load the test cases from the test modules and add them to the test suite.

    Args:
        loader (unittest.TestLoader): The test loader instance.
        tests (unittest.TestSuite): The test suite instance.
        pattern (str): The test pattern (e.g., 'test_*.py').

    Returns:
        unittest.TestSuite: The loaded test suite.
    """
    suite = unittest.TestSuite()
    for test_class in (DataCollectorTestCase, DBCollectorTestCase, RLAgentTestCase, ParameterAdjusterTestCase, DashboardTestCase, UtilsTestCase):
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    return suite

if __name__ == "__main__":
    unittest.main()
