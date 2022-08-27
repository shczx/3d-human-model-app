from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout, QComboBox, QSlider, QHBoxLayout, QVBoxLayout
from QHLine import QHLine

class ParameterEditor(QWidget):
    def __init__(self, updateModel, saveModel, paramChanged):
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

        self.stature_slider = QSlider(Qt.Horizontal)
        self.stature_slider.setRange(1400, 2000)
        self.stature_slider.setSingleStep(1)
        self.stature_slider.setSliderPosition(1754)
        self.stature_slider.setEnabled(False)
        self.stature_slider.valueChanged.connect(lambda v: (paramChanged("stature", v),
                                                       self.stature_label.setText(str(v))))
        self.stature_slider.sliderReleased.connect(updateModel)
        grid_layout.addWidget(QLabel("Stature (mm):"), 2, 1)
        grid_layout.addWidget(self.stature_slider, 2, 2)
        self.stature_label = QLabel("1754")
        grid_layout.addWidget(self.stature_label, 2, 3)
        
        self.bmi_slider = QSlider(Qt.Horizontal)
        self.bmi_slider.setRange(190, 450)
        self.bmi_slider.setSingleStep(1)
        self.bmi_slider.setSliderPosition(285)
        self.bmi_slider.setEnabled(False)
        self.bmi_slider.valueChanged.connect(lambda v: (paramChanged("bmi", v),
                                                   self.bmi_label.setText(str(v / 10))))
        self.bmi_slider.sliderReleased.connect(updateModel)
        grid_layout.addWidget(QLabel("BMI (kg/m^2):"), 3, 1)
        grid_layout.addWidget(self.bmi_slider, 3, 2)
        self.bmi_label = QLabel("28.5")
        grid_layout.addWidget(self.bmi_label, 3, 3)

        self.age_slider = QSlider(Qt.Horizontal)
        self.age_slider.setRange(18, 80)
        self.age_slider.setSingleStep(1)
        self.age_slider.setSliderPosition(40)
        self.age_slider.setEnabled(False)
        self.age_slider.valueChanged.connect(lambda v: (paramChanged("age", v),
                                                   self.age_label.setText(str(v))))
        self.age_slider.sliderReleased.connect(updateModel)
        grid_layout.addWidget(QLabel("Age (YO):"), 4, 1)
        grid_layout.addWidget(self.age_slider, 4, 2)
        self.age_label = QLabel("40")
        grid_layout.addWidget(self.age_label, 4, 3)

        self.shs_slider = QSlider(Qt.Horizontal)
        self.shs_slider.setRange(50, 54)
        self.shs_slider.setSingleStep(1)
        self.shs_slider.setSliderPosition(52)
        self.shs_slider.setEnabled(False)
        self.shs_slider.valueChanged.connect(lambda v: (paramChanged("shs", v),
                                                   self.shs_label.setText(str(v / 100))))
        self.shs_slider.sliderReleased.connect(updateModel)
        grid_layout.addWidget(QLabel("Seated Height/Stature:"), 5, 1)
        grid_layout.addWidget(self.shs_slider, 5, 2)
        self.shs_label = QLabel("0.52")
        grid_layout.addWidget(self.shs_label, 5, 3)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(top_widget)
        self.layout.addWidget(QHLine())
        self.layout.addWidget(editor)

    def setState(self, state):
        self.save_button.setEnabled(state)
        self.gender_box.setEnabled(state)
        self.stature_slider.setEnabled(state)
        self.bmi_slider.setEnabled(state)
        self.age_slider.setEnabled(state)
        self.shs_slider.setEnabled(state)
