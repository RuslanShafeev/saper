import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QDialog


class Difficulty(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('Difficulty.ui', self)
        self.buttonGroup.buttonClicked.connect(self.checked)
        self.mode = (9, 9, 10)
        self.easy.setChecked(True)
        self.okay_clicked = False
        for slider in [self.bombs_slider, self.width_slider, self.height_slider]:
            slider.valueChanged.connect(self.recalculate_sliders)

    def get_values(self):
        ex = Difficulty()
        ex.exec()
        return ex.get_mode()

    def checked(self):
        modes = {'Новичок': (9, 9, 10),
                 'Эксперт': (16, 16, 40),
                 'Бывалый': (16, 30, 99),
                 }
        if self.sender().checkedButton().text() == 'Особый':
            for slider in [self.bombs_slider, self.width_slider, self.height_slider]:
                slider.setEnabled(True)
        else:
            if self.bombs_slider.isEnabled():
                for slider in [self.bombs_slider, self.width_slider, self.height_slider]:
                    slider.setEnabled(False)
            self.mode = modes[self.sender().checkedButton().text()]

    def get_mode(self):
        return self.mode

    def recalculate_sliders(self):
        width, height = self.width_slider.value(), self.height_slider.value()
        bombs = self.bombs_slider.value()
        self.width_lcd.display(width)
        self.height_lcd.display(height)
        self.bombs_lcd.display(bombs)
        self.bombs_slider.setMaximum(width * height // 3 + 1)
        self.bombs_label.setText(f'[9-{self.bombs_slider.maximum()}]')
        self.mode = (height, width, bombs)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Difficulty()
    form.show()
    sys.exit(app.exec())
