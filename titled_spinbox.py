from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from spin_box import SpinBox
import stock_ticker_constants


class TitledSpinBox(QtWidgets.QWidget):
    value_changed = pyqtSignal(int)

    def __init__(self, default_val=0, increment_amount=5, minimum=0, maximum=100, *args, **kwargs):
        super(TitledSpinBox, self).__init__(*args, **kwargs)

        layout = QtWidgets.QHBoxLayout()

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # Spin box
        self._value = SpinBox()
        self._value.setSingleStep(increment_amount)
        self._value.setMinimum(minimum)
        self._value.setMaximum(maximum)
        self._value.setValue(default_val)

        self._value.setFixedWidth(stock_ticker_constants.spin_box_col_size)

        layout.addWidget(self._value)

        layout.addStretch(1)

        self._value.editingFinished.connect(lambda: self._check_value(increment_amount))
        self._value.stepChanged.connect(lambda: self._check_value(increment_amount))

        self.setLayout(layout)

    def get_value(self):
        return self._value.value()

    def _check_value(self, increment):
        if self._value.value() % increment != 0:
            self._value.setValue(round(self._value.value() / increment) * increment)
        self.value_changed.emit(self._value.value())

    def set_value(self, value):
        self._value.setValue(value)
