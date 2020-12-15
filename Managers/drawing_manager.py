from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from models import *

class DrawingManager:

    def drawSnake(self, snake, game_board):
        game_board.snakes.append(snake)

    def drawFood(self, food, game_board):
        game_board.food.append(food)
