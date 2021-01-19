import select
import socket

from Network.socket_manager import SocketManager, NetworkPackageFlag

class ConnectorHandle:
    def __init__(self, client_socket, socket_manager, address):
        self.client_socket = client_socket
        self.address = address
        self.socket_manager = socket_manager
        self.ready = False
        self.username = ""

    def set_ready(self):
        self.ready = True

    def set_username(self, name):
        self.username = name

class PlayerNetworkConnector:
    HOST = ""  # Current PC's IP address
    PORT = 0  # Arbitrary non-privileged port
    MAX_CONNECTIONS_LISTEN = 30 #Maximal number of connections for listen socket

    def await_client_connections(self, clients_number):
        socket_handle_dict = {}
        clients_dict = {}
        self.HOST = self.get_pc_ip()
        try:
            listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listen_socket.bind((self.HOST, self.PORT))
            listen_socket.listen(self.MAX_CONNECTIONS_LISTEN)
            ip_port = listen_socket.getsockname()
            print("Server is listening on IP and Port ", ip_port[0], ip_port[1])
        except Exception as ex:
            print("Cloud not listen at server default port. Game aborted! ",ex)
            return None

        connection_attempts = 0
        connected_clients = 0
        clients_ready = 0

        readable_sockets = []
        readable_sockets.append(listen_socket)
        while connection_attempts < self.MAX_CONNECTIONS_LISTEN:
            read, write, error = select.select(readable_sockets, [], [], 2)
            if not read:
                continue

            for socketc in read:
                # new client wants to connect, and number of connected clients is less than requested
                if socketc == listen_socket and connected_clients < clients_number:
                    connector_handle = self.__accept_connection(listen_socket)
                    socket_handle_dict[connector_handle.client_socket] = connector_handle
                    connector_handle.client_socket.setblocking(False)
                    readable_sockets.append(connector_handle.client_socket)
                    connected_clients += 1
                    connection_attempts += 1

                elif socketc != listen_socket: # connected client sent us his username or has disconnected
                    try:
                        if self.__handle_game_request(socketc, socket_handle_dict, clients_dict):
                            clients_ready += 1
                    except Exception:
                        print("Error receiving data from connecting client")
                        if socket_handle_dict[socketc].ready:
                            # If client was ready but disconnected decrease number of ready clients
                            clients_dict.pop(socket_handle_dict[socketc].username)
                            clients_ready -= 1
                        self.__handle_broken_socket(socketc, socket_handle_dict, readable_sockets)
                        print("Ready " + str(clients_ready))
                        connected_clients -= 1

            if clients_ready == clients_number:
                return clients_dict



    def __accept_connection(self, listen_socket):
        client_socket, addr = listen_socket.accept()
        print("Client with addr " + addr[0] + " has connected")

        return ConnectorHandle(client_socket, SocketManager(client_socket), addr)

    def __handle_game_request(self, client_socket, socket_handle_dict, clients_dict):
        msg, flag = socket_handle_dict[client_socket].socket_manager.recv_message()

        if flag != NetworkPackageFlag.USERNAME:
            raise Exception("Protocol error")  # protocol error

        if msg in clients_dict.keys():  # user has chosen an existing user name
            socket_handle_dict[client_socket].socket_manager.send_message(1, NetworkPackageFlag.USERNAME_INVALID)
            return False
        else:
            socket_handle_dict[client_socket].socket_manager.send_message(1, NetworkPackageFlag.USERNAME_VALID)
            socket_handle_dict[client_socket].set_ready()
            socket_handle_dict[client_socket].set_username(msg)
            clients_dict[msg] = client_socket
            print("User " + msg + " has joined the game.")
            return True


    def __handle_broken_socket(self, client_socket, handle_dict, readable_sockets):
        if client_socket in readable_sockets:
            readable_sockets.remove(client_socket)

        if client_socket in handle_dict.keys():
            socket_manager = handle_dict[client_socket].socket_manager
            socket_manager.shutdown()
            handle_dict.pop(client_socket)

        if not readable_sockets:
            #This shouldn't ever happen
            raise Exception("Something is very wrong with listener")

    def get_pc_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.shutdown(socket.SHUT_RDWR)
        s.close()
        return ip

