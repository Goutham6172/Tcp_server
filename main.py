# tcp_server.py
import socket, struct, time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 5002))
s.listen(1)

print("[TCP] Waiting for connection...")
conn, addr = s.accept()
print(f"[TCP] Connected by {addr}")

try:
    while True:
        timestamp = int(time.time() * 1000)

        targets = [
            (100.0, 0.0),
            (120.0, 45.0),
            (140.0, -30.0),
        ]

        for r, az_rel in targets:
            packet = struct.pack('<ffQ', r, az_rel, timestamp)  # Use <ffQ to match receiver
            conn.sendall(packet)

        time.sleep(1 / 20)  # 20 Hz
except (BrokenPipeError, ConnectionResetError):
    print("[TCP] Client disconnected.")
finally:
    conn.close()
    s.close()
