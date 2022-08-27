from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QCheckBox, QGridLayout, QVBoxLayout
from QHLine import QHLine

class SavedModel(QWidget):
    def __init__(self, gender, stature, bmi, age, shs, handleStateChanged):
        super().__init__()

        self.setStyleSheet("font-size: 13px; font-family: Helvetica")
 
        top_widget = QWidget()
        top_widget.setStyleSheet("QLabel { font-weight: bold; font-size: 16px}")
        top_layout = QHBoxLayout()
        top_widget.setLayout(top_layout)
        top_layout.addWidget(QLabel("Saved Model"))
        self.display_button = QCheckBox("Show")
        self.display_button.stateChanged.connect(handleStateChanged)
        top_layout.addWidget(self.display_button, alignment=Qt.AlignRight)

        info = QWidget(self)
        grid_layout = QGridLayout()
        grid_layout.setVerticalSpacing(15)
        info.setLayout(grid_layout)

        grid_layout.addWidget(QLabel("Gender:"), 1, 1)
        self.gender_label = QLabel(gender)
        grid_layout.addWidget(self.gender_label, 1, 2, alignment=Qt.AlignRight)

        grid_layout.addWidget(QLabel("Stature (mm):"), 2, 1)
        self.stature_label = QLabel(stature)
        grid_layout.addWidget(self.stature_label, 2, 2, alignment=Qt.AlignRight)

        grid_layout.addWidget(QLabel("BMI (kg/m^2):"), 3, 1)
        self.bmi_label = QLabel(bmi)
        grid_layout.addWidget(self.bmi_label, 3, 2, alignment=Qt.AlignRight)

        grid_layout.addWidget(QLabel("Age (YO):"), 4, 1)
        self.age_label = QLabel(age)
        grid_layout.addWidget(self.age_label, 4, 2, alignment=Qt.AlignRight)

        grid_layout.addWidget(QLabel("Seated Height/Stature:"), 5, 1)
        self.shs_label = QLabel(shs)
        grid_layout.addWidget(self.shs_label, 5, 2, alignment=Qt.AlignRight)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(top_widget)
        self.layout.addWidget(QHLine())
        self.layout.addWidget(info)
    
    def setSavedParameters(self, gender, stature, bmi, age, shs):
        self.gender_label.setText(gender)
        self.stature_label.setText(stature)
        self.bmi_label.setText(bmi)
        self.age_label.setText(age)
        self.shs_label.setText(shs)

    def setState(self, state):
        self.display_button.setEnabled(state)
