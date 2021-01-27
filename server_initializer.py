from Models.snake import Snake, SnakeDirection
from Models.user import User
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