import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QTableWidgetItem, QHeaderView
from results import GameStat
from PyQt5 import QtCore


class StatsDialog(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('stats.ui', self)
        self.setWindowTitle("Статистика")
        self.setFixedSize(570, 270)

        game_stat = GameStat()
        modes = ("Новичок", "Эксперт", "Бывалый", "Итого")
        columns = (game_stat.get_games, game_stat.get_wins, game_stat.get_win_rate,
                   game_stat.get_flags, game_stat.get_defused, game_stat.get_defuse_rate,
                   game_stat.get_time, game_stat.get_average_time)
        for j in range(8):
            for i in range(4):
                mode = modes[i]
                value = columns[j](mode)
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(j, i, item)

        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def show(self):
        self.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = StatsDialog()
    form.show()
    sys.exit(app.exec())