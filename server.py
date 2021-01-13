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

    # def __get_player1(self, name):
    #     snakes_player1 = []
    #     snakeParts = [
    #         SnakePart(210, 45, 15, 15, SnakePartType.HEAD)
    #         , SnakePart(195, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(180, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(165, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(150, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(135, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(120, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(105, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(90, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(75, 45, 15, 15, SnakePartType.BODY)
    #
    #     ]
    #     snake = Snake(snakeParts, name, 10, 0, SnakeDirection.RIGHT, "#fff200")
    #     snakes_player1.append(snake)
    #
    #     snakeParts1_1 = [
    #         SnakePart(210, 75, 15, 15, SnakePartType.HEAD)
    #         , SnakePart(195, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(180, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(165, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(150, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(135, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(120, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(105, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(90, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(75, 75, 15, 15, SnakePartType.BODY)
    #     ]
    #     snake1_1 = Snake(snakeParts1_1, name, 10, 0, SnakeDirection.RIGHT, "#fff200")
    #     snakes_player1.append(snake1_1)
    #
    #     player_1 = User(snakes_player1, 0, name, "#fff200")  # CRVENA BOJA IGRACA 1
    #
    #     return player_1
    #
    # def __get_player2(self, name):
    #     # create Player 2 hardcoded
    #     snakes_player2 = []
    #     snakeParts2 = [
    #         SnakePart(705, 75, 15, 15, SnakePartType.HEAD)
    #         , SnakePart(720, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(735, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(750, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(765, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(780, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(795, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(810, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(825, 75, 15, 15, SnakePartType.BODY)
    #         , SnakePart(840, 75, 15, 15, SnakePartType.BODY)
    #     ]
    #     snake2 = Snake(snakeParts2, name, 10, 0, SnakeDirection.LEFT, "#b87bba")
    #     snakes_player2.append(snake2)
    #
    #     snakeParts2_1 = [
    #         SnakePart(705, 45, 15, 15, SnakePartType.HEAD)
    #         , SnakePart(720, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(735, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(750, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(765, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(780, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(795, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(810, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(825, 45, 15, 15, SnakePartType.BODY)
    #         , SnakePart(840, 45, 15, 15, SnakePartType.BODY)
    #     ]
    #     snake2_1 = Snake(snakeParts2_1, name, 10, 0, SnakeDirection.LEFT, "#b87bba")
    #     snakes_player2.append(snake2_1)
    #     player_2 = User(snakes_player2, 0, name, "#b87bba")  # PLAVA BOJA IGRACA 2
    #     return player_2
    #
    # def __get_player3(self, name):
    #     # create Player 3 hardcoded
    #     snakes_player3 = []
    #     snakeParts3 = [
    #         SnakePart(705, 705, 15, 15, SnakePartType.HEAD)
    #         , SnakePart(720, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(735, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(750, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(765, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(780, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(795, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(810, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(825, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(840, 705, 15, 15, SnakePartType.BODY)
    #
    #     ]
    #     snake3 = Snake(snakeParts3, name, 10, 0, SnakeDirection.LEFT, "#3494e3")
    #     snakes_player3.append(snake3)
    #
    #     snakeParts3_1 = [
    #         SnakePart(705, 675, 15, 15, SnakePartType.HEAD)
    #         , SnakePart(720, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(735, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(750, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(765, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(780, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(795, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(810, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(825, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(840, 675, 15, 15, SnakePartType.BODY)
    #     ]
    #     snake3_1 = Snake(snakeParts3_1, name, 10, 0, SnakeDirection.LEFT, "#3494e3")
    #     snakes_player3.append(snake3_1)
    #     player_3 = User(snakes_player3, 0, name, "#3494e3")  # NEKA ROZA BOJA IGRACA 3
    #
    #     return player_3
    #
    # def __get_player4(self, name):
    #     # create Player 4 hardcoded
    #     snakes_player4 = []
    #     snakeParts4 = [
    #         SnakePart(210, 705, 15, 15, SnakePartType.HEAD)
    #         , SnakePart(195, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(180, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(165, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(150, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(135, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(120, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(105, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(90, 705, 15, 15, SnakePartType.BODY)
    #         , SnakePart(75, 705, 15, 15, SnakePartType.BODY)
    #     ]
    #     snake4 = Snake(snakeParts4, name, 10, 0, SnakeDirection.RIGHT, "#fa5700")
    #     snakes_player4.append(snake4)
    #
    #     snakeParts4_1 = [
    #         SnakePart(210, 675, 15, 15, SnakePartType.HEAD)
    #         , SnakePart(195, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(180, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(165, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(150, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(135, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(120, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(105, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(90, 675, 15, 15, SnakePartType.BODY)
    #         , SnakePart(75, 675, 15, 15, SnakePartType.BODY)
    #     ]
    #     snake4_1 = Snake(snakeParts4_1, name, 10, 0, SnakeDirection.RIGHT, "#fa5700")
    #     snakes_player4.append(snake4_1)
    #
    #     player_4 = User(snakes_player4, 0, name, "#fa5700")  # SVETLO PLAVA BOJA IGRACA 4
    #
    #     return player_4

    def get_players(self, number_of_players, player_names, snake_count):
        players = []
        for i in range(number_of_players):
            players.append(self.__get_player(player_names[i], i, snake_count))
        # players.append(self.__get_player1(player_names[0]))
        # if number_of_players == 1:
        #     return players
        # players.append(self.__get_player2(player_names[1]))
        # if number_of_players == 2:
        #     return players
        # players.append(self.__get_player3(player_names[2]))
        # if number_of_players == 3:
        #     return players
        # players.append(self.__get_player4(player_names[3]))
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

    collision_manager = CollisionManager(all_snakes, food, table_width, table_height)
    food_manager = FoodManager(collision_manager)
    movement_manager = MovementManager()
    snake_part_manager = SnakePartManager(part_width, part_height, collision_manager)
    shift_players_manager = ShiftPlayersManager()


    # Append all snakes
    for player in players:
        all_snakes.extend(player.snakes)

    for i in range(0, 30):
        food.append(food_manager.generate_food(1, 1, table_width, table_height, 15))

    food.append(
        food_manager.generate_food(1, 1, table_width, table_height, 15, True))  # generate superfood

    # Uncomment for testing
    #for i in range(0, 200):
        #food.append(food_manager.generate_food(1, 1, all_snakes, food, table_width, table_height, 15,True))  # generate superfood

    game = Game(players, food, collision_manager, network_manager, movement_manager, snake_part_manager, food_manager,
                shift_players_manager, table_width, table_height)
    game.run_game()
    print("Game has started")

