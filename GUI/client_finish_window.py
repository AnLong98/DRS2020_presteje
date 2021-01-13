from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QLabel, QHBoxLayout, QVBoxLayout, QPushButton


class ClientFinishWindow(QDialog):
    def __init__(self, winner, all_players):
        super(QDialog, self).__init__()
        self.setFixedSize(350, 400)
        self.setWindowTitle("Snake Game Results")

        self.winner = winner
        self.all_players = all_players
        self.number_of_players = len(self.all_players)

        self.init_fields()

    def init_fields(self):
        winner_label = QLabel(f"The winner is: {self.winner} ", self)
        winner_label.setFont(QFont("Arial", 25))

        winner_row = QHBoxLayout()
        winner_row.addStretch()
        winner_row.addWidget(winner_label)
        winner_row.addStretch()

        score_row = QHBoxLayout()
        score_row.addStretch()
        score_row_column = QVBoxLayout()
        score_label = QLabel("The score board:")
        score_label.setFont(QFont("Arial", 25))
        score_row_column.addWidget(score_label)
        for i in range(self.number_of_players):
            word = QLabel(f"{i + 1}. {self.all_players[i]}", self)
            word.setFont(QFont("Arial", 15))
            score_row_column.addWidget(word)
        score_row.addLayout(score_row_column)
        score_row.addStretch()

        space_row = QHBoxLayout()
        space_row.addWidget(QLabel("", self))

        button_row = QHBoxLayout()
        button_row.addStretch()
        button_restart = QPushButton("Restart", self)
        button_restart.setMaximumWidth(100)
        button_restart.setMaximumHeight(50)
        button_restart.clicked.connect(self.restart_button)
        button_row.addWidget(button_restart)
        button_row.addStretch()

        button_exit = QPushButton("Exit", self)
        button_exit.setMaximumWidth(100)
        button_exit.setMaximumHeight(50)
        button_exit.clicked.connect(self.exit_button)
        button_row.addWidget(button_exit)
        button_row.addStretch()

        layout = QVBoxLayout()
        layout.addLayout(winner_row)
        layout.addLayout(score_row)
        layout.addLayout(space_row)
        layout.addLayout(button_row)
        self.setLayout(layout)

    #TO-DO: Implement restart and exit game logic
    def restart_button(self):
        self.close()

    def exit_button(self):
        self.close()
