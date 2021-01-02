import socket
from threading import Thread
from queue import Queue
from Managers.network_manager import NetworkManager

class SendRequest:
    def __init__(self, data, network_flag):
        self.data = data
        self.network_flag = network_flag


class ServerNetworkSender(NetworkManager, Thread):
    _sentinel = object()
    def __init__(self, socket, queue):
        super().__init__(socket)
        self.queue = queue

    def run(self):
        while True:
            message = self.queue.get()

            if message == self._sentinel:
                return
            self.send_message(message.data, message.network_flag)


class ServerNetworkReceiver:
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 50005  # Arbitrary non-privileged port

    def await_client_connections(self, clients_number):
        clients = []
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen(clients_number)
            for i in range(1, clients_number):
                conn, addr = s.accept()
                clients.append(conn)

            return clients
