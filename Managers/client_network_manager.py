from threading import Thread
import socket
import select
from Managers.network_manager import SocketManager, NetworkPackageFlag


class ClientSocketSender(SocketManager):
    def __init__(self, socket):
        super().__init__(socket)


    def send_game_request(self, username):
        self.send_message( username, NetworkPackageFlag.USERNAME)

    def send_pressed_key(self, key):
        self.send_message(key, NetworkPackageFlag.KEY)


class ClientSocketReceiver(SocketManager, Thread):
    def __init__(self, socketc, drawing_manager):
        Thread.__init__(self)
        SocketManager.__init__(self, socketc)
        self.drawing_manager = drawing_manager
        self.socketc = socketc


    def run(self):
        readable_sockets = [self.socketc]
        while True:
            read, write, error = select.select(readable_sockets, [], [], 0)
            if not read:
                continue

            message, flag = self.recv_message()
            if not message or not flag:
                # handle disconnect
                return
            if flag == NetworkPackageFlag.FOOD:
                self.drawing_manager.draw_food(message)

            elif flag == NetworkPackageFlag.PLAYERS:
                self.drawing_manager.update_players(message)

            elif flag == NetworkPackageFlag.STOP_INPUT:
                self.drawing_manager.stop_input()

            elif flag == NetworkPackageFlag.START_INPUT:
                self.drawing_manager.start_input()

            elif flag == NetworkPackageFlag.START_TIMER:
                self.drawing_manager.start_timer()

            elif flag == NetworkPackageFlag.RESET_TIMER:
                self.drawing_manager.reset_turn_time()

            elif flag == NetworkPackageFlag.ACTIVE_SNAKE:
                self.drawing_manager.change_head(message)

            elif flag == NetworkPackageFlag.ACTIVE_PLAYER:
                self.drawing_manager.set_active_player(message)

            elif flag == NetworkPackageFlag.GAME_OVER:
                #game is over, do some game over things here
                return





