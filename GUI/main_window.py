import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from GUI.game_board import GameBoard
from GUI.score_board import ScoreBoard

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("PreSteJe Snake Game")
        self.setFixedSize(1200, 800)
        self.center_main_window()
        self.generate_window_layout()

    def center_main_window(self):
        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        return self.move(qtRectangle.topLeft())

    def generate_window_layout(self):
        game_board = GameBoard()
        score_board = ScoreBoard()
        score_board.setFrameShape(QFrame.StyledPanel)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setEnabled(False)
        splitter.addWidget(game_board)
        splitter.addWidget(score_board)

        self.setCentralWidget(splitter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
