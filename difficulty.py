import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QDialogButtonBox, QWidget, QGridLayout, QLabel
from PyQt5.QtWidgets import QRadioButton, QButtonGroup, QSlider, QLCDNumber


class DifficultyWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.modes = {'Новичок': (9, 9, 10),
                      'Эксперт': (16, 16, 40),
                      'Бывалый': (16, 30, 99)
                      }
        self.resize(389, 300)
        self.init_ui()

    def init_ui(self):
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(-70, 260, 341, 32)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayoutWidget_2 = QWidget(self)
        self.gridLayoutWidget_2.setGeometry(130, 20, 121, 91)

        self.gridLayout_2 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)

        for i, row in enumerate([('Высота', 'Ширина', 'Мины'), *self.modes.values()]):
            for j, col in enumerate(row):
                label = QLabel(self.gridLayoutWidget_2)
                label.setText(str(col))
                label.setAlignment(QtCore.Qt.AlignCenter)
                self.gridLayout_2.addWidget(label, i, j, 1, 1)

        mode_label = QLabel(self)
        mode_label.setGeometry(QtCore.QRect(65, 20, 61, 18))
        mode_label.setText('Режим')
        mode_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignCenter |
                                QtCore.Qt.AlignVCenter)

        self.buttonGroup = QButtonGroup(self)
        checkbutton_list = []
        for n, key in enumerate([*self.modes.keys(), 'Особый']):
            rb = QRadioButton(self)
            self.buttonGroup.addButton(rb)
            rb.setGeometry(60, 45 + 25 * n, 71, 17)
            rb.setText(key)
            checkbutton_list.append(rb)

        self.easy, self.normal, self.hard, self.special = checkbutton_list

        lcd_list, slider_list = [], []
        for n, (minimum, maximum) in enumerate([(9, 21), (9, 46), (9, 27)]):
            offset = 40 * n
            slider = QSlider(self)
            slider.setEnabled(False)
            slider.setGeometry(70, 150 + offset, 248, 22)
            slider.setMinimum(minimum)
            slider.setMaximum(maximum)
            slider.setOrientation(QtCore.Qt.Horizontal)
            slider_list.append(slider)

            label = QLabel(self)
            label.setGeometry(22, 147 + offset, 47, 13)
            label.setText(['Высота', 'Ширина', 'Бомбы'][n])

            sublabel = QLabel(self)
            sublabel.setGeometry(22, 157 + offset, 41, 16)
            sublabel.setText(f'[{minimum}-{maximum}]')

            lcd = QLCDNumber(self)
            lcd.setGeometry(327, 148 + offset, 41, 21)
            lcd.setDigitCount(3)
            lcd.setSegmentStyle(QLCDNumber.Flat)
            lcd.setProperty("intValue", 9)
            lcd_list.append(lcd)

        self.bombs_label = sublabel
        self.height_slider, self.width_slider, self.bombs_slider = slider_list
        self.height_lcd, self.width_lcd, self.bombs_lcd = lcd_list

        self.buttonGroup.buttonClicked.connect(self.checked)
        self.mode = (9, 9, 10)
        self.setWindowTitle("Сложность")
        self.easy.setChecked(True)
        self.okay_clicked = False
        for slider in [self.bombs_slider, self.width_slider, self.height_slider]:
            slider.valueChanged.connect(self.recalculate_sliders)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def get_values(self):
        self.exec()
        return (self.get_okay_clicked(), *self.get_mode())

    def accept(self):
        self.okay_clicked = True
        super().accept()

    def checked(self):
        if self.sender().checkedButton().text() == 'Особый':
            for slider in [self.bombs_slider, self.width_slider, self.height_slider]:
                slider.setEnabled(True)
        else:
            if self.bombs_slider.isEnabled():
                for slider in [self.bombs_slider, self.width_slider, self.height_slider]:
                    slider.setEnabled(False)
            self.mode = self.modes[self.sender().checkedButton().text()]

    def get_mode(self):
        return self.mode

    def get_okay_clicked(self):
        return self.okay_clicked

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
    form = DifficultyWindow()
    form.show()
    sys.exit(app.exec())
