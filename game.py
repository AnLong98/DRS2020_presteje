import sys
from threading import Lock
from Managers.collision_manager import CollisionManager, CollisionDetectionResult
from models import SnakeDirection
from Managers.movement_manager import  KeyPressed
from Managers.snake_part_manager import SnakePartManager


class Game:
    def __init__(self, players, food, collision_manager, drawing_manager, movement_manager, snake_part_manager, food_manager, shift_players_manager, table_width, table_height):
        self.players = players
        self.food = food
        self.collision_manager = collision_manager
        self.drawing_manager = drawing_manager
        self.movement_manager = movement_manager
        self.snake_part_manager = snake_part_manager
        self.food_manager = food_manager
        self.shift_players_manager = shift_players_manager
        self.table_width = table_width
        self.table_height = table_height
        self.all_snakes = []
        self.active_player = players[0]
        for player in players:
            self.all_snakes += player.snakes
        drawing_manager.draw_food(food)
        drawing_manager.draw_snakes(self.all_snakes)
        self.active_snake = None
        self.drawing_manager.add_player_to_scoreboard(self.players)
        self.alive_players_count = len(self.players)
        self.players_finished_turn = 0
        self.winner = None
        self.game_mutex = Lock()

    def set_active_player(self, active_player):
        self.active_player = active_player

    def set_active_snake(self, active_snake):
        self.active_snake = active_snake
        self.drawing_manager.change_head(active_snake)

    def change_player(self):
        self.game_mutex.acquire()
        self.finish_players_turn()
        next_player = self.shift_players_manager.shift_player(self.players, self.active_player)
        self.set_active_player(next_player)
        next_snake = self.active_player.snakes[0]
        self.set_active_snake(next_snake)
        self.reset_played_steps()
        self.game_mutex.release()

    def change_snake(self):
        next_snake = self.shift_players_manager.shift_snakes(self.active_snake, self.active_player)
        self.set_active_snake(next_snake)

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

    def is_it_over(self):
        if self.active_player.snakes is not None:
            return None
        count = 0
        for player in self.players:
            if player.snakes is not None and player.user_name != self.active_player.user_name:
                count += 1
        if count == 1:
            self.winner = self.shift_players_manager.shift_player(self.players, self.active_player)
            self.drawing_manager.add_winner(self.winner)
            self.drawing_manager.stop_turn_time()
        else:
            return None


    def finish_players_turn(self):
        self.players_finished_turn += 1
        if self.players_finished_turn >= self.alive_players_count:
            self.food_manager.move_all_food(self.all_snakes, self.food, self.table_width, self.table_height)
            self.drawing_manager.draw_food(self.food)
            self.players_finished_turn = 0

    def advance_game(self, key_pressed):
        self.game_mutex.acquire()
        snake_tail_x = self.active_snake.snake_parts[-1].x_coordinate
        snake_tail_y = self.active_snake.snake_parts[-1].y_coordinate
        if self.active_snake.steps != self.active_snake.played_steps:
            self.movement_manager.set_snake_direction(key_pressed, self.active_snake)
            collision_result, object_collided = self.collision_manager.check_moving_snake_collision(self.active_snake, self.all_snakes, self.food, self.table_width, self.table_height)
            if collision_result == CollisionDetectionResult.FOOD_COLLISION:
                self.food.remove(object_collided)
                self.active_snake.increase_steps(object_collided.steps_worth)
                self.active_player.increase_points(object_collided.points_worth)
                self.snake_part_manager.increase_snake(self.active_snake, snake_tail_x, snake_tail_y)
                self.drawing_manager.add_player_to_scoreboard(self.players)

                generated_food = self.food_manager.generate_food(object_collided.points_worth, object_collided.steps_worth,
                                                             self.all_snakes, self.food, self.table_width,
                                                             self.table_height, object_collided.width, object_collided.is_super_food)
                self.food.append(generated_food)


                if object_collided.is_super_food:
                    snake = self.snake_part_manager.generate_snake_for_player(self.active_player, self.table_width,
                                                                      self.table_height, 5, self.all_snakes, self.food)
                    self.active_player.add_snake(snake)
                    self.all_snakes.append(snake)

            elif collision_result == CollisionDetectionResult.FRIENDLY_COLLISION or collision_result == CollisionDetectionResult.AUTO_COLLISION:
                for snake in self.active_player.snakes:
                    self.all_snakes.remove(snake)
                self.alive_players_count -= 1
                self.active_player.snakes = None
                self.is_it_over()
                self.game_mutex.release()
                self.change_player()
                self.game_mutex.acquire()
                self.drawing_manager.reset_turn_time()

            elif collision_result != CollisionDetectionResult.NO_COLLISION:
                self.all_snakes.remove(self.active_snake)
                self.active_player.remove_snake(self.active_snake)
                self.is_it_over()
                self.game_mutex.release()
                self.change_player()
                self.game_mutex.acquire()
                self.drawing_manager.reset_turn_time()

            trapped_snakes = self.collision_manager.get_trapped_enemy_snakes(self.all_snakes, self.table_width, self.table_height, self.active_player)
            for snake in trapped_snakes:
                for player in self.players:
                    if snake.owner_name == player.user_name:
                        self.all_snakes.remove(snake)
                        player.remove_snake(snake)
            self.game_mutex.release()
            self.drawing_manager.draw_food(self.food)
            self.drawing_manager.draw_snakes(self.all_snakes)

        elif self.check_player_steps() is None:  # ako igrac vise nema koraka ni sa jednom zmijom
            self.game_mutex.release()
            self.change_player()
            self.game_mutex.acquire()
            self.drawing_manager.reset_turn_time()
            self.game_mutex.release()

        else:
            self.game_mutex.release()
