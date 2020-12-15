import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from GUI.game_board import GameBoard
from GUI.score_board import ScoreBoard

from Managers.drawing_manager import DrawingManager
from models import Snake, SnakePart, SnakePartType, DrawableComponentBase, Food


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("PreSteJe Snake Game")
        self.setFixedSize(1200, 800)

        self.gameboard = GameBoard()

        self.scoreboard = ScoreBoard()

        self.generate_window_layout()



    # def center_main_window(self):
    #     qtRectangle = self.frameGeometry()
    #     centerPoint = QDesktopWidget().availableGeometry().center()
    #     qtRectangle.moveCenter(centerPoint)
    #     return self.move(qtRectangle.topLeft())

    def generate_window_layout(self):
        splitter = QSplitter(Qt.Horizontal)
        splitter.setEnabled(False)
        splitter.addWidget(self.gameboard)
        splitter.addWidget(self.scoreboard)
        self.setCentralWidget(splitter)

    @property
    def get_gameboard(self):
        return self.gameboard

    @property
    def get_scoreboard(self):
        return self.scoreboard

    @property
    def get_mainwindow_height(self):
        return self.height()

    @property
    def get_mainwindow_width(self):
        return self.width()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
