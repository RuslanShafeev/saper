import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QCheckBox
from options_file import OptionsFile


class OptionsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Геймплей")
        self.setFixedSize(400, 160)
        self.okay_clicked = False
        self.init_ui()

    def init_ui(self):
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(30, 120, 341, 32)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.start_box = QCheckBox(self)
        self.start_box.setGeometry(QtCore.QRect(10, 10, 111, 17))
        self.start_box.setText("Безопасный старт")

        self.question_box = QCheckBox(self)
        self.question_box.setGeometry(QtCore.QRect(10, 40, 171, 17))
        self.question_box.setText("Показывать знаки вопросов")

        self.time_box = QCheckBox(self)
        self.time_box.setGeometry(QtCore.QRect(10, 70, 121, 17))
        self.time_box.setText("Показывать время")

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def show(self):
        opts = OptionsFile().read()
        self.start_box.setChecked(opts[0])
        self.question_box.setChecked(opts[1])
        self.time_box.setChecked(opts[2])
        self.exec()
        start, question, time = \
            self.start_box.isChecked(), self.question_box.isChecked(), self.time_box.isChecked()

        if self.okay_clicked:
            return OptionsFile().write(start, question, time)
        else:
            return opts

    def accept(self):
        self.okay_clicked = True
        super().accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = OptionsWindow()
    form.show()
    sys.exit(app.exec())
