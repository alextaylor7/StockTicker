from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, pyqtSignal
from incremental_value_box import IncrementalValueBox
from button_group import ButtonGroup
from buy_sell_increment import BuySellIncrement
import stock_ticker_constants

stock_colour = ["#eeee82", "#ea8ad8", "#c5e0b3", "#302316", "#f2f2f2", "#e3cb39"]
stock_title_font = ["#000000", "#000000", "#000000", "#ffffff", "#000000", "#000000"]
class StockTab(QtWidgets.QWidget):
    # id
    stock_updated = pyqtSignal(int)
    add_dividend_value = pyqtSignal(int)

    def __init__(self, title="title", stock_id=-1, *args, **kwargs):
        super(StockTab, self).__init__(*args, **kwargs)

        self._id = stock_id

        main_layout = QtWidgets.QGridLayout()

        main_layout.setSpacing(False)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setVerticalSpacing(0)
        main_layout.setHorizontalSpacing(0)

        self._title = QtWidgets.QLabel(title)
        bold_font = QtGui.QFont()
        bold_font.setBold(True)
        self._title.setFont(bold_font)
        self._title.setAlignment(Qt.AlignCenter)
        self._title.setStyleSheet("background-color: " + stock_colour[stock_id] + "; color: " + stock_title_font[stock_id])
        main_layout.addWidget(self._title, 0, 0)

        # Market Price
        # TODO: Convert to a double spin box? Maybe
        self._market_price = IncrementalValueBox(100, 5, 0, 200)
        main_layout.addWidget(self._market_price, 1, 0)

        # Amount Owned
        self._amount_owned = IncrementalValueBox(0, 500, 0, 1000000)
        main_layout.addWidget(self._amount_owned, 2, 0)

        # Owned Value
        owned_value_layout = QtWidgets.QHBoxLayout()

        self._owned_value = QtWidgets.QLabel("$$$$")
        self._owned_value.setFont(stock_ticker_constants.font)
        owned_value_layout.addWidget(self._owned_value)

        owned_value_layout.addStretch(1)

        main_layout.addLayout(owned_value_layout, 3, 0)

        self.calculate_owned_value()

        # Price/500
        price_500_layout = QtWidgets.QHBoxLayout()

        self._price_500 = QtWidgets.QLabel("$$$$")
        self._price_500.setFont(stock_ticker_constants.font)
        price_500_layout.addWidget(self._price_500)

        price_500_layout.addStretch(1)

        main_layout.addLayout(price_500_layout, 4, 0)

        self.calculate_price_value()

        # Buy
        self._to_buy = BuySellIncrement(0, 500)
        main_layout.addWidget(self._to_buy, 5, 0, 2, 1)

        # Sell
        self._to_sell = BuySellIncrement(0, 500)
        main_layout.addWidget(self._to_sell, 7, 0, 2, 1)

        # Dividends
        dividends_layout = QtWidgets.QHBoxLayout()

        dividends_layout.setSpacing(0)
        dividends_layout.setContentsMargins(0, 0, 0, 0)

        self._dividends = ButtonGroup(["5", "10", "20"])
        dividends_layout.addWidget(self._dividends)
        self._dividends.button_press.connect(self.add_dividend)

        dividends_layout.addStretch(1)

        main_layout.addLayout(dividends_layout, 9, 0)

        # Add Frame
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Box)
        frame.setLineWidth(3)
        frame.setLayout(main_layout)
        frame_layout = QtWidgets.QHBoxLayout()
        frame_layout.addWidget(frame)
        # Set main layout
        self.setLayout(frame_layout)

        self._market_price.value_changed.connect(self.market_price_changed)
        self._amount_owned.value_changed.connect(lambda: self.market_price_changed(self._market_price.get_value()))

        self._to_buy.buy_sell_changed.connect(lambda: self.stock_updated.emit(self._id))
        self._to_sell.buy_sell_changed.connect(lambda: self.stock_updated.emit(self._id))

        self.setMaximumWidth(stock_ticker_constants.stock_tab_width)
        self.setMaximumHeight(stock_ticker_constants.stock_tab_height)

    def add_dividend(self, button_amount):
        print(button_amount)
        if self._market_price.get_value() >= 100:
            dividend = round(button_amount / 100 * self._amount_owned.get_value())
            self.add_dividend_value.emit(dividend)

    def calculate_owned_value(self):
        owned_value = round(self._market_price.get_value() / 100 * self._amount_owned.get_value())
        self._owned_value.setText(str(owned_value) + "$")

    def get_owned_value(self):
        return round(self._market_price.get_value() / 100 * self._amount_owned.get_value())

    def calculate_price_value(self):
        price_value = round(self._market_price.get_value() / 100 * 500)
        self._price_500.setText(str(price_value) + "$")

    def market_price_changed(self, price):
        self.calculate_price_value()
        self.calculate_owned_value()
        self._to_buy.set_market_price(price)
        self._to_sell.set_market_price(price)
        self.stock_updated.emit(self._id)

    def amount_owned_changed(self, price):
        self.calculate_owned_value()

    def get_buy_value(self):
        return round(self._market_price.get_value() / 100 * self._to_buy.get_value())

    def get_sell_value(self):
        return round(self._market_price.get_value() / 100 * self._to_sell.get_value())

    def get_buy_amount(self):
        return self._to_buy.get_value()

    def get_sell_amount(self):
        if int(self._to_sell.get_value()) > int(self._amount_owned.get_value()):
            self._to_sell.set_amount_value_text(int(self._amount_owned.get_value()))
        return self._to_sell.get_value()

    def confirm_trade(self, buy_amount, sell_amount):
        self._to_buy.set_amount_value(0)
        self._to_sell.set_amount_value(0)
        self._amount_owned.set_value(int(self._amount_owned.get_value()) - sell_amount + buy_amount)
        self.calculate_owned_value()
