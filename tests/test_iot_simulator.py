import unittest
from unittest.mock import patch, MagicMock
from iot_simulation.iot_simulator import ConfigManager

class TestConfigManager(unittest.TestCase):

    @patch.object(ConfigManager, 'load_config', return_value={
        "AWS_IOT_ENDPOINT": "endpoint",
        "CERT_PATH": "cert_path",
        "KEY_PATH": "key_path",
        "CA_PATH": "ca_path"
    })
    def test_load_config(self, mock_load_config):
        config_manager = ConfigManager(config_file="config.json")
        
        self.assertIn("AWS_IOT_ENDPOINT", config_manager.config)
        self.assertIn("CERT_PATH", config_manager.config)
        self.assertIn("KEY_PATH", config_manager.config)
        self.assertIn("CA_PATH", config_manager.config)
    
    @patch.object(ConfigManager, 'load_config', return_value={
        "AWS_IOT_ENDPOINT": "endpoint",
        "CERT_PATH": "cert_path",
        "KEY_PATH": "key_path",
        "CA_PATH": "ca_path"
    })
    def test_get(self, mock_load_config):
        config_manager = ConfigManager(config_file="config.json")
        endpoint = config_manager.get("AWS_IOT_ENDPOINT")
        self.assertIsInstance(endpoint, str)
        self.assertEqual(endpoint, "endpoint")

if __name__ == '__main__':
    unittest.main()