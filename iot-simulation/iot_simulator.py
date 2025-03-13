import time
import json
import random
import pytz
from datetime import datetime
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

class ConfigManager:
    
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        with open(self.config_file, "r") as file:
            return json.load(file)
    
    def get(self, key):
        return self.config.get(key)


class IoTClient:
    
    def __init__(self, config):
        self.client_id = f"IoT-Thing-{random.randint(1000, 9999)}"
        self.endpoint = config.get("AWS_IOT_ENDPOINT")
        self.cert_path = config.get("CERT_PATH")
        self.key_path = config.get("KEY_PATH")
        self.ca_path = config.get("CA_PATH")
        self.topic = "warehouse/inventory"
        self.client = self.create_client()
    
    def create_client(self):
        client = AWSIoTMQTTClient(self.client_id)
        client.configureEndpoint(self.endpoint, 8883)
        client.configureCredentials(self.ca_path, self.key_path, self.cert_path)
        client.configureOfflinePublishQueueing(-1)
        client.configureDrainingFrequency(2)
        client.configureConnectDisconnectTimeout(10)
        client.configureMQTTOperationTimeout(5)
        return client
    
    def connect(self):
        self.client.connect()
        print(f"Connected to AWS IoT as {self.client_id}")
    
    def publish_data(self, payload):
        self.client.publish(self.topic, payload, QoS=1)
        print(f"Sent: {payload}")


class InventoryDataGenerator:
    
    def generate(self):
        dublin_tz = pytz.timezone('Europe/Dublin')
        current_time = datetime.now(dublin_tz)
        timestamp = current_time.strftime('%Y-%m-%d %H:%M:%S')
        
        return {
            "item_id": random.randint(1000, 9999),
            "movement": random.choice(["IN", "OUT"]),
            "quantity": random.randint(1, 50),
            "timestamp": timestamp
        }


class IoTSimulator:
    
    def __init__(self, config_file="config.json"):
        self.config_manager = ConfigManager(config_file)
        self.iot_client = IoTClient(self.config_manager.config)
        self.data_generator = InventoryDataGenerator()
    
    def run(self):
        self.iot_client.connect()
        
        while True:
            payload = json.dumps(self.data_generator.generate())
            self.iot_client.publish_data(payload)
            time.sleep(30)  # Send data every 30 seconds


if __name__ == "__main__":
    simulator = IoTSimulator(config_file="config.json")
    simulator.run()
