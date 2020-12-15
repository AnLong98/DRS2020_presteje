from models import SnakeDirection
from models import SnakePartType
from GUI.game_board import KeyPressed


class MovementManager:
    def set_snake_direction(self, key_pressed, active_snake):
        if key_pressed == KeyPressed.LEFT:
            if active_snake.direction != SnakeDirection.RIGHT:
                active_snake.direction = SnakeDirection.LEFT
                self.move_active_snake(active_snake)

        elif key_pressed == KeyPressed.RIGHT:
            if active_snake.direction != SnakeDirection.LEFT:
                active_snake.direction = SnakeDirection.RIGHT
                self.move_active_snake(active_snake)

        elif key_pressed == KeyPressed.UP:
            if active_snake.direction != SnakeDirection.DOWN:
                active_snake.direction = SnakeDirection.UP
                self.move_active_snake(active_snake)

        elif key_pressed == KeyPressed.DOWN:
            if active_snake.direction != SnakeDirection.UP:
                active_snake.direction = SnakeDirection.DOWN
                self.move_active_snake(active_snake)


    def move_active_snake(self, active_snake):
        snake_head = active_snake.snake_parts[0]

        if active_snake.direction == SnakeDirection.LEFT:
            part_previous = snake_head  # cuva prethodni
            snake_head.x_coordinate = snake_head.x_coordinate - 1

            for x in active_snake.snake_parts:
                if x.part_type == SnakePartType.HEAD:
                    continue
                part_temp = x
                x.x_coordinate, x.y_coordinate = part_previous.x_coordinate, part_previous.y_coordinate
                part_previous = part_temp

        elif active_snake.direction == SnakeDirection.RIGHT:
            part_previous = snake_head
            snake_head.x_coordinate = snake_head.x_coordinate + 1

            for x in active_snake.snake_parts:
                if x.part_type == SnakePartType.HEAD:
                    continue
                part_temp = x
                x.x_coordinate, x.y_coordinate = part_previous.x_coordinate, part_previous.y_coordinate
                part_previous = part_temp

        elif active_snake.direction == SnakeDirection.UP:
            part_previous = snake_head
            snake_head.x_coordinate = snake_head.y_coordinate - 1

            for x in active_snake.snake_parts:
                if x.part_type == SnakePartType.HEAD:
                    continue
                part_temp = x
                x.x_coordinate, x.y_coordinate = part_previous.x_coordinate, part_previous.y_coordinate
                part_previous = part_temp

        elif active_snake.direction == SnakeDirection.DOWN:
            part_previous = snake_head
            snake_head.x_coordinate = snake_head.y_coordinate + 1

            for x in active_snake.snake_parts:
                if x.part_type == SnakePartType.HEAD:
                    continue
                part_temp = x
                x.x_coordinate, x.y_coordinate = part_previous.x_coordinate, part_previous.y_coordinate
                part_previous = part_temp

        # treba mi drawing_manager instanca
        # def eraseSnake(active_snake)
        # def eraseSnake(painter, active_snake)  treba mi painter instanca