class OptionsFile:
    def __init__(self):
        self.PATH = "D:/saper_options"

    def read(self):
        try:
            with open(self.PATH) as file:
                return tuple(map(eval, file.read().split()))
        except Exception:
            return True, False, True

    def write(self, start, question, box):
        with open(self.PATH, "w") as file:
            file.write("{} {} {}".format(start, question, box))
            return start, question, box