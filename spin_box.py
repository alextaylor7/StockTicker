import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class SpinBox(QtWidgets.QSpinBox):
    stepChanged = QtCore.pyqtSignal()

    def stepBy(self, step):
        value = self.value()
        super(SpinBox, self).stepBy(step)
        if self.value() != value:
            self.stepChanged.emit()
