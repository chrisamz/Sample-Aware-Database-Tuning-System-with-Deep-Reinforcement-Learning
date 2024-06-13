import unittest
from unittest.mock import patch, MagicMock
from backend.parameter_adjuster import ParameterAdjuster

class ParameterAdjusterTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.db_connector = MagicMock()
        self.parameter_adjuster = ParameterAdjuster(self.db_connector)

    def test_initialization(self):
        """
        Test ParameterAdjuster initialization.
        """
        self.assertIsNotNone(self.parameter_adjuster.db_connector)

    @patch('backend.parameter_adjuster.ParameterAdjuster.apply_recommendation')
    def test_adjust_parameters(self, mock_apply_recommendation):
        """
        Test the adjust_parameters method.
        """
        recommendation = {'param1': 'value1', 'param2': 'value2'}
        
        self.parameter_adjuster.adjust_parameters(recommendation)
        
        mock_apply_recommendation.assert_called_once_with(recommendation)

    def test_apply_recommendation(self):
        """
        Test the apply_recommendation method.
        """
        recommendation = {'param1': 'value1', 'param2': 'value2'}
        self.parameter_adjuster.apply_recommendation(recommendation)
        
        calls = [patch.call.set_parameter('param1', 'value1'), patch.call.set_parameter('param2', 'value2')]
        self.db_connector.assert_has_calls(calls, any_order=True)

    def test_verify_adjustment(self):
        """
        Test the verify_adjustment method.
        """
        self.db_connector.get_parameter.side_effect = lambda x: 'value1' if x == 'param1' else 'value2'
        recommendation = {'param1': 'value1', 'param2': 'value2'}
        
        result = self.parameter_adjuster.verify_adjustment(recommendation)
        
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
