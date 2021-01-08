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
        random_upper_coeficient_x = table_width / self.part_width
        random_upper_coeficient_y = table_height / self.part_height
        #generate free starting position
        while True:
            elements_stack = []
            generated_x = random.randint(0, random_upper_coeficient_x) * self.part_width
            generated_y = random.randint(0, random_upper_coeficient_y) * self.part_height

            new_part = DrawableComponentBase(generated_x, generated_y, self.part_width, self.part_height)

            is_colliding = self.collision_manager.is_coordinate_colliding(all_snakes, all_food, table_width, table_height, new_part)
            if not is_colliding:
                elements_stack.append(new_part)
                snake_size -= 1
                if self.generate_body_elements_for_snake(table_width, table_height, snake_size,
                                                          all_snakes, all_food, elements_stack):
                    return self.create_snake_from_drawable_components(elements_stack, player)



    def generate_body_elements_for_snake(self, table_width, table_height, elements_to_generate, all_snakes, all_food, elements_stack):

        left_side = (-1, 0)
        right_side = (1, 0)
        top_side = (0, -1)
        down_side = (0, 1)

        sides_to_check = [left_side, right_side, top_side, down_side]

        for side in sides_to_check:
            if self.generate_drawable_component_on_tile(elements_stack, side[0] * self.part_width, side[1] * self.part_height,
                                                        all_snakes, all_food, table_width, table_height):
                elements_to_generate -= 1
                if elements_to_generate == 0:
                    return True
                # search this side of the branch for free spots
                is_found = self.generate_body_elements_for_snake(table_width, table_height, elements_to_generate,
                                                                 all_snakes, all_food, elements_stack)
                # return back if found enough free spots
                if is_found:
                    return True
                else:
                    # since left side is dead end we need to look further
                    elements_stack.pop()
                    elements_to_generate += 1
        return False


    def generate_drawable_component_on_tile(self, elements_stack, x_delta, y_delta, all_snakes, all_food, table_width, table_height):
        previous_part_x = elements_stack[-1].x_coordinate
        previous_part_y = elements_stack[-1].y_coordinate
        # check if down side is free
        part = DrawableComponentBase(previous_part_x + x_delta, previous_part_y + y_delta,
                                     self.part_width, self.part_height)
        is_colliding = self.collision_manager.is_coordinate_colliding(all_snakes, all_food, table_width,
                                                                        table_height, part)

        is_colliding = is_colliding or self.collision_manager.is_colliding_with_marked_locations(part, elements_stack)

        if not is_colliding:
            elements_stack.append(part)
            return True
        return False


    def create_snake_from_drawable_components(self, parts, player):
        snake_parts = []
        for component in parts:
            snake_parts.append(SnakePart(component.x_coordinate, component.y_coordinate, component.height, component.width, SnakePartType.BODY))

        first = snake_parts[0]
        second = snake_parts[1]
        first.part_type = SnakePartType.HEAD

        if first.x_coordinate < second.x_coordinate:
            return Snake(snake_parts, player.user_name, len(snake_parts), 0, SnakeDirection.LEFT, player.color)
        elif first.x_coordinate > second.x_coordinate:
            return Snake(snake_parts, player.user_name, len(snake_parts), 0, SnakeDirection.RIGHT, player.color)
        elif first.y_coordinate < second.y_coordinate:
            return Snake(snake_parts, player.user_name, len(snake_parts), 0, SnakeDirection.UP, player.color)
        else:
            return Snake(snake_parts, player.user_name, len(snake_parts), 0, SnakeDirection.DOWN, player.color)



