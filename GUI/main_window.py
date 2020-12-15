import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from GUI.game_board import GameBoard
from GUI.score_board import ScoreBoard
from Managers.collision_manager import CollisionManager

from Managers.drawing_manager import DrawingManager
from Managers.movement_manager import MovementManager, KeyPressed
from game import Game
from models import Snake, SnakePart, SnakePartType, DrawableComponentBase, Food, SnakeDirection, User


class MainWindow(QMainWindow):
    def __init__(self, game_board, score_board, game):
        super(MainWindow, self).__init__()
        self.setWindowTitle("PreSteJe Snake Game")
        self.setFixedSize(1200, 800)

        self.gameboard = game_board

        self.scoreboard = score_board

        self.generate_window_layout()
        self.game = game

    # def center_main_window(self):
    #     qtRectangle = self.frameGeometry()
    #     centerPoint = QDesktopWidget().availableGeometry().center()
    #     qtRectangle.moveCenter(centerPoint)
    #     return self.move(qtRectangle.topLeft())

    def generate_window_layout(self):
        splitter = QSplitter(Qt.Horizontal)
        splitter.setEnabled(False)
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

    #init game related things hardcoded for prototype
    collision_manager = CollisionManager()
    drawing_manager = DrawingManager(game_board)
    movement_manager = MovementManager()
    table_width = game_board.get_gameboard_width
    table_height = game_board.get_gameboard_height

    food = []
    food.append(Food(23, 10, 15, 15, 1, 1))
    food.append(Food(50, 50, 15, 15, 1, 1))

    snakes = []
    snakeParts = [
         SnakePart(5, 200, 15, 15, SnakePartType.HEAD)
        ,SnakePart(5, 215, 15, 15, SnakePartType.BODY)
        ,SnakePart(5, 230, 15, 15, SnakePartType.BODY)
    ]
    snake = Snake(snakeParts, 'Stefan', 1, SnakeDirection.UP)
    snakes.append(snake)

    snakes2 = []
    snakeParts2 = [
        SnakePart(70, 70, 15, 15, SnakePartType.HEAD)
        , SnakePart(85, 70, 15, 15, SnakePartType.BODY)
        , SnakePart(100, 70, 15, 15, SnakePartType.BODY)
    ]
    snake2 = Snake(snakeParts2, 'Mikisa', 1, SnakeDirection.LEFT)
    snakes2.append(snake2)

    players = []
    player = User(snakes, 0, "Stefan")
    player2 = User(snakes2, 0, "Mikisa")

    players.append(player)
    players.append(player2)

    game = Game(players, food, collision_manager, drawing_manager, movement_manager, table_width, table_height )
    game.set_active_player(player)
    game.set_active_snake(snake)

    window = MainWindow(game_board, score_board, game)
    window.show()

    app.exec_()
