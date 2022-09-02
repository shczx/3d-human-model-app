from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QDoubleSpinBox
from QHLine import QHLine

class OpacitySetting(QWidget):
    def __init__(self, opacityChanged):
        super().__init__()

        self.setStyleSheet("font-size: 13px; font-family: Helvetica")

        top_widget = QWidget()
        top_widget.setStyleSheet("QLabel { font-weight: bold; font-size: 16px}")
        top_layout = QHBoxLayout()
        top_widget.setLayout(top_layout)
        top_layout.addWidget(QLabel("Opacity"))

        editor = QWidget(self)
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(15)
        editor.setLayout(grid_layout)

        self.skt_box = QDoubleSpinBox()
        self.skt_box.setRange(0, 1)
        self.skt_box.setSingleStep(0.1)
        self.skt_box.setValue(1)
        self.skt_box.setEnabled(False)
        self.skt_box.valueChanged.connect(lambda v: opacityChanged(v, "skeleton"))
        grid_layout.addWidget(QLabel("Skeleton:"), 1, 1)
        grid_layout.addWidget(self.skt_box, 1, 2)

        self.skin_box = QDoubleSpinBox()
        self.skin_box.setRange(0, 1)
        self.skin_box.setSingleStep(1)
        self.skin_box.setValue(0.3)
        self.skin_box.setEnabled(False)
        self.skin_box.valueChanged.connect(lambda v: opacityChanged(v, "skin"))
        grid_layout.addWidget(QLabel("Skin Surface:"), 2, 1)
        grid_layout.addWidget(self.skin_box, 2, 2)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(top_widget)
        self.layout.addWidget(QHLine())
        self.layout.addWidget(editor)

    def setState(self, state):
        self.skt_box.setEnabled(state)
        self.skin_box.setEnabled(state)