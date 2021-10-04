import sys

from PyQt5.QtWidgets import QApplication

from game.core import Window


def main():
    app = QApplication(sys.argv)
    game = Window()
    game.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
