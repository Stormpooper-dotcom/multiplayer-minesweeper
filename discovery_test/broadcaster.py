import socket
import json
import uuid

DISCOVERY_PORT = 37020
GAME_INFO = {
    "game_id": str(uuid.uuid4()),
    "name": "UDP Test",
    "players": 1,
    "max_players": 4,
    "port": 5000
}

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("", DISCOVERY_PORT))
server.listen(5)

print(f"Server listening on port {DISCOVERY_PORT}")

while True:
    client, addr = server.accept()
    client.send(json.dumps(GAME_INFO).encode("utf-8"))
    client.close()