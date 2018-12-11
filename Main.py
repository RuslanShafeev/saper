import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QRadioButton, QHBoxLayout, \
    QLCDNumber, QMainWindow
from PyQt5 import QtGui
from PyQt5 import QtCore
from functools import partial
from GameField import GameField
from Difficulty import Difficulty


class Main(QMainWindow):
    def __init__(self, x, y, size, bombs):
        super().__init__()
        self.setGeometry(300, 300, x * size, y * size + 86)
        self.setFixedSize(self.width(), self.height())

        self.rows, self.cols, self.btn_size, self.bombs = x, y, size, bombs

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

        self.buttons = []
        for i in range(self.rows):
            line = []
            for j in range(self.cols):
                button = QPushButton('', self)
                button.setGeometry(j * self.btn_size, i * self.btn_size + 86, self.btn_size, self.btn_size)
                button.setFont(QtGui.QFont("MS Shell Dlg 2", 10, QtGui.QFont.Bold))
                button.clicked.connect(partial(self.move, i, j))
                line.append(button)
            self.buttons.append(line)

        self.field = GameField(y, x, bombs)

        self.lcd_smile = QPushButton(self)
        self.lcd_smile.setGeometry(self.size().width() // 2 - 25, 26, 50, 50)
        self.lcd_smile.clicked.connect(self.restart)

        self.lcd_bombs = QLCDNumber(self)
        self.lcd_bombs.display(bombs)
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

        self.statistic = QtWidgets.QMenu(self.menubar)
        self.statistic.setTitle("Статистика")

        self.difficulty = QtWidgets.QAction(self)
        self.difficulty.setText("Сложность")
        self.settings.addAction(self.difficulty)

        self.menubar.addAction(self.settings.menuAction())
        self.menubar.addAction(self.statistic.menuAction())

        self.difficulty.triggered.connect(self.change_difficulty)


    def change_difficulty(self):
        self.rows, self.cols, self.bombs = Difficulty.get_values(self)
        # Нужно вынести создание UI в отдельный метод и здесь вызвать его для перерисовки.

    def move(self, row, col):
        # if QtWidgets.qApp.mouseButtons() & QtCore.Qt.CTRL and self.field.generated:
        #    self.field.open(row, col, "f")
        # else:

        if not self.field.generated:
            self.field.generate_field(row, col)
        else:
            self.field.open(row, col, "o")

        self.update_field()

    def update_field(self):
        if self.field.det in [0, 1]:
            for i in range(self.rows):
                for j in range(self.cols):
                    symbol = self.field.get_field()[i][j]
                    if symbol:
                        self.buttons[i][j].setEnabled(False)
                        if symbol.isdigit():
                            self.buttons[i][j].setText(symbol)
                            self.buttons[i][j].setStyleSheet(f'color: {self.colors[symbol]}')
            if self.field.det == 1:
                print('Ветка победы')

        elif self.field.det == -1:
            for r, c in self.field.b_coords:
                self.buttons[r][c].setText("X")


    def restart(self):
        self.field = GameField(self.rows, self.cols, self.bombs)
        for i in range(self.rows):
            for j in range(self.cols):
                self.buttons[i][j].setText("")
                self.buttons[i][j].setStyleSheet('')
                self.buttons[i][j].setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main(20, 20, 40, 12)
    form.show()
    sys.exit(app.exec())