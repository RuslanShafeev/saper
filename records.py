import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QRadioButton, QButtonGroup, QTableWidget, QAbstractItemView
from results import GameStat
from PyQt5 import QtCore


class RecordWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Рекорды")
        self.setFixedSize(400, 300)
        self.init_ui()

    def init_ui(self):
        font = QFont()
        font.setPointSize(12)

        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(140, 0, 260, 300))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)

        self.buttonGroup = QButtonGroup(self)
        for n, text in enumerate(['Новичок', 'Эксперт', 'Бывалый']):
            rb = QRadioButton(self)
            rb.setGeometry(QtCore.QRect(30, 100 + 30 * n, 91, 17))
            rb.setText(text)
            rb.setFont(font)
            self.buttonGroup.addButton(rb)
            self.buttonGroup.setId(rb, n)

        self.buttonGroup.buttonClicked.connect(self.choose_table)

        self.tableWidget.setHorizontalHeaderLabels(["Имя", "Время"])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.game_stat = GameStat()
        self.buttonGroup.button(0).click()

    def choose_table(self):
        res = self.game_stat.get_records(self.sender().checkedButton().text())
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
