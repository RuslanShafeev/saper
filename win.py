import sys
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QLabel, QLineEdit
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from random import randint


class WinDialog(QDialog):
    def __init__(self, mode, time):
        super().__init__()
        self.setWindowTitle("Спасибо за мир без бомб!")
        self.setFixedSize(400, 190)
        self.init_ui()
        self.info.setText(self.info.text().format(mode, time))

    def init_ui(self):
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(160, 150, 71, 32)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(150, 20, 91, 21))
        self.label.setText("Победа!")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)

        self.info = QLabel(self)
        self.info.setGeometry(50, 40, 291, 81)
        self.info.setText("Уровень сложности: {}\n"
                          "Время: {}\n"
                          "Введите ваше имя:")
        font = QFont()
        font.setPointSize(12)
        self.info.setFont(font)
        self.info.setAlignment(QtCore.Qt.AlignCenter)

        self.name = QLineEdit(self)
        self.name.setGeometry(110, 120, 171, 20)
        self.name.setObjectName("name")

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def show(self):
        self.exec()
        return self.get_name()

    def get_name(self):
        rnd = "un{}".format(randint(1, 999))
        return rnd if not self.name.text() else self.name.text()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = WinDialog('Эксперт', 99)
    form.show()
    sys.exit(app.exec())
