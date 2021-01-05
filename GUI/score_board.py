from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *


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
        print("paint player frame called")
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
            self.layout.removeWidget(self.name_labels[-1])
            self.layout.removeWidget(self.points_labels[-1])
            self.name_labels.pop(-1)
            self.points_labels.pop(-1)


class TimerFrame(QFrame):
    def __init__(self):
        super(QFrame, self).__init__()

        self.setFixedSize(240, 100)
        self.setStyleSheet('background-color: #bababa')
        self.elapsedTime = 10 #zakucano vreme za potez.


        self.qTimer = QTimer()  # pocinje tajmer da radi i da odbrojava vreme, svake 1 sec poziva funkciju koja smanjuje elapsed_time
        self.qTimer.setInterval(1000)
        # connect timeout signal to signal handler
        self.qTimer.timeout.connect(self.start_timer)

        self.generate_window_layout()
        self.qTimer.start()

    def generate_window_layout(self):
        self.vbox = QVBoxLayout()
        self.time = QLabel("Time left: " + str(self.elapsedTime), self)
        self.time.setStyleSheet("color: #e31212")
        self.time.setFont(QFont('Arial', 25))
        self.vbox.addWidget(self.time)
        self.setLayout(self.vbox)

    #def paintEvent(self, event):


    def init_timer(self):
        self.reset_timer()

    def reset_timer(self):
        self.elapsedTime = 10
        self.time.setText("Time left: " + str(self.elapsedTime))

    def stop_timer(self):
        self.qTimer.stop()


    def start_timer(self):
        self.time.setText("Time left: " + str(self.elapsedTime))
        self.elapsedTime = self.elapsedTime - 1
        if self.elapsedTime == -1:
            self.reset_timer()


class ButtonFrame(QFrame):
    def __init__(self):
        super(QFrame, self).__init__()

        self.setFixedSize(240, 400)
        self.setStyleSheet('background-color: #bababa')


class ScoreBoard(QFrame):
    def __init__(self):
        super(ScoreBoard, self).__init__()
        self.define_frame_style()
        self.players = []
        self.timer = TimerFrame()
        self.player_frame = PlayerFrame()
        self.generate_window_layout()

    def generate_window_layout(self):
        self.vbox = QVBoxLayout()
        splitter = QSplitter(Qt.Vertical)
        splitter.setEnabled(False)
        splitter.addWidget(self.player_frame)
        splitter.addWidget(self.timer)
        splitter.addWidget(ButtonFrame())
        self.vbox.addWidget(splitter)
        self.setLayout(self.vbox)


    def define_frame_style(self):
        self.setFixedSize(240, 810)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color: #bababa')


    def reset_timer(self):
        self.timer.reset_timer()

    def init_timer(self):
        self.timer.init_timer()

    def update_players(self, players):
        self.player_frame.update_players(players)


    @property
    def get_painter(self):
        return self.painter

    @property
    def get_scoreboard_height(self):
        return self.height()

    @property
    def get_scoreboard_width(self):
        return self.width()

