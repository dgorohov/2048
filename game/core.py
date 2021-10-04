import pkg_resources
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QVBoxLayout, QDialog

from game.logic import Logic


class Window(QDialog):

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.__rows = 4
        self.__columns = 4
        self.__game = Game(parent=self, rows=self.__rows, columns=self.__columns)
        self.layout.addWidget(self.__game)
        css_path = pkg_resources.resource_filename(__name__, "stylesheet.css")
        with open(css_path) as css_file:
            self.setStyleSheet(css_file.read())
        width = (self.__rows * 100 + 10) + self.__rows * 10
        height = (self.__columns * 100 + 10) + self.__columns * 10
        self.setFixedSize(width, height)

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            self.__game.handle_key_press_event(event)


class GameLabel(QLabel):
    colors = {
        0: "#eaeaea",
        2: "#776e65",
        4: "#776e65",
        8: "#f9f6f2",
        16: "#f9f6f2",
        32: "#f9f6f2",
        64: "#f9f6f2",
        128: "#f9f6f2",
        256: "#f9f6f2",
        512: "#f9f6f2",
        1024: "#f9f6f2",
        2048: "#f9f6f2",
        4096: "#776e65",
        8192: "#f9f6f2",
        16384: "#776e65",
        32768: "#776e65",
        65536: "#f9f6f2",
    }
    background_colors = {
        0: "#aaaaaa",
        2: "#eee4da",
        4: "#ede0c8",
        8: "#f2b179",
        16: "#f59563",
        32: "#f67c5f",
        64: "#f65e3b",
        128: "#edcf72",
        256: "#edcc61",
        512: "#edc850",
        1024: "#edc53f",
        2048: "#edc22e",
        4096: "#eee4da",
        8192: "#edc22e",
        16384: "#f2b179",
        32768: "#f59563",
        65536: "#f67c5f",
    }

    def __init__(self, value):
        super(QLabel, self).__init__()
        self.__value = value

    def set_value(self, value: int):
        self.__value = value
        self.setText(f"{value}")
        self.setStyleSheet(
            f"background-color: {self.background_colors[value if value in self.background_colors else 0]};"
            f"color: {self.colors[value if value in self.colors else 0]}")


class Game(QWidget):
    latest_direction = (0, 0)

    def __init__(self, parent=None, rows=4, columns=4, elm_width=100, elm_height=100):
        super(QWidget, self).__init__(parent)
        self.__rows = rows
        self.__columns = columns
        self.__layout = QGridLayout()
        self.__layout.setSpacing(10)
        self.__layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.__layout)
        self.__logic = Logic(rows=rows, columns=columns)
        self.__init_widgets(elm_width, elm_height)
        self.__render_matrix()

    def __init_widgets(self, width=100, height=100):
        self.__widgets = [[self.render_number(0, width, height) for _ in range(self.__rows)] for _ in
                          range(self.__columns)]
        for row in range(0, self.__rows):
            for column in range(0, self.__columns):
                self.__layout.addWidget(self.__widgets[row][column], row, column)

    def handle_key_press_event(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key_Up and self.latest_direction[1] != -1:
            self.__logic.turn_up()
            self.latest_direction = (0, -1)
        elif event.key() == QtCore.Qt.Key_Down and self.latest_direction[1] != 1:
            self.__logic.turn_down()
            self.latest_direction = (0, 1)
        elif event.key() == QtCore.Qt.Key_Left and self.latest_direction[0] != -1:
            self.__logic.turn_left()
            self.latest_direction = (-1, 0)
        elif event.key() == QtCore.Qt.Key_Right and self.latest_direction[0] != 1:
            self.__logic.turn_right()
            self.latest_direction = (1, 0)
        self.__render_matrix()

    def __render_matrix(self):
        matrix = self.__logic.matrix
        for row in range(0, self.__rows):
            for column in range(0, self.__columns):
                self.__widgets[row][column].set_value(matrix[row][column])

    @staticmethod
    def render_number(value, width=100, height=100) -> GameLabel:
        b = GameLabel(value)
        b.setFixedSize(width, height)
        b.setAlignment(Qt.AlignCenter)
        return b
