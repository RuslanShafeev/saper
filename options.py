import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QDialog
from options_file import OptionsFile


class OptionsWindow(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('options.ui', self)
        self.setWindowTitle("Геймплей")
        self.setFixedSize(400, 160)
        self.okay_clicked = False

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