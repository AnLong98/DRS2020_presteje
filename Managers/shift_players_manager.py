class ShiftPlayersManager:
    def shift_player(self, all_players, active_player):
        player_count = len(all_players)
        current_player_index = all_players.index(active_player)
        next_player_index = (current_player_index + 1) % player_count
        next_player = all_players[next_player_index]
        while not next_player.snakes:
            current_player_index = next_player_index
            next_player_index = (current_player_index + 1) % player_count
            next_player = all_players[next_player_index]
        return next_player

    def shift_snakes(self, active_snake, active_player):
        snake_count = len(active_player.snakes)
        current_snake_index = active_player.snakes.index(active_snake)
        next_snake_index = (current_snake_index + 1) % snake_count
        next_snake = active_player.snakes[next_snake_index]
        return next_snake

