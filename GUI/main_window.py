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
from Managers.shift_players_manager import ShiftPlayersManager
from Managers.shift_snakes_manager import ShiftSnakesManager
from GUI.score_board import TimerFrame
from Managers.snake_played_steps_manager import SnakePlayedStepsManager


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

        elif key == Qt.Key_Tab:
            self.game.change_snake()

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
    timer = TimerFrame()
    score_board = ScoreBoard(timer)

    part_width = 15
    part_height = 15

    #init game related things hardcoded for prototype
    collision_manager = CollisionManager()
    food_manager = FoodManager(collision_manager)
    drawing_manager = DrawingManager(game_board, score_board)
    movement_manager = MovementManager()
    snake_part_manager = SnakePartManager(part_width, part_height, collision_manager)
    shift_players_manager = ShiftPlayersManager()
    shift_snakes_manager = ShiftSnakesManager()
    snake_played_steps_manager = SnakePlayedStepsManager()
    table_width = game_board.get_gameboard_width
    table_height = game_board.get_gameboard_height

    food = []
    all_snakes = []

    #create Player 1 hardcoded
    snakes_player1 = []
    snakeParts = [
        SnakePart(210, 45, 15, 15, SnakePartType.HEAD)
        , SnakePart(195, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(180, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(175, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(160, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(145, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(130, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(115, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(100, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(85, 45, 15, 15, SnakePartType.BODY)

    ]
    snake = Snake(snakeParts, 'Stefan', 10, 0, SnakeDirection.RIGHT, "#fff200")
    snakes_player1.append(snake)

    snakeParts1_1 = [
        SnakePart(210, 75, 15, 15, SnakePartType.HEAD)
        , SnakePart(195, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(180, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(175, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(160, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(145, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(130, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(115, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(100, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(85, 75, 15, 15, SnakePartType.BODY)
    ]
    snake1_1 = Snake(snakeParts1_1, 'Stefan', 10, 0, SnakeDirection.RIGHT, "#fff200")
    snakes_player1.append(snake1_1)

    player_1 = User(snakes_player1, 0, "Stefan", "#fff200") #CRVENA BOJA IGRACA 1

    # create Player 2 hardcoded
    snakes_player2 = []
    snakeParts2 = [
        SnakePart(705, 75, 15, 15, SnakePartType.HEAD)
        , SnakePart(720, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(735, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(750, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(765, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(780, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(795, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(810, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(825, 75, 15, 15, SnakePartType.BODY)
        , SnakePart(840, 75, 15, 15, SnakePartType.BODY)
    ]
    snake2 = Snake(snakeParts2, 'Djura', 10, 0, SnakeDirection.LEFT, "#b87bba")
    snakes_player2.append(snake2)

    snakeParts2_1 = [
        SnakePart(705, 45, 15, 15, SnakePartType.HEAD)
        , SnakePart(720, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(735, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(750, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(765, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(780, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(795, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(810, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(825, 45, 15, 15, SnakePartType.BODY)
        , SnakePart(840, 45, 15, 15, SnakePartType.BODY)
    ]
    snake2_1 = Snake(snakeParts2_1, 'Djura', 10, 0, SnakeDirection.LEFT, "#b87bba")
    snakes_player2.append(snake2_1)
    player_2 = User(snakes_player2, 0, "Djura", "#b87bba") #PLAVA BOJA IGRACA 2

    # create Player 3 hardcoded
    snakes_player3 = []
    snakeParts3 = [
        SnakePart(705, 705, 15, 15, SnakePartType.HEAD)
        , SnakePart(720, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(735, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(750, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(765, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(780, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(795, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(810, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(825, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(840, 705, 15, 15, SnakePartType.BODY)

    ]
    snake3 = Snake(snakeParts3, 'Gangula', 10, 0, SnakeDirection.LEFT, "#3494e3")
    snakes_player3.append(snake3)

    snakeParts3_1 = [
        SnakePart(705, 675, 15, 15, SnakePartType.HEAD)
        , SnakePart(720, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(735, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(750, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(765, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(780, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(795, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(810, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(825, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(840, 675, 15, 15, SnakePartType.BODY)
    ]
    snake3_1 = Snake(snakeParts3_1, 'Gangula', 10, 0, SnakeDirection.LEFT, "#3494e3")
    snakes_player3.append(snake3_1)
    player_3 = User(snakes_player3, 0, "Gangula", "#3494e3") #NEKA ROZA BOJA IGRACA 3

    # create Player 4 hardcoded
    snakes_player4 = []
    snakeParts4 = [
        SnakePart(210, 705, 15, 15, SnakePartType.HEAD)
        , SnakePart(195, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(180, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(175, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(160, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(145, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(130, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(115, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(100, 705, 15, 15, SnakePartType.BODY)
        , SnakePart(85, 705, 15, 15, SnakePartType.BODY)
    ]
    snake4 = Snake(snakeParts4, 'Beba', 10, 0, SnakeDirection.RIGHT, "#fa5700")
    snakes_player4.append(snake4)

    snakeParts4_1 = [
        SnakePart(210, 675, 15, 15, SnakePartType.HEAD)
        , SnakePart(195, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(180, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(175, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(160, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(145, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(130, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(115, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(100, 675, 15, 15, SnakePartType.BODY)
        , SnakePart(85, 675, 15, 15, SnakePartType.BODY)
    ]
    snake4_1 = Snake(snakeParts4_1, 'Beba', 10, 0, SnakeDirection.RIGHT, "#fa5700")
    snakes_player4.append(snake4_1)

    player_4 = User(snakes_player4, 0, "Beba", "#fa5700") #SVETLO PLAVA BOJA IGRACA 4


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

    for i in range(0, 30):
        food.append(food_manager.generate_food(1, 1, all_snakes, food, table_width, table_height, 15))

    food.append(food_manager.generate_food(1, 1, all_snakes, food, table_width, table_height, 15, True)) #generate superfood

    game = Game(players, food, collision_manager, drawing_manager, movement_manager, snake_part_manager, food_manager, shift_players_manager, shift_snakes_manager, snake_played_steps_manager, table_width, table_height )
    game.set_active_player(player_1)
    game.set_active_snake(snake)

    timer.set_game(game)

    window = MainWindow(game_board, score_board, game)
    window.show()

    app.exec_()
