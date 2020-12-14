from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class GameBoard(QFrame):
    def __init__(self):
        super(GameBoard, self).__init__()
        self.define_frame_style()

    def define_frame_style(self):
        self.setFixedSize(950, 800)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color: #7ffc03')

