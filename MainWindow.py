from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QLabel, QWidget, QToolBar, QAction 
from PartsSelector import PartsSelector
from pyvistaqt import QtInteractor
import pyvista as pv
#from ModelHandler import ModelHandler


class MainWindow(QMainWindow):
    """Main window of the application"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Human Model App")

        layout = QHBoxLayout()
        self.checkbox = PartsSelector(self.show_hide)
        layout.addWidget(self.checkbox, stretch=1)
        self.plotter = QtInteractor()
        layout.addWidget(self.plotter.interactor, stretch=3)
        self.actor = self.plotter.add_mesh(pv.Sphere())
        widget = QWidget()
        widget.setLayout(layout)

        self.setMinimumSize(1000, 600)
        self.setCentralWidget(widget)

        self.createToolBar()

    def createToolBar(self):
        toolbar = QToolBar()
        toolbar.setFont(QFont("Helvetica", 16))
        self.addToolBar(toolbar)

        view_xy = QAction("view xy", self)
        view_xy.triggered.connect(lambda: self.plotter.view_xy())
        toolbar.addAction(view_xy)

        view_yz = QAction("view yz", self)
        view_yz.triggered.connect(lambda: self.plotter.view_yz())
        toolbar.addAction(view_yz)

        view_xz = QAction("view xz", self)
        view_xz.triggered.connect(lambda: self.plotter.view_xz())
        toolbar.addAction(view_xz)

        fit_window = QAction("fit", self)
        fit_window.triggered.connect(lambda: self.plotter.reset_camera())
        toolbar.addAction(fit_window)

        zoom_in = QAction("zoom in", self)
        zoom_in.triggered.connect(lambda: self.plotter.camera.zoom(1.25))
        toolbar.addAction(zoom_in)

        zoom_out = QAction("zoom out", self)
        zoom_out.triggered.connect(lambda: self.plotter.camera.zoom(0.8))
        toolbar.addAction(zoom_out)

    def show_hide(self, state, part_id):
        """Handle the event when the parts checkbox is checked"""
        if state == Qt.Checked:
            self.actor.SetVisibility(True)
        else:
            self.actor.SetVisibility(False)

    def view_xy(self):
        self.plotter.view_xy()


def main():
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec_()

if __name__ == "__main__":
    main()