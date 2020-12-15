from Managers.collision_manager import CollisionManager, CollisionDetectionResult
from models import SnakeDirection
from GUI.game_board import KeyPressed

class Game:
    def __init__(self, players, food, collision_manager, drawing_manager, movement_manager, input_manager, table_width, table_height):
        self.players = players
        self.food = food
        self.collision_manager = collision_manager
        self.drawing_manager = drawing_manager
        self.movement_manager = movement_manager
        self.input_manager = input_manager
        self.table_width = table_width
        self.table_height = table_height
        self.all_snakes = []
        for player in players:
            self.all_snakes += player.snakes

    def set_active_player(self, active_player):
        self.active_player = active_player

    def set_active_snake(self, active_snake):
        self.active_snake = active_snake

    def start_game(self, key_pressed):
        self.movement_manager.set_snake_direction(key_pressed, self.active_snake)
        collision_result, object_collided = self.collision_manager.check_moving_snake_collision(self.active_snake, self.all_snakes, self.food, self.table_width, self.table_height)
        if collision_result == CollisionDetectionResult.FOOD_COLLISION:
            self.drawing_manager.erase_food(object_collided)
            self.food.remove(object_collided)
            self.active_snake.incerase_steps(object_collided.steps_worth)
        else:
            self.drawing_manager.erase_snake(self.active_snake)
            self.all_snakes.remove(self.active_snake)
            print("Collision!, game over!")


