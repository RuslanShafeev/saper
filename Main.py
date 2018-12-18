import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton, QLCDNumber, QMainWindow
from PyQt5 import QtGui
from PyQt5 import QtCore
from functools import partial
from GameField import GameField
from difficulty import DifficultyWindow
from records import RecordWindow
from win import WinDialog
from results import GameStat
from options import OptionsWindow
from options_file import OptionsFile
from stats import StatsDialog


class Main(QMainWindow):
    def __init__(self, x, y, btn_size, bombs):
        super().__init__()
        self.start_time = 0
        self.buttons = []
        self.timer = None
        self.colors = {
            '1': '#0000ff',
            '2': '#00ff00',
            '3': '#ff0000',
            '4': '#00007b',
            '5': '#7b0000',
            '6': '#007b7b',
            '7': '#000000',
            '8': '#7b7b7b'
        }
        self.SMILE_DEFAULT = ":)"
        self.SMILE_WIN = ":D"
        self.SMILE_LOSE = "X("
        self.modes = {
            (9, 9, 10): "Новичок",
            (16, 16, 40): "Эксперт",
            (16, 30, 99): "Бывалый",
        }

        self.setWindowTitle("Сапёр))")
        self.init_ui(x, y, btn_size, bombs)

        self.lcd_smile = QPushButton(self)
        self.lcd_smile.setGeometry(self.size().width() // 2 - 25, 26, 50, 50)
        self.lcd_smile.setText(self.SMILE_DEFAULT)
        self.lcd_smile.setFont(QtGui.QFont("MS Shell Dlg 2", 14, QtGui.QFont.Bold))
        self.lcd_smile.clicked.connect(self.restart)

        self.lcd_bombs = QLCDNumber(self)
        self.lcd_bombs.display(self.lcd_bombs_num)
        self.lcd_bombs.setGeometry(10, 26, 80, 50)
        self.lcd_bombs.setStyleSheet('color: red; background-color: black')
        self.lcd_bombs.setDigitCount(3)
        self.lcd_bombs.setSegmentStyle(2)

        self.lcd_step = QLCDNumber(self)
        self.lcd_step.display(0)
        self.lcd_step.setGeometry(self.size().width() - 90, 26, 80, 50)
        self.lcd_step.setStyleSheet('color: red; background-color: black')
        self.lcd_step.setDigitCount(3)
        self.lcd_step.setSegmentStyle(2)
        if not OptionsFile().read()[2]:
            self.lcd_step.hide()

        self.menubar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))

        self.settings = QtWidgets.QMenu(self.menubar)
        self.settings.setTitle('Настройки')

        self.results = QtWidgets.QMenu(self)
        self.results.setTitle("Результаты")

        self.records = QtWidgets.QAction(self)
        self.records.setText("Рекорды")
        self.results.addAction(self.records)

        self.statisctics = QtWidgets.QAction(self)
        self.statisctics.setText("Статистика")
        self.results.addAction(self.statisctics)

        self.difficulty = QtWidgets.QAction(self)
        self.difficulty.setText("Сложность")
        self.settings.addAction(self.difficulty)

        self.options = QtWidgets.QAction(self)
        self.options.setText("Геймплей")
        self.settings.addAction(self.options)

        self.menubar.addAction(self.settings.menuAction())
        self.menubar.addAction(self.results.menuAction())

        self.difficulty.triggered.connect(self.change_difficulty)
        self.records.triggered.connect(self.records_click)
        self.options.triggered.connect(self.gameplay_settings)
        self.statisctics.triggered.connect(self.stats)

    # перерисовка поля
    def init_ui(self, x, y, size, bombs):
        self.setGeometry(300, 300, x * size, y * size + 86)
        self.setFixedSize(x * size, y * size + 86)
        self.rows, self.cols, self.btn_size, self.bombs = y, x, size, bombs
        self.lcd_bombs_num = bombs

        if self.buttons:
            for l in self.buttons:
                for b in l:
                    b.hide()
            self.lcd_bombs.display(bombs)
            self.lcd_step.display(0)
            self.lcd_smile.setGeometry(self.size().width() // 2 - 25, 26, 50, 50)
            self.lcd_step.setGeometry(self.size().width() - 90, 26, 80, 50)
            self.buttons = []
            if self.timer is not None:
                self.timer.stop()

        for i in range(self.rows):
            line = []
            for j in range(self.cols):
                button = QPushButton('', self)
                button.setGeometry(j * self.btn_size, i * self.btn_size + 86, self.btn_size,
                                   self.btn_size)
                button.setFont(QtGui.QFont("MS Shell Dlg 2", 10, QtGui.QFont.Bold))
                button.clicked.connect(partial(self.move, i, j))
                button.show()
                line.append(button)
            self.buttons.append(line)

        self.field = GameField(y, x, bombs)
        self.mode = self.modes[(y, x, bombs)] if (y, x, bombs) in self.modes else "Особый"

    # смена режима сложности
    def change_difficulty(self):
        clicked, rows, cols, bombs = DifficultyWindow().get_values()
        if clicked:
            self.init_ui(cols, rows, self.btn_size, bombs)

    # нажатие на кнопку поля
    def move(self, row, col):
        if not self.field.generated:
            self.field.generate_field(row, col)
            self.stopwatch()
        elif self.field.get_field()[row][col] == self.field.cell["flag"]:
            return
        else:
            self.field.open(row, col, "o")

        self.update_field()

    # отображение массива GameField на кнопочное поле
    def update_field(self):
        if self.field.det in (0, 1):
            for i in range(self.rows):
                for j in range(self.cols):
                    symbol = self.field.get_field()[i][j]
                    if symbol in [self.field.cell[i] for i in ["flag", "untouched", "question"]]:
                        self.buttons[i][j].setText(symbol)
                    elif symbol:
                        if self.buttons[i][j].isEnabled():
                            self.buttons[i][j].setEnabled(False)
                            self.buttons[i][j].setStyleSheet('color: rgb(204, 204, 204)')
                        if symbol.isdigit() and not self.buttons[i][j].text().isdigit():
                            self.buttons[i][j].setText(symbol)
                            self.buttons[i][j].setStyleSheet(f'color: {self.colors[symbol]}')

            if self.field.det == 1:
                # Победа
                flags, win = 0, 1
                for r, c in self.field.b_coords:
                    if self.field.get_field()[r][c] == self.field.cell["flag"]:
                        flags += 1
                    self.buttons[r][c].setText(self.field.cell["flag"])
                self.lcd_smile.setText(self.SMILE_WIN)
                self.lcd_bombs.display(0)
                self.show_win_dialog()
                GameStat().update_stats(self.mode, win, flags, flags, self.lcd_step.intValue())

        elif self.field.det == -1:
            # Поражение
            flags, defused, win = 0, 0, 0
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.field.get_field()[i][j] == self.field.cell["flag"]:
                        flags += 1
                        if (i, j) in self.field.b_coords:
                            defused += 1
                        else:
                            self.buttons[i][j].setStyleSheet('color: red')
                    else:
                        if (i, j) in self.field.b_coords:
                            self.buttons[i][j].setText("X")
            self.lcd_smile.setText(self.SMILE_LOSE)
            GameStat().update_stats(self.mode, win, flags, defused, self.lcd_step.intValue())

    # Нажатие на смайлик - заново
    def restart(self):
        self.field = GameField(self.rows, self.cols, self.bombs)
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].setText("")
                self.buttons[i][j].setStyleSheet('')
                self.buttons[i][j].setEnabled(True)
        self.lcd_step.display(0)
        self.lcd_bombs_num = self.bombs
        self.lcd_bombs.display(self.lcd_bombs_num)
        self.lcd_smile.setText(self.SMILE_DEFAULT)
        self.timer.stop()

    # Запуск секундомера
    def stopwatch(self):
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start()
        self.start_time = time.time()

    # Обновление дисплея времени
    def update_timer(self):
        if self.field.det != 0:
            self.timer.stop()
        self.lcd_step.display(round(time.time() - self.start_time))

    # Обработка нажатия правой кнопкой мыши
    def mousePressEvent(self, event):
        if not self.field.generated:
            return
        if self.lcd_bombs_num == 0:
            return
        if event.button() == QtCore.Qt.RightButton:
            x, y = event.x(), event.y()
            if y < 0:
                return
            row, col = (y - 86) // self.btn_size, x // self.btn_size
            if self.buttons[row][col].text().isdigit():
                return
            self.field.open(row, col, mode="f")
            if self.field.get_field()[row][col] == self.field.cell["flag"]:
                self.lcd_bombs_num -= 1
            elif self.lcd_bombs_num < self.bombs:
                self.lcd_bombs_num += 1
            self.lcd_bombs.display(self.lcd_bombs_num)
            self.update_field()

    # Показать диалоговое окно с победой
    def show_win_dialog(self):
        time = self.lcd_step.intValue()
        wd = WinDialog(self.mode, self.lcd_step.intValue())
        name = wd.show()
        GameStat().put_record(self.mode, name, time)

    # Показать диалоговое окно с таблицей рекордов
    def records_click(self):
        RecordWindow().show()

    # Показать диалоговое окно со статистикой
    def stats(self):
        StatsDialog().show()

    # Показать диалоговое окно с опциями и изменить видимость дисплея времени
    def gameplay_settings(self):
        args = OptionsWindow().show()
        time = args[2]
        if not time:
            self.lcd_step.hide()
        else:
            self.lcd_step.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main(16, 16, 40, 40)
    form.show()
    sys.exit(app.exec())
