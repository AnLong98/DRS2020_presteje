from PyQt5.QtWidgets import QApplication
from GUI.server_start_window import ServerStackedWidgets
from GUI.server_signals import *
import sys

if __name__ == "__main__":
    input_signal = InputSignal()
    hosting_signal = HostingSignal()
    shutdown_signal = ShutdownSignal()

    app = QApplication(sys.argv)
    startWindow = ServerStackedWidgets(input_signal, hosting_signal, shutdown_signal)
    startWindow.show()
    print("Server is up and running")
    app.exec()

    clients_number = startWindow.server_stack.player_count
    snake_count = startWindow.server_stack.snake_count

    if clients_number is None or snake_count is None:
        print("Server window has been shutdown!")
        sys.exit()