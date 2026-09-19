import time
import random
import json
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "fab/sensor/litho_01"

# Penyesuaian parameter callback untuk paho-mqtt versi 2
def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("Status: TERHUBUNG ke Pabrik (MQTT Broker)!")
    else:
        print(f"Gagal terhubung, kode error: {reason_code}")

# Deklarasi eksplisit API v2
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Litho_Machine_01")
client.on_connect = on_connect

print("Menghubungkan mesin ke jaringan pabrik...")
client.connect(BROKER, PORT, 60)
client.loop_start()

def generate_machine_data():
    return {
        "equipment_id": "LITHO-01",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": random.choice(["IDLE", "RUNNING", "MAINTENANCE"]),
        "temperature_c": round(random.uniform(20.0, 23.0), 2),
        "pressure_bar": round(random.uniform(1.0, 1.5), 2),
        "wafer_processed": random.randint(100, 500)
    }

if __name__ == "__main__":
    print("Mesin Litografi siap ngirim data metrik via MQTT...\n")
    try:
        while True:
            data = generate_machine_data()
            payload = json.dumps(data)
            
            client.publish(TOPIC, payload)
            
            print(f"[{time.strftime('%H:%M:%S')}] Data terkirim ke topik '{TOPIC}':")
            print(f" -> {payload}\n")
            
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\nMesin dimatikan oleh operator (Ctrl+C).")
        client.loop_stop()
        client.disconnect()
