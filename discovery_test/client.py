import socket
import json
from concurrent.futures import ThreadPoolExecutor

DISCOVERY_PORT = 37020
available_games = []

# auto-detect local subnet
def get_local_subnet():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # no packets sent
        local_ip = s.getsockname()[0]
    finally:
        s.close()
    parts = local_ip.split(".")
    return ".".join(parts[:3]) + "."  # assume /24 subnet

subnet = get_local_subnet()
print(f"Scanning subnet {subnet}0/24 for servers...")

# attempt connection to each host in subnet
def try_connect(i):
    ip = subnet + str(i)
    try:
        s = socket.create_connection((ip, DISCOVERY_PORT), timeout=0.2)
        data = s.recv(2048)
        info = json.loads(data.decode("utf-8"))
        available_games.append((ip, info))
        s.close()
    except (socket.timeout, ConnectionRefusedError, OSError):
        pass

# scan concurrently for speed
with ThreadPoolExecutor(max_workers=50) as executor:
    executor.map(try_connect, range(1, 255))

print("Found games:")
for ip, info in available_games:
    print(ip, info)
