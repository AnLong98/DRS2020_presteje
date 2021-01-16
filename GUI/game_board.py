from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from Models.snake_part import SnakePartType

class Repaint(QObject):
    repaint_signal = pyqtSignal()


class GameBoard(QFrame):
    def __init__(self, repaint):
        super(GameBoard, self).__init__()
        self.snakes = []
        self.food = []
        self.active_player = None
        self.define_frame_style()
        self.repaint_signal = repaint.repaint_signal
        self.repaint_signal.connect(self.update)

    def define_frame_style(self):
        self.setFixedSize(960, 810)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color: #27962d')

    @property
    def get_gameboard_height(self):
        return self.height()

    @property
    def get_gameboard_width(self):
        return self.width()

    # square width method
    def square_width(self):
        return 15

    # square height
    def square_height(self):
        return 15

    def set_snakes(self, snakes):
        self.snakes = snakes

    def set_active_player(self, player):
        self.active_player = player

    def set_food(self, food):
        self.food = food

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        active_player_name = ''

        if self.active_player:
            active_player_name = self.active_player.user_name
            for snake in self.active_player.snakes:
                for part in snake.snake_parts:
                    self.draw_square(qp, part, snake)

        for snake in self.snakes:
            if snake.owner_name == active_player_name:
                continue
            for part in snake.snake_parts:
                self.draw_square(qp, part, snake)

        for f in self.food:
            self.draw_square_food(qp, f)
        qp.end()

    def draw_square(self, qp, snake_part, snake):
        rect = self.contentsRect()

        if snake_part.part_type == SnakePartType.HEAD:
            if snake.is_active:
                color = QColor('#000000')
            else:
                color = QColor('#d1d1d1')
        else:
            color = QColor(snake.color)

        qp.fillRect(rect.left() + snake_part.x_coordinate, snake_part.y_coordinate, self.square_width() - 1, self.square_height() - 1, color)

    def draw_square_food(self, qp, food):
        if food.is_super_food:
            color = QColor('#00FFFF')
        else:
            color = QColor('#ff911c')
        rect = self.contentsRect()

        qp.fillRect(rect.left() + food.x_coordinate, food.y_coordinate, self.square_width() - 1, self.square_height() - 1,
                    color)
