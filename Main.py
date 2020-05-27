# This Python file uses the following encoding: utf-8
from PyQt5 import QtWidgets
import sys
from mainwindow import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    mainWindow = MainWindow()
    mainWindow.show()

    sys.exit(app.exec_())
