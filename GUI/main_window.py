import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from GUI.game_board import GameBoard
from GUI.score_board import ScoreBoard
from Managers.collision_manager import CollisionManager

from Managers.drawing_manager import DrawingManager
from Managers.food_manager import FoodManager
from Managers.movement_manager import MovementManager, KeyPressed
from game import Game
from models import Snake, SnakePart, SnakePartType, DrawableComponentBase, Food, SnakeDirection, User
from Managers.snake_part_manager import SnakePartManager


class MainWindow(QMainWindow):
    def __init__(self, game_board, score_board, game):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Turn Snake - PreSteJe")
        self.setFixedSize(1200, 810)

        self.gameboard = game_board
        self.scoreboard = score_board

        self.generate_window_layout()

        self.game = game

    def generate_window_layout(self):
        splitter = QSplitter(Qt.Horizontal)
        splitter.setEnabled(False)
        splitter.setStyleSheet("QSplitter::handle {image: none;}")
        splitter.addWidget(self.gameboard)
        splitter.addWidget(self.scoreboard)
        self.setCentralWidget(splitter)

    def keyPressEvent(self, event):
        if self.game is None:
            pass
        key = event.key()

        if key == Qt.Key_Left:
            self.game.advance_game(KeyPressed.LEFT)

        elif key == Qt.Key_Right:
            self.game.advance_game(KeyPressed.RIGHT)

        elif key == Qt.Key_Up:
            self.game.advance_game(KeyPressed.UP)

        elif key == Qt.Key_Down:
            self.game.advance_game(KeyPressed.DOWN)

    @property
    def get_gameboard(self):
        return self.gameboard

    @property
    def get_scoreboard(self):
        return self.scoreboard

    @property
    def get_mainwindow_height(self):
        return self.height()

    @property
    def get_mainwindow_width(self):
        return self.width()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game_board = GameBoard()
    score_board = ScoreBoard()

    part_width = 15
    part_height = 15

    #init game related things hardcoded for prototype
    collision_manager = CollisionManager()
    food_manager = FoodManager(collision_manager)
    drawing_manager = DrawingManager(game_board, score_board)
    movement_manager = MovementManager()
    snake_part_manager = SnakePartManager(part_width, part_height)
    table_width = game_board.get_gameboard_width
    table_height = game_board.get_gameboard_height

    food = []
    all_snakes = []

    #create Player 1 hardcoded
    snakes_player1 = []
    snakeParts = [
        SnakePart(200, 45, 15, 15, SnakePartType.HEAD)
        , SnakePart(185, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(170, 45, 15, 15, SnakePartType.BODY)
    ]
    snake = Snake(snakeParts, 'Stefan', 1, SnakeDirection.RIGHT)
    snakes_player1.append(snake)

    snakeParts1_1 = [
        SnakePart(200, 75, 15, 15, SnakePartType.HEAD)
        , SnakePart(185, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(170, 75, 15, 15, SnakePartType.BODY)
    ]
    snake1_1 = Snake(snakeParts1_1, 'Stefan', 1, SnakeDirection.RIGHT)
    snakes_player1.append(snake1_1)

    player_1 = User(snakes_player1, 0, "Stefan")

    # create Player 2 hardcoded
    snakes_player2 = []
    snakeParts2 = [
        SnakePart(700, 75, 15, 15, SnakePartType.HEAD)
        , SnakePart(715, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(730, 75, 15, 15, SnakePartType.BODY)
    ]
    snake2 = Snake(snakeParts2, 'Djura', 1, SnakeDirection.LEFT)
    snakes_player2.append(snake2)

    snakeParts2_1 = [
        SnakePart(700, 45, 15, 15, SnakePartType.HEAD)
        , SnakePart(715, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(730, 45, 15, 15, SnakePartType.BODY)
    ]
    snake2_1 = Snake(snakeParts2_1, 'Djura', 1, SnakeDirection.LEFT)
    snakes_player2.append(snake2_1)
    player_2 = User(snakes_player2, 0, "Djura")

    # create Player 3 hardcoded
    snakes_player3 = []
    snakeParts3 = [
        SnakePart(700, 700, 15, 15, SnakePartType.HEAD)
        , SnakePart(715, 700, 15, 15, SnakePartType.BODY)
        , SnakePart(730, 700, 15, 15, SnakePartType.BODY)
    ]
    snake3 = Snake(snakeParts3, 'Gangula', 1, SnakeDirection.LEFT)
    snakes_player3.append(snake3)

    snakeParts3_1 = [
        SnakePart(700, 670, 15, 15, SnakePartType.HEAD)
        , SnakePart(715, 670, 15, 15, SnakePartType.BODY)
        , SnakePart(730, 670, 15, 15, SnakePartType.BODY)
    ]
    snake3_1 = Snake(snakeParts3_1, 'Gangula', 1, SnakeDirection.LEFT)
    snakes_player3.append(snake3_1)
    player_3 = User(snakes_player3, 0, "Gangula")

    # create Player 4 hardcoded
    snakes_player4 = []
    snakeParts4 = [
        SnakePart(200, 700, 15, 15, SnakePartType.HEAD)
        , SnakePart(185, 700, 15, 15, SnakePartType.BODY)
        , SnakePart(170, 700, 15, 15, SnakePartType.BODY)
    ]
    snake4 = Snake(snakeParts4, 'Beba', 1, SnakeDirection.RIGHT)
    snakes_player4.append(snake4)

    snakeParts4_1 = [
        SnakePart(200, 670, 15, 15, SnakePartType.HEAD)
        , SnakePart(185, 670, 15, 15, SnakePartType.BODY)
        , SnakePart(170, 670, 15, 15, SnakePartType.BODY)
    ]
    snake4_1 = Snake(snakeParts4_1, 'Beba', 1, SnakeDirection.RIGHT)
    snakes_player4.append(snake4_1)

    player_4 = User(snakes_player4, 0, "Beba")


    players = []

    players.append(player_1)
    players.append(player_2)
    players.append(player_3)
    players.append(player_4)

    #Append all snakes
    all_snakes.extend(player_1.snakes)
    all_snakes.extend(player_2.snakes)
    all_snakes.extend(player_3.snakes)
    all_snakes.extend(player_4.snakes)

    for i in range(0,4):
        food.append(food_manager.generate_food(1,1, all_snakes, food, table_width, table_height, 15))

    game = Game(players, food, collision_manager, drawing_manager, movement_manager, snake_part_manager, food_manager, table_width, table_height )
    game.set_active_player(player_1)
    game.set_active_snake(snake)

    window = MainWindow(game_board, score_board, game)
    window.show()

    app.exec_()
