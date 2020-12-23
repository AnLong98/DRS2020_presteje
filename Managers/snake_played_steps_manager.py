class SnakePlayedStepsManager:
    def reset_played_steps(self, active_player, all_players):  # nece biti dobro ako uve samo prethodnom resetujemo
        for player in all_players:
            if player.snakes is not None and player.user_name != active_player.user_name:
                for snake in player.snakes:
                    snake.played_steps = 0


#Pedja 23.12.2020 Da li i ovo moze u game?