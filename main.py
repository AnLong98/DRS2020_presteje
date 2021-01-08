import sys

from PyQt5.QtWidgets import QApplication
from GUI.start_window import StartWindow
from start_up import InGameInitializer

if __name__ == "__main__":
    app = QApplication(sys.argv)

    startWindow = StartWindow()
    startWindow.exec()

    player_names = startWindow.playerNames
    snake_count = startWindow.snakeCount.value()

    a = InGameInitializer(player_names, snake_count)
    a.start_main()

