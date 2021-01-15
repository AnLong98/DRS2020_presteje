import select
import socket
import errno
import time
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
            send_blocked = True
            while send_blocked:
                try:
                     self.send_message(message.data, message.network_flag)
                     break
                except Exception as exc:
                    print("Client sender disconnected %s", exc)
                    self.shutdown()
                    return

