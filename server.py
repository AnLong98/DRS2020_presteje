from PyQt5.QtWidgets import QApplication
import sys

from GUI.server_start_window import ServerStackedWidgets, InputWidget, HostingWidget, ShutdownWindow

if __name__ == "__main__":
    input_signal = InputWidget()
    hosting_signal = HostingWidget()
    shutdown_signal = ShutdownWindow()
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