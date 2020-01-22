#!/usr/bin/env python3
import sys
import random
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QHBoxLayout)
from PySide2.QtSvg import QSvgWidget
from PySide2.QtCore import Slot, Qt
from PySide2.QtGui import QPalette, QColor, QMovie

class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.hello = ["Hallo Welt", "你好，世界", "Hei maailma",
            "Hola Mundo", "Привет мир"]

        self.button = QPushButton("Click me!")
        self.text = QLabel("Hello World")
        self.text.setAlignment(Qt.AlignCenter)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        # Connecting the signal
        self.button.clicked.connect(self.magic)

    @Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    layout = QHBoxLayout()
    
    N = 3
    for n in range(0, N): 
        widget = QSvgWidget("sheep_white.svg")
        layout.addWidget(widget)
    
    for n in range(0, N): 
        widget = QSvgWidget("sheep_black.svg")
        layout.addWidget(widget)

    movie = QMovie("success.gif")
    processLabel = QLabel()
    processLabel.setMovie(movie)
    layout.addWidget(processLabel)
    movie.start()

    window.setLayout(layout)
    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())
