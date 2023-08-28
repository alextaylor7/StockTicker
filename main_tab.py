from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
from stock_tab import StockTab
from total_tab import TotalTab
from label_tab import LabelTab
import math


class MainTab(QtWidgets.QWidget):
    stocks = ["GRAIN", "INDUSTRY", "BONDS", "OIL", "SILVER", "GOLD"]
    stock_values = [0, 0, 0, 0, 0, 0]
    stock_buys = [0, 0, 0, 0, 0, 0]
    stock_sells = [0, 0, 0, 0, 0, 0]
    stock_tabs = []

    def __init__(self, *args, **kwargs):
        super(MainTab, self).__init__(*args, **kwargs)
        main_layout = QtWidgets.QVBoxLayout()

        # export_button = QtWidgets.QPushButton("Export")
        # export_button.setFixedSize(75, 25)
        # main_layout.addWidget(export_button)

        # divider = QtWidgets.QFrame()
        # divider.setFrameStyle(QtWidgets.QFrame.Shape.HLine)
        # divider.setLineWidth(3)
        # main_layout.addWidget(divider)

        tab_layout = QtWidgets.QGridLayout()
        tab_layout.setSpacing(0)
        tab_layout.setContentsMargins(0, 0, 0, 0)
        tab_layout.setVerticalSpacing(0)
        tab_layout.setHorizontalSpacing(0)

        label_tab = LabelTab()
        tab_layout.addWidget(label_tab, 0, 0)
        label_tab_2 = LabelTab()
        tab_layout.addWidget(label_tab_2, 1, 0)

        size = 3

        for i in range(len(self.stocks)):
            stock_tab = StockTab(self.stocks[i], i)
            stock_tab.stock_updated.connect(lambda stock_id: self.set_total_buy_sell())
            stock_tab.add_dividend_value.connect(self.add_dividend)
            self.stock_tabs.append(stock_tab)
            row = math.floor(i / size)
            col = (i % size) + 1
            tab_layout.addWidget(stock_tab, row, col)

        self._totals_tab = TotalTab()
        self._totals_tab.confirm_trade.connect(lambda: self.confirm_trade())
        tab_layout.addWidget(self._totals_tab, 0, 5, 2, 1)

        main_layout.addLayout(tab_layout)

        self.setLayout(main_layout)

    def add_dividend(self, dividend_amount):
        self._totals_tab.add_to_liquid(dividend_amount)
        self.set_total_buy_sell()

    def set_total_buy_sell(self):
        total_buy = 0
        total_sell = 0
        total_value = 0
        for i in range(len(self.stocks)):
            self.stock_buys[i] = self.stock_tabs[i].get_buy_amount()
            self.stock_sells[i] = self.stock_tabs[i].get_sell_amount()
            total_buy += self.stock_tabs[i].get_buy_value()
            total_sell += self.stock_tabs[i].get_sell_value()
            total_value += self.stock_tabs[i].get_owned_value()
        self._totals_tab.set_total_buy(total_buy)
        self._totals_tab.set_total_sell(total_sell)

        self._totals_tab.set_networth(total_value)

    def confirm_trade(self):
        total_value = 0
        for i in range(len(self.stocks)):
            self.stock_tabs[i].confirm_trade(self.stock_buys[i], self.stock_sells[i])
            total_value += self.stock_tabs[i].get_owned_value()
        self._totals_tab.set_networth(total_value)

    def export(self):
        self._totals_tab.get_turn_networths()