import socket
import threading
from queue import Queue

from Network.Server.server_network_receiver import ServerNetworkReceiver
from Network.Server.server_network_sender import ServerSocketSender
from Network.socket_manager import SocketManager, NetworkPackageFlag
from Network.Server.server_network_helpers import SendRequest


class ServerNetworkManager:
    def __init__(self, clients_number, network_connector, shutdown_signal):
        self.shutdown_signal = shutdown_signal
        self.clients_dict = network_connector.await_client_connections(clients_number)
        self.client_out_queue_dict, self.client_senders_dict  = self.__create_client_senders(self.clients_dict)
        self.receiver_exit_event = threading.Event()
        self.recv_queue, self.receiver = self.__get_reading_queue_and_receiver(self.receiver_exit_event)

    @property
    def get_recv_queue(self):
        return self.recv_queue


    @property
    def get_client_names(self):
        return list(self.clients_dict.keys())

    def __create_client_senders(self, clients_dict):
        client_queues_dict = {}
        client_senders_dict = {}

        for username in clients_dict.keys():
            client_queues_dict[username] = Queue()
            client_senders_dict[username] = ServerSocketSender(clients_dict[username], client_queues_dict[username])
            client_senders_dict[username].setDaemon(True)
            client_senders_dict[username].start()


        return client_queues_dict, client_senders_dict

    def __get_reading_queue_and_receiver(self, receiver_exit_event):
        recv_queue = Queue()
        receiver = ServerNetworkReceiver(self.clients_dict, recv_queue, receiver_exit_event, self.shutdown_signal)
        receiver.setDaemon(True)
        receiver.start()
        return recv_queue, receiver

    def send_food_to_players(self, food):
        food_message = SendRequest(food, NetworkPackageFlag.FOOD)
        for username in self.client_out_queue_dict.keys():
            self.client_out_queue_dict[username].put(food_message)

    def send_players_to_players(self, players):
        message = SendRequest(players, NetworkPackageFlag.PLAYERS)
        for username in self.client_out_queue_dict.keys():
            self.client_out_queue_dict[username].put(message)

    def send_state_to_players(self, food, players, active_player):
        message = SendRequest([food, players, active_player], NetworkPackageFlag.GAME_STATE)
        for username in self.client_out_queue_dict.keys():
            self.client_out_queue_dict[username].put(message)

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

    def notify_game_over(self, winner, all_players):
        winner_and_players = []
        winner_and_players.append([winner])
        winner_and_players.append(all_players)  # [winner, [all_players]]
        player_message = SendRequest(winner_and_players, NetworkPackageFlag.GAME_OVER)
        for username in self.client_out_queue_dict.keys():
            self.client_out_queue_dict[username].put(player_message)

    def notify_game_restart(self):
        player_message = SendRequest(1, NetworkPackageFlag.GAME_RESTART)
        for username in self.client_out_queue_dict.keys():
            self.client_out_queue_dict[username].put(player_message)

    def shutdown_user(self, username):
        if username in self.client_senders_dict.keys() and username in self.client_out_queue_dict.keys():
            sentinel = self.client_senders_dict[username].sentinel
            self.client_out_queue_dict[username].put(sentinel)
            self.client_senders_dict.pop(username)
            self.client_out_queue_dict.pop(username)
            self.clients_dict.pop(username)

    def shutdown_all_user_connections(self):
        if not self.receiver_exit_event.is_set():
            self.receiver_exit_event.set() #Shutdown receiver
        for username in self.client_out_queue_dict.keys():
            self.client_out_queue_dict[username].put(self.client_senders_dict[username].sentinel)
            self.client_senders_dict.pop(username)
            self.client_out_queue_dict.pop(username)
            self.clients_dict.pop(username)



