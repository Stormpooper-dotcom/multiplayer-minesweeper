import socket
import json
import time
import uuid

DISCOVERY_PORT = 37020

game_info = {
    "type": "beacon",
    "game_id": str(uuid.uuid4()),
    "name": "UDP Test",
    "players": 1,
    "max_players": 4,
    "port": 5000
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

print("Broadcasting beacon, press Ctrl+C to stop")

while True:
    data = json.dumps(game_info).encode("utf-8")
    sock.sendto(data, ("192.168.0.255", DISCOVERY_PORT))
    time.sleep(1)