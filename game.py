import sys

from Managers.collision_manager import CollisionManager, CollisionDetectionResult
from models import SnakeDirection
from Managers.movement_manager import  KeyPressed
from Managers.snake_part_manager import SnakePartManager


class Game:
    def __init__(self, players, food, collision_manager, drawing_manager, movement_manager, snake_part_manager, table_width, table_height):
        self.players = players
        self.food = food
        self.collision_manager = collision_manager
        self.drawing_manager = drawing_manager
        self.movement_manager = movement_manager
        self.snake_part_manager = snake_part_manager
        self.table_width = table_width
        self.table_height = table_height
        self.all_snakes = []
        self.active_player = players[0]
        for player in players:
            self.all_snakes += player.snakes
        drawing_manager.draw_food(food)
        drawing_manager.draw_snakes(self.all_snakes)
        self.active_snake = None


    def set_active_player(self, active_player):
        self.active_player = active_player

    def set_active_snake(self, active_snake):
        self.active_snake = active_snake

    def advance_game(self, key_pressed):
        snake_tail_x = self.active_snake.snake_parts[-1].x_coordinate
        snake_tail_y = self.active_snake.snake_parts[-1].y_coordinate
        self.movement_manager.set_snake_direction(key_pressed, self.active_snake)
        collision_result, object_collided = self.collision_manager.check_moving_snake_collision(self.active_snake, self.all_snakes, self.food, self.table_width, self.table_height)
        if collision_result == CollisionDetectionResult.FOOD_COLLISION:
            self.food.remove(object_collided)
            self.active_snake.incerase_steps(object_collided.steps_worth)
            self.snake_part_manager.increase_snake(self.active_snake, snake_tail_x, snake_tail_y)
            self.drawing_manager.draw_food(self.food)
        elif collision_result != CollisionDetectionResult.NO_COLLISION:
            self.all_snakes.remove(self.active_snake)
            self.active_player.remove_snake(self.active_snake)
            print("Collision!, game over!")
        self.drawing_manager.draw_snakes(self.all_snakes)

