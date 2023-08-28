from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from titled_spinbox import TitledSpinBox
import stock_ticker_constants


class BuySellIncrement(QtWidgets.QWidget):
    buy_sell_changed = pyqtSignal()

    def __init__(self, default_val=0, increment_amount=5, minimum=0, maximum=1000000, *args, **kwargs):
        super(BuySellIncrement, self).__init__(*args, **kwargs)

        self._market_price = 100

        main_layout = QtWidgets.QVBoxLayout()

        main_layout.setSpacing(10)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self._value = TitledSpinBox(default_val, increment_amount, minimum, maximum)
        main_layout.addWidget(self._value)

        # Money
        h_layout = QtWidgets.QHBoxLayout()

        h_layout.setSpacing(0)
        h_layout.setContentsMargins(0, 0, 0, 0)

        self._amount_value = QtWidgets.QLabel("0$")
        self._amount_value.setFont(stock_ticker_constants.font)
        self._amount_value.setFixedWidth(75)
        h_layout.addWidget(self._amount_value)

        h_layout.addStretch(1)
        # Main
        main_layout.addLayout(h_layout)

        self.setLayout(main_layout)

        self._value.value_changed.connect(self.set_amount_value)

    def get_value(self):
        return self._value.get_value()

    def set_market_price(self, price):
        self._market_price = price
        self.set_amount_value(self._value.get_value())

    def set_amount_value(self, amount):
        self.set_amount_value_text(amount)
        self.buy_sell_changed.emit()

    def set_amount_value_text(self, amount):
        self._value.set_value(amount)
        self._amount_value.setText(str(round((self._market_price / 100) * amount)) + "$")
