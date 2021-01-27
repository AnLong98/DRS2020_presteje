from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from GUI.TimerFrame import TimerFrame


class PlayerFrame(QFrame):
    def __init__(self):
        super(QFrame, self).__init__()

        self.name_labels = []
        self.points_labels = []
        self.layout = QVBoxLayout()
        self.should_init = True

        self.setFixedSize(240, 300)
        self.setStyleSheet('background-color: #bababa')
        self.create_layout()


    def create_layout(self):
        for i in range(0, 4):
            self.name_labels.append(QLabel("Player: -", self))
            self.name_labels[i].setFont(QFont('Arial', 17))
            self.name_labels[i].setStyleSheet('color: ' + "#fff200")

            self.points_labels.append(QLabel("Points: 0", self))
            self.points_labels[i].setFont(QFont('Arial', 17))
            self.points_labels[i].setStyleSheet('color: ' + "#fff200")
            self.layout.addWidget(self.name_labels[i])
            self.layout.addWidget(self.points_labels[i])
        self.layout.addStretch(1)
        self.setLayout(self.layout)


    def update_players(self, players):

        i = 0
        for player in players:
            print(player.user_name)
            self.name_labels[i].setText("Player: " + str(player.user_name))
            self.points_labels[i].setText("Points: " + str(player.points))
            if self.should_init: #eliminate flicker
                self.name_labels[i].setStyleSheet('color: ' + player.color)
                self.points_labels[i].setStyleSheet('color: ' + player.color)
            i += 1
        self.should_init = False
        if len(self.name_labels) == len(players):
            return

        for j in range(i, 4):
            self.name_labels[j].setText("")
            self.points_labels[j].setText("")
            # self.layout.removeWidget(self.name_labels[-1])
            # self.layout.removeWidget(self.points_labels[-1])
            # self.name_labels.pop(-1)
            # self.points_labels.pop(-1)

class InformationFrame(QFrame):
    def __init__(self):
        super(QFrame, self).__init__()

        self.active_player = None
        self.active_snake = None
        self.color = None
        self.scores = []

        self.setFixedSize(240, 400)
        self.setStyleSheet('background-color: #bababa')

        self.define_frame_style()

    def set_active_player_(self, active_player):
        self.active_player = active_player
        for snake in active_player.snakes:
            if snake.is_active == True:
                self.active_snake = snake
        self.update_scores()

    def define_frame_style(self):
        layout = QVBoxLayout()
        font1 = QFont("Arial", 12)
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
            labels[1].setText(self.active_player.user_name)
            labels[3].setText(str(self.active_snake.steps - self.active_snake.played_steps))

class ScoreBoard(QFrame):
    def __init__(self):
        super(ScoreBoard, self).__init__()
        self.define_frame_style()
        self.players = []
        self.timer = TimerFrame()
        self.player_frame = PlayerFrame()
        self.winner = None
        self.active_player = None
        self.information_frame = InformationFrame()
        self.generate_window_layout()

    def generate_window_layout(self):
        self.vbox = QVBoxLayout()
        splitter = QSplitter(Qt.Vertical)
        splitter.setEnabled(False)
        splitter.addWidget(self.player_frame)
        splitter.addWidget(self.timer)
        splitter.addWidget(self.information_frame)
        self.vbox.addWidget(splitter)
        self.setLayout(self.vbox)


    def define_frame_style(self):
        self.setFixedSize(240, 810)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color: #bababa')


    def reset_timer(self):
        self.timer.reset_timer()

    def advance_time(self):
        self.timer.advance_time()

    def init_timer(self):
        self.timer.init_timer()

    def update_players(self, players):
        self.player_frame.update_players(players)

    def set_active_player_on_information_frame(self, active_player):
        self.active_player = active_player
        self.information_frame.set_active_player_(active_player)

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
    def set_winner(self, player):
        self.winner = player

