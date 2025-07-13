# tcp_server.py
import socket, struct, time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 5000))
s.listen(1)

print("[TCP] Waiting for connection...")
conn, addr = s.accept()
print(f"[TCP] Connected by {addr}")

while True:
    ts = int(time.time() * 1000)
    for r, az in [(100, 0), (120, 45), (140, -30)]:
        conn.sendall(struct.pack('ffQ', r, az, ts))
    time.sleep(1/20)
