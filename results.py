import json


RECORDS_PATH = "E:/saper_game_records.json"
STATISTICS_PATH = "E:/saper_game_stats.json"


class GameStat:
    def __init__(self):
        try:
            with open(RECORDS_PATH) as file:
                self.rec = json.loads(file.read())
        except FileNotFoundError:
            self.rec = {}
        try:
            with open(STATISTICS_PATH) as file:
                self.stat = json.loads(file.read())
        except FileNotFoundError:
            default_stat = {
                "games": 0,
                "wins": 0,
                "flags": 0,
                "time": 0,
                "defused": 0
            }
            self.stat = {
                "Новичок": {**default_stat},
                "Эксперт": {**default_stat},
                "Бывалый": {**default_stat},
                "Итого": {**default_stat}
            }

    def get_records(self, mode):
        sl = self.rec[mode] if mode in self.rec else []
        return sorted(sl, key=lambda x: x["time"])

    def put_record(self, mode, player_name, time):
        if mode not in self.rec:
            self.rec[mode] = [
                {
                    "name": player_name,
                    "time": time
                }]
        else:
            self.rec[mode].append(
                {
                    "name": player_name,
                    "time": time
                })

        with open(RECORDS_PATH, "w") as file:
            file.write(json.dumps(self.rec, sort_keys=True, indent=4))

    def get_stats(self, mode):
        mode_stat = self.stat[mode]
        return mode_stat

    def get_games(self, mode):
        return self.get_stats(mode)["games"]

    def get_wins(self, mode):
        return self.get_stats(mode)["wins"]

    def get_flags(self, mode):
        return self.get_stats(mode)["flags"]

    def get_defused(self, mode):
        return self.get_stats(mode)["defused"]

    def get_time(self, mode):
        return self.get_stats(mode)["time"]

    def get_win_rate(self, mode):
        games = self.get_games(mode)
        if games == 0:
            return 0
        return 100 * int(self.get_wins(mode) / games)

    def get_defuse_rate(self, mode):
        flags = self.get_flags(mode)
        if flags == 0:
            return 0
        return 100 * int(self.get_defused(mode) / flags)

    def get_average_time(self, mode):
        games = self.get_games(mode)
        if games == 0:
            return 0
        return int(self.get_time(mode) / games)

    def update_stats(self, mode, win, flags, defused, time):
        for m in (mode, "Итого"):
            self.stat[m]["games"] += 1
            self.stat[m]["wins"] += win
            self.stat[m]["flags"] += flags
            self.stat[m]["defused"] += defused
            self.stat[m]["time"] += time

        with open(STATISTICS_PATH, "w") as file:
            file.write(json.dumps(self.stat, sort_keys=True, indent=4))