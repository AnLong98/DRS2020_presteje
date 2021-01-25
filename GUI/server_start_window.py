from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Network.Server.player_network_connector import PlayerNetworkConnector
from game_worker import GameWorker


class HostingWindow(QWidget):
    def __init__(self):
        super(QWidget, self).__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle("Snake Game Hosting Information")

        self.host_address = None
        self.host_port = None
        self.define_widget_style()

    def define_widget_style(self):
        self.host_address_label = QLabel("Hosted on Address:")
        self.host_address_label.setFont(QFont("Arial", 10))
        self.host_port_label = QLabel("Hosted on Port:")
        self.host_port_label.setFont(QFont("Arial", 10))

        self.host_address_field = QLineEdit()
        self.host_address_field.setFont(QFont("Arial", 10))
        self.host_address_field.setReadOnly(True)
        self.host_port_field = QLineEdit()
        self.host_port_field.setFont(QFont("Arial", 10))
        self.host_port_field.setReadOnly(True)

        vbox = QVBoxLayout()
        vbox.addStretch()
        vbox.addWidget(self.host_address_label)
        self.host_address_label.setAlignment(Qt.AlignHCenter)
        vbox.addWidget(self.host_address_field)
        vbox.addStretch()
        vbox.addWidget(self.host_port_label)
        self.host_port_label.setAlignment(Qt.AlignHCenter)
        vbox.addWidget(self.host_port_field)
        vbox.addStretch()
        self.setLayout(vbox)

    def update_qlineedit_values(self):
        self.host_address_field.setText(self.host_address)
        self.host_port_field.setText(self.host_port)


class InputWindow(QWidget):
    def __init__(self, hosting_signal):
        super(QWidget, self).__init__()
        self.setFixedSize(400, 300)
        self.setWindowTitle("Snake Game Settings")

        self.player_count = None
        self.snake_count = None

        self.hosting_signal = hosting_signal
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
        self.hosting_signal.emit()


class ServerStackedWidgets(QWidget):
    def __init__(self, input_signal, hosting_signal, shutdown_signal):
        super(QWidget, self).__init__()
        self.thread = QThread()
        self.clients_number = 0
        self.snake_count = 0
        self.worker = None
        self.setMinimumSize(400, 300)
        self.setWindowTitle("Hosting Information")

        self.shutdown_signal = shutdown_signal.shutdown_signal
        self.shutdown_signal.connect(self.close_server_window)

        self.server_input_signal = input_signal.input_widget_signal
        self.server_input_signal.connect(self.display_server_input_widget)

        self.server_hosting_signal = hosting_signal.hosting_widget_signal
        self.server_hosting_signal.connect(self.display_server_hosting_widget)

        self.stack = QStackedWidget(self)
        self.server_stack = InputWindow(self.server_hosting_signal)
        self.hosting_stack = HostingWindow()

        self.define_stacked_widget_style()
        self.stack.setCurrentIndex(0)

    def define_stacked_widget_style(self):
        self.stack.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.stack.addWidget(self.server_stack)
        self.stack.addWidget(self.hosting_stack)

        hbox = QVBoxLayout()
        hbox.addWidget(self.stack)
        self.setLayout(hbox)
        self.layout().setContentsMargins(0, 0, 0, 0)

    def display_server_input_widget(self):
        self.stack.setCurrentIndex(0)

    def display_server_hosting_widget(self):
        self.stack.setCurrentIndex(1)
        network_connector = PlayerNetworkConnector()
        self.hosting_stack.host_port_field.setText(str(1))
        self.hosting_stack.host_address_field.setText(str(1))
        self.worker = GameWorker(self.server_stack.player_count,
                                 self.server_stack.snake_count, network_connector,
                                 self.shutdown_signal)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def close_server_window(self):
        self.close()
