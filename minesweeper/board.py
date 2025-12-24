import random

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
