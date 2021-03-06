import random

from Managers.collision_manager import CollisionDetectionResult
from Models.food import Food


class FoodManager:
    def __init__(self,  collision_manager, table_width, table_height):
        self.table_width = table_width
        self.table_height = table_height
        self.collision_manager = collision_manager

    def generate_food(self, points_worth, steps_worth, food_size, all_snakes, all_food, is_super_food=False):
        random_upper_coeficient_x = self.table_width / food_size
        random_upper_coeficient_y = self.table_height / food_size
        while True:
            generated_x = random.randint(0, random_upper_coeficient_x) * food_size
            generated_y = random.randint(0, random_upper_coeficient_y) * food_size


            generated_food = Food(generated_x, generated_y, food_size, food_size, points_worth, steps_worth, is_super_food)
            if not self.collision_manager.is_component_colliding_with_any(all_snakes, all_food, generated_food):
                return generated_food


    def move_all_food(self, all_food, all_snakes):
        for food in all_food:
            if food.is_super_food is not True:
                movements_list = [-3, -2, -1, 1, 2, 3]
                food_x = food.x_coordinate
                food_y = food.y_coordinate
                is_moved = False
                random.shuffle(movements_list)
                move_direction = random.randint(1, 2)

                if move_direction == 1: # move by x coordinate
                    for step in movements_list:
                        food.x_coordinate = food_x + step * 15
                        collision_result, _ = self.collision_manager.check_generated_food_collision(all_snakes, all_food,
                                                                                                    food)
                        if collision_result == CollisionDetectionResult.NO_COLLISION:
                            is_moved = True
                            break

                if move_direction == 2 or not is_moved: # move by y coordinate
                    food.x_coordinate = food_x
                    movements_list.append(0)
                    for step in movements_list:
                        food.y_coordinate = food_y + step * 15
                        collision_result, _ = self.collision_manager.check_generated_food_collision(all_snakes, all_food,
                                                                                                    food)
                        if collision_result == CollisionDetectionResult.NO_COLLISION:
                            break





