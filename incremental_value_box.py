from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from titled_spinbox import TitledSpinBox


class IncrementalValueBox(QtWidgets.QWidget):
    value_changed = pyqtSignal(int)

    def __init__(self, default_val=0, increment_amount=5, minimum=0, maximum=100, *args, **kwargs):
        super(IncrementalValueBox, self).__init__(*args, **kwargs)

        main_layout = QtWidgets.QHBoxLayout()

        main_layout.setSpacing(10)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self._value = TitledSpinBox(default_val, increment_amount, minimum, maximum)
        main_layout.addWidget(self._value)

        self._value.value_changed.connect(self.value_changed)

        main_layout.addStretch(1)

        self.setLayout(main_layout)

    def get_value(self):
        return self._value.get_value()

    def set_value(self, value):
        self._value.set_value(value)
