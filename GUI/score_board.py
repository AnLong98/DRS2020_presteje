from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


class PlayerFrame(QFrame):
    def __init__(self, players):
        super(QFrame, self).__init__()

        self.players = players
        self.scores = []

        self.setFixedSize(240, 300)
        self.setStyleSheet('background-color: #bababa')

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
            font = QFont('Arial', 17)
            name_label.setFont(font)
            name_label.setStyleSheet('color: '+ player.color)

            points_label = QLabel("Points: " + str(player.points), self)
            points_label.setFont(font)
            points_label.setStyleSheet('color: ' + player.color)

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
        self.setStyleSheet('background-color: #bababa')
        self.elapsedTime = 10 #zakucano vreme za potez.

        vbox = QVBoxLayout()
        self.time = QLabel("Time left: " + str(self.elapsedTime), self)
        self.time.setStyleSheet("color: #e31212")
        self.time.setFont(QFont('Arial', 25))
        vbox.addWidget(self.time)
        self.setLayout(vbox)
        self.game = None

        self.qTimer = QTimer()  # pocinje tajmer da radi i da odbrojava vreme, svake 1 sec poziva funkciju koja smanjuje elapsed_time
        self.qTimer.setInterval(1000)
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.start_timer)
        # start timer
        self.qTimer.start()

    def set_game(self, game):
        self.game = game

    def reset_timer(self):
        self.elapsedTime = 10

    def start_timer(self):
        self.time.setText("Time left: " + str(self.elapsedTime))
        self.elapsedTime = self.elapsedTime - 1
        if self.elapsedTime == 0:
            self.time.setText("Time left: " + str(self.elapsedTime))
            self.reset_timer()
            self.game.change_player()
            # self.qTimer.stop()



class ButtonFrame(QFrame):
    def __init__(self):
        super(QFrame, self).__init__()

        self.setFixedSize(240, 400)
        self.setStyleSheet('background-color: #bababa')


class ScoreBoard(QFrame):
    def __init__(self, timer_frame):
        super(ScoreBoard, self).__init__()
        self.define_frame_style()
        self.players = []

        self.qTimer = QTimer()
        self.qTimer.setInterval(100)
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.getPlayersData)
        # start timer
        self.qTimer.start()
        self.timer_frame = timer_frame

        # if self.players:
        #     self.getPlayersData()

    def define_frame_style(self):
        self.setFixedSize(240, 810)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color: #bababa')

    def reset_timer(self):
        self.timer_frame.reset_timer()

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
            self.splitter.addWidget(self.timer_frame)
            self.splitter.addWidget(ButtonFrame())
            self.vbox.addWidget(self.splitter)
            self.setLayout(self.vbox)
            self.qTimer.stop()