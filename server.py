import json
import paho.mqtt.client as mqtt

# Harus sama persis dengan yang ada di mesin
BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "fab/sensor/litho_01"

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print(f"Status: Server TERHUBUNG ke Pabrik.")
        print(f"Mendengarkan saluran metrik: {TOPIC}...\n")
        # Server wajib 'subscribe' ke topik yang sama dengan mesin
        client.subscribe(TOPIC)
    else:
        print(f"Gagal terhubung, kode error: {reason_code}")

# Fungsi ini otomatis terpanggil setiap kali ada data masuk dari mesin
def on_message(client, userdata, msg):
    payload = msg.payload.decode('utf-8')
    data = json.loads(payload)
    
    # Format tampilan layaknya log di control room
    print(f"[DATA MASUK] Mesin: {data['equipment_id']} | Status: {data['status']} | Suhu: {data['temperature_c']}°C | Tekanan: {data['pressure_bar']} bar")

# Inisialisasi Server sebagai MQTT Client (Subscriber)
server_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, "Fab_Server_Central")
server_client.on_connect = on_connect
server_client.on_message = on_message

print("Menyalakan Server Pusat Pabrik...")
server_client.connect(BROKER, PORT, 60)

try:
    # Loop forever membuat server standby terus menerus tanpa mati
    server_client.loop_forever() 
except KeyboardInterrupt:
    print("\nServer dimatikan oleh Admin.")
    server_client.disconnect()
