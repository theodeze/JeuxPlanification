import sys
import time
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QHBoxLayout,
                               QGridLayout, QScrollArea, QSpinBox,
                               QMessageBox, QTabWidget, QSizePolicy,
                               QSpacerItem)
from PySide2.QtSvg import QSvgWidget
from PySide2.QtCore import Slot, Signal, Qt, QTimer
from PySide2.QtGui import QIcon, QPalette, QColor

class Bucket(QWidget):
    IMG_EMPTY = QIcon("img/Empty_bucket.svg")
    IMG_FULL = QIcon("img/Full_bucket.svg")
    IMG_HALF = QIcon("img/Half_full_bucket.svg")
    selected = Signal(object)
    removed = Signal(object)
    
    def __init__(self, capacity, init, goal):
        super().__init__()
        self.capacity = capacity
        self.init = init
        self.current = init
        self.goal = goal
        self.editable = False
        self.btn = QPushButton()
        self.btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.btn.clicked.connect(self.select)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.btn)

        self.btn_remove = QPushButton("X")
        self.btn_remove.clicked.connect(self.remove)
        self.layout.addWidget(self.btn_remove)

        self.edit_capacity = QSpinBox()
        self.edit_capacity.setPrefix("Capacity ")
        self.edit_capacity.setSuffix(" L")
        self.edit_capacity.valueChanged.connect(self.change_capacity)
        self.layout.addWidget(self.edit_capacity)
        self.edit_capacity.hide()
        self.edit_init = QSpinBox()
        self.edit_init.setPrefix("Init ")
        self.edit_init.setSuffix(" L")
        self.edit_init.valueChanged.connect(self.change_init)
        self.layout.addWidget(self.edit_init)
        self.edit_init.hide()
        self.edit_goal = QSpinBox()
        self.edit_goal.setPrefix("Goal ")
        self.edit_goal.setSuffix(" L")
        self.edit_goal.valueChanged.connect(self.change_goal)
        self.layout.addWidget(self.edit_goal)
        self.edit_goal.hide()
        self.update()
        self.setLayout(self.layout)

    def switch_editable(self):
        self.editable = not self.editable
        if self.editable:
            self.edit_capacity.show()
            self.edit_init.show()
            self.edit_goal.show()
            self.btn.setEnabled(False)
        else:
            self.edit_capacity.hide()
            self.edit_init.hide()
            self.edit_goal.hide()
            self.btn.setEnabled(True)

    def change_capacity(self, capacity):
        self.capacity = capacity
        self.update()

    def change_init(self, init):
        self.init = init
        self.current = init
        self.update()

    def change_goal(self, goal):
        self.goal = goal
        self.update()

    def reset(self):
        self.current = self.init
        self.update()

    def remove(self):
        self.removed.emit(self)

    def select(self):
        self.selected.emit(self)

    def update(self):
        self.update_spin()
        self.update_image()
        self.update_text()

    def update_spin(self):
        self.edit_capacity.setValue(self.capacity)
        self.edit_capacity.setMinimum(self.init)
        self.edit_init.setValue(self.init)
        self.edit_init.setMaximum(self.capacity)
        self.edit_goal.setValue(self.goal)
        self.edit_goal.setMaximum(self.capacity)

    def update_text(self):
        self.btn.setText(f"{self.current} ({self.goal}) / {self.capacity} L")

    def update_image(self):
        if self.current == 0:
            self.btn.setIcon(self.IMG_EMPTY)
        elif  self.current == self.capacity:
            self.btn.setIcon(self.IMG_FULL)
        else:
            self.btn.setIcon(self.IMG_HALF)

    def emptying(self, bucket):
        value = min([self.current, bucket.capacity - bucket.current])
        self.current -= value
        self.update()
        bucket.current += value
        bucket.update()

    def full(self):
        return self.capacity == self.current

    def good(self):
        return self.goal == self.current

    def changed_color(self, actived=False, color=Qt.blue):
        pal = QPushButton().palette() # self.btn
        if actived:
            pal.setColor(QPalette.Button, QColor(color))
        elif self.good():
            pal.setColor(QPalette.Button, QColor(Qt.green))
        self.btn.setPalette(pal)

        
