from PyQt5.QtGui import QFont, QIntValidator
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QVBoxLayout, QHBoxLayout, QPushButton


class ClientServerParametersWindow(QDialog):
    def __init__(self):
        super(QDialog, self).__init__()
        self.setFixedSize(400,150)
        self.setWindowTitle("Server parameters")
        self.server_ip = None
        self.server_port = None
        self.player_input_field()
        self.server_ip_field.setFocus()


    def player_input_field(self):
        self.server_ip_label = QLabel("IP: ")
        self.server_ip_label.setFont(QFont("Arial", 12))

        self.server_port_label = QLabel("PORT: ")
        self.server_port_label.setFont(QFont("Arial", 12))

        self.error_label = QLabel(self)
        self.error_label.setFont(QFont("Arial", 12))
        self.error_label.setStyleSheet("QLabel { color: red; }")

        self.server_ip_field = QLineEdit()
        self.server_port_field = QLineEdit()
        self.onlyInt = QIntValidator()
        self.server_port_field.setValidator(self.onlyInt)

        self.button = QPushButton('Confirm', self)
        self.button.setFont(QFont("Arial", 12))
        self.button.setMaximumWidth(70)
        self.button.setMaximumHeight(30)

        server_ip_row = QHBoxLayout()
        server_ip_row.addStretch()
        server_ip_row.addWidget(self.server_ip_label)
        server_ip_row.addWidget(self.server_ip_field)
        server_ip_row.addStretch()

        server_port_row = QHBoxLayout()
        server_port_row.addStretch()
        server_port_row.addWidget(self.server_port_label)
        server_port_row.addWidget(self.server_port_field)
        server_port_row.addStretch()

        error_row = QHBoxLayout()
        error_row.addStretch()
        error_row.addWidget(self.error_label)
        error_row.addStretch()

        button_row = QHBoxLayout()
        self.button.clicked.connect(self.confirm_parameters)
        button_row.addWidget(self.button)

        layout = QVBoxLayout()
        layout.addLayout(server_ip_row)
        layout.addLayout(server_port_row)
        layout.addLayout(error_row)
        layout.addLayout(button_row)

        self.setLayout(layout)

    def confirm_parameters(self):
        if len(self.server_ip_field.text()) == 0:
            self.error_label.setText("Server IP can't be an empty string.")
        elif len(self.server_port_field.text()) == 0:
            self.error_label.setText("Server PORT can't be an empty string.")
        elif self.is_good_ipv4(self.server_ip_field.text()) == False:
            self.error_label.setText("Please enter a server IP address in a valid IPv4 format.")
        else:
            self.server_ip = self.server_ip_field.text()
            self.server_port = int(self.server_port_field.text())
            self.close()

    def is_good_ipv4(self, s):
        pieces = s.split('.')
        if len(pieces) != 4: return False
        try:
            return all(0 <= int(p) < 256 for p in pieces)
        except ValueError:
            return False

    def close_window(self):
        self.close()