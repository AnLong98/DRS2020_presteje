import select
import socket
import threading
from threading import Thread

from Network.Server.server_network_helpers import ClientCommand, SocketInfo
from Network.socket_manager import SocketManager


class ServerNetworkReceiver(Thread):
    def __init__(self, clients_dict, queue, exit_event):
        Thread.__init__(self)
        self.queue = queue
        self.clients_dict = clients_dict
        self.exit_event = exit_event
        self.sockets = []
        self.socket_to_info_dict = {}
        for username in clients_dict.keys():
            self.sockets.append(clients_dict[username])
            self.socket_to_info_dict[clients_dict[username]] = SocketInfo(SocketManager(clients_dict[username]), username)

    def run(self):
        while not self.exit_event.is_set():
            read, write, error = select.select(self.sockets, [], self.sockets, 0)
            for broken_socket in error:
                self.__handle_broken_socket(broken_socket)

            if not read:
                continue
            for readable in read:
                try:
                    message, flag = self.socket_to_info_dict[readable].socket_manager.recv_message()
                except Exception:
                    self.__handle_broken_socket(readable)
                    continue

                self.__enqueue_command(message, self.socket_to_info_dict[readable].username)

    def __enqueue_command(self, message, username):
        try:
            self.queue.put(ClientCommand(message, username))
        except:
            self.exit_event.set()

    def __handle_broken_socket(self, socket):
        # Shutdown and remove socket as it is corrupted
        socket_info = self.socket_to_info_dict[socket]
        self.__enqueue_command(None, socket_info.username)
        socket_info.socket_manager.shutdown()
        self.socket_to_info_dict.pop(socket)
        self.sockets.remove(socket)
        print("Client " + socket_info.username + " has disconnected")
        if not self.sockets:
            print("All client's have disconnected. Shutting receiver down")
            self.exit_event.set()
