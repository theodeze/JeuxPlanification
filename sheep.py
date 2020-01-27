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
    selected = Signal(object)

    def __init__(self, color, position):
        super().__init__()
        self.color = color 
        self.position = position
        self.setMinimumHeight(100)
        self.changed_color(False)
        if color == self.BLACK:
            self.setText("Noir")
            self.setIcon(self.IMG_SHEEP_BLACK)
        elif color == self.WHITE:
            self.setText("Blanc")
            self.setIcon(self.IMG_SHEEP_WHITE)
        self.clicked.connect(self.select)

    def changed_color(self, actived=False, color=Qt.blue):
        pal = QPushButton().palette()
        if actived:
            pal.setColor(QPalette.Button, QColor(color))
        else:
            pal.setColor(QPalette.Button, QColor(Qt.gray))
        self.setPalette(pal)
    
    def select(self):
        self.selected.emit(self)

class SheepGame(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.n_move = 0

        self.title = QLabel()
        self.layout.addWidget(self.title)

        self.layoutSheeps = QHBoxLayout()
        self.widgetSheeps = QWidget()
        self.sheep_selected = None
        self.init_sheeps(5)
        self.update_title()
        self.update_sheep()
        self.widgetSheeps.setLayout(self.layoutSheeps)
        self.layout.addWidget(self.widgetSheeps)

        self.num = QSpinBox()
        self.num.setRange(3,7)
        self.num.setSingleStep(2)
        self.num.setValue(5)
        self.num.valueChanged.connect(self.modify_num_sheep)
        self.layout.addWidget(self.num)

        self.setLayout(self.layout)


    def is_victory(self):
        for x1 in range(len(self.sheeps)):
            for x2 in range(x1 + 1, len(self.sheeps)):
                if self.get_sheep(x1).color == Sheep.WHITE and self.get_sheep(x2).color == Sheep.BLACK:
                    return False
        return True

    def update_title(self):
        if self.is_victory():
            self.title.setText(f"Victoire en {self.n_move} tours")
            for sheep in self.sheeps:
                sheep.changed_color(True, Qt.green)
        else:
            self.title.setText(f"Tours {self.n_move}")
        
    def get_sheep(self, position):
        for sheep in self.sheeps:
            if sheep.position == position:
                return sheep
        return None

    def modify_num_sheep(self, size):
        for i in reversed(range(self.layoutSheeps.count())): 
            self.layoutSheeps.itemAt(i).widget().setParent(None)
        self.n_move = 0
        self.init_sheeps(size)
        self.update_sheep()
        self.update_title()

    def init_sheeps(self, size):
        self.sheeps = []
        for i in range(0, size // 2):
            self.sheeps.append(Sheep(Sheep.WHITE, i))
        self.sheeps.append(Sheep(Sheep.EMPTY, size // 2))
        for i in range(0, size // 2):
            self.sheeps.append(Sheep(Sheep.BLACK, i + 1 + size // 2))
        for sheep in self.sheeps:
            sheep.selected.connect(self.move)

    def move(self, sheep):
        if self.sheep_selected is None:
            self.sheep_selected = sheep
            self.sheep_selected.changed_color(True)
        elif self.sheep_selected == sheep:
            self.sheep_selected.changed_color(False)
            self.sheep_selected = None
        else:
            if self.move_possible(self.sheep_selected, sheep):
                self.switch(self.sheep_selected, sheep)
                self.n_move += 1
                self.sheep_selected.changed_color(False)
            else:
                self.sheep_selected.changed_color(True, Qt.red)
                QTimer.singleShot(1000, self.sheep_selected.changed_color)
            self.sheep_selected = None
        self.update_title()
        
    def switch(self, sheep1, sheep2):
        tmp = sheep1.position
        sheep1.position = sheep2.position
        sheep2.position = tmp
        self.update_sheep()

    def move_possible(self, sheep1, sheep2):
        dif = sheep1.position - sheep2.position
        if sheep2.color != Sheep.EMPTY:
            return False
        elif dif > 0 and abs(dif) <= 2 and sheep1.color == Sheep.BLACK:
            return True
        elif dif < 0 and abs(dif) <= 2  and sheep1.color == Sheep.WHITE:
            return True
        return False

    def update_sheep(self):
        for sheep in sorted(self.sheeps, key=lambda x: x.position):
            self.layoutSheeps.addWidget(sheep)
