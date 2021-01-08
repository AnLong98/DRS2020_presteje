from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class StartWindow(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.setFixedSize(800, 800)
        self.setWindowTitle("Snake Game Settings")

        self.gameStarted = False

        self.playerInputFields = []
        self.playerNames = []

        playerNumberComponent = self.PlayerCountCompontent()
        snakeNumberComponent = self.SnakeCountComponent()

        self.numberConformationButton = QPushButton('Confirm Selection', self)
        self.numberConformationButton.setToolTip('Continue with current Selection')
        self.numberConformationButton.setFont(QFont('Arial', 12))
        self.numberConformationButton.setMaximumHeight(200)
        self.numberConformationButton.setMaximumWidth(250)
        self.numberConformationButton.clicked.connect(self.GeneratePlayerInputFields)

        self.errorLabel = QLabel(self)
        self.errorLabel.setFont(QFont('Arial', 12))


        self.gridLayout = QVBoxLayout()
        self.gridLayout.addStretch(1)

        self.label = QLabel("", self)
        self.mainWindowPicture = QPixmap("snake_game_1533210447.jpg")
        self.label.setPixmap(self.mainWindowPicture)

        self.gridLayout.addWidget(self.label)
        self.gridLayout.setAlignment(self.label, Qt.AlignHCenter)
        self.gridLayout.addLayout(playerNumberComponent)
        self.gridLayout.setAlignment(playerNumberComponent, Qt.AlignHCenter)
        self.gridLayout.addLayout(snakeNumberComponent)
        self.gridLayout.setAlignment(snakeNumberComponent, Qt.AlignHCenter)
        self.gridLayout.addStretch(1)
        self.gridLayout.addWidget(self.numberConformationButton)
        self.gridLayout.setAlignment(self.numberConformationButton, Qt.AlignHCenter)
        self.gridLayout.addWidget(self.errorLabel)
        self.gridLayout.setAlignment(self.errorLabel, Qt.AlignHCenter)
        self.gridLayout.addStretch(4)
        self.setLayout(self.gridLayout)

    # adds player input fields to the input
    def GeneratePlayerInputFields(self):
        for i in range(self.playerCount.value()):
            self.gridLayout.addStretch(1)
            playerInputComponent = self.PlayerInputComponent(i)
            self.gridLayout.addLayout(playerInputComponent)
            self.gridLayout.setAlignment(playerInputComponent, Qt.AlignHCenter)
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
        self.gridLayout.setAlignment(self.startGameButton, Qt.AlignHCenter)
        self.gridLayout.addStretch()

    # used for player number input
    def PlayerCountCompontent(self):
        self.playerCountLabel = QLabel("Select Number of Players: ", self)
        self.playerCountLabel.setFont(QFont('Arial', 12))
        self.playerCount = QSpinBox(self)
        self.playerCount.setGeometry(100, 100, 100, 40)
        self.playerCount.setMinimum(2)
        self.playerCount.setMaximum(4)
        self.playerCount.setMaximumWidth(250)
        self.playerCount.setMaximumHeight(200)
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
        self.snakeCount.setMaximumHeight(200)
        self.snakeCount.setMaximumWidth(250)
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
        playerNameInputBox.setMaximumHeight(200)
        playerNameInputBox.setMaximumWidth(250)
        playerNameInputBox.setFont(QFont('Arial', 12))
        self.playerInputFields.append(playerNameInputBox)

        hbox = QHBoxLayout()
        hbox.addWidget(playerNameLabel)
        hbox.setAlignment(playerNameLabel, Qt.AlignRight)
        hbox.addWidget(playerNameInputBox)
        hbox.setAlignment(playerNameInputBox, Qt.AlignLeft)
        return hbox

    def InitiateSnakeGame(self):
        uniqueNames = [_input.text() for _input in self.playerInputFields]
        if '' in uniqueNames:
            self.errorLabel.setText("Player Name Can't be left Empty")
        elif len(uniqueNames) != len(set(uniqueNames)):
            self.errorLabel.setText("Player Names Must be Unique")
        else:
            self.errorLabel.setText("")
            self.playerNames = [label.text() for label in self.playerInputFields]
            self.gameStarted = True
            self.close()
