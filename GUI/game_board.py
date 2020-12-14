from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class GameBoard(QFrame):
    def __init__(self):
        super(GameBoard, self).__init__()
        self.define_frame_style()
        self.painter = QPainter(self)

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
