from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QDialog

from game.controls.label import GameLabel
from game.controls.overlay import Overlay
from game.logic import Logic


class GameDialog(QDialog):
    latest_direction = (0, 0, 0, 0)

    def __init__(self, parent=None, rows=4, columns=4):
        super(QDialog, self).__init__(parent)
        self.__overlay = None
        self.__done = False
        self.__rows = rows
        self.__columns = columns
        self.__layout = QGridLayout()
        self.__layout.setSpacing(10)
        self.__layout.setContentsMargins(10, 10, 10, 10)
        self.setLayout(self.__layout)
        width = (rows * 100 + 10) + rows * 10
        height = (columns * 100 + 10) + columns * 10
        self.setFixedSize(width, height)
        self.__logic = Logic(rows=rows, columns=columns)
        self.__init_widgets(100, 100)
        self.__render_matrix()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
        else:
            self.handle_key_press_event(event)

    def __init_widgets(self, width=100, height=100):
        self.__widgets = [
            [self.render_number(width, height) for _ in range(self.__rows)]
            for _ in range(self.__columns)
        ]
        for row in range(0, self.__rows):
            for column in range(0, self.__columns):
                self.__layout.addWidget(self.__widgets[row][column], row, column)

    def handle_key_press_event(self, event: QtGui.QKeyEvent):
        if self.__done:
            self.close()
        if event.key() == QtCore.Qt.Key_Up and self.latest_direction[0] != 1:
            self.make_turn(self.__logic.turn_up, (1, 0, 0, 0))
        elif event.key() == QtCore.Qt.Key_Down and self.latest_direction[1] != 1:
            self.make_turn(self.__logic.turn_down, (0, 1, 0, 0))
        elif event.key() == QtCore.Qt.Key_Left and self.latest_direction[2] != 1:
            self.make_turn(self.__logic.turn_left, (0, 0, 1, 0))
        elif event.key() == QtCore.Qt.Key_Right and self.latest_direction[3] != 1:
            self.make_turn(self.__logic.turn_right, (0, 0, 0, 1))
        self.__render_matrix()

    def make_turn(self, f, direction):
        avail, done = f()
        if not done and avail:
            self.latest_direction = direction
        elif not avail:
            self.no_moves()
        elif done:
            self.end_game()

    def end_game(self):
        self.__done = True
        self.latest_direction = (1, 1, 1, 1)
        if self.__overlay is None:
            self.__overlay = Overlay(parent=self)
            self.__overlay.normalMessage("Good job!", "Congratulations! Now turn off your computer and go sleep!")
            self.__overlay.show()

    def no_moves(self):
        self.__done = True
        self.latest_direction = (1, 1, 1, 1)
        if self.__overlay is None:
            self.__overlay = Overlay(parent=self)
            self.__overlay.errorMessage("Game over", "Pack your things and go away!")
            self.__overlay.show()

    def __render_matrix(self):
        matrix = self.__logic.matrix
        for row in range(0, self.__rows):
            for column in range(0, self.__columns):
                self.__widgets[row][column].set_value(matrix[row][column])

    @staticmethod
    def render_number(width=100, height=100) -> GameLabel:
        b = GameLabel()
        b.setFixedSize(width, height)
        b.setAlignment(Qt.AlignCenter)
        return b
