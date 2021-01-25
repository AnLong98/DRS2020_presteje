from PyQt5.QtCore import *


class HostingSignal(QObject):
    hosting_widget_signal = pyqtSignal()


class InputSignal(QObject):
    input_widget_signal = pyqtSignal()


class ShutdownSignal(QObject):
    shutdown_signal = pyqtSignal()