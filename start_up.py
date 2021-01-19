import sys
import copy
from PyQt5.QtWidgets import *
from GUI.game_board import GameBoard
from GUI.score_board import ScoreBoard
from Managers.collision_manager import CollisionManager

from Managers.drawing_manager import DrawingManager
from Managers.food_manager import FoodManager
from Managers.movement_manager import MovementManager
from models import Snake, SnakeDirection, User
from Managers.snake_part_manager import SnakePartManager
from Managers.shift_players_manager import ShiftPlayersManager
from GUI.score_board import TimerFrame
from GUI.main_window import MainWindow
from game import Game

from player_snakes import PlayerSnakes

class InGameInitializer:
    def __init__(self, players, snakes):

        self.players = players
        self.snakes_count = snakes
        ps = PlayerSnakes()
        all_players = []
        all_snakes = []
        colors = ["#fff200", "#b87bba", "#3494e3", "#fa5700"]

        self.game_board = GameBoard()
        timer_frame = TimerFrame()
        self.score_board = ScoreBoard(timer_frame)

        part_width = 15
        part_height = 15


        collision_manager = CollisionManager()
        self.food_manager = FoodManager(collision_manager)
        drawing_manager = DrawingManager(self.game_board, self.score_board)
        movement_manager = MovementManager()
        snake_part_manager = SnakePartManager(part_width, part_height, collision_manager)
        shift_players_manager = ShiftPlayersManager()
        table_width = self.game_board.get_gameboard_width
        table_height = self.game_board.get_gameboard_height

        food = []
        #deus_ex_machina = None

        for i in range(len(players)):
            p_snake = ps.all_snakes[i][:snakes]
            player_snake = []
            for snake_part in p_snake:
                if (i + 1) % 2 == 0:
                    snake = Snake(snake_part, players[i], 10, 0, SnakeDirection.LEFT, colors[i])
                else:
                    snake = Snake(snake_part, players[i], 10, 0, SnakeDirection.RIGHT, colors[i])

                player_snake.append(snake)

            all_players.append(User(player_snake, 0, players[i], colors[i]))
            all_snakes.extend(player_snake)

        for i in range(0, 30):
            food.append(self.food_manager.generate_food(1, 1, all_snakes, food, None, table_width, table_height, 15))

        #deus_ex_machina = self.food_manager.generate_food(0, 0, all_snakes, food, table_width, table_height, 15, True)  # generate superfood

        self.game = Game(all_players, food, collision_manager, drawing_manager, movement_manager, snake_part_manager, self.food_manager, shift_players_manager, table_width, table_height, self)
        self.game.set_active_player(all_players[0])
        self.game.set_active_snake(all_players[0].snakes[0])

        self.score_board.set_active_player_on_button_frame(all_players[0])
        self.score_board.set_active_snake_on_button_frame(all_players[0].snakes[0])

        timer_frame.set_game(self.game)

        self.last_players = copy.deepcopy(all_players)
        self.last_snakes = copy.deepcopy(all_snakes)


    def restart_game(self):
        self.copy_last_players = copy.deepcopy(self.last_players)
        self.copy_last_snakes = copy.deepcopy(self.last_snakes)
        self.game.players = self.copy_last_players
        food = []
        #deux_ex_machine = None

        for i in range(0, 30):
            food.append(self.food_manager.generate_food(1, 1, self.copy_last_snakes, food, None, self.game.table_width, self.game.table_height, 15))

        #deus_ex_machina = self.food_manager.generate_food(0, 0, self.copy_last_snakes, food, self.game.table_width, self.game.table_height, 15, True)  # generate superfood
        self.game.food = food
        #self.game.deux_ex_machine = deus_ex_machina

        self.score_board.set_active_player_on_button_frame(self.copy_last_players[0])
        self.score_board.set_active_snake_on_button_frame(self.copy_last_players[0].snakes[0])

    def exit_game(self):
        self.window.close()

    def start_main(self):
        app = QApplication(sys.argv)
        self.window = MainWindow(self.game_board, self.score_board, self.game)
        self.window.show()
        app.exec_()
