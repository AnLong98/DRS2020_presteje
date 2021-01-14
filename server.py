from PyQt5.QtWidgets import QApplication
import sys
from Managers.collision_manager import CollisionManager
from Managers.food_manager import FoodManager
from Managers.movement_manager import MovementManager
from Models.snake import Snake, SnakeDirection
from Models.snake_part import SnakePart, SnakePartType
from Models.user import User
from Network.Server.player_network_connector import PlayerNetworkConnector
from Network.Server.server_network_manager import ServerNetworkManager
from Managers.shift_players_manager import ShiftPlayersManager
from Managers.snake_part_manager import SnakePartManager
from GUI.server_start_window import ServerStartWindow
from game import Game
from Models.player_snakes import PlayerSnakes


class ServerInitializer:
    def __init__(self):
        self.colors = ["#fff200", "#b87bba", "#3494e3", "#fa5700"]
        self.all_snake_parts = PlayerSnakes()

    def __get_player(self, name, player_number, snake_count):
        player_snake_parts = self.all_snake_parts.all_snakes[player_number][:snake_count]
        player_snakes = []
        for snake_part in player_snake_parts:
            if (player_number + 1) % 2 == 0:
                snake = Snake(snake_part, name, 10, 0, SnakeDirection.LEFT, self.colors[player_number])
            else:
                snake = Snake(snake_part, name, 10, 0, SnakeDirection.RIGHT, self.colors[player_number])
            player_snakes.append(snake)
        player = User(player_snakes, 0, name, self.colors[player_number])
        return player


    def get_players(self, number_of_players, player_names, snake_count):
        players = []
        for i in range(number_of_players):
            players.append(self.__get_player(player_names[i], i, snake_count))
        return players

if __name__ == "__main__":
    part_width = 15
    part_height = 15
    # clients_number = 2

    # start window for inputting number of player and snakes per player
    app = QApplication(sys.argv)
    startWindow = ServerStartWindow()
    startWindow.exec()

    clients_number = startWindow.player_count
    snake_count = startWindow.snake_count

    if clients_number == None and snake_count == None:
        print("Server window has been shutdown!")
        sys.exit()

    # init game related things hardcoded for prototype
    print("Server is up and running")

    network_connector = PlayerNetworkConnector()
    network_manager = ServerNetworkManager(clients_number, network_connector)
    player_names = network_manager.get_client_names
    table_width = 960
    table_height = 810

    food = []
    all_snakes = []

    players = ServerInitializer().get_players(clients_number, player_names, snake_count)

    collision_manager = CollisionManager(table_width, table_height)
    food_manager = FoodManager(collision_manager, table_width, table_height)
    movement_manager = MovementManager()
    snake_part_manager = SnakePartManager(part_width, part_height, collision_manager, table_width, table_height)
    shift_players_manager = ShiftPlayersManager()


    # Append all snakes
    for player in players:
        all_snakes.extend(player.snakes)

    for i in range(0, 150):
        food.append(food_manager.generate_food(1, 1, 15, all_snakes, food))

    food.append(
        food_manager.generate_food(1, 1, 15, all_snakes, food, True))  # generate superfood

    # Uncomment for testing
    #for i in range(0, 200):
        #food.append(food_manager.generate_food(1, 1, all_snakes, food, table_width, table_height, 15,True))  # generate superfood

    game = Game(players, food, collision_manager, network_manager, movement_manager, snake_part_manager, food_manager,
                shift_players_manager, table_width, table_height)
    game.run_game()
    print("Game has started")

