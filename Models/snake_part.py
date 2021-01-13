from Models.drawable_component_base import DrawableComponentBase


class SnakePartType:
  HEAD = 1
  BODY = 2

class SnakePart(DrawableComponentBase):
  def __init__(self, x_coordinate, y_coordinate, height, width, part_type):
    super().__init__(x_coordinate, y_coordinate, height, width)
    self.part_type = part_type
