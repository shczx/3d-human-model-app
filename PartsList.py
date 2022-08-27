from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QCheckBox, QListWidget, QLabel, QListWidgetItem
from QHLine import QHLine

class PartsList(QWidget):
    def __init__(self, parent, selectedPartsChanged, alignStateChanged):
        super().__init__()

        self.setStyleSheet("font-size: 13px; font-family: Helvetica")

        top_widget = QWidget()
        top_widget.setStyleSheet("QLabel { font-weight: bold; font-size: 16px}")
        top_layout = QHBoxLayout()
        top_widget.setLayout(top_layout)
        top_layout.addWidget(QLabel("Parts"))
        self.align_button = QCheckBox("Align")
        self.align_button.setEnabled(False)
        self.align_button.stateChanged.connect(alignStateChanged)
        top_layout.addWidget(self.align_button, alignment=Qt.AlignRight)

        self.parts_list = QListWidget(parent)
        self.parts_list.setSelectionMode(QListWidget.ExtendedSelection)
        self.parts_list.installEventFilter(parent)
        self.parts_list.itemSelectionChanged.connect(selectedPartsChanged)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(top_widget)
        self.layout.addWidget(QHLine())
        self.layout.addWidget(self.parts_list)
    
    def getPartsList(self):
        return self.parts_list
    
    def getSelectedParts(self):
        return [p.row() for p in self.parts_list.selectedIndexes()]

    def addItem(self, part_name):
        pixmap = QPixmap(15, 15)
        pixmap.fill(QColor(147, 255, 62))
        self.parts_list.addItem(QListWidgetItem(QIcon(pixmap), "☑ " + part_name))

    def getItem(self, index):
        return self.parts_list.item(index)

    def setState(self, state):
        self.align_button.setChecked(state)
        self.align_button.setEnabled(state)

    def selectAll(self):
        self.parts_list.selectAll()