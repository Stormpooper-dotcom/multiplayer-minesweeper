import json

def send(sock, obj):
    data = json.dumps(obj).encode() + b"\n"
    sock.sendall(data)

def recv(file):
    line = file.readline()
    if not line:
        raise ConnectionError("Disconnected")
    return json.loads(line.decode())