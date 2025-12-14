import socket
import json
import time
import uuid

MCAST_GRP = "239.255.0.1"
MCAST_PORT = 37020

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

LOCAL_IP = get_ip()

game_info = {
    "type": "beacon",
    "game_id": str(uuid.uuid4()),
    "name": "UDP Test",
    "players": 1,
    "max_players": 4,
    "port": 5000
}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Tell Windows which IP to multicast on
sock.setsockopt(
    socket.IPPROTO_IP,
    socket.IP_MULTICAST_IF,
    socket.inet_aton(LOCAL_IP)
)

sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)

print(f"Multicast beacon started on {LOCAL_IP}, press Ctrl+C to stop")

while True:
    data = json.dumps(game_info).encode("utf-8")
    sock.sendto(data, (MCAST_GRP, MCAST_PORT))
    time.sleep(1)