# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Emergente1.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(356, 277)
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(40, 10, 256, 192))
        self.listWidget.setObjectName("listWidget")
        self.botonAceptar = QtWidgets.QPushButton(Dialog)
        self.botonAceptar.setGeometry(QtCore.QRect(270, 250, 75, 23))
        self.botonAceptar.setObjectName("botonAceptar")
        self.botonAgr = QtWidgets.QPushButton(Dialog)
        self.botonAgr.setGeometry(QtCore.QRect(40, 210, 75, 23))
        self.botonAgr.setObjectName("botonAgr")
        self.lineEdit = QtWidgets.QLineEdit(Dialog)
        self.lineEdit.setGeometry(QtCore.QRect(120, 210, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.botonBor = QtWidgets.QPushButton(Dialog)
        self.botonBor.setGeometry(QtCore.QRect(40, 240, 75, 23))
        self.botonBor.setObjectName("botonBor")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.botonAceptar.setText(_translate("Dialog", "Aceptar"))
        self.botonAgr.setText(_translate("Dialog", "Agregar"))
        self.botonBor.setText(_translate("Dialog", "Borrar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

