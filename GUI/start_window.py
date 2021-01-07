import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class StartWindow(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.setFixedSize(800, 600)
        self.setWindowTitle("Snake Game Settings")

        self.gameStarted = False

        self.playerInputFields = []
        self.playerNames = []

        playerNumberComponent = self.PlayerCountCompontent()
        snakeNumberComponent = self.SnakeCountComponent()

        self.numberConformationButton = QPushButton('Confirm Selection', self)
        self.numberConformationButton.setToolTip('Continue with current Selection')
        self.numberConformationButton.setFont(QFont('Arial', 12))
        self.numberConformationButton.clicked.connect(self.GeneratePlayerInputFields)

        self.errorLabel = QLabel(self)
        self.errorLabel.setFont(QFont('Arial', 12))
        self.gridLayout = QVBoxLayout()
        self.gridLayout.addStretch(1)
        self.gridLayout.addLayout(playerNumberComponent)
        self.gridLayout.addLayout(snakeNumberComponent)
        self.gridLayout.addStretch()
        self.gridLayout.addWidget(self.numberConformationButton)
        self.gridLayout.addWidget(self.errorLabel)
        self.gridLayout.addStretch(5)
        self.setLayout(self.gridLayout)

    # adds player input fields to the input
    def GeneratePlayerInputFields(self):
        for i in range(self.playerCount.value()):
            self.gridLayout.addStretch(1)
            self.gridLayout.addLayout(self.PlayerInputComponent(i))
            self.gridLayout.addStretch(1)
        self.numberConformationButton.disconnect()
        self.numberConformationButton.setEnabled(False)
        self.playerCount.setEnabled(False)
        self.snakeCount.setEnabled(False)

        self.startGameButton = QPushButton('Start Game', self)
        self.startGameButton.setToolTip('Start the game with current Selection')
        self.startGameButton.setFont(QFont('Arial', 12))
        self.startGameButton.clicked.connect(self.InitiateSnakeGame)
        self.gridLayout.addWidget(self.startGameButton)
        self.gridLayout.addStretch()

    # used for player number input
    def PlayerCountCompontent(self):
        self.playerCountLabel = QLabel("Select Number of Players: ", self)
        self.playerCountLabel.setFont(QFont('Arial', 12))
        self.playerCount = QSpinBox(self)
        self.playerCount.setGeometry(100, 100, 100, 40)
        self.playerCount.setMinimum(2)
        self.playerCount.setMaximum(4)
        self.playerCount.setFont(QFont('Arial', 12))

        hbox = QVBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.playerCountLabel)
        hbox.addWidget(self.playerCount)
        return hbox

    # used for snake number input
    def SnakeCountComponent(self):
        self.snakeCountLabel = QLabel("Select Number of Snakes: ", self)
        self.snakeCountLabel.setFont(QFont('Arial', 12))
        self.snakeCount = QSpinBox(self)
        self.snakeCount.setGeometry(100, 100, 100, 40)
        self.snakeCount.setMinimum(1)
        self.snakeCount.setMaximum(4)
        self.snakeCount.setFont(QFont('Arial', 12))

        hbox = QVBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.snakeCountLabel)
        hbox.addWidget(self.snakeCount)
        return hbox

    # creates player input fields
    def PlayerInputComponent(self, playerNumber):
        playerNameLabel = QLabel(f"Player {playerNumber} Name: ", self)
        playerNameLabel.setFont(QFont('Arial', 12))
        playerNameInputBox = QLineEdit(self)
        playerNameInputBox.setFont(QFont('Arial', 12))
        self.playerInputFields.append(playerNameInputBox)

        hbox = QHBoxLayout()
        hbox.addWidget(playerNameLabel)
        hbox.addWidget(playerNameInputBox)
        return hbox

    def InitiateSnakeGame(self):
        uniqueNames = [_input.text() for _input in self.playerInputFields]
        if "" in uniqueNames:
            self.errorLabel.setText("Player Name Can't be left Empty")
        elif len(uniqueNames) != len(set(uniqueNames)):
            self.errorLabel.setText("Player Names Must be Unique")
        else:
            self.errorLabel.setText("")
            self.playerNames = [label.text() for label in self.playerInputFields]
            self.gameStarted = True
            self.close()