import glob
import io
import os
import threading
from os.path import exists
from PyQt5 import QtWidgets
from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
                             QLineEdit, QListView, QSizePolicy, QToolButton,
                             QWidget, QFileDialog, QMenu, QPushButton, QAction, QMessageBox, QToolBar)
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3

#defaults
import defaults

#

track = 0
disk_number = 0
myDocuments = 5

class Ui_Dialog(object):
    my_tag = ""
    show_title = ""
    show_artist = ""
    album_artist = ""
    composer = album_artist

    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(320, 240)
#

#
        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 200, 301, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Apply | QDialogButtonBox.Close)
#
        self.toolButton = QToolButton(Dialog)
        self.toolButton.setObjectName(u"toolButton")
        self.toolButton.setGeometry(QRect(260, 30, 25, 19))

#
        self.listView = QListView(Dialog)
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)

        self.listView.setObjectName(u"listView")
        self.listView.setGeometry(QRect(10, 60, 281, 131))
        self.listView.setAlternatingRowColors(True)
        self.listView.children().clear()
#
        self.lineEdit = QLineEdit(Dialog)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(10, 30, 241, 20))
#
        self.retranslateUi(Dialog)
        self.toolButton.clicked.connect(self.find_folder)

#
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.clicked.connect(self.what_button)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Browse for mp3 folder", None))
#if QT_CONFIG(statustip)
        Dialog.setStatusTip("")
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(tooltip)
        self.toolButton.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.toolButton.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.toolButton.setText(QCoreApplication.translate("Dialog", u"...", None))
    # retranslateUi

    def find_folder(self):
        print("find folder")
        dir = QFileDialog.getExistingDirectory(caption="Open MP3 folder ")
        self.lineEdit.setText(dir)

        filez = glob.glob(f"{dir}\\{self.my_tag}*.mp3")  # get array of filename with mp3 extension
        # print the first element of filez:
        self.model.clear()
        self.toolButton.setEnabled(False)
        self.lineEdit.setEnabled(False)
        for thisfile in filez:

            # print (thisfile)
            this_file_list = thisfile.split("\\")  # seperate filename from path
            last_chunk = len(this_file_list) - 1
            if this_file_list[last_chunk].count(" pt") > 0:
                # if it ends ' pt' then part number  in the filemame then ok to carry on or raise an error
                self.model.appendRow(QStandardItem(this_file_list[last_chunk]))

            else:
                pass

                #self.model.appendRow(f"{thisfile} has no part number.")


    def what_button(self,t_button):
        print (f"What Button {t_button.text()}")
        if t_button.text() == "Apply":
            self.tagger(self.lineEdit.text())

    def read_config(self):

        confHandle = io.open(defaults.confPath, mode="r")
        line = confHandle.readline().rstrip()

        if line == defaults.taggerName:
            self.my_tag = confHandle.readline().rstrip()
            self.show_title = confHandle.readline().rstrip()
            self.show_artist = confHandle.readline().rstrip()
            self.album_artist = confHandle.readline().rstrip()
            self.composer = self.album_artist
            confHandle.close()

        else:
            confHandle.close()



    def wipe_config(self):
        if exists(defaults.confPath):
            l_title = "Are you sure?"
            response = QMessageBox.question(message="Are you sure you want to erase the tag data?")
            if response:
                os.remove(defaults.confPath)

    def tagger_thread(self,filename):
        self.model.appendRow(QStandardItem(f"tagging {filename}"))
        #print(f" The file is {filename}")
        #print(f"tagging {filename}")
        this_file_list = filename.split("\\")  # seperate filename from path
        last_chunk = len(this_file_list) - 1
        song = this_file_list[last_chunk].split('.')[0]  # remove file extension
        file_section = song.split(' pt')[0]  # seperate filename and part number
        track = song.split(' pt')[1]  # seperate filename and part number
        disk_number = track
        mp3file = MP3(filename, ID3=EasyID3)  # retag here
        mp3file["encodedby"] = 'id3tagger'
        mp3file["Title"] = self.show_title
        mp3file["Artist"] = self.show_artist
        mp3file["AlbumArtist"] = self.album_artist
        mp3file["composer"] = self.composer
        mp3file["Album"] = f"{file_section} pt{track}"
        mp3file["Tracknumber"] = track
        mp3file["Discnumber"] = disk_number

        mp3file.save()  # save changes. don't forget this line.
    def tagger(self, tPath):

        if exists(tPath):
            segs_path = tPath
        else:

            segs_path = "P:\\HRH\\20230530_1500"
        # tags = [{'artist':f'{show_artist}'}, {'title':f"{show_title} "}]

        filez = glob.glob(f"{segs_path}\\{self.my_tag}*.mp3")  # get array of filename with mp3 extension
        # print the first element of filez:
        self.model.clear()
        for thisfile in filez:

            # print (thisfile)
            this_file_list = thisfile.split("\\")  # seperate filename from path
            last_chunk = len(this_file_list) - 1
            if this_file_list[last_chunk].count(" pt") > 0:
                # if it ends ' pt' then part number  in the filemame then ok to carry on or raise an error
                self.model.appendRow(QStandardItem(thisfile))
                threading.Thread(target=self.tagger_thread, args=(thisfile,)).start()
            else:
                pass

                #self.model.appendRow(QStandardItem((f"{thisfile} has no part number.")))


if __name__ == "__main__":
    import sys


    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    if exists(defaults.confPath):
        ui.read_config()
        Dialog.show()
    else:
        pass
    sys.exit(app.exec())

