
class DrawingManager:
    def __init__(self, game_board, score_board):
        self.game_board = game_board
        self.score_board = score_board

    def draw_snakes(self, snakes):
        self.game_board.update_snakes(snakes)

    def draw_food(self, food):
        self.game_board.update_food(food)

    def add_player_to_scoreboard(self, players):
        self.score_board.update_players(players)

    def change_head(self, snake):
        self.game_board.change_head_color(snake)

    def reset_turn_time(self):
        self.score_board.reset_timer()

    def stop_turn_time(self):
        self.score_board.kill_timer()

    def add_winner(self, player):
        self.score_board.set_winner(player)

    def set_active_player_on_score_board(self, active_player):
        self.score_board.set_active_player_on_button_frame(active_player)

    def set_active_snake_on_score_board(self, active_snake):
        self.score_board.set_active_snake_on_button_frame(active_snake)
