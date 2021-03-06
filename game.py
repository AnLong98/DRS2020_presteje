import sys
import time
from threading import Lock, Timer
from Managers.collision_manager import CollisionDetectionResult
from Managers.movement_manager import KeyPressed
from random import randrange


class Game:
    def __init__(self, players, food, collision_manager, network_manager, movement_manager, snake_part_manager,
                 food_manager, shift_players_manager, table_width, table_height, initializer):
        self.players = players
        self.food = food
        self.collision_manager = collision_manager
        self.network_manager = network_manager
        self.movement_manager = movement_manager
        self.snake_part_manager = snake_part_manager
        self.food_manager = food_manager
        self.shift_players_manager = shift_players_manager
        self.table_width = table_width
        self.table_height = table_height
        self.initializer = initializer
        self.setup_game()

    def setup_game(self):
        self.all_snakes = []
        self.active_player = self.players[0]

        for player in self.players:
            self.all_snakes.extend(player.snakes)

        self.active_snake = None
        self.alive_players_count = len(self.players)
        self.players_finished_turn = 0
        self.winner = None
        self.deux_ex_machine = None
        self.timer = Timer(30, self.generate_deux_ex_machine)
        self.timer.start()
        self.game_timer = Timer(10.0, self.change_player)
        self.display_timer = Timer(1.0, self.advance_game_time)
        self.game_mutex = Lock()

    def restart_game(self):
        self.game_timer.cancel()
        self.display_timer.cancel()
        self.players, self.food = self.initializer.get_players_deepcopy()
        pl = []
        for player in self.players: #filtriranje players po userame - uzimam samo zive klijente iz network_manager.get_clients_names - property
            for client in self.network_manager.get_client_names:
                if player.user_name == client:
                    pl.append(player)


        self.network_manager.get_recv_queue.queue.clear()
        self.players = pl
        self.setup_game()
        self.initialize_start_parameters()

    def initialize_start_parameters(self):
        self.set_active_player(self.players[0])
        self.set_active_snake(self.players[0].snakes[0])
        self.game_timer.start()
        self.display_timer.start()
        self.network_manager.send_state_to_players(self.food, self.players, self.active_player)
        self.network_manager.notify_game_restart()
        self.network_manager.notify_start_input(self.active_player.user_name)

    def advance_game_time(self):
        self.network_manager.notify_second_elapsed()
        self.display_timer = Timer(1.0, self.advance_game_time)
        self.display_timer.start()

    def reset_timer(self):
        self.game_timer.cancel()
        self.display_timer.cancel()
        self.game_timer = Timer(10.0, self.change_player)
        self.display_timer = Timer(1.0, self.advance_game_time)
        self.game_timer.start()
        self.display_timer.start()
        self.network_manager.notify_reset_timer()

    def set_active_player(self, active_player):
        self.active_player = active_player

    def set_active_snake(self, active_snake):
        if self.active_snake:
            self.active_snake.set_inactive()
        self.active_snake = active_snake
        self.active_snake.set_active()

    def change_player(self):
        self.game_mutex.acquire()
        self.finish_players_turn()
        self.network_manager.notify_stop_input(self.active_player.user_name)
        next_player = self.shift_players_manager.shift_player(self.players, self.active_player)
        self.set_active_player(next_player)
        self.network_manager.notify_start_input(next_player.user_name)
        next_snake = self.active_player.snakes[0]
        self.set_active_snake(next_snake)
        self.reset_played_steps()
        self.network_manager.send_state_to_players(self.food, self.players, self.active_player)
        self.reset_timer()
        self.game_mutex.release()

    def change_snake(self):
        next_snake = self.shift_players_manager.shift_snakes(self.active_snake, self.active_player)
        self.set_active_snake(next_snake)

    def generate_deux_ex_machine(self):
        self.timer.cancel()
        self.deux_ex_machine = self.food_manager.generate_food(0, 0, 15, self.all_snakes, self.food, True)
        self.food.append(self.deux_ex_machine)

    def activate_deux_ex_machine(self):
        self.deux_ex_machine = None
        self.timer = Timer(10, self.generate_deux_ex_machine)
        self.timer.start()
        if randrange(10) % 2 == 0:
            snake = self.snake_part_manager.generate_snake_for_player(self.active_player, 5,
                                                                      self.all_snakes, self.food)
            self.active_player.add_snake(snake)
            self.all_snakes.append(snake)
        else:
            if self.active_snake.steps - self.active_snake.played_steps >= 2:
                self.active_snake.played_steps = 0
            elif self.active_snake.steps - self.active_snake.played_steps == 1:
                self.active_snake.played_steps = 1
            elif self.active_snake.steps - self.active_snake.played_steps == 0:
                self.active_snake.played_steps = 2
            self.active_snake.steps = 2
            # self.network_manager.send_state_to_players(self.food, self.players, self.active_player)

    def reset_played_steps(self):
        for player in self.players:  # ne moze samo prethodnom
            if player.snakes is not None and player.user_name != self.active_player.user_name:
                for snake in player.snakes:
                    snake.played_steps = 0

    def check_player_steps(self):
        for snake in self.active_player.snakes:
            if snake.steps != snake.played_steps:
                return not None
        return None

    def winner_found_solo(self):
        self.winner = self.shift_players_manager.shift_player(self.players,
                                                              self.active_player)
        self.game_timer.cancel()
        self.display_timer.cancel()
        self.timer.cancel()
        self.deux_ex_machine = None

        self.network_manager.notify_game_over(self.winner, self.players)
        time.sleep(30)


    def winner_found(self):
        self.winner = self.shift_players_manager.shift_player(self.players,
                                                              self.active_player)  # aktivan igrac je i dalje isti, samo sto smo rekli ko je winner
        self.game_timer.cancel()
        self.display_timer.cancel()
        self.timer.cancel()
        self.deux_ex_machine = None
        # ako se ide na play again i odmah je prikaze onda ovde osveziti

        self.network_manager.notify_game_over(self.winner, self.players)
        time.sleep(30)
        self.game_mutex.release()
        self.change_player()
        self.game_mutex.acquire()

    def winner_found_trapping(self):
        self.winner = self.active_player
        self.game_timer.cancel()
        self.display_timer.cancel()
        self.timer.cancel()
        self.deux_ex_machine = None
        self.network_manager.send_state_to_players(self.food, self.players, self.active_player)

        self.network_manager.notify_game_over(self.winner, self.players)
        time.sleep(30)

    def is_it_over_player_alone(self):
        count = 0
        for player in self.players:
            if player.snakes is not None:
                count += 1

        if count == 1:
            self.winner_found_solo()
            return 1
        else:
            return None

    def is_it_game_over(self):
        if self.active_player.snakes is not None:
            return None
        count = 0  # aktivnom igracu su sve zmije None
        for player in self.players:
            if player.snakes is not None:
                if player.user_name != self.active_player.user_name:
                    count += 1

        if count == 1:
            self.winner_found()
            return 1
        else:
            return None

    def is_it_game_over_by_trapping_an_enemy_snake(self):
        for player in self.players:
            if player.snakes is not None and player.user_name != self.active_player.user_name:
                return None

        self.winner_found_trapping()
        return 1

    def finish_players_turn(self):
        self.players_finished_turn += 1
        if self.players_finished_turn >= self.alive_players_count:
            self.food_manager.move_all_food(self.food, self.all_snakes)
            self.players_finished_turn = 0

    def disconnect_player(self, username):
        print("DISKONEKTUJEM JEDNOG KLIJENTA")
        self.game_mutex.acquire()
        for player in self.players:
            if player.user_name == username:
                player.snakes = None
        self.network_manager.shutdown_user(username)
        self.game_mutex.release()
        self.change_player()

    def run_game(self):
        # send initial game parameters to all clients
        self.initialize_start_parameters()

        while True:
            command = self.network_manager.get_recv_queue.get()
            # skip if issuer is not active player
            if command.key is None:
                self.disconnect_player(command.username)
                if self.is_it_over_player_alone() is not None:
                    continue

            if command.username != self.active_player.user_name:
                continue

            self.game_mutex.acquire()
            if command.key == KeyPressed.TAB:
                self.change_snake()
            elif self.active_snake.steps > self.active_snake.played_steps:  # ako igrac ima koraka sa trenutnom zmijom
                snake_tail_x = self.active_snake.snake_parts[-1].x_coordinate
                snake_tail_y = self.active_snake.snake_parts[-1].y_coordinate
                if self.movement_manager.set_snake_direction(command.key, self.active_snake) is not None:
                    self.game_mutex.release()
                    continue

                collision_result, object_collided = self.collision_manager.check_moving_snake_collision(self.active_snake,
                                                                                                        self.all_snakes,
                                                                                                        self.food)
                if collision_result == CollisionDetectionResult.FOOD_COLLISION:
                    self.food.remove(object_collided)
                    if object_collided.is_super_food is not True:
                        self.active_snake.increase_steps(object_collided.steps_worth)
                        self.active_player.increase_points(object_collided.points_worth)
                        self.snake_part_manager.increase_snake(self.active_snake, snake_tail_x, snake_tail_y)

                        generated_food = self.food_manager.generate_food(object_collided.points_worth,
                                                                         object_collided.steps_worth,
                                                                         object_collided.width, self.all_snakes, self.food,
                                                                         object_collided.is_super_food)
                        self.food.append(generated_food)
                    else:
                        self.activate_deux_ex_machine()

                elif collision_result == CollisionDetectionResult.FRIENDLY_COLLISION or\
                        collision_result == CollisionDetectionResult.AUTO_COLLISION:
                    for snake in self.active_player.snakes:
                        self.all_snakes.remove(snake)
                    self.alive_players_count -= 1
                    self.active_player.snakes = None
                    if self.is_it_game_over() is None:
                        self.game_mutex.release()
                        self.change_player()
                        self.game_mutex.acquire()
                        self.reset_timer()
                    else:
                        self.restart_game()
                        continue

                elif collision_result != CollisionDetectionResult.NO_COLLISION:
                    self.all_snakes.remove(self.active_snake)
                    self.active_player.remove_snake(self.active_snake)
                    if self.is_it_game_over() is None:
                        self.game_mutex.release()
                        self.change_player()
                        self.game_mutex.acquire()
                        self.reset_timer()
                    else:
                        self.restart_game()
                        continue

                trapped_snakes = self.collision_manager.get_trapped_enemy_snakes(self.all_snakes, self.active_player)
                if trapped_snakes:
                    for snake in trapped_snakes:
                        for player in self.players:
                            if snake.owner_name == player.user_name:
                                self.all_snakes.remove(snake)
                                player.remove_snake(snake)

                    if self.is_it_game_over_by_trapping_an_enemy_snake() is not None:
                        self.restart_game()
                        continue

                if self.check_player_steps() is None:
                    self.game_mutex.release()
                    self.change_player()
                    self.game_mutex.acquire()
                    self.reset_timer()

            self.network_manager.send_state_to_players(self.food, self.players, self.active_player)
            self.game_mutex.release()


