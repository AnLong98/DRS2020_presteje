import socket
import select
from threading import Thread
from queue import Queue
from Managers.network_manager import SocketManager, NetworkPackageFlag
from Managers.server_network_helpers import SocketInfo, ClientCommand, SendRequest


class ServerSocketSender(SocketManager, Thread):
    _sentinel = object()
    def __init__(self, socket, queue):
        Thread.__init__(self)
        SocketManager.__init__(self, socket)
        self.queue = queue

    def run(self):
        while True:
            message = self.queue.get()

            if message == self._sentinel:
                return
            self.send_message(message.data, message.network_flag)


class ServerNetworkReceiver(Thread):
    _sentinel = object()
    def __init__(self, clients_dict, queue):
        Thread.__init__(self)
        self.queue = queue
        self.clients_dict = clients_dict
        self.sockets = []
        self.socket_to_info_dict = {}
        for username in clients_dict.keys():
            self.sockets.append(clients_dict[username])
            self.socket_to_info_dict[clients_dict[username]] = SocketInfo(SocketManager(clients_dict[username]), username)

    def run(self):
        while True:
            read, write, error = select.select(self.sockets, [], [], 0)
            if not read:
                continue
            for readable in read:
                message, flag = self.socket_to_info_dict[readable].socket_manager.recv_message()
                self.queue.put(ClientCommand(message, self.socket_to_info_dict[readable].username))



class ServerNetworkManager:
    HOST = ''  # Symbolic name meaning all available interfaces
    PORT = 50005  # Arbitrary non-privileged port
    def __init__(self, clients_number):
        self.clients_dict = self.__await_client_connections(clients_number)
        self.client_out_queue_dict = self.__create_client_senders(self.clients_dict)
        self.recv_queue = self.__get_reading_queue()

    @property
    def get_recv_queue(self):
        return self.recv_queue

    @property
    def get_client_names(self):
        return list(self.clients_dict.keys())

    def __await_client_connections(self, clients_number):
        sockets = {}
        clients = []
        clients_dict = {}
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen(clients_number)
            for i in range(0, clients_number):
                sockets[i], addr = s.accept()
                #sockets[i].setblocking(True)
                clients.append(SocketManager(sockets[i]))

            # receive client user names
            for client_socket in clients:
                username, flag = client_socket.recv_message()
                if flag != NetworkPackageFlag.USERNAME:
                    return None # protocol error

                if username in clients_dict:
                    #TODO: Add some code to prevent multiple users form having same username
                    pass
                else:
                    clients_dict[username] = client_socket.socket
                    client_socket.socket.setblocking(False)

            return clients_dict

    def __create_client_senders(self, clients_dict):
        client_queues_dict = {}

        for username in clients_dict.keys():
            client_queues_dict[username] = Queue()
            ServerSocketSender(clients_dict[username], client_queues_dict[username]).start()

        return client_queues_dict

    def __get_reading_queue(self):
        recv_queue = Queue()
        ServerNetworkReceiver(self.clients_dict, recv_queue).start()
        return recv_queue

    def send_state_to_players(self, food, players):
        food_message = SendRequest(food, NetworkPackageFlag.FOOD)
        players_message = SendRequest(players, NetworkPackageFlag.PLAYERS)
        for username in self.client_out_queue_dict.keys():
            self.client_out_queue_dict[username].put(food_message)
            self.client_out_queue_dict[username].put(players_message)

    def notify_start_input(self, username):
        input_message = SendRequest(1, NetworkPackageFlag.START_INPUT)
        if username not in self.client_out_queue_dict:
            return

        self.client_out_queue_dict[username].put(input_message)

    def notify_stop_input(self, username):
        input_message = SendRequest(1, NetworkPackageFlag.STOP_INPUT)
        if username not in self.client_out_queue_dict:
            return

        self.client_out_queue_dict[username].put(input_message)

    def notify_reset_timer(self):
        timer_message = SendRequest(1, NetworkPackageFlag.RESET_TIMER)
        for username in self.client_out_queue_dict.keys():
            self.client_out_queue_dict[username].put(timer_message)

    def notify_start_timer(self):
        timer_message = SendRequest(1, NetworkPackageFlag.START_TIMER)
        for username in self.client_out_queue_dict.keys():
            self.client_out_queue_dict[username].put(timer_message)

    def notify_active_player(self, player):
        player_message = SendRequest(player, NetworkPackageFlag.ACTIVE_PLAYER)
        for username in self.client_out_queue_dict.keys():
            self.client_out_queue_dict[username].put(player_message)

    def notify_active_snake(self, snake):
        snake_message = SendRequest(snake, NetworkPackageFlag.ACTIVE_SNAKE)
        for username in self.client_out_queue_dict.keys():
            self.client_out_queue_dict[username].put(snake_message)




