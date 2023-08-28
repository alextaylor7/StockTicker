from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt, pyqtSignal
import stock_ticker_constants


class TotalTab(QtWidgets.QWidget):
    confirm_trade = pyqtSignal()
    end_turn = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(TotalTab, self).__init__(*args, **kwargs)

        self._sell_value = 0
        self._buy_value = 0

        self._turn_networths = [10000]
        self._turn_number = 1

        spacer_layout = QtWidgets.QVBoxLayout()
        main_layout = QtWidgets.QGridLayout()

        self._turn_number_label = QtWidgets.QLabel("Turn " + str(self._turn_number))
        self._turn_number_label.setFont(stock_ticker_constants.font)
        main_layout.addWidget(self._turn_number_label, 0, 1)

        total_title = QtWidgets.QLabel("TOTALS")
        bold_font = QtGui.QFont()
        bold_font.setBold(True)
        total_title.setFont(bold_font)
        main_layout.addWidget(total_title, 0, 0)

        networth_title = QtWidgets.QLabel("Networth")
        networth_title.setFont(stock_ticker_constants.font)
        main_layout.addWidget(networth_title, 1, 0)

        self._networth = QtWidgets.QLineEdit("10000")
        self._networth.setEnabled(False)
        self._networth.setFixedWidth(stock_ticker_constants.spin_box_col_size)
        main_layout.addWidget(self._networth, 2, 0)

        self._networth_change = QtWidgets.QLabel("0.00%")
        main_layout.addWidget(self._networth_change, 2, 1)

        liquid_title = QtWidgets.QLabel("Liquid")
        liquid_title.setFont(stock_ticker_constants.font)
        main_layout.addWidget(liquid_title, 3, 0)

        self._liquid = QtWidgets.QLineEdit("10000")
        self._liquid.setFixedWidth(stock_ticker_constants.spin_box_col_size)
        main_layout.addWidget(self._liquid, 4, 0)

        buy_spacer = QtWidgets.QLabel("Buy Total:")
        buy_spacer.setFont(stock_ticker_constants.font)
        main_layout.addWidget(buy_spacer, 5, 0)

        self._buy_price = QtWidgets.QLabel("+" + str(self._buy_value) + "$")
        self._buy_price.setFont(stock_ticker_constants.font)
        main_layout.addWidget(self._buy_price, 6, 0)

        sell_spacer = QtWidgets.QLabel("Sell Total:")
        sell_spacer.setFont(stock_ticker_constants.font)
        main_layout.addWidget(sell_spacer, 7, 0)

        self._sell_price = QtWidgets.QLabel("-" + str(self._sell_value) + "$")
        self._sell_price.setFont(stock_ticker_constants.font)
        main_layout.addWidget(self._sell_price, 8, 0)

        liquid_spacer = QtWidgets.QLabel("Remaining Liquid:")
        liquid_spacer.setFont(stock_ticker_constants.font)
        main_layout.addWidget(liquid_spacer, 9, 0)

        self._liquid_remain = QtWidgets.QLabel(self._liquid.text() + "$")
        self._liquid_remain.setFont(stock_ticker_constants.font)
        main_layout.addWidget(self._liquid_remain, 10, 0)

        self._confirm_trade_button = QtWidgets.QPushButton("Confirm Trade")
        self._confirm_trade_button.setFont(stock_ticker_constants.font)
        self._confirm_trade_button.setFixedWidth(stock_ticker_constants.spin_box_col_size)
        main_layout.addWidget(self._confirm_trade_button, 11, 0)
        self._confirm_trade_button.clicked.connect(lambda: self.confirm_trade_pushed())

        self._end_turn_button = QtWidgets.QPushButton("End Turn")
        self._end_turn_button.setFont(stock_ticker_constants.font)
        self._end_turn_button.setFixedWidth(stock_ticker_constants.spin_box_col_size)
        main_layout.addWidget(self._end_turn_button, 13, 0)
        self._end_turn_button.clicked.connect(lambda: self.end_turn())

        spacer_layout.addLayout(main_layout)
        spacer_layout.addStretch(1)

        # Add Frame
        frame = QtWidgets.QFrame()
        frame.setFrameStyle(QtWidgets.QFrame.Box)
        frame.setLineWidth(3)
        frame.setLayout(spacer_layout)
        frame_layout = QtWidgets.QHBoxLayout()
        frame_layout.addWidget(frame)
        # Set main layout
        self.setLayout(frame_layout)

    def confirm_trade_pushed(self):
        total = int(self._liquid.text()) + self._sell_value - self._buy_value
        self._liquid.setText(str(total))
        self.confirm_trade.emit()

    def set_total_buy(self, buy_value):
        self._buy_value = buy_value
        self._buy_price.setText("+" + str(self._buy_value) + "$")
        self.validate_trade()

    def set_total_sell(self, sell_value):
        self._sell_value = sell_value
        self._sell_price.setText("-" + str(self._sell_value) + "$")
        self.validate_trade()

    def validate_trade(self):
        total = int(self._liquid.text()) + self._sell_value - self._buy_value
        self._confirm_trade_button.setEnabled(total >= 0)
        self._liquid_remain.setText(str(total) + "$")

    def end_turn(self):
        last_networth = self._turn_networths[-1]
        self._turn_networths.append(int(self._networth.text()))
        change = (self._turn_networths[-1] / last_networth * 100) - 100
        self._networth_change.setText("{:.2f}%".format(round(change, 2)))
        self._turn_number += 1
        self._turn_number_label.setText("Turn " + str(self._turn_number))

    def set_networth(self, total_value):
        total = int(self._liquid.text()) + total_value
        self._networth.setText(str(total))

    def add_to_liquid(self, amount):
        self._liquid.setText(str(int(self._liquid.text()) + amount))

    def get_turn_networths(self):
        return self._turn_networths
