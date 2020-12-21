
class DrawingManager:
    def __init__(self, game_board, score_board):
        self.game_board = game_board
        self.score_board = score_board

    def draw_snakes(self, snakes):
        self.game_board.update_snakes(snakes)

    def draw_food(self, food):
        self.game_board.update_food(food)

    def add_player_to_scoreboard(self, players):
        self.score_board.players = players