
class CollisionDetectionResult:
    NO_COLLISION = 1
    ENEMY_COLLISION = 2
    WALL_COLLISION = 3
    AUTO_COLLISION = 4
    FRIENDLY_COLLISION = 5
    FOOD_COLLISION = 6


class CollisionManager:
    def check_moving_snake_collision(self, moving_snake, all_snakes, all_food, table_length, table_height):
        snake_head = moving_snake.snake_parts[0]

        #check if snake head collided with window border
        if snake_head.x_coordinate >= table_length or snake_head.x_coordinate < 0:
            return CollisionDetectionResult.WALL_COLLISION, None
        if snake_head.y_coordinate >= table_height or snake_head.y_coordinate < 0:
            return CollisionDetectionResult.WALL_COLLISION, None

        #check if snake collided with itself
        if self.check_head_to_body_collision(snake_head, moving_snake):
            return CollisionDetectionResult.AUTO_COLLISION, moving_snake

        #check for collision with food
        for food in all_food:
            if snake_head.x_coordinate == food.x_coordinate and snake_head.y_coordinate == food.y_coordinate:
                return CollisionDetectionResult.FOOD_COLLISION, food

        #check for collision with other snakes:
        for snake in all_snakes:
            is_colliding = self.check_head_to_body_collision(snake_head, snake)
            if is_colliding and snake.owner_name == moving_snake.owner_name:
                return CollisionDetectionResult.FRIENDLY_COLLISION, snake
            elif not is_colliding and snake.owner_name != moving_snake.owner_name:
                return CollisionDetectionResult.ENEMY_COLLISION, snake


    def check_head_to_body_collision(self, snake_head, snake):
        for snake_part in snake.snake_parts:
            if snake_part == snake_head:
                continue

            if snake_head.x_coordinate == snake_part.x_coordinate and snake_head.y_coordinate == snake_part.y_coordinate:
                return True

