from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from models import Snake, SnakePart, SnakePartType, DrawableComponentBase


class GameBoard(QFrame):
    def __init__(self):
        super(GameBoard, self).__init__()
        self.define_frame_style()
        self.painter = QPainter(self)
        self.snakeParts = [
             SnakePart(5, 10, 15, 15, SnakePartType.HEAD)
            ,SnakePart(5, 11, 15, 15, SnakePartType.BODY)
            ,SnakePart(5, 12, 15, 15, SnakePartType.BODY)
        ]
        self.snake = Snake(self.snakeParts, 'Stefan', 1)
        print(self.snake)

    def define_frame_style(self):
        self.setFixedSize(950, 800)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color: #7ffc03')

    @property
    def get_painter(self):
        return self.painter

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

    def paintEvent(self, event):
        qp = QPainter(self)
        for part in self.snake.snake_parts:
            self.draw_square(qp, part)

    def draw_square(self, painter, snake_part):
        color = QColor(Qt.black)
        rect = self.contentsRect()
        if snake_part.part_type == SnakePartType.HEAD:
            color = QColor(Qt.red)
        else:
            color = QColor(Qt.black)
        painter.fillRect(rect.left() + snake_part.x_coordinate * 15 + 1, snake_part.y_coordinate * 15 + 1, self.square_width() - 2, self.square_height() - 2, color)


