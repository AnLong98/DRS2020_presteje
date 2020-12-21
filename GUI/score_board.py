from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class PlayerFramer(QFrame):
    def __init__(self, name, points):
        super(QFrame, self).__init__()
        self.painter = QPainter(self)

        self.name = name
        self.points = points

        self.setFixedSize(240, 120)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color: #eeeee')

    def define_frame_style(self):
        self.name_label = QLabel(self.name, self)
        self.points_label = QLabel(self.points, self)

        layout = QHBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.points_label)
        self.setLayout(layout)

class ScoreBoard(QFrame):
    def __init__(self):
        super(ScoreBoard, self).__init__()
        self.painter = QPainter(self)
        self.define_frame_style()
        self.active_players = []

    def define_frame_style(self):
        self.setFixedSize(240, 810)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color: #dedede')

    @property
    def get_painter(self):
        return self.painter

    @property
    def get_scoreboard_height(self):
        return self.height()

    @property
    def get_scoreboard_width(self):
        return self.width()

    def add_player_frames(self):
        splitter = QSplitter(Qt.Horizontal)
        splitter.setEnabled(False)
        #splitter.setStyleSheet("QSplitter::handle {image: none;}")
        self.setCentralWidget(splitter)
        for player in self.active_players:
            splitter.addWidget(PlayerFramer(player.user_name, player.points))

