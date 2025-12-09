import sys

import classes

if __name__ == "__main__":
    if len(sys.argv) > 2:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        game = classes.Game(x, y)
    else:
        game = classes.Game()
    game.play()