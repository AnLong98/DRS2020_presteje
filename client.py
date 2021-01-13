import socket
import sys
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from GUI.game_board import GameBoard
from GUI.score_board import ScoreBoard
from Network.Client.client_network_manager import ClientSocketSender, ClientSocketReceiver

from Managers.drawing_manager import DrawingManager

from Managers.movement_manager import KeyPressed


class MainWindow(QMainWindow):
    def __init__(self, game_board, score_board, client_sender, exit_event, player_username):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Turn Snake - " + player_username)
        self.setFixedSize(1200, 810)

        self.gameboard = game_board
        self.scoreboard = score_board
        self.client_sender = client_sender
        self.sending_active = False
        self.exit_event = exit_event
        self.generate_window_layout()

    def generate_window_layout(self):
        splitter = QSplitter(Qt.Horizontal)
        splitter.setEnabled(False)
        splitter.setStyleSheet("QSplitter::handle {image: none;}")
        splitter.addWidget(self.gameboard)
        splitter.addWidget(self.scoreboard)
        self.setCentralWidget(splitter)

    def keyPressEvent(self, event):
        if not self.sending_active:
            return
        key = event.key()

        send_successfull = True
        if key == Qt.Key_Left:
            send_successfull = self.client_sender.send_pressed_key(KeyPressed.LEFT)

        elif key == Qt.Key_Right:
            send_successfull = self.client_sender.send_pressed_key(KeyPressed.RIGHT)

        elif key == Qt.Key_Up:
            send_successfull = self.client_sender.send_pressed_key(KeyPressed.UP)

        elif key == Qt.Key_Down:
            send_successfull = self.client_sender.send_pressed_key(KeyPressed.DOWN)

        elif key == Qt.Key_Tab:
            send_successfull = self.client_sender.send_pressed_key(KeyPressed.TAB)

        if not send_successfull:
            print("Couldn't send data to server, connection lost!")
            self.exit_event.set()
            self.close()

    def closeEvent(self, event):
        if not self.exit_event.is_set():
            self.exit_event.set() #signal receiver thread to stop receiving and shut down

    def activate_sending(self):
        self.sending_active = True

    def deactivate_sending(self):
        self.sending_active = False

    @property
    def get_gameboard(self):
        return self.gameboard

    @property
    def get_scoreboard(self):
        return self.scoreboard

    @property
    def get_mainwindow_height(self):
        return self.height()

    @property
    def get_mainwindow_width(self):
        return self.width()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game_board = GameBoard()

    print("Type in your username: ")
    username = input()

    #init game related things hardcoded for prototype
    HOST = 'localhost'  # The remote host
    PORT = 50005  # The same port as used by the server

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    socket_sender = ClientSocketSender(client_socket)
    socket_sender.send_game_request(username)
    client_socket.setblocking(False)

    score_board = ScoreBoard()
    exit_event = threading.Event()
    window = MainWindow(game_board, score_board, socket_sender, exit_event, username)
    drawing_manager = DrawingManager(game_board, score_board, window)

    client_receiver = ClientSocketReceiver(client_socket, drawing_manager, exit_event)
    client_receiver.setDaemon(True)
    client_receiver.start()

    window.show()

    app.exec_()
