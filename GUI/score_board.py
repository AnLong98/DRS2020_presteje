from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class ScoreBoard(QFrame):
    def __init__(self):
        super(ScoreBoard, self).__init__()
        self.define_frame_style()

    def define_frame_style(self):
        self.setFixedSize(250, 800)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color: #8f918d')