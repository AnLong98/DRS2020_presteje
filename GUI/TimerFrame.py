from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


class TimerFrame(QFrame):
    def __init__(self):
        super(QFrame, self).__init__()

        self.setFixedSize(240, 100)
        self.setStyleSheet('background-color: #bababa')
        self.elapsed_time = 10  # zakucano vreme za potez.

        self.generate_window_layout()

    def generate_window_layout(self):
        self.vbox = QVBoxLayout()
        self.time = QLabel("Time left: " + str(self.elapsed_time), self)
        self.time.setStyleSheet("color: #e31212")
        self.time.setFont(QFont('Arial', 25))
        self.vbox.addWidget(self.time)
        self.setLayout(self.vbox)

    def init_timer(self):
        self.reset_timer()

    def advance_time(self):
        self.elapsed_time -= 1
        if self.elapsed_time < 0:
            self.elapsed_time = 10
        self.time.setText("Time left: " + str(self.elapsed_time))

    def reset_timer(self):
        self.elapsed_time = 10
        self.time.setText("Time left: " + str(self.elapsed_time))

    def stop_timer(self):
        self.qTimer.stop()

    def start_timer(self):
        self.time.setText("Time left: " + str(self.elapsed_time))