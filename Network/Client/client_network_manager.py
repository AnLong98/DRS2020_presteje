import errno
import socket
import threading
from datetime import datetime
from threading import Thread
import select

from GUI.client_finish_window import ClientFinishWindow
from Network.socket_manager import SocketManager, NetworkPackageFlag


class ClientSocketSender(SocketManager):
    def __init__(self, socket):
        super().__init__(socket)


    def send_game_request(self, username):
        try:
            self.send_message( username, NetworkPackageFlag.USERNAME)
            return True
        except Exception as exc:
            self.shutdown()
            return False

    def send_pressed_key(self, key):
        try:
            self.send_message(key, NetworkPackageFlag.KEY)
            return True
        except Exception as exc:
            self.shutdown()
            return False


class ClientSocketReceiver(SocketManager, Thread):
    def __init__(self, socketc, drawing_manager, exit_event):
        Thread.__init__(self)
        SocketManager.__init__(self, socketc)
        self.drawing_manager = drawing_manager
        self.socketc = socketc
        self.exit_event = exit_event


    def run(self):
        readable_sockets = [self.socketc]
        while not self.exit_event.is_set():
            read, write, error = select.select(readable_sockets, [], readable_sockets, 1)

            if error:
                print('Error occured on select')
                self.shutdown()
                self.exit_event.set()
                self.drawing_manager.close_window()
                return

            if not read:
                continue
            try:
                message, flag = self.recv_message()
            except Exception as exc:
                self.shutdown()
                print("Error occurred on receive ", exc)
                self.exit_event.set()
                self.drawing_manager.close_window()
                return

            if not message or not flag:
                self.exit_event.set()
                self.drawing_manager.close_window()
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

            elif flag == NetworkPackageFlag.ACTIVE_PLAYER:
                self.drawing_manager.set_active_player(message)

            elif flag == NetworkPackageFlag.GAME_STATE:
                food = message[0]
                players = message[1]
                print("IMENA USERA -- :")
                for p in players:
                    print(p.user_name)
                active_p = message[2]
                print(f"activ-{active_p.user_name}")
                self.drawing_manager.update_game_state(players, food, active_p)

            elif flag == NetworkPackageFlag.GAME_OVER:
                #game is over, do some game over things here
                self.drawing_manager.stop_input()
                #finish_window = ClientFinishWindow(message[0],message[1])
                #finish_window.exec()
                print("cekaj 30 sekundi i pocinje gejm")
                continue





