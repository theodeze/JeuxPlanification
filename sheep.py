import sys
import time
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QHBoxLayout,
                               QGridLayout, QScrollArea, QSpinBox,
                               QMessageBox, QTabWidget)
from PySide2.QtSvg import QSvgWidget
from PySide2.QtCore import Slot, Signal, Qt, QTimer
from PySide2.QtGui import QIcon, QPalette, QColor

class Sheep(QPushButton):
    BLACK = 0
    WHITE = 1
    EMPTY = 2
    IMG_SHEEP_BLACK = QIcon("img/sheep_black.svg")
    IMG_SHEEP_WHITE = QIcon("img/sheep_white.svg")

    def __init__(self, color):
        super().__init__()
        self.color = color 
        self.setMinimumHeight(100)
        self.changed_color(True, Qt.gray)
        if color == self.BLACK:
            self.setText("Noir")
            self.setIcon(self.IMG_SHEEP_BLACK)
        elif color == self.WHITE:
            self.setText("Blanc")
            self.setIcon(self.IMG_SHEEP_WHITE)

    def changed_color(self, actived=False, color=Qt.blue):
        pal = QPushButton().palette() # self.btn
        if actived:
            pal.setColor(QPalette.Button, QColor(color))
        elif self.good():
            pal.setColor(QPalette.Button, QColor(Qt.green))
        self.setPalette(pal)

class SheepGame(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layoutSheeps = QHBoxLayout()
        self.widgetSheeps = QWidget()
        self.update_sheep()
        self.widgetSheeps.setLayout(self.layoutSheeps)
        self.layout.addWidget(self.widgetSheeps)
        self.setLayout(self.layout)

    def update_sheep(self):
        size = 5
        for i in range(0, size // 2):
            self.layoutSheeps.addWidget(Sheep(Sheep.WHITE))
        self.layoutSheeps.addWidget(Sheep(Sheep.EMPTY))
        for i in range(0, size // 2):
            self.layoutSheeps.addWidget(Sheep(Sheep.BLACK))
