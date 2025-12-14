import socket
import struct
import json
import time

MCAST_GRP = "239.255.0.1"
MCAST_PORT = 37020

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(("", MCAST_PORT))

mreq = struct.pack(
    "4sl",
    socket.inet_aton(MCAST_GRP),
    socket.INADDR_ANY
)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

print("Listening for beacons...")

seen = {}

while True:
    data, addr = sock.recvfrom(2048)
    info = json.loads(data.decode("utf-8"))

    ip = addr[0]
    seen[ip] = time.time()

    print(f"Found game from {ip}: {info}")