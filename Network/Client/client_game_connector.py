import socket
import sys

from GUI.client_start_window import ClientStartWindow
from GUI.client_server_parameters_window import ClientServerParametersWindow
from Network.Client.client_network_manager import ClientSocketSender
from Network.socket_manager import SocketManager, NetworkPackageFlag


class ClientGameConnector:
    def connect(self):

        server_parameters_window = ClientServerParametersWindow()
        server_parameters_window.exec()
        while True:
            HOST = server_parameters_window.server_ip
            PORT = server_parameters_window.server_port

            if HOST is None or PORT is None:
                return None

            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((HOST, PORT))
                socket_sender = ClientSocketSender(client_socket)
                client_recv = SocketManager(client_socket)
                break
            except Exception:
                server_parameters_window.error_label.setText("Invalid IP or PORT, please enter again.")
                server_parameters_window.exec()

        client_window = ClientStartWindow()
        client_window.exec()

        while True:
            username = client_window.username
            if username is None:
                return None

            socket_sender.send_game_request(username)

            response = client_recv.recv_message()

            if response[1] != NetworkPackageFlag.USERNAME_INVALID:
                client_socket.setblocking(False)
                return client_socket, socket_sender, username
            else:
                client_window.error_label.setText("Username already exists. Try again.")
                client_window.exec()

