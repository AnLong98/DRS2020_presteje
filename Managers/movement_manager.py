from Models.snake import SnakeDirection
from Models.snake_part import SnakePartType


class KeyPressed:
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    TAB = 5


class MovementManager:
    def set_snake_direction(self, key_pressed, active_snake):

        if key_pressed == KeyPressed.LEFT:
            if active_snake.direction != SnakeDirection.RIGHT:
                active_snake.direction = SnakeDirection.LEFT
                self.move_active_snake(active_snake)
                active_snake.increase_played_steps()

        elif key_pressed == KeyPressed.RIGHT:
            if active_snake.direction != SnakeDirection.LEFT:
                active_snake.direction = SnakeDirection.RIGHT
                self.move_active_snake(active_snake)
                active_snake.increase_played_steps()

        elif key_pressed == KeyPressed.UP:
            if active_snake.direction != SnakeDirection.DOWN:
                active_snake.direction = SnakeDirection.UP
                self.move_active_snake(active_snake)
                active_snake.increase_played_steps()

        elif key_pressed == KeyPressed.DOWN:
            if active_snake.direction != SnakeDirection.UP:
                active_snake.direction = SnakeDirection.DOWN
                self.move_active_snake(active_snake)
                active_snake.increase_played_steps()


    def move_active_snake(self, active_snake):
        snake_head_x = active_snake.snake_parts[0].x_coordinate
        snake_head_y = active_snake.snake_parts[0].y_coordinate
        movement_size = 15

        if active_snake.direction == SnakeDirection.LEFT:
            part_previous_x = snake_head_x
            part_previous_y = snake_head_y
            active_snake.snake_parts[0].x_coordinate = active_snake.snake_parts[0].x_coordinate - movement_size

            for x in active_snake.snake_parts:
                if x.part_type == SnakePartType.HEAD:
                    continue
                part_temp_x = x.x_coordinate
                part_temp_y = x.y_coordinate
                x.x_coordinate, x.y_coordinate = part_previous_x, part_previous_y
                part_previous_x = part_temp_x
                part_previous_y = part_temp_y

        elif active_snake.direction == SnakeDirection.RIGHT:
            part_previous_x = snake_head_x
            part_previous_y = snake_head_y
            active_snake.snake_parts[0].x_coordinate = active_snake.snake_parts[0].x_coordinate + movement_size

            for x in active_snake.snake_parts:
                if x.part_type == SnakePartType.HEAD:
                    continue
                part_temp_x = x.x_coordinate
                part_temp_y = x.y_coordinate
                x.x_coordinate, x.y_coordinate = part_previous_x, part_previous_y
                part_previous_x = part_temp_x
                part_previous_y = part_temp_y

        elif active_snake.direction == SnakeDirection.UP:
            part_previous_x = snake_head_x
            part_previous_y = snake_head_y
            active_snake.snake_parts[0].y_coordinate = active_snake.snake_parts[0].y_coordinate - movement_size

            for x in active_snake.snake_parts:
                if x.part_type == SnakePartType.HEAD:
                    continue
                part_temp_x = x.x_coordinate
                part_temp_y = x.y_coordinate
                x.x_coordinate, x.y_coordinate = part_previous_x, part_previous_y
                part_previous_x = part_temp_x
                part_previous_y = part_temp_y

        elif active_snake.direction == SnakeDirection.DOWN:
            part_previous_x = snake_head_x
            part_previous_y = snake_head_y
            active_snake.snake_parts[0].y_coordinate = active_snake.snake_parts[0].y_coordinate + movement_size

            for x in active_snake.snake_parts:
                if x.part_type == SnakePartType.HEAD:
                    continue
                part_temp_x = x.x_coordinate
                part_temp_y = x.y_coordinate
                x.x_coordinate, x.y_coordinate = part_previous_x, part_previous_y
                part_previous_x = part_temp_x
                part_previous_y = part_temp_y
