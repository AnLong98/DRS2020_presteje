from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from models import *

class DrawingManager:

    def painter(self, e):
        qp = QPainter()
        qp.begin(self)
        self.paint(qp)
        qp.end()

    def drawSnake(self, painter, snake):
        color = QColor(Qt.black)
        painter.setBrush(color)
        painter.drawRect(130, 15, 90, 60)


    def eraseSnake(self, snake):
        pass


    def drawFood(self, food):
        pass


    def eraseFood(self, food):
        pass


    def drawMultipleSnakes(self, snakes):
        pass


    def eraseAllSnakes(self, snakes):
        pass


    def drawAllFood(self, food):
        pass


    def eraseAllFood(self, food):
        pass




