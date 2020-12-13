import unittest
from unittest.mock import MagicMock
from Managers.collision_manager import  CollisionManager


class CollisionManagerTests(unittest.TestCase):
    #def setUp(self):
    def test__heck_head_to_body_collision__no_collision__returns_false(self):
        snake_parts = []
        snake_head = MagicMock()
        snake_head.x_coordinate = 1
        snake_head.y_coordinate = 1
        snake_part_1 = MagicMock()
        snake_part_1.x_coordinate = 1
        snake_part_1.y_coordinate = 5
        snake_part_2 = MagicMock()
        snake_part_2.x_coordinate = 4
        snake_part_2.y_coordinate = 1
        snake_part_3 = MagicMock()
        snake_part_3.x_coordinate = 6
        snake_part_3.y_coordinate = 7

        snake_parts.append(snake_part_1)
        snake_parts.append(snake_part_2)
        snake_parts.append(snake_part_3)
        snake_parts.append(snake_head)

        snake = MagicMock()
        snake.snake_parts = snake_parts

        collision_manager =  CollisionManager()
        self.assertFalse(collision_manager.check_head_to_body_collision(snake_head, snake))


    def test__heck_head_to_body_collision__collision__returns_true(self):
        snake_parts = []
        snake_head = self.mock_snake_part(1,1)
        snake_part_1 = self.mock_snake_part(1,2)
        snake_part_2 = self.mock_snake_part(1,3)
        snake_part_3 = self.mock_snake_part(1,1)

        snake_parts.append(snake_part_1)
        snake_parts.append(snake_part_2)
        snake_parts.append(snake_part_3)
        snake_parts.append(snake_head)

        snake = MagicMock()
        snake.snake_parts = snake_parts

        collision_manager =  CollisionManager()
        self.assertTrue(collision_manager.check_head_to_body_collision(snake_head, snake))



    def mock_snake_part(self, x, y):
        snake_part = MagicMock()
        snake_part.x_coordinate = x
        snake_part.y_coordinate = y

        return snake_part