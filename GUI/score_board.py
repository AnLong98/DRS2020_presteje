from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class PlayerFrame(QFrame):
    def __init__(self, players):
        super(QFrame, self).__init__()

        self.players = players
        self.scores = []

        self.setFixedSize(240, 300)
        self.setStyleSheet('background-color: #e8eb34')

        self.define_frame_style()

        self.qTimer = QTimer()
        self.qTimer.setInterval(500)
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.update_scores)
        # start timer
        self.qTimer.start()

    def define_frame_style(self):
        layout = QVBoxLayout()
        for player in self.players:
            name_label = QLabel("Player: " + player.user_name, self)
            name_label.setFont(QFont('Arial', 10))

            points_label = QLabel("Points: " + str(player.points), self)
            points_label.setFont(QFont('Arial', 10))

            self.scores.append([name_label, points_label])
            layout.addWidget(name_label)
            layout.addWidget(points_label)
        layout.addStretch(1)
        self.setLayout(layout)

    def update_scores(self):
        for labels, player in zip(self.scores, self.players):
            labels[1].setText("Points: " + str(player.points))


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

        self.qTimer = QTimer()
        self.qTimer.setInterval(100)
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.getPlayersData)
        # start timer
        self.qTimer.start()

        # if self.players:
        #     self.getPlayersData()

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
        if self.players:
            self.vbox = QVBoxLayout()
            self.splitter = QSplitter(Qt.Vertical)
            self.splitter.setEnabled(False)
            self.splitter.addWidget(PlayerFrame(self.players))
            self.splitter.addWidget(TimerFrame())
            self.splitter.addWidget(ButtonFrame())
            self.vbox.addWidget(self.splitter)
            self.setLayout(self.vbox)
            self.qTimer.stop()