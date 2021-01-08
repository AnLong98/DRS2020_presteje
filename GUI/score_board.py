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
        self.time.setText("Time left: " + str(self.elapsedTime))
        self.qTimer.timeout.connect(self.start_timer)
        # start timer
        self.qTimer.start()

    def set_game(self, game):
        self.game = game

    def reset_timer(self):
        self.qTimer.stop()
        self.elapsedTime = 10
        self.time.setText("Time left: " + str(self.elapsedTime))
        self.qTimer.start()

    def start_timer(self):
        self.time.setText("Time left: " + str(self.elapsedTime))
        self.elapsedTime = self.elapsedTime - 1
        if self.elapsedTime == -1:
            self.reset_timer()
            self.game.change_player()

    def kill_timer(self):
        self.killTimer(self.qTimer.timerId())


class ButtonFrame(QFrame):
    def __init__(self, active_player, active_snake):
        super(QFrame, self).__init__()

        self.active_player = active_player
        self.active_snake = active_snake
        self.scores = []

        self.setFixedSize(240, 400)
        self.setStyleSheet('background-color: #bababa')

        self.define_frame_style()

        self.qTimer = QTimer()
        self.qTimer.setInterval(140)
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.update_scores)
        # start timer
        self.qTimer.start()

    def set_active_player_(self, active_player):
        self.active_player = active_player

    def set_active_snake_(self, active_snake):
        self.active_snake = active_snake

    def define_frame_style(self):
        layout = QVBoxLayout()
        font1 = QFont('Arial', 11.5)
        font2 = QFont('Arial', 17)

        label1 = QLabel("Active player: ", self)
        label1.setFont(font1)
        label1.setStyleSheet("color: #6e6e6e")

        label1_1 = QLabel("", self)
        label1_1.setFont(font2)
        label1_1.setStyleSheet("color: #6e6e6e")

        label2 = QLabel("The number of remaining steps\nof the active snake: ", self)
        label2.setFont(font1)
        label2.setStyleSheet("color: #6e6e6e")

        label2_1 = QLabel("", self)
        label2_1.setFont(font2)
        label2_1.setStyleSheet("color: #6e6e6e")

        self.scores.append([label1, label1_1, label2, label2_1])
        layout.addWidget(label1)
        layout.addWidget(label1_1)
        layout.addWidget(label2)
        layout.addWidget(label2_1)

        layout.addStretch(1)
        self.setLayout(layout)

    def update_scores(self):
        for labels in self.scores:
            labels[1].setStyleSheet("color: " + self.active_player.color)
            labels[3].setStyleSheet("color: " + self.active_player.color)
            #labels[1].setStyleSheet("font-weight: bold")
            #labels[3].setStyleSheet("font-weight: bold")
            labels[1].setText(self.active_player.user_name)
            labels[3].setText(str(self.active_snake.steps - self.active_snake.played_steps))


class ScoreBoard(QFrame):
    def __init__(self, timer_frame):
        super(ScoreBoard, self).__init__()
        self.define_frame_style()
        self.players = []
        self.player_frame = None
        self.qTimer = QTimer()
        self.qTimer.setInterval(100)
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.getPlayersData)
        # start timer
        self.qTimer.start()
        self.timer_frame = timer_frame

        self.winner = None
        self.active_player = None
        self.active_snake = None
        self.button_frame = ButtonFrame(self.active_player, self.active_snake)
        # if self.players:
        #     self.getPlayersData()

    def update_players(self, players):
        self.players = players
        if self.player_frame is not None:
            self.player_frame.players = players

    def define_frame_style(self):
        self.setFixedSize(240, 810)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color: #bababa')

    def reset_timer(self):
        self.timer_frame.reset_timer()

    def kill_timer(self):
        self.timer_frame.kill_timer()


    def set_winner(self, player):
        self.winner = player

    @property
    def get_painter(self):
        return self.painter

    @property
    def get_scoreboard_height(self):
        return self.height()

    @property
    def get_scoreboard_width(self):
        return self.width()

    @property
    def get_scoreboard_width(self):
        return self.width()

    def set_active_player_on_button_frame(self, active_player):
        self.active_player = active_player
        self.button_frame.set_active_player_(active_player)

    def set_active_snake_on_button_frame(self, active_snake):
        self.active_snake = active_snake
        self.button_frame.set_active_snake_(active_snake)

    def getPlayersData(self):
        if self.players:
            self.vbox = QVBoxLayout()
            self.splitter = QSplitter(Qt.Vertical)
            self.splitter.setEnabled(False)
            self.player_frame = PlayerFrame(self.players)
            self.splitter.addWidget(self.player_frame)
            self.splitter.addWidget(self.timer_frame)
            self.splitter.addWidget(self.button_frame)
            self.vbox.addWidget(self.splitter)
            self.setLayout(self.vbox)
            self.qTimer.stop()