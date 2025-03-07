import time
import json
import random
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

with open("config.json", "r") as config_file:
    config = json.load(config_file)

AWS_IOT_ENDPOINT = config["AWS_IOT_ENDPOINT"]
CERT_PATH = config["CERT_PATH"]
KEY_PATH = config["KEY_PATH"]
CA_PATH = config["CA_PATH"]
TOPIC = "warehouse/inventory"
CLIENT_ID = f"IoT-Thing-{random.randint(1000, 9999)}"

# MQTT Client Setup
client = AWSIoTMQTTClient(CLIENT_ID)
client.configureEndpoint(AWS_IOT_ENDPOINT, 8883)
client.configureCredentials(CA_PATH, KEY_PATH, CERT_PATH)

# MQTT Connection Configuration
client.configureOfflinePublishQueueing(-1)
client.configureDrainingFrequency(2)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)

# Connect to AWS IoT Core
client.connect()
print(f"Connected to AWS IoT as {CLIENT_ID}")

def generate_inventory_data():
    return {
        "item_id": random.randint(1000, 9999),
        "movement": random.choice(["IN", "OUT"]),
        "quantity": random.randint(1, 50),
        "timestamp": int(time.time())
    }

# Publish data to MQTT topic
while True:
    payload = json.dumps(generate_inventory_data())
    client.publish(TOPIC, payload, QoS = 1)
    print(f"Sent: {payload}")
    time.sleep(30)
