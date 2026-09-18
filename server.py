import socket
import json

HOST = '127.0.0.1'
PORT = 5000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"Server Pabrik Aktif! Memantau aliran data di {HOST}:{PORT}...")

while True:
    data, addr = sock.recvfrom(1024)
    payload = json.loads(data.decode('utf-8'))
    
    # 1. Simpan data otomatis ke file log pabrik
    with open("fab_telemetry.log", "a") as f:
        f.write(json.dumps(payload) + "\n")
        
    # 2. Logika Deteksi Anomali (Rule-based Monitoring)
    temp = payload.get("temperature_c", 0)
    status = payload.get("status", "")
    
    if temp > 22.5:
        print(f"[ALERT - OVERHEAT] Mesin {payload['equipment_id']} Suhu Tinggi: {temp}°C!")
    elif status == "MAINTENANCE":
        print(f"[WARNING] Mesin {payload['equipment_id']} Butuh Perbaikan Segera!")
    else:
        print(f"[OK - NORMAL] Log tersimpan dari {payload['equipment_id']}")
