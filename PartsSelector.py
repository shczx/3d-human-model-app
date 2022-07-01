from ctypes import alignment
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QCheckBox, QVBoxLayout


class PartsSelector(QWidget):
    """A checkbox widget enabling user to show or hide a particular part"""
    def __init__(self, show_hide):
        super().__init__()
        self.checkbox = QCheckBox("Check me")
        part_id = 10000
        self.checkbox.stateChanged.connect(lambda s: show_hide(s, part_id))
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.checkbox)
        self.setLayout(layout)