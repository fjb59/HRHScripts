import argparse
import os
import sys
import tkinter.messagebox as messagebox
from os.path import exists

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QLabel, QPushButton, QVBoxLayout, QDialog, QApplication, QFileDialog

import parsexml
import id3tag_dialog
import defaults


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("HRH Stuff !")
        self.label = QLabel("<font color=green size=25>Select option !</font>")

        self.button1 = QPushButton("import playlist to clipboard")
        self.button2 = QPushButton("Tag Mp3 files")
        self.button3 = QPushButton("Wipe config")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        self.setLayout(layout)
        self.button1.clicked.connect(self.callback1)
        self.button2.clicked.connect(self.callback2)
        self.button3.clicked.connect(self.callback3)

    def callback1(self):
        # name = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        name = QFileDialog.getOpenFileName(self, "Select File", filter="Proppfrexxx files (*.pfp)")
        print(name[0])
        parsexml.ParseXML(name[0], includeTrackTitle=True)

    def callback2(self):

        ui = id3tag_dialog.Ui_Dialog(self)
        if exists(defaults.confPath):
            ui.read_config()
        ui.show()


    def callback3(self):
        self.wipe_config()

    def wipe_config(self):
        if exists(defaults.confPath):
            l_title = "Are you sure?"
            response = messagebox.askyesno("Are you sure?", "Are you sure you want to erase the tag data?")
            if response:
                os.remove(defaults.confPath)


if __name__ == '__main__':




    errmsg = 'Error!'
    app = QtCore.QCoreApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(sys.argv)
        form = Form()
        #    ui = Ui_Dialog()
        #    ui.setupUi(Dialog)
        form.show()
        if exists(defaults.confPath):
            form.read_config()

        else:
            pass
        sys.exit(app.exec())

    app.quitOnLastWindowClosed()
    app.exec()


