import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QTableWidgetItem
from results import GameStat
from random import randint


class WinDialog(QDialog):
    def __init__(self, mode, time):
        super().__init__()
        uic.loadUi('win.ui', self)
        self.setWindowTitle("Спасибо за мир без бомб!")
        self.setFixedSize(400, 190)
        self.info.setText(self.info.text().format(mode, time))

        self.game_stat = GameStat()

    def show(self):
        self.exec()
        return self.get_name()

    def get_name(self):
        rnd = "un{}".format(randint(1, 999))
        return rnd if not self.name.text() else self.name.text()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = WinDialog()
    form.show()
    sys.exit(app.exec())