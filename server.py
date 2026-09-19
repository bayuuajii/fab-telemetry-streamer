import json
import paho.mqtt.client as mqtt

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "fab/sensor/litho_01"

# Ambang batas aman
TEMP_LIMIT = 22.5
PRESS_LIMIT = 1.35

def on_connect(client, userdata, flags, rc, properties=None):
    print("Status: Server Monitoring & Quality Control Aktif.")
    client.subscribe(TOPIC)
    print(f"Mendengarkan metrik di {TOPIC}...\n")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        eq_id = payload.get("equipment_id")
        temp = payload.get("temperature_c")
        press = payload.get("pressure_bar")
        status = payload.get("status")

        # Logika Deteksi Anomali
        if temp > TEMP_LIMIT or press > PRESS_LIMIT:
            print(f"[CRITICAL WARNING] Mesin: {eq_id} | Suhu: {temp}°C | Tekanan: {press} bar | ABNORMAL!")
        else:
            print(f"[NORMAL] Mesin: {eq_id} | Status: {status} | Suhu: {temp}°C | Tekanan: {press} bar")

    except Exception as e:
        print(f"Error membaca data: {e}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()
