from classes import Board

class GameController:
    def __init__(self, width=10, height=10, num_mines=None, max_players=4):
        self.board = Board(width, height, num_mines)
        self.max_players = max_players
        self.required_players = max_players
        self.players = []
        self.state = "LOBBY"
        self.turn = 0

    def add_player(self, player_id):
        if self.state != "LOBBY":
            return False
        if len(self.players) >= self.max_players:
            return False
        self.players.append(player_id)
        return True
    
    def set_required_players(self, count):
        if self.state == "LOBBY":
            self.required_players = count
    
    def can_start(self):
        return len(self.players) >= self.required_players
    
    def start(self):
        if self.can_start():
            self.state = "RUNNING"
            self.turn = 0

    def current_player(self):
        return self.players[self.turn]
    
    def next_turn(self):
        self.turn = (self.turn + 1) % len(self.players)

    def make_move(self, player_id, action, x, y):
        if self.state != "RUNNING":
            return "not_running"
        
        if player_id != self.current_player():
            return "not_your_turn"
        
        if action == "m":
            result = self.board.make_move(x, y)
            if result in ("flagged", "already"):
                return result
            if result == "mine":
                self.state = "FINISHED"
                return "mine"
            
        elif action == "f":
            result = self.board.toggle_flag(x, y)
            if result == "revealed":
                return result

        if self.board.check_win():
            self.state = "FINISHED"
            return "win"
        
        self.next_turn()
        return "ok"