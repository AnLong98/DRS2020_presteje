
class SendRequest:
    def __init__(self, data, network_flag):
        self.data = data
        self.network_flag = network_flag

class ClientCommand:
    def __init__(self, key, username):
        self.key = key
        self.username = username

class SocketInfo:
    def __init__(self, socket_manager, socket_user_name):
        self.socket_manager = socket_manager
        self.username = socket_user_name

