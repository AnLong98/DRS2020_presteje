import socket

from GUI.client_start_window import ClientStartWindow
from Network.Client.client_network_manager import ClientSocketSender
from Network.socket_manager import SocketManager, NetworkPackageFlag


class ClientGameConnector:
    # TODO: Let client input these parameters
    HOST = socket.gethostbyname(socket.gethostname())  # Current PC's IP address
    PORT = 50005  # The same port as used by the server

    def connect(self):

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.HOST, self.PORT))
        socket_sender = ClientSocketSender(client_socket)
        client_recv = SocketManager(client_socket)
        while True:
            client_window = ClientStartWindow()
            client_window.exec()
            username = client_window.username
            if username is None:
                return None
            socket_sender.send_game_request(username)

            response = client_recv.recv_message()
            print(response[1])

            if response[1] != NetworkPackageFlag.USERNAME_INVALID:
                client_socket.setblocking(False)
                return client_socket, socket_sender, username
