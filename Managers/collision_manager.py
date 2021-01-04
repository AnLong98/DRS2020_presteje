from models import DrawableComponentBase


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


    def is_coordinate_colliding(self, all_snakes, all_food, table_width, table_height, drawable_component):

        # check if component collided with window border
        if self.check_component_to_wall_collision(drawable_component, wall_width=table_width, wall_height=table_height):
            return True

        # check for collision with food
        for food in all_food:
            if self.check_components_collision(food, drawable_component):
                return True

        # check for collision with other snakes:
        for snake in all_snakes:
            for snake_part in snake.snake_parts:
                is_colliding = self.check_components_collision(snake_part, drawable_component)
                if is_colliding:
                    return True

        return False

    def is_snake_side_blocked(self, all_snakes, table_width, table_height, side_drawable_component, snake_owner):

        # check if component collided with window border
        if self.check_component_to_wall_collision(side_drawable_component, wall_width=table_width, wall_height=table_height):
            return CollisionDetectionResult.WALL_COLLISION

        # check for collision with other snakes:
        for snake in all_snakes:
            for snake_part in snake.snake_parts:
                is_colliding = self.check_components_collision(snake_part, side_drawable_component)
                if is_colliding and snake.owner_name == snake_owner:
                    return CollisionDetectionResult.FRIENDLY_COLLISION
                elif is_colliding:
                    return CollisionDetectionResult.ENEMY_COLLISION

        return CollisionDetectionResult.NO_COLLISION

    def is_colliding_with_marked_locations(self, drawable_component, marked_locations):
        for component in marked_locations:
            if self.check_components_collision(component, drawable_component):
                return True

        return False

    def get_trapped_enemy_snakes(self, all_snakes, table_width, table_height, current_player):
        trapped_snakes = []
        for snake in all_snakes:
            if snake.owner_name == current_player.user_name:
                continue
            if self.is_snake_surrounded(snake, all_snakes, table_width, table_height):
                trapped_snakes.append(snake)

        return trapped_snakes



    def is_snake_surrounded(self, snake, all_snakes, table_width, table_height):
        collision_results = []

        snake_head = snake.snake_parts[0]
        head_move_coordinates = []
        head_move_coordinates.append(DrawableComponentBase(snake_head.x_coordinate - snake_head.width,
                                                           snake_head.y_coordinate, snake_head.width,
                                                           snake_head.height))   #head moving left
        head_move_coordinates.append(DrawableComponentBase(snake_head.x_coordinate + snake_head.width,
                                                           snake_head.y_coordinate, snake_head.width,
                                                           snake_head.height))  # head moving right
        head_move_coordinates.append(DrawableComponentBase(snake_head.x_coordinate,
                                                           snake_head.y_coordinate - snake_head.height, snake_head.width,
                                                           snake_head.height))  # head moving up
        head_move_coordinates.append(DrawableComponentBase(snake_head.x_coordinate,
                                                           snake_head.y_coordinate + snake_head.height,
                                                           snake_head.width,
                                                           snake_head.height))  # head moving down

        for snake_side in head_move_coordinates:
            collision_results.append(self.is_snake_side_blocked(all_snakes, table_width, table_height,
                                                               snake_side, snake.owner_name))
            if collision_results[-1] == CollisionDetectionResult.NO_COLLISION:
                return False

        for collision_result in collision_results:
            if collision_result == CollisionDetectionResult.ENEMY_COLLISION:
                return True

        return False



