class SnakePartType:
  HEAD = 1
  BODY = 2

class DrawableComponentBase:
  def __init__(self, x_coordinate, y_coordinate, height, width):
    self.x_coordinate = x_coordinate
    self.y_coordinate = y_coordinate
    self.height = height
    self.width = width


class Snake:
  def __init__(self, snake_parts, owner_name, steps):
    self.snake_parts = snake_parts
    self.owner_name = owner_name
    self.steps = steps

  def add_snake_part(self, snake_part):
    self.snake_parts.append(snake_part)

  def incerase_steps(self, steps):
    self.steps += steps


class SnakePart(DrawableComponentBase):
  def __init__(self, x_coordinate, y_coordinate, height, width, part_type):
    super().__init__(x_coordinate, y_coordinate, height, width)
    self.part_type = part_type


class User:
  def __init__(self, snakes, points, user_name):
    self.snakes = snakes
    self.points = points
    self.user_name = user_name


class Food(DrawableComponentBase):
  def __init__(self, x_coordinate, y_coordinate, height, width, points_worth, steps_worth):
    super().__init__(x_coordinate, y_coordinate, height, width)
    self.points_worth = points_worth
    self.steps_worth = steps_worth