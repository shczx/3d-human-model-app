from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QSlider
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

        self.skt_slider = QSlider(Qt.Horizontal)
        self.skt_slider.setRange(0, 10)
        self.skt_slider.setSingleStep(1)
        self.skt_slider.setSliderPosition(10)
        self.skt_slider.setEnabled(False)
        self.skt_slider.valueChanged.connect(lambda v: (opacityChanged(v / 10, "skeleton"),
                                                        self.skt_label.setText(str(v / 10))))
        grid_layout.addWidget(QLabel("Skeleton:"), 1, 1)
        grid_layout.addWidget(self.skt_slider, 1, 2)
        self.skt_label = QLabel("1")
        grid_layout.addWidget(self.skt_label, 1, 3)

        self.skin_slider = QSlider(Qt.Horizontal)
        self.skin_slider.setRange(0, 10)
        self.skin_slider.setSingleStep(1)
        self.skin_slider.setSliderPosition(3)
        self.skin_slider.setEnabled(False)
        self.skin_slider.valueChanged.connect(lambda v: (opacityChanged(v / 10, "skin"),
                                                        self.skin_label.setText(str(v / 10))))
        grid_layout.addWidget(QLabel("Skin Surface:"), 2, 1)
        grid_layout.addWidget(self.skin_slider, 2, 2)
        self.skin_label = QLabel("0.3")
        grid_layout.addWidget(self.skin_label, 2, 3)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(top_widget)
        self.layout.addWidget(QHLine())
        self.layout.addWidget(editor)

    def setState(self, state):
        self.skt_slider.setEnabled(state)
        self.skin_slider.setEnabled(state)