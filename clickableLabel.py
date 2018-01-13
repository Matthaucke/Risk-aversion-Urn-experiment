from PyQt4.QtCore import *
from PyQt4.QtGui import *

class ClickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self,mouseEvent):
        self.clicked.emit()
    def dragenable(self):
        self.setDragEnabled(True)
