
class DrawingManager:
    def __init__(self, game_board, score_board, main_window):
        self.game_board = game_board
        self.score_board = score_board
        self.main_window = main_window

    def draw_food(self, food):
        self.game_board.update_food(food)

    def reset_turn_time(self):
        self.score_board.reset_timer()

    def update_players(self, players):
        #TODO: Add code here to update all player-related info: snakes, remaining steps, score
        snakes = []
        for player in players:
            if player.snakes:
                snakes.extend(player.snakes)

        self.game_board.update_snakes(snakes)
        self.score_board.update_players(players)

    def stop_input(self):
        self.main_window.deactivate_sending()

    def start_input(self):
        self.main_window.activate_sending()

    def start_timer(self):
        self.score_board.init_timer()

    def set_active_player(self, player):
        self.game_board.update_active_player(player)
        self.score_board.set_active_player_on_information_frame(player)

    def close_window(self):
        self.main_window.close()

    def add_winner(self, player):
        self.score_board.set_winner(player)

    def change_head(self, snake):
        self.game_board.change_head_color(snake)

