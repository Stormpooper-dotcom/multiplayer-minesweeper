import socket
import json
import time

DISCOVERY_PORT = 37020

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sock.bind(("0.0.0.0", DISCOVERY_PORT))

print("Listening for beacons...")

seen = {}

while True:
    data, addr = sock.recvfrom(2048)
    info = json.loads(data.decode("utf-8"))

    ip = addr[0]
    seen[ip] = time.time()

    print(f"Found game from {ip}: {info}")