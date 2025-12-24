import socket
import threading
import time
from minesweeper.controller import GameController
from network.protocol import send, recv

class MultiplayerServer:
    def __init__(self, host="0.0.0.0", port=5000):
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((host, port))
        self.sock.listen()

        self.controller = GameController()
        self.clients = {} # player_id -> socket
        self.had_players = False

        required = int(input("Players required to start (1-4) > "))
        self.controller.set_required_players(required)

    def start(self):
        print("Server listening")
        try:
            while self.running:
                try:
                    conn, _ = self.sock.accept()
                except OSError:
                    break
                threading.Thread(
                    target=self.handle_client,
                    args=(conn,),
                    daemon=True
                ).start()
        except KeyboardInterrupt:
            print("\nServer shutting down...")
            self.shutdown()
    
    def handle_client(self, conn: socket.socket):
        file = conn.makefile("rwb")
        join = recv(file)

        player_id = join["player_id"]
        if not self.controller.add_player(player_id):
            send(conn, {"type": "error", "message": "Cannot join"})
            conn.close()
            return
        
        self.clients[player_id] = conn
        self.had_players = True

        if self.controller.can_start():
            self.controller.start()

        self.broadcast_state()

        try:
            while True:
                msg = recv(file)
                result = self.controller.make_move(
                    player_id,
                    msg["action"],
                    msg["x"],
                    msg["y"]
                )

                send(conn, {"type": "result", "result": result})
                self.broadcast_state()

                if self.controller.state == "FINISHED":
                    self.broadcast_state()
                    print("Game finished, shutting down server")
                    self.shutdown()
                    return
                
        except (ConnectionError, OSError):
            pass

        finally:
            self.cleanup_disconnect(player_id, conn)

    def cleanup_disconnect(self, player_id, conn):
        if player_id in self.clients:
            del self.clients[player_id]
        
        if player_id in self.controller.players:
            index = self.controller.players.index(player_id)
            self.controller.players.remove(player_id)

            # Adjust turn
            if index < self.controller.turn or self.controller.turn >= len(self.players):
                self.controller.turn = self.controller.turn % len(self.controller.players) if self.controller.players else 0

        try:
            conn.close()
        except:
            pass

        # Shutdown if everyone left after at least one joined
        if self.had_players and not self.clients:
            print("All players left, shutting down server")
            self.shutdown()

    def broadcast_state(self):
        board_data = self.controller.board.serialise()
        board_data["mine_map"] = self.controller.board.mine_map
        
        state = {
            "type": "state",
            "board": board_data,
            "current_player": (
                self.controller.current_player()
                if self.controller.state == "RUNNING"
                else self.controller.players[0] if self.controller.players else None
            ),
            "state": self.controller.state,
            "players": len(self.controller.players),
            "required": self.controller.required_players
        }
        for conn in self.clients.values():
            try:
                send(conn, state)
            except ConnectionError:
                pass

    def shutdown(self):
        self.controller.state = "FINISHED"
        self.broadcast_state()

        time.sleep(1)

        for conn in self.clients.values():
            try:
                conn.close()
            except:
                pass
        self.clients.clear()
        self.running = False

        try:
            self.sock.close()
        except:
            pass