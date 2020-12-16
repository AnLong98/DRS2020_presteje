from models import SnakePart
from models import SnakePartType


class SnakePartManager:
    def increase_snake(self, active_snake):
        x_coordinate_last = active_snake.snake_parts[(len(active_snake.snake_parts)) - 1].x_coordinate
        y_coordinate_last = active_snake.snake_parts[(len(active_snake.snake_parts)) - 1].y_coordinate
        #direction = active_snake.direction

        new_part = SnakePart(x_coordinate_last, y_coordinate_last, 15, 15, SnakePartType.BODY)
        active_snake.add_snake_part(new_part)
