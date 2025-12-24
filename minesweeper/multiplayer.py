import os
import time
from frontends.console import ConsoleUI
from network.client import MultiplayerClient

RESULT_MESSAGES = {
    "flagged": "Can't dig up a flagged square",
    "already": "Square already revealed",
    "revealed": "Can't flag a revealed square",
    "not_your_turn": "Not your turn",
    "not_running": "Game not running",
}

class MultiplayerGame:
    def __init__(self, host, port, player_id):
        self.ui = ConsoleUI()
        self.state = "LOBBY"
        self.board = None
        self.players = 0
        self.required = 0
        self.current_player = None
        self.last_message = None
        self.player_id = player_id

        self.client = MultiplayerClient(
            host,
            port,
            player_id,
            self.handle_message
        )

    def handle_message(self, msg):
        if msg["type"] == "state":
            self.board = msg["board"]
            self.current_player = msg["current_player"]
            self.state = msg["state"]
            self.players = msg["players"]
            self.required = msg["required"]

            self.mine_map = self.board.get("mine_map")

        elif msg["type"] == "result":
            result = msg["result"]
            if result in RESULT_MESSAGES:
                self.last_message = RESULT_MESSAGES[result]
            
            elif result == "mine":
                self.last_message = "You hit a mine!"

            elif result == "win":
                self.last_message = "You win!"
    
    def play(self):
        while True:
            os.system("clear") if os.name == "posix" else os.system("cls")

            if self.board:
                if self.state != "FINISHED":
                    self.ui.print_board(self.board["guess_map"])
                    if self.state == "RUNNING":
                        turn_str = ">> YOU <<" if self.current_player == self.player_id else self.current_player
                        print(f"Current turn: {turn_str}")
                    else:
                        print("Game finished")
                else:
                    print("Final board:")
                    guess = self.board["guess_map"]
                    mines = self.mine_map
                    if mines:
                        self.ui.print_loss_map(guess, mines, -1, -1)
                    else:
                        self.ui.print_board(guess)
                    print("Game over!")

            if self.last_message:
                print(self.last_message)
                input("Press Enter to continue")
                self.last_message = None

            if self.state == "LOBBY":
                print(f"Lobby: {self.players}/{self.required} players")
                print("Waiting for players...")
                time.sleep(1)
                continue

            if self.state == "FINISHED":
                break

            if self.player_id != self.current_player:
                print("Waiting for your turn...")
                time.sleep(1)
                continue
            
            move = self.ui.handle_input(
                self.board["width"],
                self.board["height"]
            )
            if move is None:
                break

            action, x, y = move
            try:
                self.client.send_move(action, x, y)
            except (ConnectionError, OSError):
                print("\n[Disconnected from server]")
                break