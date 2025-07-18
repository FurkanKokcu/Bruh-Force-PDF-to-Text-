from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os
from pdf2image import convert_from_path
import pytesseract


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(532, 102)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(10, 0, 511, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(10, 30, 80, 26))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.file_selector)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 30, 80, 26))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.converter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 532, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def file_selector(self):
        file = QFileDialog.getOpenFileName(None, "Dosya Seç", "", "PDF Dosyaları (*.pdf)")[0]
        self.selectedfile = file

    def succ(self):
        msg = QMessageBox()
        msg.setWindowTitle("Finished")
        msg.setText("The file created succ")
        y = msg.exec_()

    def blankerror(self):
        msg = QMessageBox()
        msg.setWindowTitle("Not a file")
        msg.setText("Choose a file!")
        msg.setIcon(QMessageBox.Critical)
        x = msg.exec_()

    def converter(self):
        # PDF'yi resimlere çevir
        file = self.selectedfile
        if not file:
            self.blankerror()
            return

        images = convert_from_path(self.selectedfile)
        filename= os.path.splitext(file)[0]  # .pdf uzantısını kaldır
        imagelen = len(images)

        # OCR işlemi yap ve metni kaydet
        with open(filename + ".txt", "w", encoding="utf-8") as f:
            for i, img in enumerate(images):
                text = pytesseract.image_to_string(img, lang="tur")  # Türkçe OCR için
                f.write(text + "\n\n")
                a = int((i+1)/imagelen*100)
                progress = self.progressBar.setValue(a)
                if a == 100:
                    self.succ()
                    return
                    
                QtWidgets.QApplication.processEvents()  # UI'nin donmasını önler


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Bruh Force\'s PDF to TEXT Converter"))
        self.pushButton.setText(_translate("MainWindow", "Open file"))
        self.pushButton_2.setText(_translate("MainWindow", "Start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
