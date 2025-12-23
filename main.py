import sys
from singleplayer import SinglePlayerGame
from multiplayer import MultiplayerGame
from network.server import MultiplayerServer

if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "host":
        server = MultiplayerServer()
        server.start()
    
    elif len(sys.argv) >= 2 and sys.argv[1] == "join":
        host = sys.argv[2]
        name = sys.argv[3]
        game = MultiplayerGame(host, 5000, name)
        game.play()

    else:
        game = SinglePlayerGame()
        game.play()