from app_ui import *
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt
from image_manager import ImageManager
from PIL import ImageColor
import os


class MyApplication(QWidget):
    def __init__(self):
        super(MyApplication, self).__init__()

        # setting up ui from my ui file
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # making list of all the combo boxes and populating them with possible selections
        self.combo_boxes = [self.ui.comboBox, self.ui.comboBox_2, self.ui.comboBox_3, self.ui.comboBox_4,
                            self.ui.comboBox_5, self.ui.comboBox_6]
        self.populate_combo_boxes()

        self.ui.pushButton.clicked.connect(self.button_pushed)

    def populate_combo_boxes(self):
        # adds the proper selections to go into the combo boxes
        for i in self.combo_boxes:
            i.addItems(['∞', 'A', 'B', 'C', 'D', 'E'])
            i.setCurrentText('A')
        self.ui.comboBox_7.addItems(['White', 'Black'])
        self.ui.comboBox_7.setCurrentText('Black')

        # adds all color options to combo boxes 8 and 9
        for name, code in ImageColor.colormap.items():
            self.ui.comboBox_8.addItem(name)
            self.ui.comboBox_9.addItem(name)
        self.ui.comboBox_9.setCurrentText('gray')
    def button_pushed(self):
        # creates an instance of the image manager and creates the background
        image_manager = ImageManager()
        image_manager.create_background()

        # gives the background a gradient if desired
        if not self.ui.checkBox_2.isChecked():
            image_manager.generate_gradient(self.ui.comboBox_8.currentText())

        # gets the relative path of the desired image, resizes the image if desired, then places the image onto the
        # background
        if self.ui.lineEdit_4.text():
            relative_path = os.path.relpath(self.ui.lineEdit_4.text(), os.getcwd())
            if relative_path[0] == '"' and relative_path[-1] == '"':
                relative_path = relative_path[1:-1]
            image_manager.place_stand_image(relative_path, self.ui.checkBox.isChecked())

        # gets desired rankings from the combo boxes, makes the stat wheel, and places it on background
        rankings = []
        displacements = []
        for i in self.combo_boxes:
            rankings.append(i.currentText())
            if i.currentText() == '∞':
                displacements.append(8)
            else:
                displacements.append(0)
        image_manager.draw_polygon(rankings, displacements, self.ui.comboBox_9.currentText())

        # places the stand name and user name onto the background
        image_manager.place_names(self.ui.lineEdit.text(), self.ui.lineEdit_2.text(), self.ui.comboBox_7.currentText())

        # displays the created image
        image_manager.bg.show()

