CELL_COLOURS = {0: "\033[32m",
                1: "\033[31m",
                2: "\033[36m",
                3: "\033[35m",
                4: "\033[33m",
                5: "\033[1;34m",
                6: "\033[0m",
                7: "\033[1;35m",
                8: "\033[1;36m"}

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
                    print(f"{CELL_COLOURS[cell]}{cell}\033[0m", end=" ")
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
                        print(f"{CELL_COLOURS[g]}{g}\033[0m", end=" ")
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
