from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from models import Snake, SnakePart, SnakePartType, DrawableComponentBase
from models import SnakeDirection


class GameBoard(QFrame):
    def __init__(self):
        super(GameBoard, self).__init__()
        self.snakes = []
        self.food = []
        self.define_frame_style()

    def define_frame_style(self):
        self.setFixedSize(950, 800)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color: #7ffc03')

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

    def update_snakes(self, snakes):
        self.snakes = snakes
        self.update()

    def update_food(self, food):
        self.food = food
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        for snake in self.snakes:
            for part in snake.snake_parts:
                self.draw_square(qp, part)

        for f in self.food:
            self.draw_square_food(qp, f)

    def draw_square(self, qp, snake_part):
        color = QColor(Qt.black)
        rect = self.contentsRect()
        if snake_part.part_type == SnakePartType.HEAD:
            color = QColor(Qt.red)
        else:
            color = QColor(Qt.black)
        qp.fillRect(rect.left() + snake_part.x_coordinate, snake_part.y_coordinate, self.square_width(), self.square_height(), color)

    def draw_square_food(self, qp, food):
        color = QColor(Qt.white)
        rect = self.contentsRect()

        qp.fillRect(rect.left() + food.x_coordinate, food.y_coordinate, self.square_width(), self.square_height(), color)
