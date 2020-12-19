
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
        if self.check_component_to_wall_collision(snake_head, wall_width=table_length, wall_height=table_height):
            return CollisionDetectionResult.WALL_COLLISION, None

        #check if snake collided with itself
        if self.check_head_to_body_collision(snake_head, moving_snake):
            return CollisionDetectionResult.AUTO_COLLISION, moving_snake

        #check for collision with food
        for food in all_food:
            if self.check_components_collision(food, snake_head):
                return CollisionDetectionResult.FOOD_COLLISION, food

        #check for collision with other snakes:
        for snake in all_snakes:
            is_colliding = self.check_head_to_body_collision(snake_head, snake)
            if is_colliding and snake.owner_name == moving_snake.owner_name:
                return CollisionDetectionResult.FRIENDLY_COLLISION, snake
            elif is_colliding and snake.owner_name != moving_snake.owner_name:
                return CollisionDetectionResult.ENEMY_COLLISION, snake

        return CollisionDetectionResult.NO_COLLISION, None


    def check_head_to_body_collision(self, snake_head, snake):
        for snake_part in snake.snake_parts:
            if snake_part == snake_head:
                continue

            if self.check_components_collision(snake_head, snake_part):
                return True

        return False


    def check_components_collision(self, drawable_component1, drawable_component2):
        if (drawable_component1.x_coordinate < drawable_component2.x_coordinate + drawable_component2.width and
            drawable_component1.x_coordinate + drawable_component1.width > drawable_component2.x_coordinate and
            drawable_component1.y_coordinate < drawable_component2.y_coordinate + drawable_component2.height and
            drawable_component1.y_coordinate + drawable_component1.height > drawable_component2.y_coordinate):
            return True
        return False


    def check_component_to_wall_collision(self, drawable_component, wall_width, wall_height):
        if drawable_component.x_coordinate + drawable_component.width > wall_width or drawable_component.x_coordinate < 0:
            return True
        if drawable_component.y_coordinate + drawable_component.height > wall_height or drawable_component.y_coordinate < 0:
            return True

        return False


    def check_generated_food_collision(self, all_snakes, all_food, table_width, table_height, generated_food):

        # check if food collided with window border
        if self.check_component_to_wall_collision(generated_food, wall_width=table_width, wall_height=table_height):
            return CollisionDetectionResult.WALL_COLLISION, None

        # check for collision with other food
        for food in all_food:
            if self.check_components_collision(food, generated_food):
                return CollisionDetectionResult.FOOD_COLLISION, food

        # check for collision with other snakes:
        for snake in all_snakes:
            is_colliding = self.check_head_to_body_collision(generated_food, snake)
            if is_colliding:
                return CollisionDetectionResult.ENEMY_COLLISION, snake

        return CollisionDetectionResult.NO_COLLISION, None


