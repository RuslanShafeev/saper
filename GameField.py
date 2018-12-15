import random
from options_file import OptionsFile


class GameField:
    def __init__(self, rows, cols, bombs):
        self.rows = rows
        self.cols = cols
        self.bombs = bombs
        self.cell = {
            "empty": "[ ]",
            "untouched": "",
            "flag": "\u26F3",
            "question": "?",
            "mark": "{}",
            "bomb": "X"
        }
        self.field = [[self.cell["untouched"] for i in range(cols)] for j in range(rows)]
        self.b_coords = []
        self.nbs = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        self.det = 0
        # det - определитель:
        # -1 поражение
        # 0 идет игра
        # 1 победа
        self.generated = False

    # Найти количество бомб вокруг клетки
    def bombs_around(self, row, col):
        k = 0
        for x, y in self.nbs:
            r, c = row + y, col + x
            if r < 0 or c < 0 or r >= self.rows or c >= self.cols:
                continue
            if (r, c) in self.b_coords:
                k += 1
        return k

    # Проверить, выиграл ли игрок
    def check_for_win(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.field[i][j] == self.cell["untouched"] and (i, j) not in self.b_coords:
                    return False
        return True

    # Генерация поля
    # В зависимости от опции "Безопасный старт", положение бомб может находится на кнопке старта
    def generate_field(self, row, col):
        bombs = 0
        arr = []
        for i in range(self.rows * self.cols):
            r1 = i // self.rows
            c1 = i % self.cols
            if OptionsFile().read()[0] and (r1, c1) == (row, col):
                continue
            arr.append((r1, c1))

        while bombs != self.bombs:
            rnd = random.choice(arr)
            self.b_coords.append(rnd)
            arr.remove(rnd)
            bombs += 1

        self.open(row, col, "o")
        self.generated = True

    # Процесс рекурсивного открытия клеток
    def open_cells(self, row, col):
        if self.field[row][col] == self.cell["flag"]:
            return

        bombs = self.bombs_around(row, col)
        if bombs:
            self.field[row][col] = self.cell["mark"].format(bombs)
            return

        self.field[row][col] = self.cell["empty"]
        for y, x in self.nbs:
            r, c = row + y, col + x
            if r < 0 or c < 0 or r >= self.rows or c >= self.cols:
                continue
            if self.field[r][c] == self.cell["empty"] or self.field[r][c].isdigit():
                continue
            self.open_cells(r, c)

    # Открытие клетки
    def open(self, row, col, mode="o"):
        if mode == "f":
            if OptionsFile().read()[1]:
                sym, res = self.field[row][col], 0
                if sym == self.cell["untouched"]:
                    res = self.cell["flag"]
                elif sym == self.cell["flag"]:
                    res = self.cell["question"]
                elif sym == self.cell["question"]:
                    res = self.cell["untouched"]
                self.field[row][col] = res
            else:
                self.field[row][col] = self.cell["untouched"] \
                    if self.field[row][col] == self.cell["flag"] else self.cell["flag"]
        elif mode == "o":
            if (row, col) in self.b_coords:
                self.det = -1
            else:
                self.open_cells(row, col)
                if self.check_for_win():
                    self.det = 1

    def get_field(self):
        return self.field

    def get_state(self):
        return self.det

