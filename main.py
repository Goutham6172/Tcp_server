# tcp_server.py
import socket, struct, time

s = socket.socket()
s.bind(("0.0.0.0", 5000))
s.listen(1)
conn, _ = s.accept()

while True:
    ts = int(time.time() * 1000)
    for r, az in [(100, 0), (120, 45), (140, -30)]:
        conn.sendall(struct.pack('ffQ', r, az, ts))
    time.sleep(1)
