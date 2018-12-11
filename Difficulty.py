import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QDialog


class Difficulty(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Difficulty.ui', self)
        self.buttonGroup.buttonClicked.connect(self.checked)
        self.mode = (9, 9, 10)
        self.easy.setChecked(True)

    def get_values(self):
        ex = Difficulty()
        ex.exec()
        return ex.get_mode()

    def checked(self):
        modes = {'Новичок': (9, 9, 10),
                 'Эксперт': (16, 16, 40),
                 'Бывалый': (16, 30, 99),
                 }
        self.mode = modes[self.sender().checkedButton().text()]

    def get_mode(self):
        return self.mode
