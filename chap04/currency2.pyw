#!/usr/bin/env python3
# Copyright (c) 2008-10 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

import locale

locale.setlocale(locale.LC_ALL, "")

import sys
import urllib.request
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Form(QDialog):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        date = self.getdata()
        rates = sorted(self.rates.keys(), key=str.lower)

        dateLabel = QLabel(date)
        self.fromComboBox = QComboBox()
        self.fromComboBox.addItems(rates)
        self.fromSpinBox = QDoubleSpinBox()
        self.fromSpinBox.setRange(0.01, 10000000.00)
        self.fromSpinBox.setValue(1.00)
        self.toComboBox = QComboBox()
        self.toComboBox.addItems(rates)
        self.toLabel = QLabel("1.00")
        grid = QGridLayout()
        grid.addWidget(dateLabel, 0, 0)
        grid.addWidget(self.fromComboBox, 1, 0)
        grid.addWidget(self.fromSpinBox, 1, 1)
        grid.addWidget(self.toComboBox, 2, 0)
        grid.addWidget(self.toLabel, 2, 1)
        self.setLayout(grid)
        self.fromComboBox.currentIndexChanged.connect(self.updateUi)
        self.toComboBox.currentIndexChanged.connect(self.updateUi)
        self.fromSpinBox.valueChanged.connect(self.updateUi)
        self.setWindowTitle("Currency")

    def updateUi(self):
        to = self.toComboBox.currentText()
        from_ = self.fromComboBox.currentText()
        amount = ((self.rates[from_] / self.rates[to]) *
                  self.fromSpinBox.value())
        self.toLabel.setText(locale.format("%0.2f", amount, True))

    def getdata(self):  # Idea taken from the Python Cookbook
        self.rates = {}
        try:
            date = "Unknown"
            with open("exchange_eng.csv") as f:
                for line in f:
                    line = line.rstrip()
                    if not line or line.startswith(("#", "Closing ")):
                        continue
                    fields = line.split(",")
                    if line.startswith("Date "):
                        date = fields[-1]
                    else:
                        try:
                            value = float(fields[-1])
                            self.rates[fields[0]] = value
                        except ValueError:
                            pass
                self.rates["Canadian Dollar"] = 1.00
                return "Exchange Rates Date: " + date
        except Exception as e:
            return "Failed to open:\n{}".format(e)


app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
