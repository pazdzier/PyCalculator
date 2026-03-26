"""This part contains GUI code for PyCalculator

Implement missing features (NOT_IMPLEMENTED under constants)
"""

import os
import functools
import itertools as it

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QLineEdit
)

from constants import ALL, NOT_IMPLEMENTED


class CalculatorWindow(QDialog):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lbl = QVBoxLayout()
        self.lcd = self.create_lcd()
        self.lbl.addWidget(self.lcd)
        self.lbl.addLayout(self.add_buttons())
        self.setLayout(self.lbl)
        self.add_buttons()
        self.window_settings()

    def window_settings(self) -> None:
        """
        Here we configure some final widget settings, like title, min/max size, etc.
        :return:
        """
        self.setWindowTitle("PyCalculator")
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "static", "calculator.svg")))

    @staticmethod
    def create_lcd() -> QLineEdit:
        """
        creates QLineEdit with input/output representation of user's actions upon interface
        :return:
        """
        display = QLineEdit("0")
        display.setStyleSheet("""
            QLineEdit {
                border: none; 
                font-family: 'Courier New'; 
                font-size: 24px; 
                font-weight: bold; 
                padding-right: 4px; 
            }
            """)
        display.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        return display

    def btn_pressed(self, value: str) -> None:
        """

        :param value: str
        :return: None; it updates QLineEDit value inplace

        calcs should be moved outside this function
        calcs should not be performed in eval (safety...); need refactoring

        """
        if self.lcd.text() == "0":
            self.lcd.clear()
        if value == "C":
            self.lcd.clear()
            value = 0
        if value == "=":
            try:
                value = round(eval(self.lcd.text()), 3)
            except SyntaxError:
                value = 0
            self.lcd.clear()
        self.lcd.insert(str(value))

    def add_buttons(self) -> QGridLayout:
        """
        creates own layout with buttons visible for end user in GUI, can be later added to main Layout
        :return: QGridLayout
        """
        layout = QGridLayout()
        for row_idx, row in enumerate(it.batched(ALL, 4)):
            for col_idx, col in enumerate(row):
                btn = QPushButton(col)
                if col in NOT_IMPLEMENTED:
                    btn.setDisabled(True)
                btn.clicked.connect(functools.partial(self.btn_pressed, col))
                layout.addWidget(btn, row_idx, col_idx)
        return layout


if __name__ == "__main__":
    app = QApplication()
    calc = CalculatorWindow()
    calc.show()
    app.exec()
