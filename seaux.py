#!/usr/bin/env python3

import sys
import time
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QHBoxLayout,
                               QGridLayout, QScrollArea, QSpinBox,
                               QMessageBox, QTabWidget)
from PySide2.QtSvg import QSvgWidget
from PySide2.QtCore import Slot, Signal, Qt, QTimer
from PySide2.QtGui import QIcon, QPalette, QColor


from bucket import BucketGame
from sheep import SheepGame

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QTabWidget()

    window.addTab(BucketGame(), "Jeux du seaux")
    window.addTab(SheepGame(), "Jeux du saut mouton")

    window.resize(800, 600)
    window.show()

    sys.exit(app.exec_())
