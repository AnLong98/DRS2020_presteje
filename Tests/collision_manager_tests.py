import unittest
from unittest.mock import MagicMock
from Managers.collision_manager import CollisionManager, CollisionDetectionResult


class CollisionManagerTests(unittest.TestCase):
    def setUp(self):
        self.collision_manager = CollisionManager()
        self.table_height = 100
        self.table_width = 100


    def test__heck_head_to_body_collision__no_collision__returns_false(self):
        snake_parts = []
        snake_part_6 = self.mock_component(0, 0, 1, 1)
        snake_part_1 = self.mock_component(1, 0, 1, 1)
        snake_part_2 = self.mock_component(2, 0, 1, 1)
        snake_part_3 = self.mock_component(3, 0, 1, 1)
        snake_part_4 = self.mock_component(3, 1, 1, 1)
        snake_part_5 = self.mock_component(2, 1, 1, 1)
        snake_head = self.mock_component(1, 1, 1, 1)

        snake_parts.append(snake_part_1)
        snake_parts.append(snake_part_2)
        snake_parts.append(snake_part_3)
        snake_parts.append(snake_part_4)
        snake_parts.append(snake_part_5)
        snake_parts.append(snake_part_6)
        snake_parts.append(snake_head)

        snake = MagicMock()
        snake.snake_parts = snake_parts

        self.assertFalse(self.collision_manager.check_head_to_body_collision(snake_head, snake))


    def test__heck_head_to_body_collision__collision__returns_true(self):
        snake_parts = []
        snake_part_6 = self.mock_component(0,0,1,1)
        snake_part_1 = self.mock_component(1,0,1,1)
        snake_part_2 = self.mock_component(2,0,1,1)
        snake_part_3 = self.mock_component(3,0,1,1)
        snake_part_4 = self.mock_component(3, 1, 1, 1)
        snake_part_5 = self.mock_component(2, 1, 1, 1)
        snake_head = self.mock_component(2,0,1,1)

        snake_parts.append(snake_part_1)
        snake_parts.append(snake_part_2)
        snake_parts.append(snake_part_3)
        snake_parts.append(snake_part_4)
        snake_parts.append(snake_part_5)
        snake_parts.append(snake_part_6)
        snake_parts.append(snake_head)

        snake = MagicMock()
        snake.snake_parts = snake_parts

        self.assertTrue(self.collision_manager.check_head_to_body_collision(snake_head, snake))

    def test__check_components_collision__no_collision__returns_false(self):
        snake_part1 = self.mock_component(10, 10, 10, 10)
        snake_part2 = self.mock_component(21, 21, 10, 10)

        self.assertFalse(self.collision_manager.check_components_collision(snake_part1, snake_part2))

    def test__check_components_collision__partial_collison_of_squares__returns_true(self):
        snake_part1 = self.mock_component(10, 10, 10, 10)
        snake_part2 = self.mock_component(15, 15, 10, 10)

        self.assertTrue(self.collision_manager.check_components_collision(snake_part1, snake_part2))

    def test__check_components_collision__full_collison_of_squares__returns_true(self):
        snake_part1 = self.mock_component(10, 10, 10, 10)
        snake_part2 = self.mock_component(10, 10, 10, 10)

        self.assertTrue(self.collision_manager.check_components_collision(snake_part1, snake_part2))

    def test__check_components_collision__collison_of_rectangles_variable_dimensions__returns_true(self):
        snake_part1 = self.mock_component(10, 3, 5, 6)
        snake_part2 = self.mock_component(13, 7, 3, 6)

        self.assertTrue(self.collision_manager.check_components_collision(snake_part1, snake_part2))

    def test__check_components_collision__touching_component_no_collision__returns_false(self):
        snake_part1 = self.mock_component(0, 0, 4, 5)
        snake_part2 = self.mock_component(5, 0, 4, 5)

        self.assertFalse(self.collision_manager.check_components_collision(snake_part1, snake_part2))

    def test__check_component_to_wall_collision__no_collision__returns_false(self):
        snake_part1 = self.mock_component(0, 0, 4, 5)

        self.assertFalse(self.collision_manager.check_component_to_wall_collision(snake_part1, self.table_width, self.table_height))

    def test__check_component_to_wall_collision__collision_negative_x__returns_true(self):
        snake_part1 = self.mock_component(-2, 0, 4, 5)

        self.assertTrue(
            self.collision_manager.check_component_to_wall_collision(snake_part1, self.table_width, self.table_height))

    def test__check_component_to_wall_collision__collision_x_boundary__returns_true(self):
        snake_part1 = self.mock_component(98, 0, 4, 5)

        self.assertTrue(
            self.collision_manager.check_component_to_wall_collision(snake_part1, self.table_width, self.table_height))

    def test__check_component_to_wall_collision__collision_y_boundary__returns_true(self):
        snake_part1 = self.mock_component(98, 98, 1, 5)

        self.assertTrue(
            self.collision_manager.check_component_to_wall_collision(snake_part1, self.table_width, self.table_height))

    def test__check_component_to_wall_collision__collision_negative_y__returns_true(self):
        snake_part1 = self.mock_component(98, -1, 1, 5)

        self.assertTrue(
            self.collision_manager.check_component_to_wall_collision(snake_part1, self.table_width, self.table_height))

    def test__check_component_to_wall_collision__x_y_boundary_collision__returns_true(self):
        snake_part1 = self.mock_component(98, 98, 5, 5)

        self.assertTrue(
            self.collision_manager.check_component_to_wall_collision(snake_part1, self.table_width, self.table_height))

    def test__check_moving_snake_collision__wall_collision__returns_wall_collision(self):
        snake_parts = []
        snake_head = self.mock_component(98, 98, 5, 5)
        snake_parts.append(snake_head)
        snake = MagicMock()
        snake.snake_parts = snake_parts


        collison_result, object_collided = self.collision_manager.check_moving_snake_collision(snake, None, None, self.table_width, self.table_height)
        self.assertEqual(collison_result, CollisionDetectionResult.WALL_COLLISION)
        self.assertEqual(object_collided, None)

    def test__check_moving_snake_collision__auto_collision__returns_auto_collision(self):
        snake_parts = []
        snake_part_6 = self.mock_component(0, 0, 1, 1)
        snake_part_1 = self.mock_component(1, 0, 1, 1)
        snake_part_2 = self.mock_component(2, 0, 1, 1)
        snake_part_3 = self.mock_component(3, 0, 1, 1)
        snake_part_4 = self.mock_component(3, 1, 1, 1)
        snake_part_5 = self.mock_component(2, 1, 1, 1)
        snake_head = self.mock_component(2, 0, 1, 1)
        snake_parts.append(snake_head)
        snake_parts.append(snake_part_1)
        snake_parts.append(snake_part_2)
        snake_parts.append(snake_part_3)
        snake_parts.append(snake_part_4)
        snake_parts.append(snake_part_5)
        snake_parts.append(snake_part_6)

        snake = MagicMock()
        snake.snake_parts = snake_parts

        collison_result, object_collided = self.collision_manager.check_moving_snake_collision(snake, None, None,
                                                                                               self.table_width,
                                                                                               self.table_height)
        self.assertEqual(collison_result, CollisionDetectionResult.AUTO_COLLISION)
        self.assertEqual(object_collided, snake)

    def test__check_moving_snake_collision__food_collision__returns_food_collision(self):
        snake_parts = []
        snake_part_1 = self.mock_component(1, 0, 1, 1)
        snake_head = self.mock_component(1, 1, 1, 1)
        snake_parts.append(snake_head)
        snake_parts.append(snake_part_1)
        snake = MagicMock()
        snake.snake_parts = snake_parts

        food = self.mock_component(1,1,3,3)
        all_food = []
        all_food.append(food)

        collison_result, object_collided = self.collision_manager.check_moving_snake_collision(snake, None, all_food,
                                                                                               self.table_width,
                                                                                               self.table_height)
        self.assertEqual(collison_result, CollisionDetectionResult.FOOD_COLLISION)
        self.assertEqual(object_collided, food)

    def test__check_moving_snake_collision__friendly_collision__returns_friendly_collision(self):
        snake_parts = []
        snake_part_1 = self.mock_component(1, 0, 1, 1)
        snake_head = self.mock_component(1, 1, 1, 1)
        snake_parts.append(snake_head)
        snake_parts.append(snake_part_1)
        snake = MagicMock()
        snake.snake_parts = snake_parts
        snake.owner_name = "pedja"

        snake_parts2 = []
        snake2_part_1 = self.mock_component(1, 1, 1, 1)
        snake2_head = self.mock_component(1, 2, 1, 1)
        snake_parts2.append(snake2_head)
        snake_parts2.append(snake2_part_1)
        snake2 = MagicMock()
        snake2.snake_parts = snake_parts2
        snake2.owner_name = "pedja"

        food = self.mock_component(99,99,1,1)
        all_food = []
        all_food.append(food)

        all_snakes = []
        all_snakes.append(snake)
        all_snakes.append(snake2)

        collison_result, object_collided = self.collision_manager.check_moving_snake_collision(snake, all_snakes, all_food,
                                                                                               self.table_width,
                                                                                               self.table_height)
        self.assertEqual(collison_result, CollisionDetectionResult.FRIENDLY_COLLISION)
        self.assertEqual(object_collided, snake2)


    def test__check_moving_snake_collision__enemy_collision__returns_enemy_collision(self):
        snake_parts = []
        snake_part_1 = self.mock_component(1, 0, 1, 1)
        snake_head = self.mock_component(1, 1, 1, 1)
        snake_parts.append(snake_head)
        snake_parts.append(snake_part_1)
        snake = MagicMock()
        snake.snake_parts = snake_parts
        snake.owner_name = "pedja"

        snake_parts2 = []
        snake2_part_1 = self.mock_component(1, 1, 1, 1)
        snake2_head = self.mock_component(1, 2, 1, 1)
        snake_parts2.append(snake2_head)
        snake_parts2.append(snake2_part_1)
        snake2 = MagicMock()
        snake2.snake_parts = snake_parts2
        snake2.owner_name = "miki"

        food = self.mock_component(99,99,1,1)
        all_food = []
        all_food.append(food)

        all_snakes = []
        all_snakes.append(snake)
        all_snakes.append(snake2)

        collison_result, object_collided = self.collision_manager.check_moving_snake_collision(snake, all_snakes, all_food,
                                                                                               self.table_width,
                                                                                               self.table_height)
        self.assertEqual(collison_result, CollisionDetectionResult.ENEMY_COLLISION)
        self.assertEqual(object_collided, snake2)

    def test__check_moving_snake_collision__no_collision__returns_no_collision(self):
        snake_parts = []
        snake_part_1 = self.mock_component(1, 0, 1, 1)
        snake_head = self.mock_component(1, 1, 1, 1)
        snake_parts.append(snake_head)
        snake_parts.append(snake_part_1)
        snake = MagicMock()
        snake.snake_parts = snake_parts
        snake.owner_name = "pedja"

        snake_parts2 = []
        snake2_part_1 = self.mock_component(1, 3, 1, 1)
        snake2_head = self.mock_component(1, 2, 1, 1)
        snake_parts2.append(snake2_head)
        snake_parts2.append(snake2_part_1)
        snake2 = MagicMock()
        snake2.snake_parts = snake_parts2
        snake2.owner_name = "miki"

        food = self.mock_component(99, 99, 1, 1)
        all_food = []
        all_food.append(food)

        all_snakes = []
        all_snakes.append(snake)
        all_snakes.append(snake2)

        collison_result, object_collided = self.collision_manager.check_moving_snake_collision(snake, all_snakes,
                                                                                               all_food,
                                                                                               self.table_width,
                                                                                               self.table_height)


    def mock_component(self, x, y, height, width):
        snake_part = MagicMock()
        snake_part.x_coordinate = x
        snake_part.y_coordinate = y
        snake_part.height = height
        snake_part.width = width

        return snake_part