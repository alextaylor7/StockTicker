from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

import stock_ticker_constants


class ButtonGroup(QtWidgets.QWidget):
    button_press = pyqtSignal(int)

    def __init__(self, values=None, *args, **kwargs):
        super(ButtonGroup, self).__init__(*args, **kwargs)

        if values is None:
            values = []

        self._button_group = QtWidgets.QButtonGroup()

        layout = QtWidgets.QHBoxLayout()

        for val in values:
            button = QtWidgets.QPushButton(val)
            button.setFixedWidth(30)
            button.setFont(stock_ticker_constants.font)
            self._button_group.addButton(button, int(val))
            layout.addWidget(button)

        self._button_group.buttonClicked.connect(self.on_button_pressed)

        self.setLayout(layout)

    def on_button_pressed(self, button):
        self.button_press.emit(int(button.text()))