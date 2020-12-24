from Managers.collision_manager import CollisionDetectionResult
from models import SnakePart, SnakeDirection, Snake, DrawableComponentBase
from models import SnakePartType
import random


class SnakePartManager:
    def __init__(self, part_width, part_height, collision_manager):
        self.part_width = part_width
        self.part_height = part_height
        self.collision_manager = collision_manager

    def increase_snake(self, active_snake, snake_tail_previous_x, snake_tail_previous_y):
        #TODO: Add snake tail creation here when pictures are added
        new_part = SnakePart(snake_tail_previous_x, snake_tail_previous_y, self.part_width, self.part_height, SnakePartType.BODY)
        active_snake.add_snake_part(new_part)


    def generate_snake_for_player(self, player, table_width, table_height, snake_size, all_snakes, all_food):
        movement_stack = []
        spots_found = 0
        parts = []
        snake = Snake(parts, player.user_name, 0, 0, SnakeDirection.RIGHT ,player.color)

        #generate free starting position
        while True:
            generated_x = random.randint(0, table_width) % self.part_width
            generated_y = random.randint(0, table_height) % self.part_height

            new_part = DrawableComponentBase(generated_x, generated_y, self.part_width, self.part_height)

            is_colliding = self.collision_manager.is_coordinate_free(all_snakes, all_food, table_width, table_height, new_part)
            if not is_colliding:
                movement_stack.append(new_part)
                spots_found += 1
                break



        #generate body
        while True:
            previous_part_x = movement_stack[-1].x_coordinate
            previous_part_y = movement_stack[-1].y_coordinate

            #check_left side
            part = DrawableComponentBase(previous_part_x - self.part_width, previous_part_y,
                                        self.part_width, self.part_height )
            is_colliding = self.collision_manager.is_coordinate_free(all_snakes, all_food, table_width,
                                                                     table_height, part)
            if not is_colliding:
                movement_stack.append(new_part)
                spots_found += 1
                break


    def generate_body_element_for_snake(self, table_width, table_height, elements_to_generate, all_snakes, all_food, current_element):
        if elements_to_generate == 0:
            pass
