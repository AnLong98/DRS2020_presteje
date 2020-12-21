from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class PlayerFrame(QFrame):
    def __init__(self, players):
        super(QFrame, self).__init__()

        self.players = players

        self.setFixedSize(240, 300)
        self.setStyleSheet('background-color: #e8eb34')

        self.define_frame_style()

    def define_frame_style(self):
        self.name_label = QLabel("Player: ", self)
        self.name_label.setGeometry(0, 0, 10, 5)
        self.name_label.setMinimumSize(10, 5)
        self.points_label = QLabel("Points: ", self)
        self.points_label.setGeometry(0, 0, 10, 5)
        self.points_label.setMinimumSize(10, 5)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.name_label)
        layout.addWidget(self.points_label)
        self.setLayout(layout)

    def add_player_frames(self):
        splitter = QSplitter(Qt.Vertical)
        #splitter.setEnabled(False)
        splitter.setStyleSheet("QSplitter::handle {image: none;}")
        vbox = QVBoxLayout()
        if len(self.players) != 0:
            for player in self.players:
                vbox.addWidget(PlayerFrame(self.player.user_name, self.player.points))

        self.setLayout(vbox)

class TimerFrame(QFrame):
    def __init__(self):
        super(QFrame, self).__init__()

        self.setFixedSize(240, 100)
        self.setStyleSheet('background-color: #34ebdf')

class ButtonFrame(QFrame):
    def __init__(self):
        super(QFrame, self).__init__()

        self.setFixedSize(240, 400)
        self.setStyleSheet('background-color: #b134eb')

class ScoreBoard(QFrame):
    def __init__(self):
        super(ScoreBoard, self).__init__()
        self.define_frame_style()
        self.players = []

        self.vbox = QVBoxLayout()
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.setEnabled(False)
        self.splitter.addWidget(PlayerFrame(self.players))
        self.splitter.addWidget(TimerFrame())
        self.splitter.addWidget(ButtonFrame())
        self.vbox.addWidget(self.splitter)
        self.setLayout(self.vbox)



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
