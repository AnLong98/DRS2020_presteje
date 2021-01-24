from PyQt5.QtWidgets import QApplication
import sys

from GUI.server_start_window import ServerStackedWidgets, InputWidget, HostingWidget

if __name__ == "__main__":
    input_signal = InputWidget()
    hosting_sigal = HostingWidget()

    app = QApplication(sys.argv)
    startWindow = ServerStackedWidgets(input_signal, hosting_sigal)
    startWindow.show()
    print("Server is up and running")
    app.exec()

    clients_number = startWindow.server_stack.player_count
    snake_count = startWindow.server_stack.snake_count

    if clients_number is None or snake_count is None:
        print("Server window has been shutdown!")
        sys.exit()