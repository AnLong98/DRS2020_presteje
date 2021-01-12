from Models.drawable_component_base import DrawableComponentBase


class Food(DrawableComponentBase):
  def __init__(self, x_coordinate, y_coordinate, height, width, points_worth, steps_worth, is_super_food=False):
    super().__init__(x_coordinate, y_coordinate, height, width)
    self.points_worth = points_worth
    self.steps_worth = steps_worth
    self.is_super_food = is_super_food