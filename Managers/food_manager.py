import random

from Managers.collision_manager import CollisionDetectionResult
from models import Food


class FoodManager:
    def __init__(self,  collision_manager):
        self.collision_manager = collision_manager

    def generate_food(self, points_worth, steps_worth, all_snakes, all_food, table_width, table_height, food_size):
        #TODO : Add generating different food types
        while True:
            generated_x = random.randint(0, table_width - food_size)
            generated_y = random.randint(0, table_height - food_size)

            generated_food = Food(generated_x, generated_y, food_size, food_size, points_worth, steps_worth)
            collision_result, _ = self.collision_manager.check_generated_food_collision(all_snakes,
                                                                                         all_food,
                                                                                         table_width,
                                                                                         table_height,
                                                                                         generated_food)

            if collision_result == CollisionDetectionResult.NO_COLLISION:
                return generated_food


