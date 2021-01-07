import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class FinishWindow(QDialog):
    def __init__(self, winnerName):
        super(QDialog, self).__init__()
        self.setFixedSize(600, 250)
        self.setWindowTitle("Snake Game Results")

        self.layout = QVBoxLayout()

        self.winnerLabel = QLabel("You are the Winner!", self)
        self.winnerNameLabel = QLabel(winnerName, self)

        self.winnerLabel.setFont(QFont('Arial', 26))
        self.winnerNameLabel.setFont(QFont('Arial', 26))

        hbox = QHBoxLayout()
        self.restartButton = QPushButton("Restart", self)
        self.restartButton.setFixedSize(100, 50)
        self.restartButton.setToolTip('Start Game Again')
        self.restartButton.setFont(QFont('Arial', 12))
        self.restartButton.setMaximumWidth(200)
        # call the method for restarting the game
        #self.restartButton.clicked.connect(self.GeneratePlayerInputFields)

        self.exitButton = QPushButton("Exit", self)
        self.exitButton.setFixedSize(100, 50)
        self.exitButton.setToolTip('Exit the game')
        self.exitButton.setFont(QFont('Arial', 12))
        self.exitButton.setMaximumWidth(200)
        self.exitButton.clicked.connect(self.ExitGame)

        hbox.addWidget(self.restartButton)
        hbox.addWidget(self.exitButton)

        self.layout.addWidget(self.winnerLabel)
        self.layout.addWidget(self.winnerNameLabel)
        self.layout.addStretch(1)
        self.layout.addLayout(hbox)

        self.layout.setAlignment(self.restartButton, Qt.AlignCenter)
        self.layout.setAlignment(self.winnerLabel, Qt.AlignCenter)
        self.layout.setAlignment(self.winnerNameLabel, Qt.AlignCenter)

        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def ExitGame(self):
        self.close()

