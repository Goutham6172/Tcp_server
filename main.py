# tcp_server.py
import socket
import struct
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', 5002))
sock.listen(1)

conn, addr = sock.accept()
print(f"Client connected: {addr}")

while True:
    # Send 3 targets with (range, rel_azimuth)
    for r, az in [(100.0, 0.0), (120.0, 45.0), (150.0, -30.0)]:
        conn.sendall(struct.pack('ff', r, az))
    time.sleep(1)
