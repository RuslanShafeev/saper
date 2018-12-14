import json


FILE_PATH = "D:/saper_game_stat.json"
MODE_EASY = "easy"
MODE_MEDIUM = "medium"
MODE_HARD = "hard"


class GameStat:
    def __init__(self):
        try:
            with open(FILE_PATH) as file:
                self.stat = json.loads(file.read())
        except FileNotFoundError:
            self.stat = {}

    def get_list(self, mode):
        sl = self.stat[mode] if mode in self.stat else []
        return sorted(sl, key=lambda x: x["time"])

    def put(self, mode, player_name, time):
        if mode not in self.stat:
            self.stat[mode] = [
                {
                    "name": player_name,
                    "time": time
                }]
        else:
            self.stat[mode].append(
                {
                    "name": player_name,
                    "time": time
                })

        with open(FILE_PATH, "w") as file:
            file.write(json.dumps(self.stat, sort_keys=True, indent=4))


# gs = GameStat()
# res = gs.get_list(MODE_EASY)
# print(res)
# gs.put(MODE_EASY, "Sanya", 58)
# print(gs.get_list(MODE_EASY))