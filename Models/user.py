class User:
  def __init__(self, snakes, points, user_name, color):
    self.snakes = snakes
    self.points = points
    self.user_name = user_name
    self.color = color

  def remove_snake(self, snake):
    self.snakes.remove(snake)
    if not self.snakes:
      self.snakes = None

  def add_snake(self, snake):
    self.snakes.append(snake)

  def increase_points(self, points):
    self.points += points