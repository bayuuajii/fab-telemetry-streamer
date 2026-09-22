import time
import json
import random
import paho.mqtt.client as mqtt

# Status mesin (Global Flag)
mesin_hidup = True

def on_connect(client, userdata, flags, rc):
    print("Status: TERHUBUNG ke Pabrik (MQTT Broker)!")
    # Mesin mendaftarkan diri ke jalur komando khusus
    client.subscribe("fab/command/litho_01")

def on_message(client, userdata, msg):
    global mesin_hidup
    pesan = msg.payload.decode()
    if pesan == "SHUTDOWN":
        print("\n[!!! ALARM !!!] MENDAPAT PERINTAH SHUTDOWN DARI SERVER!")
        print("MENGHENTIKAN MESIN LITHOGRAFI SECARA DARURAT...\n")
        mesin_hidup = False  # Mematikan loop utama

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message # Fungsi baru untuk mendengar perintah
client.connect("broker.hivemq.com", 1883, 60)
client.loop_start() # Menjalankan pendengar di background

print("Menghubungkan mesin ke jaringan pabrik...")
time.sleep(2)

wafer_count = 0
# Loop utama hanya berjalan selama mesin belum disuruh mati
while mesin_hidup:
    # Simulasi suhu kita naikkan sedikit batas atasnya agar lebih cepat error
    suhu = round(random.uniform(20.0, 23.5), 2) 
    tekanan = round(random.uniform(1.0, 1.5), 2)
    wafer_count += random.randint(10, 50)

    payload = {
        "equipment_id": "LITHO-01",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": "RUNNING",
        "temperature_c": suhu,
        "pressure_bar": tekanan,
        "wafer_processed": wafer_count
    }

    client.publish("fab/sensor/litho_01", json.dumps(payload))
    print(f"Mengirim data: Suhu {suhu}°C | Tekanan {tekanan} bar")
    time.sleep(2)

# Pesan ini hanya muncul jika loop berhenti karena perintah SHUTDOWN
print("Status Mesin: HALTED (Berhenti Total). Wafer aman dari kerusakan.")
