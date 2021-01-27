from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton


class ClientStartWindow(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.setFixedSize(300, 150)
        self.setWindowTitle("Username input")
        self.username = None
        self.player_input_field()
        self.username_field.setFocus()

    def player_input_field(self):
        self.username_label = QLabel("Username: ")
        self.username_label.setFont(QFont("Arial", 12))

        self.error_label = QLabel(self)
        self.error_label.setFont(QFont("Arial", 12))
        self.error_label.setStyleSheet("QLabel { color: red; }")

        self.username_field = QLineEdit()
        self.username_field.setFixedWidth(120)
        self.button = QPushButton('Confirm', self)
        self.button.setFont(QFont("Arial", 12))
        self.button.setMaximumWidth(70)
        self.button.setMaximumHeight(30)

        username_row = QHBoxLayout()
        username_row.addStretch()
        username_row.addWidget(self.username_label)
        username_row.addWidget(self.username_field)
        username_row.addStretch()

        error_row = QHBoxLayout()
        error_row.addStretch()
        error_row.addWidget(self.error_label)
        error_row.addStretch()

        button_row = QHBoxLayout()
        self.button.clicked.connect(self.confirm_username)
        button_row.addStretch()
        button_row.addWidget(self.button)
        button_row.addStretch()

        layout = QVBoxLayout()
        layout.addLayout(username_row)
        layout.addLayout(error_row)
        layout.addLayout(button_row)

        self.setLayout(layout)

    def confirm_username(self):
        if len(self.username_field.text()) == 0:
            self.error_label.setText("Player name can't be an empty string.")
        else:
            self.username = self.username_field.text()
            self.close()

    def close_window(self):
        self.close()
