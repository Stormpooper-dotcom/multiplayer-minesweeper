import socket
import json
from concurrent.futures import ThreadPoolExecutor

def get_local_subnet():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn’t actually send data, just figures out the LAN IP
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
    finally:
        s.close()

    # Extract subnet (assumes /24, most LANs use 255.255.255.0)
    parts = local_ip.split(".")
    subnet = ".".join(parts[:3]) + "."
    return subnet

def try_connect(i):
    ip = subnet + str(i)
    try:
        s = socket.create_connection((ip, DISCOVERY_PORT), timeout=0.2)
        data = s.recv(2048)
        info = json.loads(data.decode("utf-8"))
        available_games.append((ip, info))
        s.close()
    except (socket.timeout, ConnectionRefusedError):
        pass

DISCOVERY_PORT = 37020
available_games = []

subnet = get_local_subnet()
print(f"Scanning local subnet {subnet}0/24 for servers")

with ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(try_connect, range(1, 255))

print("Found games:")
for ip, info in available_games:
    print(ip, info)