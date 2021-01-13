import pickle
import socket
import struct

class NetworkPackageFlag:
    PLAYERS = 1
    FOOD = 2
    KEY = 3
    USERNAME = 4
    GAME_OVER = 5
    STOP_INPUT = 6
    START_INPUT = 7
    START_TIMER = 8
    RESET_TIMER = 9
    ACTIVE_PLAYER = 10
    ACTIVE_SNAKE = 12
    USERNAME_INVALID = 11


class SocketManager:
    def __init__(self, socketc):
        self.socket = socketc

    def send_message(self, message, package_flag):
        message_bytes = pickle.dumps(message)
        message_size = struct.pack(">I", len(message_bytes))
        flag = struct.pack(">I", package_flag)
        network_message = message_size + flag + message_bytes
        self.socket.sendall(network_message)

    def recv_message(self):
        msglen = self.socket.recv(4)
        message_length = struct.unpack(">I", msglen)[0]
        msgflag = self.socket.recv(4)
        message_flag = struct.unpack(">I", msgflag)[0]
        data = self.__recvall(self.socket, message_length)
        message = pickle.loads(data)
        return message, message_flag

    def __recvall(self, sock, length):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < length:
            packet = sock.recv(length - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def shutdown(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
