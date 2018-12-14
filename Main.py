import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QRadioButton, QHBoxLayout, \
    QLCDNumber, QMainWindow
from PyQt5 import QtGui
from PyQt5 import QtCore
from functools import partial
from GameField import GameField
from Difficulty import Difficulty
from records import RecordWindow
from win import WinDialog
from stat import GameStat

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

        self.menubar = QtWidgets.QMenuBar(self)
        self.setMenuBar(self.menubar)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))

        self.settings = QtWidgets.QMenu(self.menubar)
        self.settings.setTitle('Настройки')

        self.statistic = QtWidgets.QMenu(self)
        self.statistic.setTitle("Статистика")

        self.records = QtWidgets.QAction(self)
        self.records.setText("Рекорды")
        self.statistic.addAction(self.records)

        self.difficulty = QtWidgets.QAction(self)
        self.difficulty.setText("Сложность")
        self.settings.addAction(self.difficulty)

        self.menubar.addAction(self.settings.menuAction())
        self.menubar.addAction(self.statistic.menuAction())

        self.difficulty.triggered.connect(self.change_difficulty)
        self.records.triggered.connect(self.stat)

    def init_ui(self, x, y, size, bombs):
        print(x, y, size, bombs)
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
                button.setGeometry(j * self.btn_size, i * self.btn_size + 86, self.btn_size, self.btn_size)
                button.setFont(QtGui.QFont("MS Shell Dlg 2", 10, QtGui.QFont.Bold))
                button.clicked.connect(partial(self.move, i, j))
                button.show()
                line.append(button)
            self.buttons.append(line)

        self.field = GameField(y, x, bombs)

    def change_difficulty(self):
        self.rows, self.cols, self.bombs = Difficulty().get_values()
        self.init_ui(self.cols, self.rows, self.btn_size, self.bombs)

    def move(self, row, col):
        if not self.field.generated:
            self.field.generate_field(row, col)
            self.stopwatch()
        elif self.field.get_field()[row][col] == self.field.cell["flag"]:
            return
        else:
            self.field.open(row, col, "o")

        self.update_field()

    def update_field(self):
        if self.field.det in (0, 1):
            for i in range(self.rows):
                for j in range(self.cols):
                    symbol = self.field.get_field()[i][j]
                    if symbol == self.field.cell["flag"]:
                        self.buttons[i][j].setText(symbol)
                    elif symbol == self.field.cell["untouched"]:
                        self.buttons[i][j].setText(symbol)
                    elif symbol:
                        self.buttons[i][j].setEnabled(False)
                        if symbol.isdigit():
                            self.buttons[i][j].setText(symbol)
                            self.buttons[i][j].setStyleSheet(f'color: {self.colors[symbol]}')
            if self.field.det == 1:
                for r, c in self.field.b_coords:
                    self.buttons[r][c].setText(self.field.cell["flag"])
                self.lcd_smile.setText(self.SMILE_WIN)
                self.lcd_bombs.display(0)
                self.showWinDialog()

        elif self.field.det == -1:
            for i in range(self.rows):
                for j in range(self.cols):
                    if (i, j) in self.field.b_coords:
                        self.buttons[i][j].setText("X")
                    elif self.field.get_field()[i][j] == self.field.cell["flag"]:
                        self.buttons[i][j].setStyleSheet('color: red')
            for r, c in self.field.b_coords:
                self.buttons[r][c].setText("X")
            self.lcd_smile.setText(self.SMILE_LOSE)

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

    def stopwatch(self):
        self.timer = QtCore.QTimer(self)
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_timer)
        self.timer.start()
        self.start_time = time.time()

    def update_timer(self):
        if self.field.det != 0:
            self.timer.stop()
        self.lcd_step.display(round(time.time() - self.start_time))

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
            if self.buttons[row][col].text() == self.field.cell["flag"]:
                self.lcd_bombs_num += 1
            else:
                self.lcd_bombs_num -= 1
            self.field.open(row, col, mode="f")
            self.lcd_bombs.display(self.lcd_bombs_num)
            self.update_field()

    def showWinDialog(self):
        args = (self.rows, self.cols, self.bombs)
        modes = {(9, 9, 10): "Новичок",
                 (16, 16, 40): "Эксперт",
                 (16, 30, 99): "Бывалый",
                 }
        mode = modes[args] if args in modes else "Особый"
        time = self.lcd_step.intValue()
        wd = WinDialog(mode, self.lcd_step.intValue())
        name = wd.show()
        GameStat().put(mode, name, time)

    def stat(self):
        RecordWindow().show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main(16, 16, 40, 40)
    form.show()
    sys.exit(app.exec())