

class SnakePartType:
  HEAD = 1
  BODY = 2

class DrawableComponentBase:
  def __init__(self, x_coordinate, y_coordinate):
    self.x_coordinate = x_coordinate
    self.y_coordinate = y_coordinate


class Snake:
  def __init__(self, snake_parts, owner_name, steps):
    self.snake_parts = snake_parts
    self.owner_name = owner_name
    self.steps = steps


class SnakePart(DrawableComponentBase):
  def __init__(self, x_coordinate, y_coordinate, part_type):
    super().__init__(x_coordinate, y_coordinate,)
    self.part_type = part_type


class User:
  def __init__(self, snakes, points, user_name):
    self.snakes = snakes
    self.points = points
    self.user_name = user_name


class Food(DrawableComponentBase):
  def __init__(self, x_coordinate, y_coordinate, points_worth):
    super().__init__(x_coordinate, y_coordinate,)