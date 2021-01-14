from functools import partial

from Models.drawable_component_base import DrawableComponentBase
import multiprocessing


class CollisionDetectionResult:
    NO_COLLISION = 1
    ENEMY_COLLISION = 2
    WALL_COLLISION = 3
    AUTO_COLLISION = 4
    FRIENDLY_COLLISION = 5
    FOOD_COLLISION = 6


class CollisionManager:
    def __init__(self, table_length, table_height):
        self.table_length = table_length
        self.table_height = table_height
        self.collision_detection_pool = multiprocessing.Pool(5)

    def check_moving_snake_collision(self, moving_snake, all_snakes, all_food):
        snake_head = moving_snake.snake_parts[0]

        #Delegate detection to pool workers
        food_collision_result = self.collision_detection_pool.apply_async(self.is_colliding_with_food,
                                                                          args=(snake_head, all_food))

        wall_collision_result = self.collision_detection_pool.apply_async(self.check_component_to_wall_collision,
                                                                          args=(snake_head, ))

        self_collision_result = self.collision_detection_pool.apply_async(self.check_head_to_body_collision,
                                                                          args=(snake_head, moving_snake))

        other_snakes_collision_result = self.collision_detection_pool.apply_async(self.check_snake_to_snakes_collision,
                                                                                  args=(moving_snake, all_snakes))

        #Get results form workers
        result = food_collision_result.get()
        if result[0]:
            return CollisionDetectionResult.FOOD_COLLISION, all_food[result[1]]

        result = wall_collision_result.get()
        if result:
            return CollisionDetectionResult.WALL_COLLISION, None

        result = self_collision_result.get()
        if result:
            return CollisionDetectionResult.AUTO_COLLISION, moving_snake

        result = other_snakes_collision_result.get()
        if result[0] != CollisionDetectionResult.NO_COLLISION:
            return result[0], all_snakes[result[1]]

        return CollisionDetectionResult.NO_COLLISION, None


    def is_colliding_with_food(self, drawable_component, all_food):
        i = 0
        for food in all_food:
            if self.check_components_collision(food, drawable_component):
                return True, i
            i += 1
        return False, None


    def check_snake_to_snakes_collision(self, moving_snake, all_snakes):
        snake_head = moving_snake.snake_parts[0]
        i = 0
        # check for collision with other snakes:
        for snake in all_snakes:
            is_colliding = self.check_head_to_body_collision(snake_head, snake)
            if is_colliding and snake.owner_name == moving_snake.owner_name:
                return CollisionDetectionResult.FRIENDLY_COLLISION, i
            elif is_colliding and snake.owner_name != moving_snake.owner_name:
                return CollisionDetectionResult.ENEMY_COLLISION, i
            i += 1
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


    def check_component_to_wall_collision(self, drawable_component):
        if drawable_component.x_coordinate + drawable_component.width > self.table_length or drawable_component.x_coordinate < 0:
            return True
        if drawable_component.y_coordinate + drawable_component.height > self.table_height or drawable_component.y_coordinate < 0:
            return True

        return False


    def check_generated_food_collision(self, all_snakes, all_food, generated_food):

        # check if food collided with window border
        if self.check_component_to_wall_collision(generated_food):
            return CollisionDetectionResult.WALL_COLLISION, None

        # check for collision with other food
        for food in all_food:
            if food == generated_food:
                continue
            if self.check_components_collision(food, generated_food):
                return CollisionDetectionResult.FOOD_COLLISION, food

        # check for collision with other snakes:
        for snake in all_snakes:
            is_colliding = self.check_head_to_body_collision(generated_food, snake)
            if is_colliding:
                return CollisionDetectionResult.ENEMY_COLLISION, snake

        return CollisionDetectionResult.NO_COLLISION, None

    def is_coordinate_colliding(self, all_snakes, all_food, drawable_component):

        # check if component collided with window border
        if self.check_component_to_wall_collision(drawable_component):
            return True

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

    def is_snake_side_blocked(self, all_snakes, side_drawable_component, snake_owner):

        # check if component collided with window border
        if self.check_component_to_wall_collision(side_drawable_component):
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

    def get_trapped_enemy_snakes(self, all_snakes, current_player):
        trapped_snakes = []
        for snake in all_snakes:
            if snake.owner_name == current_player.user_name:
                continue
            if self.is_snake_surrounded(snake, all_snakes):
                trapped_snakes.append(snake)

        return trapped_snakes



    def is_snake_surrounded(self, snake, all_snakes):
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
            collision_results.append(self.is_snake_side_blocked(all_snakes, snake_side, snake.owner_name))
            if collision_results[-1] == CollisionDetectionResult.NO_COLLISION:
                return False

        for collision_result in collision_results:
            if collision_result == CollisionDetectionResult.ENEMY_COLLISION:
                return True

        return False

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['collision_detection_pool']
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)
