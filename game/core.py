import pkg_resources
from PyQt5 import QtGui, QtCore, uic
from PyQt5.QtWidgets import QDialog

from game.main import GameDialog

main_ui_path = pkg_resources.resource_filename(__name__, "main.ui")
MainDialogClass = uic.loadUiType(main_ui_path)[0]


class MainDialog(QDialog, MainDialogClass):

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.setupUi(self)

        self.__game = None

        self.startButton.clicked.connect(self.start_game)

    def start_game(self):
        rows, columns = (4, 4) if self.buttonGroup.checkedButton() == self.fourPerFour else (8, 8)
        self.__game = GameDialog(parent=self, rows=rows, columns=columns)
        self.__game.exec_()

    def keyPressEvent(self, event: QtGui.QKeyEvent):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
