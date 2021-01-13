class Snake:
  def __init__(self, snake_parts, owner_name, steps, played_steps, direction, color):
    self.snake_parts = snake_parts
    self.owner_name = owner_name
    self.steps = steps
    self.played_steps = played_steps
    self.direction = direction
    self.color = color
    self.is_active = False

  def add_snake_part(self, snake_part):
    self.snake_parts.append(snake_part)

  def increase_steps(self, steps):
    self.steps += steps

  def increase_played_steps(self):
    self.played_steps += 1

  def set_active(self):
    self.is_active = True

  def set_inactive(self):
    self.is_active = False


class SnakeDirection:
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
