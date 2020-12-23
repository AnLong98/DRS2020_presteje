class ShiftSnakesManager:
    def shift_snakes(self, active_snake, active_player):
        snake_count = len(active_player.snakes)
        current_snake_index = active_player.snakes.index(active_snake)
        next_snake_index = (current_snake_index + 1) % snake_count
        next_snake = active_player.snakes[next_snake_index]
        return next_snake

    #Pedja 23.12.2020 razmisliti da l;i za ovo treba posebna klasa ili da bacimo u game.py
