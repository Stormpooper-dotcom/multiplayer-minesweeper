import sys
from singleplayer import SinglePlayerGame

if __name__ == "__main__":
    if len(sys.argv) > 2:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
        game = SinglePlayerGame(x, y)
    else:
        game = SinglePlayerGame()
    game.play()