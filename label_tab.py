from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
import stock_ticker_constants


class LabelTab(QtWidgets.QWidget):

    def __init__(self, *args, **kwargs):
        super(LabelTab, self).__init__(*args, **kwargs)

        main_layout = QtWidgets.QVBoxLayout()

        main_layout.setSpacing(False)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addSpacing(17)
        market_price = QtWidgets.QLabel("Market Price")
        market_price.setFont(stock_ticker_constants.font)
        main_layout.addWidget(market_price)

        amount_owned = QtWidgets.QLabel("Amount Owned")
        amount_owned.setFont(stock_ticker_constants.font)
        main_layout.addWidget(amount_owned)

        owned_value = QtWidgets.QLabel("Owned Value")
        owned_value.setFont(stock_ticker_constants.font)
        main_layout.addWidget(owned_value)

        price_500 = QtWidgets.QLabel("Price/500")
        price_500.setFont(stock_ticker_constants.font)
        main_layout.addWidget(price_500)

        buy_layout = QtWidgets.QVBoxLayout()
        to_buy = QtWidgets.QLabel("To Buy")
        to_buy.setFont(stock_ticker_constants.font)
        buy_layout.addWidget(to_buy)

        buy_layout.addSpacing(10)
        main_layout.addLayout(buy_layout)

        main_layout.addSpacing(27)

        sell_layout = QtWidgets.QVBoxLayout()
        to_sell = QtWidgets.QLabel("To Sell")
        to_sell.setFont(stock_ticker_constants.font)
        sell_layout.addWidget(to_sell)

        sell_layout.addSpacing(10)
        main_layout.addLayout(sell_layout)

        main_layout.addSpacing(27)

        dividends = QtWidgets.QLabel("Dividends")
        dividends.setFont(stock_ticker_constants.font)
        main_layout.addWidget(dividends)

        main_layout.addSpacing(5)

        # Add Frame
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Box)
        frame.setLineWidth(3)
        frame.setLayout(main_layout)
        frame_layout = QtWidgets.QHBoxLayout()
        frame_layout.addWidget(frame)
        # Set main layout
        self.setLayout(frame_layout)

