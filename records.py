import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QTableWidgetItem, QHeaderView
from results import GameStat
from PyQt5 import QtCore


class RecordWindow(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('records.ui', self)
        self.setWindowTitle("Рекорды")
        self.setFixedSize(400, 300)
        self.novichok.clicked.connect(self.new)
        self.expert.clicked.connect(self.exp)
        self.bivalii.clicked.connect(self.leery)

        self.tableWidget.setHorizontalHeaderLabels(["Имя", "Время"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.game_stat = GameStat()
        self.new()

    def new(self):
        res = self.game_stat.get_records("Новичок")
        self.tableWidget.setRowCount(len(res))
        for i in range(len(res)):
            name = QTableWidgetItem(res[i]["name"])
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            time = QTableWidgetItem(str(res[i]["time"]))
            time.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 0, name)
            self.tableWidget.setItem(i, 1, time)

        # self.tableWidget.resizeColumnsToContents()

    def exp(self):
        res = self.game_stat.get_records("Эксперт")
        self.tableWidget.setRowCount(len(res))
        for i in range(len(res)):
            name = QTableWidgetItem(res[i]["name"])
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            time = QTableWidgetItem(str(res[i]["time"]))
            time.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 0, name)
            self.tableWidget.setItem(i, 1, time)

        # self.tableWidget.resizeColumnsToContents()

    def leery(self):
        res = self.game_stat.get_records("Бывалый")
        self.tableWidget.setRowCount(len(res))
        for i in range(len(res)):
            name = QTableWidgetItem(res[i]["name"])
            name.setTextAlignment(QtCore.Qt.AlignCenter)
            time = QTableWidgetItem(str(res[i]["time"]))
            time.setTextAlignment(QtCore.Qt.AlignCenter)
            self.tableWidget.setItem(i, 0, name)
            self.tableWidget.setItem(i, 1, time)

        # self.tableWidget.resizeColumnsToContents()

    def show(self):
        self.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = RecordWindow()
    form.show()
    sys.exit(app.exec())