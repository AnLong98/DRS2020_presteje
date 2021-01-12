import socket
from threading import Thread

from Network.socket_manager import SocketManager


class ServerSocketSender(SocketManager, Thread):
    sentinel = object()
    def __init__(self, socket, queue):
        Thread.__init__(self)
        SocketManager.__init__(self, socket)
        self.queue = queue

    def run(self):
        while True:
            message = self.queue.get()

            if message == self.sentinel:
                return
            try:
                self.send_message(message.data, message.network_flag)
            except Exception as exc:
                print("Client sender disconnected %s", exc)
                return

