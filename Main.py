import sys

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QRadioButton, QHBoxLayout, \
    QLCDNumber
from PyQt5 import QtGui


class Main(QWidget):
    def __init__(self, x, y, size, bombs):
        super().__init__()
        self.setGeometry(300, 300, x * size, y * size + 60)
        self.setFixedSize(x * size, y * size + 60)

        font = QtGui.QFont()
        font.setPointSize(100)

        self.buttons = []
        for i in range(0, size * x, size):
            line = []
            for j in range(0, size * y, size):
                button = QPushButton('', self)
                button.setGeometry(i, j + 60, size, size)
                button.clicked.connect(self.step)
                line.append(button)
            self.buttons.append(line)

        self.lcd_smile = QPushButton(self)
        self.lcd_smile.setGeometry(self.size().width() // 2 - 25, 5, 50, 50)

        self.lcd_bombs = QLCDNumber(self)
        self.lcd_bombs.display(bombs)
        self.lcd_bombs.setGeometry(10, 5, 80, 50)
        self.lcd_bombs.setStyleSheet('color: red; background-color: black')
        self.lcd_bombs.setDigitCount(3)
        self.lcd_bombs.setSegmentStyle(2)

        self.lcd_step = QLCDNumber(self)
        self.lcd_step.display(0)
        self.lcd_step.setGeometry(self.size().width() - 90, 5, 80, 50)
        self.lcd_step.setStyleSheet('color: red; background-color: black')
        self.lcd_step.setDigitCount(3)
        self.lcd_step.setSegmentStyle(2)

    def step(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main(10, 10, 40, 12)
    form.show()
    sys.exit(app.exec())
