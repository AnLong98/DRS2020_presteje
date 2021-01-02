
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

    def change_head(self, snake):
        self.game_board.change_head_color(snake)

    def reset_turn_time(self):
        self.score_board.reset_timer()

    def update_players(self, players):
        #TODO: Add code here to update all player-related info: snakes, remaining steps, score
        pass