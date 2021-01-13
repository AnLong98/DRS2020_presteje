from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

class ServerStartWindow(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle("Snake Game Settings")

        self.player_count = None
        self.snake_count = None

        self.setLayout(self.create_window_layuot())

    def create_window_layuot(self):
        player_spinbox_component = self.player_spinbox_component()
        snake_spinbox_component = self.snake_spinbox_component()

        self.conformation_button = QPushButton('Confirm Selection', self)
        self.conformation_button.setToolTip('Confirm player and snake count input')
        self.conformation_button.setFont(QFont('Arial', 12))
        self.conformation_button.setMaximumHeight(200)
        self.conformation_button.setMaximumWidth(250)
        self.conformation_button.clicked.connect(self.extract_input_values)

        self.grid_layout = QVBoxLayout()
        self.grid_layout.addStretch(1)
        self.grid_layout.addLayout(player_spinbox_component)
        self.grid_layout.setAlignment(player_spinbox_component, Qt.AlignHCenter)
        self.grid_layout.addStretch(1)

        self.grid_layout.addLayout(snake_spinbox_component)
        self.grid_layout.setAlignment(snake_spinbox_component, Qt.AlignHCenter)
        self.grid_layout.addStretch(1)

        self.grid_layout.addWidget(self.conformation_button)
        self.grid_layout.setAlignment(self.conformation_button, Qt.AlignHCenter)
        self.grid_layout.addStretch(1)
        return self.grid_layout

    def player_spinbox_component(self):
        self.player_spinbox_label = QLabel("Select Number of Players: ", self)
        self.player_spinbox_label.setFont(QFont('Arial', 12))
        self.player_spinbox = QSpinBox(self)
        self.player_spinbox.setGeometry(100, 100, 100, 40)
        self.player_spinbox.setMinimum(2)
        self.player_spinbox.setMaximum(4)
        self.player_spinbox.setMaximumWidth(250)
        self.player_spinbox.setMaximumHeight(200)
        self.player_spinbox.setFont(QFont('Arial', 12))

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.player_spinbox_label)
        vbox.addWidget(self.player_spinbox)
        return vbox

    def snake_spinbox_component(self):
        self.snake_spinbox_label = QLabel("Select Number of Snakes: ", self)
        self.snake_spinbox_label.setFont(QFont('Arial', 12))
        self.snake_spinbox = QSpinBox(self)
        self.snake_spinbox.setGeometry(100, 100, 100, 40)
        self.snake_spinbox.setMaximumHeight(200)
        self.snake_spinbox.setMaximumWidth(250)
        self.snake_spinbox.setMinimum(1)
        self.snake_spinbox.setMaximum(4)
        self.snake_spinbox.setFont(QFont('Arial', 12))

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.snake_spinbox_label)
        vbox.addWidget(self.snake_spinbox)
        return vbox

    def extract_input_values(self):
        self.player_count = self.player_spinbox.value()
        self.snake_count = self.snake_spinbox.value()
        self.close()