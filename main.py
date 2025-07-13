# # tcp_server.py
# import socket, struct, time

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(("0.0.0.0", 5002))
# s.listen(1)

# print("[TCP] Waiting for connection...")
# conn, addr = s.accept()
# print(f"[TCP] Connected by {addr}")

# try:
#     while True:
#         timestamp = int(time.time() * 1000)

#         targets = [
#             (100.0, 0.0),
#             (120.0, 45.0),
#             (140.0, -30.0),
#         ]

#         for r, az_rel in targets:
#             packet = struct.pack('<ffQ', r, az_rel, timestamp)  # Use <ffQ to match receiver
#             conn.sendall(packet)

#         time.sleep(1 / 20)  # 20 Hz
# except (BrokenPipeError, ConnectionResetError):
#     print("[TCP] Client disconnected.")
# finally:
#     conn.close()
#     s.close()


# tcp_many_targets_simulator.py
import socket
import struct
import time
import random

HOST = "0.0.0.0"
PORT = 5002
UPDATE_HZ = 30
NUM_TARGETS = 30

# Initialize random targets with range and azimuth, and drift values
targets = []
for _ in range(NUM_TARGETS):
    target = {
        "r": random.uniform(80, 250),
        "az": random.uniform(0, 360),
        "dr": random.uniform(-0.5, 0.5),
        "daz": random.uniform(-1.0, 1.0)
    }
    targets.append(target)

# TCP setup
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)

print("[TCP] Waiting for radar application to connect...")
conn, addr = s.accept()
print(f"[TCP] Connected by {addr}")

try:
    while True:
        timestamp = int(time.time() * 1000)
        packet = b''

        for t in targets:
            # Update range/azimuth slightly per frame
            t["r"] += t["dr"]
            t["az"] = (t["az"] + t["daz"]) % 360

            # Clamp range within radar range
            if t["r"] < 60 or t["r"] > 280:
                t["dr"] *= -1

            packet += struct.pack('<ffQ', t["r"], t["az"], timestamp)

        conn.sendall(packet)
        time.sleep(1 / UPDATE_HZ)

except (BrokenPipeError, ConnectionResetError):
    print("[TCP] Client disconnected.")
finally:
    conn.close()
    s.close()
