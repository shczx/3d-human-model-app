from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QFont, QPixmap, QColor, QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QToolBar,
    QAction,
    QFileDialog,
    QDialog,
    QMenu,
)
from pyqt_color_picker import ColorPickerDialog
from pyvistaqt import QtInteractor
from qd.cae.dyna import KeyFile, Element
import pyvista as pv
import numpy as np
from scipy.io import loadmat
from ParameterEditor import ParameterEditor
from PartsList import PartsList
from SavedModel import SavedModel
from OpacitySetting import OpacitySetting


class MainWindow(QMainWindow):
    """Main window of the application"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Human Model App")

        main_widget = QWidget()
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)
        self.parts_list = PartsList(self, self.handleSelectedPartsChanged, self.handleAlignStateChanged)
        left_layout.addWidget(self.parts_list, stretch=2)
        self.opacity_setting = OpacitySetting(self.handleOpacityChanged)
        left_layout.addWidget(self.opacity_setting, stretch=1, alignment=Qt.AlignTop)
        main_layout.addWidget(left_widget, stretch=1)

        self.plotter = QtInteractor(self)
        self.plotter.show_axes()
        main_layout.addWidget(self.plotter.interactor, stretch=4)

        right_widget = QWidget()
        self.right_layout = QVBoxLayout()
        right_widget.setLayout(self.right_layout)
        self.param_widget = ParameterEditor(self.updateModel, self.saveModel, self.handleParamChanged)
        self.right_layout.addWidget(self.param_widget, stretch=1, alignment=Qt.AlignTop)
        main_layout.addWidget(right_widget, stretch=1)

        self.setMinimumSize(1400, 700)
        self.setCentralWidget(main_widget)

        self.createMenuBar()
        self.createToolBar()

        # Read in regression data matrices
        data = loadmat("hermes_stat_model_no_gpa_2022_07_26.mat")
        self.A_f = np.array(data["A_f"])
        self.A_m = np.array(data["A_m"])
        self.mu_f = np.array(data["mu_f"])
        self.mu_m = np.array(data["mu_m"])

        self.file = None
        self.parts = []
        self.meshes = []
        self.actors = []
        self.selected_parts = []
        self.saved_meshes = []
        self.saved_actors = []
        self.aligned_actor = None
        self.aligned_part = None
        self.params = {"gender": 1, "stature": 1754, "bmi": 28.5, "age": 40, "shs": 0.52}
        self.visibility = []
        self.saved_model_shown = False
        self.prev_camera = None
        self.coords = None
        self.id_to_index = {}

    def createToolBar(self):
        toolbar = QToolBar(self)
        toolbar.setFont(QFont("Helvetica", 13))
        self.addToolBar(toolbar)

        view_front = QAction("Front View", self)
        view_front.triggered.connect(lambda: self.setFrontView())
        toolbar.addAction(view_front)

        view_left = QAction("Left View", self)
        view_left.triggered.connect(lambda: self.plotter.view_xz())
        toolbar.addAction(view_left)

        view_right = QAction("Right View", self)
        view_right.triggered.connect(lambda: self.setRightView())
        toolbar.addAction(view_right)

        fit_window = QAction("Fit", self)
        fit_window.triggered.connect(lambda: self.plotter.reset_camera())
        toolbar.addAction(fit_window)

        zoom_in = QAction("Zoom in", self)
        zoom_in.triggered.connect(lambda: self.plotter.camera.zoom(1.25))
        toolbar.addAction(zoom_in)

        zoom_out = QAction("Zoom out", self)
        zoom_out.triggered.connect(lambda: self.plotter.camera.zoom(0.8))
        toolbar.addAction(zoom_out)

    def setFrontView(self):
        self.plotter.camera_position = [(-2938.982763458312, -2.1489028930664062, 150),
                                        (324.42564392089844, -2.1489028930664062, 150),
                                        (0.0, 0.0, 1.0)]
        self.plotter.reset_camera()

    def setRightView(self):
        self.plotter.camera_position = [(-324.42564392089844, 3265.557310272277, 235.68580627441406),
                                        (-324.42564392089844, 2.1489028930664062, 235.68580627441406),
                                        (0.0, 0.0, 1.0)]
        self.plotter.reset_camera()

    def createMenuBar(self):
        menu_bar = self.menuBar()
        menu_bar.setFont(QFont("Helvetica", 13))
        self.open_action = QAction("&Open Default", self)
        self.open_action.triggered.connect(self.loadDefault)
        self.export_action = QAction("&Export", self)
        self.export_action.triggered.connect(self.exportModel)
        self.export_action.setEnabled(False)
        
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.export_action)
    
    def loadModel(self, filename):
        self.file = KeyFile(filename, parse_mesh=True)
        nodes = np.matmul(self.A_m, np.array([[1.0, 1754, 28.5, 40, 0.52]]).transpose()).transpose() + self.mu_m
        self.coords = nodes.reshape(-1, 3)
        self.id_to_index = {id: i for i, id in enumerate(self.file.get_node_ids())}

        for part in self.file.get_parts():
            part_nodes = np.zeros(shape=(part.get_nNodes(), 3))
            for i, id in enumerate(part.get_node_ids()):
                part_nodes[i] = self.coords[self.id_to_index[id]]

            node_ids = [n.get_id() for n in part.get_nodes()]
            node_dict = {id: i for i, id in enumerate(node_ids)}

            tria_nodes = part.get_element_node_ids(Element.shell, nNodes=3)
            for row in tria_nodes:
                for col in range(3):
                    row[col] = node_dict[row[col]]
            faces3 = np.full((tria_nodes.shape[0], tria_nodes.shape[1]+1), 3)
            faces3[:, 1:] = tria_nodes

            quad_nodes = part.get_element_node_ids(Element.shell, nNodes=4)
            for row in quad_nodes:
                for col in range(4):
                    row[col] = node_dict[row[col]]
            faces4 = np.full((quad_nodes.shape[0], quad_nodes.shape[1]+1), 4)
            faces4[:, 1:] = quad_nodes
            
            faces = np.concatenate((faces3.flatten(), faces4.flatten()))

            mesh = pv.PolyData(part_nodes, faces)
            #smooth = mesh.smooth(200)
            if 'Skin' in part.get_name() or 'Shoe' in part.get_name():
                #actor = self.plotter.add_mesh(smooth, opacity=0.3)
                actor = self.plotter.add_mesh(mesh, opacity=0.3, color="#93ff3e")
            else:
                #actor = self.plotter.add_mesh(smooth)
                actor = self.plotter.add_mesh(mesh, color="#93ff3e")

            self.meshes.append(mesh)
            self.actors.append(actor)
            self.parts.append(part.get_name())
            self.visibility.append(True)

            self.parts_list.addItem(part.get_name())

    def loadDefault(self):
        # fname, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Keyword Files (*.k)")
        self.setFrontView()
        self.loadModel("./HERMES_M50_Disp.k")
        self.param_widget.setState(True)
        self.opacity_setting.setState(True)
        self.open_action.setEnabled(False)
        self.export_action.setEnabled(True)

    def handleParamChanged(self, field, value):
        if field == "gender":
            self.params["gender"] = 1 - value
            self.updateModel()
        elif field == "age" or field == "stature":
            self.params[field] = value
        elif field == "bmi":
            self.params[field] = value / 10
        else:
            self.params[field] = value / 100

    def updateModel(self):
        para_matrix = np.array([[1.0,
                                 self.params["stature"],
                                 self.params["bmi"],
                                 self.params["age"],
                                 self.params["shs"]
                               ]])
        if self.params["gender"] == 0:
            A = self.A_f
            mu = self.mu_f
        else:
            A = self.A_m
            mu = self.mu_m
        
        pred_coords = np.matmul(A, para_matrix.transpose()).transpose() + mu
        pred_coords = np.reshape(pred_coords, (-1, 3))
        self.coords = pred_coords

        for i, part in enumerate(self.file.get_parts()):
            part_nodes = np.zeros(shape=(part.get_nNodes(), 3))
            for j, id in enumerate(part.get_node_ids()):
                part_nodes[j] = pred_coords[self.id_to_index[id]]
            self.plotter.update_coordinates(part_nodes, self.meshes[i])

    def saveModel(self):
        if not self.meshes:
            return

        if self.params["gender"] == 1:
            str_gender = "Male"
        else:
            str_gender = "Female"

        if not self.saved_meshes:
            self.saved_model = SavedModel(str_gender,
                                          str(self.params["stature"]),
                                          str(self.params["bmi"]),
                                          str(self.params["age"]),
                                          str(self.params["shs"]),
                                          self.handleDisplayStateChanged)
            self.right_layout.addWidget(self.saved_model, stretch=2, alignment=Qt.AlignTop)
        else:
            self.saved_model.setSavedParameters(str_gender,
                                                str(self.params["stature"]),
                                                str(self.params["bmi"]),
                                                str(self.params["age"]),
                                                str(self.params["shs"]))

        for actor in self.saved_actors:
            self.plotter.remove_actor(actor)
        self.saved_actors = []
        
        self.saved_meshes = []
        for mesh in self.meshes:
            self.saved_meshes.append(mesh.copy())

        for i, mesh in enumerate(self.saved_meshes):
            if "Skin" in self.parts[i] or "Shoe" in self.parts[i]:
                actor = self.plotter.add_mesh(mesh, color="#ff87f3", opacity=0.3)
            else:
                actor = self.plotter.add_mesh(mesh, color="#ff87f3")
            actor.SetVisibility(False)
            self.saved_actors.append(actor)
 
    def handleDisplayStateChanged(self, s):
        if s == Qt.Checked:
            self.saved_model_shown = True
            for i, actor in enumerate(self.saved_actors):
                if self.visibility[i]:
                    actor.SetVisibility(True)
        else:
            self.saved_model_shown = False
            for i, actor in enumerate(self.saved_actors):
                if self.visibility[i]:
                    actor.SetVisibility(False)

    def handleSelectedPartsChanged(self):
        self.selected_parts = self.parts_list.getSelectedParts()

    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.parts_list.getPartsList():
            if not self.meshes:
                return True

            menu = QMenu()

            align_action = QAction("Align", self)
            align_action.triggered.connect(self.alignPart)

            if self.aligned_part is not None:
                if not (len(self.selected_parts) == 1 and self.selected_parts[0] == self.aligned_part):
                    menu.addAction(align_action)
                exit_align_action = QAction("Exit Align Mode", self)
                exit_align_action.triggered.connect(self.exitAlignMode)
                menu.addAction(exit_align_action)
            else:
                show_parts_action = QAction("Show", self)
                show_parts_action.triggered.connect(lambda: self.show_hide(True))
                menu.addAction(show_parts_action)
                if self.saved_actors and len(self.selected_parts) == 1:
                    menu.addAction(align_action)
                hide_parts_action = QAction("Hide", self)
                hide_parts_action.triggered.connect(lambda: self.show_hide(False))
                menu.addAction(hide_parts_action)
                set_color_action = QAction("Set Color", self)
                set_color_action.triggered.connect(self.launchColorPickerDialog)
                menu.addAction(set_color_action)
                select_all_action = QAction("Select All", self)
                select_all_action.triggered.connect(self.parts_list.selectAll)
                menu.addAction(select_all_action)

            menu.exec_(event.globalPos())
            return True

        return super().eventFilter(source, event)

    def launchColorPickerDialog(self):
        dialog = ColorPickerDialog()
        reply = dialog.exec() 
        if reply == QDialog.Accepted: 
            color = dialog.getColor()
            for part in self.selected_parts:
                r, g, b = color.red(), color.green(), color.blue() 
                pixmap = QPixmap(15, 15)
                pixmap.fill(QColor(r, g, b))
                self.parts_list.getItem(part).setIcon(QIcon(pixmap))
                self.actors[part].GetProperty().SetColor(r / 255, g / 255, b / 255)

    def show_hide(self, state):
        if state:
            prev_icon = "☐"
            new_icon = "☑"
        else:
            prev_icon = "☑"
            new_icon = "☐"
        
        if self.saved_model_shown:
            for part in self.selected_parts:
                self.parts_list.getItem(part).setText(self.parts_list.getItem(part).text().replace(prev_icon, new_icon))
                self.actors[part].SetVisibility(state)
                self.saved_actors[part].SetVisibility(state)
                self.visibility[part] = state
        else:
            for part in self.selected_parts:
                self.parts_list.getItem(part).setText(self.parts_list.getItem(part).text().replace(prev_icon, new_icon))
                self.actors[part].SetVisibility(state)
                self.visibility[part] = state

    def alignPart(self):
        if self.aligned_actor is not None:
            self.plotter.remove_actor(self.aligned_actor)
            self.aligned_actor = None
        else:
            self.prev_camera = self.plotter.camera_position

        self.param_widget.setState(False)
        self.saved_model.setState(False)
        self.opacity_setting.setState(False)

        self.aligned_part = self.selected_parts[0]
        for i in range(len(self.parts)):
            if i != self.aligned_part:
                self.actors[i].SetVisibility(False)
            else:
                self.actors[i].SetVisibility(True)
            self.saved_actors[i].SetVisibility(False)

        cur_center = self.meshes[self.aligned_part].center
        saved_center = self.saved_meshes[self.aligned_part].center
        dir = (cur_center[0] - saved_center[0],
               cur_center[1] - saved_center[1],
               cur_center[2] - saved_center[2])
        self.aligned_actor = self.plotter.add_mesh(self.saved_meshes[self.aligned_part].translate(dir, inplace=False), color="#ff87f3")
        self.setFrontView()
        self.parts_list.setState(True)

    def handleAlignStateChanged(self, state):
        if state == Qt.Checked:
            self.saved_actors[self.aligned_part].SetVisibility(False)
            self.aligned_actor.SetVisibility(True)
        else:
            self.aligned_actor.SetVisibility(False)
            self.saved_actors[self.aligned_part].SetVisibility(True)

    def exitAlignMode(self):
        self.parts_list.setState(False)
        self.saved_actors[self.aligned_part].SetVisibility(False)

        self.plotter.remove_actor(self.aligned_actor)

        self.aligned_part = None
        self.aligned_actor = None

        if self.saved_model_shown:
             for i in range(len(self.actors)):
                if self.visibility[i]:
                    self.actors[i].SetVisibility(True)
                    self.saved_actors[i].SetVisibility(True)
        else:
            for i in range(len(self.actors)):
                if self.visibility[i]:
                    self.actors[i].SetVisibility(True)

        self.plotter.camera_position = self.prev_camera
        self.prev_camera = None

        self.param_widget.setState(True)
        self.saved_model.setState(True)
        self.opacity_setting.setState(True)

    def exportModel(self):
        """Export model to .k file."""
        output_dir = QFileDialog.getExistingDirectory(self, "Select Directory")
        fhand = KeyFile("HERMES_M50_Disp.k")
        fhand.remove_keyword("*NODE")
        kw = fhand.add_keyword("*NODE")
        node_ids = self.file.get_node_ids()
        for i, id in enumerate(node_ids):
            kw.append_line(f"{id:>8}{self.coords[i, 0]:>16.5f}{self.coords[i, 1]:>16.5f}{self.coords[i, 2]:>16.5f}{0.0:>8}{0.0:>8}")
        str_gender = "female" if self.params['gender'] == 0 else 'male'
        output_file = f"{output_dir}/{str_gender}_{self.params['age']}yr_{self.params['stature'] / 10}cm_bmi{self.params['bmi']}_shs{self.params['shs']}.k"
        fhand.save(output_file)

    def handleOpacityChanged(self, opacity, mesh_type):
        """Handle the event when user change opacity through sliders."""
        if mesh_type == "skin":
            self.actors[0].GetProperty().SetOpacity(opacity)
            self.actors[18].GetProperty().SetOpacity(opacity)
            self.actors[19].GetProperty().SetOpacity(opacity)
            try:
                self.saved_actors[0].GetProperty().SetOpacity(opacity)
                self.saved_actors[18].GetProperty().SetOpacity(opacity)
                self.saved_actors[19].GetProperty().SetOpacity(opacity)
            except:
                return
        else:
            for i in range(1, 18):
                self.actors[i].GetProperty().SetOpacity(opacity)
                try:
                    self.saved_actors[i].GetProperty().SetOpacity(opacity)
                except:
                    continue
