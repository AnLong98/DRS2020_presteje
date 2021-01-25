from PyQt5.QtCore import QObject, QThread, pyqtSignal

from Managers.collision_manager import CollisionManager
from Managers.food_manager import FoodManager
from Managers.movement_manager import MovementManager
from Managers.shift_players_manager import ShiftPlayersManager
from Managers.snake_part_manager import SnakePartManager
from Network.Server.player_network_connector import PlayerNetworkConnector
from Network.Server.server_network_manager import ServerNetworkManager
from game import Game
from server_initializer import ServerInitializer


class GameWorker(QObject):
    def __init__(self, clients_number, snake_number, network_connector, shutdown_signal):
        super().__init__()
        self.clients_number = clients_number
        self.snake_number = snake_number
        self.network_connector = network_connector
        self.food = []
        self.all_snakes = []
        self.shutdown_signal = shutdown_signal
        self.game = None

    def run(self):
        part_width = 15
        part_height = 15
        table_width = 960
        table_height = 810

        #network_connector = PlayerNetworkConnector()
        network_manager = ServerNetworkManager(self.clients_number, self.network_connector, self.shutdown_signal)
        player_names = network_manager.get_client_names

        players = ServerInitializer().get_players(self.clients_number, player_names, self.snake_number)
        collision_manager = CollisionManager(table_width, table_height)
        food_manager = FoodManager(collision_manager, table_width, table_height)
        movement_manager = MovementManager()
        snake_part_manager = SnakePartManager(part_width, part_height, collision_manager, table_width, table_height)
        shift_players_manager = ShiftPlayersManager()

        # Append all snakes
        for player in players:
            self.all_snakes.extend(player.snakes)

        for i in range(0, 30):
            self.food.append(food_manager.generate_food(1, 1, 15, self.all_snakes, self.food))

        self.food.append(
            food_manager.generate_food(1, 1, 15, self.all_snakes, self.food, True))  # generate superfood

        self.game = Game(players, self.food, collision_manager, network_manager, movement_manager, snake_part_manager,
                         food_manager, shift_players_manager, table_width, table_height)
        print("Game has started")
        self.game.run_game()