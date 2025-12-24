### Multiplayer Minesweeper

Hello there, this is the multiplayer-minesweeper repo, development section. **Multiplayer has finally been released!**

### What's inside:
- Fully functional text-based **multiplayer and singleplayer** Minesweeper game
- Framework for LAN server discovery
- Fancy text colours

### Requirements
- Python 3.13

### Installation
Using Git:
```
git clone https://github.com/Stormpooper-dotcom/multiplayer-minesweeper.git
cd multiplayer-minesweeper
git checkout v1.0.1
```

Or, you can download and extract the zip from [here](https://github.com/Stormpooper-dotcom/multiplayer-minesweeper/archive/refs/tags/v1.0.1.zip).

### Running
```
cd path/to/multiplayer-minesweeper
python main.py host ## Starts a server
[or]
python main.py join "<server_ip>" <username> ## Joins server at <server_ip> as <username>
[or]
python main.py ## Starts a single-player game
```