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

        layout = QVBoxLayout()
        for player in self.players:
            name_label = QLabel("Player: " + player.user_name, self)
            name_label.setFont(QFont('Arial', 10))

            points_label = QLabel("Points: " + str(player.points), self)
            points_label.setFont(QFont('Arial', 10))
            layout.addWidget(name_label)
            layout.addWidget(points_label)
        layout.addStretch(1)
        self.setLayout(layout)

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
        if self.players:
            self.getPlayersData()

        self.qTimer = QTimer()
        self.qTimer.setInterval(1000)
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.getPlayersData)
        # start timer
        self.qTimer.start()

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

    def getPlayersData(self):
        self.vbox = QVBoxLayout()
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.setEnabled(False)
        self.splitter.addWidget(PlayerFrame(self.players))
        self.splitter.addWidget(TimerFrame())
        self.splitter.addWidget(ButtonFrame())
        self.vbox.addWidget(self.splitter)
        self.setLayout(self.vbox)