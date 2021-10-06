import sys

import pkg_resources
from PyQt5 import QtWidgets

from game.core import MainDialog


def main():
    app = QtWidgets.QApplication(sys.argv)

    css_path = pkg_resources.resource_filename(__name__, "stylesheet.css")
    with open(css_path, encoding="UTF-8") as css_file:
        app.setStyleSheet(css_file.read())

    dlg = MainDialog()
    dlg.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
