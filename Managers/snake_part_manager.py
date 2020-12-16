from models import SnakePart, SnakeDirection
from models import SnakePartType


class SnakePartManager:
    def __init__(self, part_width, part_height):
        self.part_width = part_width
        self.part_height = part_height

    def increase_snake(self, active_snake, snake_tail_previous_x, snake_tail_previous_y):
        #TODO: Add snake tail creation here when pictures are added
        new_part = SnakePart(snake_tail_previous_x, snake_tail_previous_y , self.part_width, self.part_height, SnakePartType.BODY)
        active_snake.add_snake_part(new_part)
