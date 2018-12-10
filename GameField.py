import random


class GameField:
    def __init__(self, rows, cols, bombs):
        self.rows = rows
        self.cols = cols
        self.bombs = bombs
        self.cell = {
            "empty": "[ ]",
            "untouched": "",
            "flag": "F",
            "question": "?",
            "mark": "{}",
            "bomb": "X"
        }
        self.field = [[self.cell["untouched"] for i in range(cols)] for j in range(rows)]
        self.b_coords = []
        self.nbs = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        self.det = 0
        self.generated = False

    def bombs_around(self, row, col):
        k = 0
        for x, y in self.nbs:
            r, c = row + y, col + x
            if r < 0 or c < 0 or r >= self.rows or c >= self.cols:
                continue
            if (r, c) in self.b_coords:
                k += 1
        return k

    def check_for_win(self):
        k = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.field[i][j] == self.cell["empty"] or self.field[i][j].isdigit():
                    continue
                if self.field[i][j] in ("F", "?"):
                    continue
                k += 1
                if k > self.bombs:
                    return False
        return True

    def generate_field(self, row, col):
        bombs = 0
        while bombs != self.bombs:
            r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (r != row or c != col) and not (r, c) in self.b_coords:
                self.b_coords.append((r, c))
                bombs += 1
        self.open(row, col, "o")
        self.generated = True

    def open_cells(self, row, col):
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

    def open(self, row, col, mode="o"):
        if mode == "f":
            self.field[row][col] = self.cell["untouched"] \
                if self.field[row][col] == self.cell["flag"] else self.cell["flag"]
        elif mode == "q":
            self.field[row][col] = self.cell["untouched"] \
                if self.field[row][col] == self.cell["question"] else self.cell["question"]
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

