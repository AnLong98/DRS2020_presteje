from PyQt5.QtCore import *


class Repaint(QObject):
    repaint_signal = pyqtSignal()


class EndGame(QObject):
    end_game_signal = pyqtSignal()


class StartGame(QObject):
    start_game_signal = pyqtSignal()
