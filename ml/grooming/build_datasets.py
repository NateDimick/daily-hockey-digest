from csv import writer
from datetime import date
from enum import Enum
from json import load
from os import listdir
from os.path import dirname, realpath, join
from requests import get
from sys import argv
project_directory = dirname(realpath(argv[0]))

class Bet(Enum):
    pass

class TeamRecord:
    def __init__(self, name):
        self.name = name
        self.venues = []  # 0 or 1, 0 for home, 1 for away
        self.rest_hours = [] # hours between puck drop an last puck drop
        self.goals_scored = []
        self.goals_allowed = []
        self.shots_taken = []  # sum of shots + blocked
        self.shots_blocked = []  # just blocked
        self.shots_allowed = []
        self.blocked_shots = []
        self.giveaways = []
        self.takeaways = []
        self.hits = []
        self.hits_taken = []
        self.penalty_minutes = []
        self.power_play_minutes = []  # opponent PIM
        self.power_play_opportunities = []
        self.power_plays_allowed = []

    def append(self, skaterStats: dict, oppSkaterStats: dict) -> None:
        """
        update a team's record with skaterStats from a boxscore
        """
        pass

    def per_game(self, stat_name: str, through: int = 0) -> float:
        """
        stat_name: name of a property of this class
        through: the number of games through to calculate """
        self_as_dict = self.__dict__
        stat_record = self_as_dict.get(stat_name, [])
        if through:
            return sum(stat_record[:through]) / len(stat_record[:through])
        else:
            return sum(stat_record) / len(stat_record)

    def games_played(self) -> int:
        return len(self.goals_scored)

    def shooting_splits(self, through: int = 0) -> tuple:
        """
        return a tuple with shots-on-goal %, and goal %
        """



def get_season_dates(season_start_year: int) -> tuple:
    url = f"https://statsapi.web.nhl.com/api/v1/seasons/{season_start_year}{season_start_year + 1}"
    response = get(url)
    if response.ok:
        data = response.json()
        #print(data)
        season = data["seasons"][0]
        return (season["regularSeasonStartDate"], season["regularSeasonEndDate"])
    else:
        print(url, response.status_code, response.reason)


def build_season_dataset(year: int) -> None:
    # get season start and end dates
    # get names of files
    # iterate over dates from season start to end, reading files that start with the current date
    # generate stats
    # categorize game
    # write stats to csv
    pass


if __name__ == '__main__':
    print("hello")
    testRecord = TeamRecord("Bruins")
    testRecord.goals_scored = [5, 5, 8, 1, 3, 4, 2]
    print(testRecord.per_game("goals_scored", 4))