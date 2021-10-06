from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QLabel


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

    sizes = {
        1: 30,
        2: 30,
        3: 20,
        4: 15
    }

    def __init__(self, width=100, height=100):
        super().__init__()
        self.__value = None
        self.__width = width
        self.__height = height
        self.__animation = QtCore.QPropertyAnimation(self, b"size")
        self.__animation.setDuration(1000)
        self.__animation.setStartValue(QSize(10, 10))
        self.__animation.setEndValue(QSize(self.__width, self.__height))

    def set_value(self, value: int):
        if value != self.__value:
            self.__value = value
            self.setText(f"{value}")
            n = len(str(value))
            self.setStyleSheet(
                f"background-color: {self.background_colors[value if value in self.background_colors else 0]};"
                f"font-size: {self.sizes[n]}px;"
                f"color: {self.colors[value if value in self.colors else 0]}")

    def animate(self):
        self.__animation.start()