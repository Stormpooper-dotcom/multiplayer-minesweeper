import socket
import threading
from network.protocol import send, recv

class MultiplayerClient:
    def __init__(self, host, port, player_id, on_message):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.file = self.sock.makefile("rwb")
        self.on_message = on_message

        send(self.sock, {
            "type": "join",
            "player_id": player_id
        })

        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        while True:
            try:
                msg = recv(self.file)
                self.on_message(msg)
            except (ConnectionError, OSError):
                print("\n[Disconnected from server]")
                break

    def send_move(self, action, x, y):
        send(self.sock, {
            "type": "move",
            "action": action,
            "x": x,
            "y": y
        })