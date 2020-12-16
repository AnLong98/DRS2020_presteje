from models import SnakePart, SnakeDirection
from models import SnakePartType


class SnakePartManager:
    def increase_snake(self, active_snake):
        snake_len = len(active_snake.snake_parts)
        x_coordinate_last = active_snake.snake_parts[snake_len - 1].x_coordinate
        y_coordinate_last = active_snake.snake_parts[snake_len - 1].y_coordinate

        x_last_part_delta = x_coordinate_last - active_snake.snake_parts[snake_len - 2].x_coordinate
        y_last_part_delta = y_coordinate_last - active_snake.snake_parts[snake_len - 2].y_coordinate

        new_x = x_coordinate_last + x_last_part_delta
        new_y = y_coordinate_last + y_last_part_delta
        new_part = SnakePart(new_x, new_y , 15, 15, SnakePartType.BODY)
        active_snake.add_snake_part(new_part)
