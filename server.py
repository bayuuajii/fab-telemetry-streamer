import json
import logging
import paho.mqtt.client as mqtt

# Setup Logging ke File dan Terminal
logging.basicConfig(
    filename="fab_telemetry.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

BROKER = "broker.hivemq.com"
PORT = 1883
TOPIC = "fab/sensor/litho_01"

TEMP_LIMIT = 22.5
PRESS_LIMIT = 1.35

def on_connect(client, userdata, flags, rc, properties=None):
    msg = "Status: Server Monitoring & Quality Control (With Logging) Aktif."
    print(msg)
    logging.info(msg)
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        eq_id = payload.get("equipment_id")
        temp = payload.get("temperature_c")
        press = payload.get("pressure_bar")
        status = payload.get("status")

        if temp > TEMP_LIMIT or press > PRESS_LIMIT:
            log_msg = f"[CRITICAL WARNING] Mesin: {eq_id} | Suhu: {temp}°C | Tekanan: {press} bar | ABNORMAL!"
            print(log_msg)
            logging.warning(log_msg)
        else:
            log_msg = f"[NORMAL] Mesin: {eq_id} | Status: {status} | Suhu: {temp}°C | Tekanan: {press} bar"
            print(log_msg)
            logging.info(log_msg)

    except Exception as e:
        err_msg = f"Error membaca data: {e}"
        print(err_msg)
        logging.error(err_msg)

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()
