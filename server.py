import json
import logging
import paho.mqtt.client as mqtt

logging.basicConfig(filename='fab_telemetry.log', level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(message)s')

def on_connect(client, userdata, flags, rc):
    print("Status: Server Monitoring & Auto-Control Aktif.")
    client.subscribe("fab/sensor/litho_01")

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())
    suhu = data['temperature_c']
    tekanan = data['pressure_bar']
    mesin = data['equipment_id']

    # Logika Deteksi
    if suhu > 22.5 or tekanan > 1.4:
        peringatan = f"Mesin: {mesin} | Suhu: {suhu}°C | Tekanan: {tekanan} bar | ABNORMAL!"
        print(f"[CRITICAL WARNING] {peringatan}")
        logging.warning(peringatan)

        # LOGIKA CLOSED-LOOP CONTROL (REAKSI OTOMATIS)
        if suhu > 22.5:
            print(f"[AUTO-CONTROL] Suhu melebihi 22.5°C! Menembakkan perintah SHUTDOWN ke {mesin}...")
            client.publish("fab/command/litho_01", "SHUTDOWN")
            logging.critical(f"SHUTDOWN command auto-fired to {mesin} due to temp ({suhu}°C)")
    else:
        normal_msg = f"Mesin: {mesin} | Status: {data['status']} | Suhu: {suhu}°C | Tekanan: {tekanan} bar"
        print(f"[NORMAL] {normal_msg}")
        logging.info(normal_msg)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", 1883, 60)
client.loop_forever()
