import socket
import json
import time

DISCOVERY_PORT = 37020

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", DISCOVERY_PORT))

print("Listening for beacons...")

seen = {}

while True:
    data, addr = sock.recvfrom(2048)
    info = json.loads(data.decode("utf-8"))

    ip = addr[0]
    seen[ip] = time.time()

    print(f"Found game at {ip}: {info}")