class BucketGame(QWidget):

    def __init__(self):
        super().__init__()
        self.buckets = []
        self.add = QPushButton("+")
        self.solve = QPushButton("Solve")
        self.edit = QPushButton("Edit")
        self.reset = QPushButton("Reset")
        self.layout = QGridLayout()
        self.main_layout = QVBoxLayout()

        self.n_move = 0
        self.title = QLabel()
        self.main_layout.addWidget(self.title)

        self.btn_layout = QHBoxLayout()

        self.main_layout.addLayout(self.layout)

        self.btn_layout.addWidget(self.add)
        self.btn_layout.addWidget(self.solve)
        self.btn_layout.addWidget(self.edit)
        self.btn_layout.addWidget(self.reset)
        self.main_layout.addLayout(self.btn_layout)

        self.setLayout(self.main_layout)
        self.update_layout()
        self.bucket_selected = None
        self.add.clicked.connect(self.new_bucket)
        self.solve.clicked.connect(self.to_solve)
        self.reset.clicked.connect(self.reset_all)
        self.edit.clicked.connect(self.edit_all)

    def reset_all(self):
        for b in self.buckets:
            b.reset()

    def edit_all(self):
        if self.is_possible():
            for b in self.buckets:
                b.switch_editable()
            self.n_move = 0
        else:
            QMessageBox.warning(self, "Attention", f"Le problème est insoluble")  

    def is_possible(self):
        total_init = sum([b.init for b in self.buckets])
        total_goal = sum([b.goal for b in self.buckets])
        return total_init == total_goal

    def update_layout(self):
        i = 0
        max_columns = 4
        self.layout.removeWidget(self.add)
        for bucket in self.buckets:
            self.layout.removeWidget(bucket)
            self.layout.addWidget(bucket, i // max_columns, i % max_columns)
            i += 1
        if i % max_columns > 0:
            self.layout.addItem(QSpacerItem(1, 1, QSizePolicy.Expanding, QSizePolicy.Expanding), i // max_columns, i % max_columns, i // max_columns, max_columns)

    def add_bucket(self, bucket):
        self.buckets.append(bucket)
        bucket.selected.connect(self.select)
        bucket.removed.connect(self.remove)
        self.update_layout()
        self.update_title()
    
    def new_bucket(self):
        self.add_bucket(Bucket(0, 0, 0))

    def remove(self, bucket):
        self.buckets.remove(bucket)
        self.layout.removeWidget(bucket)
        bucket.hide()
        self.update_layout()

    def select(self, bucket):
        if self.bucket_selected is None:
            if bucket.current == 0:
                bucket.changed_color(True, Qt.red)
                QTimer.singleShot(1000, bucket.changed_color)
            else:
                bucket.changed_color(True)
                self.bucket_selected = bucket
        elif self.bucket_selected == bucket:
            bucket.changed_color(False)
            self.bucket_selected = None
        elif bucket.full():
            bucket.changed_color(True, Qt.red)
            QTimer.singleShot(1000, bucket.changed_color)
        else:
            self.bucket_selected.emptying(bucket)
            self.bucket_selected.changed_color(False)
            self.bucket_selected = None    
            self.n_move += 1
            bucket.changed_color(False)
        self.update_title()

    def is_victory(self):
        for b in self.buckets:
            if not b.good():
                return False
        return True

    def update_title(self):
        if self.is_victory():
            self.title.setText(f"Victoire en {self.n_move} tours")
            #for bucket in self.buckets:
            #    bucket.changed_color(True, Qt.green)
        else:
            self.title.setText(f"Tours {self.n_move}")


    def move_auto(self, transfered, total_steps, i = 1):
        transfer = transfered[i]
        self.select(self.buckets[transfer[0] - 1])
        self.select(self.buckets[transfer[1] - 1])
        self.update_layout()
        self.update_title()
        if i != total_steps:
            QTimer.singleShot(500, lambda: self.move_auto(transfered, total_steps, i + 1))

    def to_solve(self):
        from minizinc import Instance, Model, Solver
        seaux = Model("./seaux.mzn")
        gecode = Solver.lookup("gecode")
        instance = Instance(gecode, seaux)
        instance["N"] = len(self.buckets)
        instance["init"] = [b.current for b in self.buckets] 
        instance["storage"] = [b.capacity for b in self.buckets] 
        instance["goal"] = [b.goal for b in self.buckets] 
        result = instance.solve()
        if result is not None:
            print(result)
            #QMessageBox.information(self, "Solution", f"Le problème peut être résoulu en {result['total_steps']}")
            self.move_auto(result["transfered"], result["total_steps"] - 1)
        else:
            QMessageBox.information(self, "Solution", f"Le problème est insoluble")