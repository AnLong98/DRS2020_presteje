import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class FinishWindow(QWidget):
    def __init__(self, winnerName):
        super(QWidget, self).__init__()
        self.setFixedSize(600, 250)
        self.setWindowTitle("Snake Game Results")

        self.layout = QVBoxLayout()

        self.winnerLabel = QLabel("You are the Winner!", self)
        self.winnerNameLabel = QLabel(winnerName, self)

        self.winnerLabel.setFont(QFont('Arial', 26))
        self.winnerNameLabel.setFont(QFont('Arial', 26))

        self.restartButton = QPushButton("Restart", self)
        self.restartButton.setFixedSize(100, 50)
        self.restartButton.setToolTip('Start Game Again')
        self.restartButton.setFont(QFont('Arial', 12))
        self.restartButton.setMaximumWidth(200)

        self.layout.addWidget(self.winnerLabel)
        self.layout.addWidget(self.winnerNameLabel)
        self.layout.addStretch(3)
        self.layout.addWidget(self.restartButton)

        self.layout.setAlignment(self.restartButton, Qt.AlignCenter)
        self.layout.setAlignment(self.winnerLabel, Qt.AlignCenter)
        self.layout.setAlignment(self.winnerNameLabel, Qt.AlignCenter)

        self.layout.addStretch(1)
        self.setLayout(self.layout)


