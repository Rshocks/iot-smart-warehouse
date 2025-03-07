import unittest
import time
from iot_simulator import InventoryDataGenerator, ConfigManager

class TestConfigManager(unittest.TestCase):
    
    def test_load_config(self):
        config_manager = ConfigManager(config_file="config.json")
    
        self.assertIn("AWS_IOT_ENDPOINT", config_manager.config)
        self.assertIn("CERT_PATH", config_manager.config)
        self.assertIn("KEY_PATH", config_manager.config)
        self.assertIn("CA_PATH", config_manager.config)

    def test_get(self):
        config_manager = ConfigManager(config_file="config.json")
        
        endpoint = config_manager.get("AWS_IOT_ENDPOINT")
        self.assertIsInstance(endpoint, str)

class TestInventoryDataGenerator(unittest.TestCase):
    
    def test_generate(self):
        data_generator = InventoryDataGenerator()
        generated_data = data_generator.generate()

        self.assertIn("item_id", generated_data)
        self.assertIn("movement", generated_data)
        self.assertIn("quantity", generated_data)
        self.assertIn("timestamp", generated_data)
        
        self.assertIsInstance(generated_data["item_id"], int)
        self.assertIsInstance(generated_data["movement"], str)
        self.assertIsInstance(generated_data["quantity"], int)
        self.assertIsInstance(generated_data["timestamp"], int)

if __name__ == "__main__":
    unittest.main()