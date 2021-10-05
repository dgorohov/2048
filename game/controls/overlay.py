import pkg_resources
from PyQt5 import uic
from PyQt5.QtWidgets import QWidget

overlay_ui_path = pkg_resources.resource_filename(__name__, "overlay.ui")
GameOverlayClass = uic.loadUiType(overlay_ui_path)[0]


class Overlay(QWidget, GameOverlayClass):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)
        self.__error = False
        if parent is not None:
            self.setFixedSize(parent.width(), parent.height())

    def errorMessage(self, title, description):
        self.setMessage(title, description)
        self.setError(True)

    def normalMessage(self, title, description):
        self.setMessage(title, description)
        self.setError(False)

    def setMessage(self, title, description):
        self.overlayTitle.setText(title)
        self.overlayDescription.setText(description)

    def getError(self):
        return self.OverlayBackground.property("error")

    def setError(self, error):
        self.OverlayBackground.setProperty("error", error)
        self.setStyle(self.style())
