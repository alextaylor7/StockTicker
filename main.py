from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from main_tab import MainTab

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stock Ticker")
        self.setWindowIcon(QtGui.QIcon('Stock-Icon.ico'))

        main_layout = QtWidgets.QHBoxLayout()
        main_tabs = MainTab()
        main_layout.addWidget(main_tabs)

        main_layout.addStretch(2)
        self.setLayout(main_layout)
        self.setFixedSize(775, 600)


app = QtWidgets.QApplication([])
window = MainWindow()
window.show()
app.exec_()
