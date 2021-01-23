from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys
from Models.snake_part import SnakePartType
from PyQt5 import QtWidgets


class Repaint(QObject):
    repaint_signal = pyqtSignal()

class EndGame(QObject):
    end_game_signal = pyqtSignal()

class StartGame(QObject):
    start_game_signal = pyqtSignal()

class ResultsBoard(QFrame):
    def __init__(self, winner, all_players):
        super(ResultsBoard, self).__init__()
        self.setFixedSize(960, 810)
        self.winner = winner
        self.all_players = all_players
        self.number_of_players = len(self.all_players)


        #self.winner_label = None
        self.scoreboard_rows = []

        self.define_frame_style()

    def define_frame_style(self):
        self.frame_layout = QVBoxLayout()

        # creating label for header and winner username
        winner_label_heading = QLabel(f"The game has ended!")
        winner_label_heading.setFont(QFont("Arial", 25))
        self.winner_label = QLabel("", self)
        self.winner_label.setFont(QFont("Arial", 25))

        # creating scoreboard for results
        scoreboard_layout = QHBoxLayout()
        scoreboard_layout.addStretch()
        score_row_column = QVBoxLayout()
        score_label = QLabel("Results:")
        score_label.setFont(QFont("Arial", 25))
        score_row_column.addWidget(score_label)
        for i in range(4):
            username_label = QLabel("", self)
            self.scoreboard_rows.append(username_label)
            username_label.setFont(QFont("Arial", 15))
            score_row_column.addWidget(username_label)
        scoreboard_layout.addLayout(score_row_column)
        scoreboard_layout.addStretch()

        # creating exit and restart button
        restart_button = QPushButton("Restart")
        restart_button.setMaximumWidth(100)
        restart_button.setMaximumHeight(50)
        restart_button.setCheckable(True)
        restart_button.toggle()

        exit_button = QPushButton("Exit")
        exit_button.setMaximumWidth(100)
        exit_button.setMaximumHeight(50)

        restart_button.clicked.connect(self.restart_game)
        exit_button.clicked.connect(self.exit_game)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(restart_button)
        buttons_layout.addWidget(exit_button)

        self.frame_layout.addWidget(winner_label_heading)
        winner_label_heading.setAlignment(Qt.AlignHCenter)
        self.frame_layout.addWidget(self.winner_label)
        self.winner_label.setAlignment(Qt.AlignHCenter)
        self.frame_layout.addLayout(scoreboard_layout)
        self.frame_layout.addLayout(buttons_layout)
        self.frame_layout.addStretch()
        self.setLayout(self.frame_layout)

    def write_game_results(self):
        self.winner_label.setText(f"Winner is: {self.winner}")
        for i, player in enumerate(self.all_players):
            self.scoreboard_rows[i].setText(f"{i + 1}. {self.all_players[i].user_name}")

    def exit_game(self):
        pass

    def restart_game(self):
        pass


class GameBoard(QFrame):
    def __init__(self, repaint):
        super(GameBoard, self).__init__()
        self.setFixedSize(960, 810)
        self.setFrameShape(QFrame.StyledPanel)
        self.setStyleSheet('background-color: #27962d')

        self.snakes = []
        self.food = []
        self.active_player = None

        self.repaint_signal = repaint.repaint_signal
        self.repaint_signal.connect(self.update)

    @property
    def get_gameboard_height(self):
        return self.height()

    @property
    def get_gameboard_width(self):
        return self.width()

    # square width method
    def square_width(self):
        return 15

    # square height
    def square_height(self):
        return 15

    def set_snakes(self, snakes):
        self.snakes = snakes

    def set_active_player(self, player):
        self.active_player = player

    def set_food(self, food):
        self.food = food

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        active_player_name = ''

        if self.active_player:
            active_player_name = self.active_player.user_name
            for snake in self.active_player.snakes:
                for part in snake.snake_parts:
                    self.draw_square(qp, part, snake)

        for snake in self.snakes:
            if snake.owner_name == active_player_name:
                continue
            for part in snake.snake_parts:
                self.draw_square(qp, part, snake)

        for f in self.food:
            self.draw_square_food(qp, f)
        qp.end()

    def draw_square(self, qp, snake_part, snake):
        rect = self.contentsRect()

        if snake_part.part_type == SnakePartType.HEAD:
            if snake.is_active:
                color = QColor('#000000')
            else:
                color = QColor('#d1d1d1')
        else:
            color = QColor(snake.color)

        qp.fillRect(rect.left() + snake_part.x_coordinate, snake_part.y_coordinate, self.square_width() - 1, self.square_height() - 1, color)

    def draw_square_food(self, qp, food):
        if food.is_super_food:
            color = QColor('#00FFFF')
        else:
            color = QColor('#ff911c')
        rect = self.contentsRect()

        qp.fillRect(rect.left() + food.x_coordinate, food.y_coordinate, self.square_width() - 1, self.square_height() - 1,
                    color)


class StackedFrames(QWidget):
    def __init__(self, start_game, end_game, painter, winner, all_players):
        super(StackedFrames, self).__init__()

        self.setMinimumSize(960, 810)

        self._painter = painter
        self._winner = winner
        self._all_players = all_players

        self.end_game_signal = end_game.end_game_signal
        self.end_game_signal.connect(self.display_finish_frame)

        self.start_game_signal = start_game.start_game_signal
        self.start_game_signal.connect(self.display_game_board_frame)

        self.define_stacked_widget_style()

    def define_stacked_widget_style(self):
        self.stack = QStackedWidget(self)
        self.stack.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)

        self.game_stack = GameBoard(self._painter)
        self.stack.addWidget(self.game_stack)

        self.finish_stack = ResultsBoard(self._winner, self._all_players)
        self.stack.addWidget(self.finish_stack)

        hbox = QVBoxLayout()
        hbox.addWidget(self.stack)
        self.setLayout(hbox)
        self.layout().setContentsMargins(0, 0, 0, 0)



    def display_game_board_frame(self):
        self.stack.setCurrentIndex(0)

    def display_finish_frame(self):
        self.finish_stack.write_game_results()
        self.stack.setCurrentIndex(1)
