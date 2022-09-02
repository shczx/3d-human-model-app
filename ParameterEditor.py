from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QComboBox, QSlider, QSpinBox, QDoubleSpinBox, QHBoxLayout, QVBoxLayout
from QHLine import QHLine

class ParameterEditor(QWidget):
    def __init__(self, saveModel, paramChanged):
        super().__init__()

        self.setStyleSheet("font-size: 13px; font-family: Helvetica")

        top_widget = QWidget()
        top_widget.setStyleSheet("QLabel { font-weight: bold; font-size: 16px}")
        top_layout = QHBoxLayout()
        top_widget.setLayout(top_layout)
        top_layout.addWidget(QLabel("Parameters"))
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(saveModel)
        self.save_button.setEnabled(False)
        top_layout.addWidget(self.save_button, alignment=Qt.AlignRight)

        editor = QWidget(self)
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(15)
        editor.setLayout(grid_layout)

        grid_layout.addWidget(QLabel("Gender:"), 1, 1)
        self.gender_box = QComboBox()
        self.gender_box.addItems(["Male", "Female"])
        self.gender_box.currentIndexChanged.connect(lambda i: paramChanged("gender", i))
        self.gender_box.setEnabled(False)
        grid_layout.addWidget(self.gender_box, 1, 2)

        self.stature_box = QSpinBox()
        self.stature_box.setRange(1400, 2000)
        self.stature_box.setSingleStep(10)
        self.stature_box.setValue(1754)
        self.stature_box.setEnabled(False)
        self.stature_box.valueChanged.connect(lambda v: paramChanged("stature", v))
        grid_layout.addWidget(QLabel("Stature (mm):"), 2, 1)
        grid_layout.addWidget(self.stature_box, 2, 2)
        
        self.bmi_box = QDoubleSpinBox()
        self.bmi_box.setRange(19, 45)
        self.bmi_box.setSingleStep(0.1)
        self.bmi_box.setValue(28.5)
        self.bmi_box.setEnabled(False)
        self.bmi_box.valueChanged.connect(lambda v: paramChanged("bmi", v))
        grid_layout.addWidget(QLabel("BMI (kg/m^2):"), 3, 1)
        grid_layout.addWidget(self.bmi_box, 3, 2)

        self.age_box = QSpinBox()
        self.age_box.setRange(18, 80)
        self.age_box.setSingleStep(1)
        self.age_box.setValue(40)
        self.age_box.setEnabled(False)
        self.age_box.valueChanged.connect(lambda v: paramChanged("age", v))
        grid_layout.addWidget(QLabel("Age (YO):"), 4, 1)
        grid_layout.addWidget(self.age_box, 4, 2)

        self.shs_box = QDoubleSpinBox()
        self.shs_box.setRange(0.5, 0.54)
        self.shs_box.setSingleStep(0.01)
        self.shs_box.setValue(0.52)
        self.shs_box.setEnabled(False)
        self.shs_box.valueChanged.connect(lambda v: paramChanged("shs", v))
        grid_layout.addWidget(QLabel("Seated Height/Stature:"), 5, 1)
        grid_layout.addWidget(self.shs_box, 5, 2)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(top_widget)
        self.layout.addWidget(QHLine())
        self.layout.addWidget(editor)

    def setState(self, state):
        self.save_button.setEnabled(state)
        self.gender_box.setEnabled(state)
        self.stature_box.setEnabled(state)
        self.bmi_box.setEnabled(state)
        self.age_box.setEnabled(state)
        self.shs_box.setEnabled(state)
