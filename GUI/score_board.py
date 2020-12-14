from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class ScoreBoard(QFrame):
    def __init__(self):
        super(ScoreBoard, self).__init__()
        self.painter = QPainter(self)
        self.define_frame_style()

    def define_frame_style(self):
        self.setFixedSize(250, 800)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color: #8f918d')

    @property
    def get_painter(self):
        return self.painter

    @property
    def get_scoreboard_height(self):
        return self.height()

    @property
    def get_scoreboard_width(self):
        return self.width()
