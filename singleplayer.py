import os
from controller import GameController
from classes import ConsoleUI

class SinglePlayerGame:
    def __init__(self, width=10, height=10, num_mines=None):
        self.controller = GameController(width, height, num_mines)
        self.ui = ConsoleUI()
        self.player_id = "local"

        self.controller.add_player(self.player_id)
        self.controller.start()

    def play(self):
        while self.controller.state == "RUNNING":
            os.system("clear") if os.name == "posix" else os.system("cls")

            print(f"Mines: {self.controller.board.num_mines}")
            print(f"Remaining: {self.controller.board.num_mines - self.controller.board.num_flags}")
            print("Current Board:")
            self.ui.print_board(self.controller.board.guess_map)

            move = self.ui.handle_input(
                self.controller.board.width,
                self.controller.board.height
            )

            if move is None:
                break

            action, x, y = move
            result = self.controller.make_move(self.player_id, action, x, y)

            message = None
            if result == "flagged":
                message = "Can't dig a flagged square"
            elif result == "already":
                message = "Square already revealed"
            elif result == "revealed":
                message = "Can't flag a revealed square"
            elif result == "not_your_turn":
                message = "Not your turn"
            elif result == "not_running":
                message = "Game not running"

            if message:
                print(message)
                input("Press Enter to continue...")
            
            if result == "mine":
                print("You hit a mine!")
                self.ui.print_loss_map(
                    self.controller.board.guess_map,
                    self.controller.board.mine_map,
                    x, y
                )
                break

            if result == "win":
                print("You win!")
                self.ui.print_board(self.controller.board.guess_map)
                break