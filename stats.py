import sys
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QHeaderView, QTableWidget, \
    QAbstractItemView
from results import GameStat
from PyQt5 import QtCore


class StatsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Статистика")
        self.setFixedSize(570, 270)

        game_stat = GameStat()
        modes = ("Новичок", "Эксперт", "Бывалый", "Итого")
        columns = (game_stat.get_games, game_stat.get_wins, game_stat.get_win_rate,
                   game_stat.get_flags, game_stat.get_defused, game_stat.get_defuse_rate,
                   game_stat.get_time, game_stat.get_average_time)
        self.init_ui()
        for j in range(8):
            for i in range(4):
                mode = modes[i]
                value = columns[j](mode)
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(j, i, item)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def init_ui(self):
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 570, 270))
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setRowCount(8)
        self.tableWidget.setColumnCount(4)

        for n, text in enumerate(["Новичок", "Эксперт", "Бывалый", "Итого"]):
            item = QTableWidgetItem()
            item.setText(text)
            self.tableWidget.setHorizontalHeaderItem(n, item)
        self.tableWidget.verticalHeader().setStretchLastSection(True)

        for n, text in enumerate(["Всего игр", "Всего побед", "Процент побед", "Всего флажков",
                                  "Обезврежено флажками", "Процент обезвреживания", "Общее время",
                                  "Среднее время"]):
            item = QTableWidgetItem()
            item.setText(text)
            self.tableWidget.setVerticalHeaderItem(n, item)

    def show(self):
        self.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = StatsDialog()
    form.show()
    sys.exit(app.exec())
