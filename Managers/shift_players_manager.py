class ShiftPlayersManager:
    def shift_player(self, all_players, active_player):
        player_count = len(all_players)
        current_player_index = all_players.index(active_player)
        next_player_index = (current_player_index + 1) % player_count
        next_player = all_players[next_player_index]
        while next_player.snakes == None:
            current_player_index = next_player_index
            next_player_index = (current_player_index + 1) % player_count
            next_player = all_players[next_player_index]
        return next_player