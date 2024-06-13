import unittest
from unittest.mock import patch, MagicMock
import torch
import numpy as np
from backend.rl_agent import RLAgent

class RLAgentTestCase(unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment before each test.
        """
        self.state_dim = 10
        self.action_dim = 5
        self.rl_agent = RLAgent(self.state_dim, self.action_dim)

    def test_initialization(self):
        """
        Test RLAgent initialization.
        """
        self.assertEqual(self.rl_agent.state_dim, self.state_dim)
        self.assertEqual(self.rl_agent.action_dim, self.action_dim)
        self.assertIsNotNone(self.rl_agent.model)

    def test_select_action(self):
        """
        Test action selection.
        """
        state = np.random.rand(self.state_dim)
        action = self.rl_agent.select_action(state)
        self.assertTrue(0 <= action < self.action_dim)

    @patch('backend.rl_agent.RLAgent.update')
    def test_update(self, mock_update):
        """
        Test the update method.
        """
        state = np.random.rand(self.state_dim)
        action = 1
        reward = 1.0
        next_state = np.random.rand(self.state_dim)
        done = False

        self.rl_agent.update(state, action, reward, next_state, done)
        mock_update.assert_called_once_with(state, action, reward, next_state, done)

    def test_save_model(self):
        """
        Test saving the model.
        """
        with patch('torch.save') as mock_save:
            self.rl_agent.save_model('test_model.pth')
            mock_save.assert_called_once()

    def test_load_model(self):
        """
        Test loading the model.
        """
        with patch('torch.load') as mock_load, patch.object(self.rl_agent.model, 'load_state_dict') as mock_load_state_dict:
            self.rl_agent.load_model('test_model.pth')
            mock_load.assert_called_once()
            mock_load_state_dict.assert_called_once()

if __name__ == '__main__':
    unittest.main()
