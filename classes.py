import random
import os

cell_colours = {0: "\033[32m",
                1: "\033[31m",
                2: "\033[36m",
                3: "\033[35m",
                4: "\033[33m",
                5: "\033[1;34m",
                6: "\033[0m",
                7: "\033[1;35m",
                8: "\033[1;36m"}

class Board:
    def __init__(self, width=10, height=10, num_mines=None):
        self.width = width
        self.height = height
        self.num_mines = num_mines or (width + height) // 2
        self.num_flags = 0
        self.mine_map = self._create_mine_map()
        self.guess_map = self._create_board(-1)

    def _create_board(self, fill):
        return [[fill for _ in range(self.width)] for _ in range(self.height)]

    def _create_mine_map(self):
        board = self._create_board(0)
        placed = 0
        while placed < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if board[y][x] == 0:
                board[y][x] = 1
                placed += 1
        return board

    def get_neighbors(self, x, y):
        offsets = [(-1, -1), (0, -1), (1, -1),
                   (-1, 0),          (1, 0),
                   (-1, 1),  (0, 1), (1, 1)]
        return [(x+dx, y+dy) for dx, dy in offsets
                if 0 <= x+dx < self.width and 0 <= y+dy < self.height]

    def flood_fill(self, x, y):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if self.guess_map[cy][cx] != -1:
                continue
            neighbors = self.get_neighbors(cx, cy)
            count = sum(1 for nx, ny in neighbors if self.mine_map[ny][nx] == 1)
            self.guess_map[cy][cx] = count
            if count == 0:
                for nx, ny in neighbors:
                    if self.guess_map[ny][nx] == -1:
                        stack.append((nx, ny))

    def make_move(self, x, y):
        if self.guess_map[y][x] == 9:  # flagged square
            return "flagged"
        if self.guess_map[y][x] != -1:  # already revealed
            return "already"
        if self.mine_map[y][x] == 1:  # mine
            return "mine"
        self.flood_fill(x, y)
        return "ok"

    def toggle_flag(self, x, y):
        # Can't flag revealed cells
        if self.guess_map[y][x] not in (-1, 9):
            return "revealed"

        if self.guess_map[y][x] == -1:
            self.guess_map[y][x] = 9
            self.num_flags += 1
        elif self.guess_map[y][x] == 9:
            self.guess_map[y][x] = -1
            self.num_flags -= 1

        return "ok"

    def check_win(self):
        # Count only truly revealed cells (0..8). Flags (9) are not revealed.
        revealed_cells = sum(
            1 for row in self.guess_map for cell in row
            if isinstance(cell, int) and 0 <= cell <= 8
        )
        return revealed_cells == self.width * self.height - self.num_mines
    
    def serialise(self):
        return {
            "width": self.width,
            "height": self.height,
            "guess_map": self.guess_map,
            "num_flags": self.num_flags,
            "num_mines": self.num_mines
        }


class ConsoleUI:
    @staticmethod
    def print_board(board, debug=False):
        for row in board:
            for cell in row:
                if cell == -1:
                    print("-" if not debug else cell, end=" ")
                elif cell == 9:
                    print("\033[1;31mF\033[0m", end=" ")
                else:
                    print(f"{cell_colours[cell]}{cell}\033[0m", end=" ")
            print()
        print()

    @staticmethod
    def print_loss_map(guess_map, mine_map, death_x, death_y):
        for y in range(len(guess_map)):
            for x in range(len(guess_map[y])):
                g = guess_map[y][x]
                m = mine_map[y][x]

                if x == death_x and y == death_y:
                    print("\033[1;31mX\033[0m", end=" ")
                    continue

                if m == 1:
                    if g == 9:
                        print("\033[1;31mF\033[0m", end=" ")
                    else:
                        print("\033[1;31mM\033[0m", end=" ")
                else:
                    if g == -1:
                        print("-", end=" ")
                    elif g == 9:
                        print("\033[1;3;31mF\033[0m", end=" ")
                    else:
                        print(f"{cell_colours[g]}{g}\033[0m", end=" ")
            print()
        print()


    @staticmethod
    def handle_input(width, height):
        while True:
            raw = input("Enter move (M x y | F x y | exit): ").strip().lower()
            if raw == "exit":
                return None
            parts = raw.split()
            if len(parts) != 3 or parts[0] not in ("m", "f"):
                print("Invalid move syntax")
                continue
            try:
                x = int(parts[1]) - 1
                y = int(parts[2]) - 1
            except ValueError:
                print("Coordinates must be integers")
                continue
            if not (0 <= x < width and 0 <= y < height):
                print("Out of bounds")
                continue
            return (parts[0], x, y)