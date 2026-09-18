import socket
import time
import random
import json

HOST = '127.0.0.1'
PORT = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def generate_machine_data():
    return json.dumps({
        "equipment_id": "LITHO-01",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": random.choice(["IDLE", "RUNNING", "MAINTENANCE"]),
        "temperature_c": round(random.uniform(20.0, 23.0), 2),
        "pressure_bar": round(random.uniform(1.0, 1.5), 2),
        "wafer_processed": random.randint(100, 500)
    })

if __name__ == "__main__":
    print("Mesin Litografi siap ngirim data...")
    try:
        while True:
            payload = generate_machine_data()
            sock.sendto(payload.encode('utf-8'), (HOST, PORT))
            print(f"[TERKIRIM KE SERVER] {payload}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nMesin dimatikan.")
