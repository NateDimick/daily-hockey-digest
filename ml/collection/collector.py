from json import dump, load
from typing import Any
from os.path import dirname, realpath, join
from requests import get
from sys import argv
from time import time, sleep

project_directory = dirname(realpath(argv[0]))

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

def get_season_schedule(year: int, start_end_dates: tuple) -> None:
    """
    year needs to be included because sometimes seasons start late
    examples: 2012 (CBA lockout) and 2020 (pandemic) started in 2013 and 2021
    """
    url = f"https://statsapi.web.nhl.com/api/v1/schedule"
    query_params = {
        "startDate": start_end_dates[0],
        "endDate": start_end_dates[1]
    }
    response = get(url, params=query_params)
    if response.ok:
        data = response.json()
        print(data["totalGames"])
        with open(join(project_directory, "..", "seasons", f"{year}-nhl-season.json"), "w") as f:
            dump(data, f, indent=4)
            
    else:
        print(url, response.status_code, response.reason)

def get_seasons_in_range(start_year: int, end_year: int) -> None:
    """
    inclusive of end_year
    """
    for year in range(start_year, end_year + 1):
        dates = get_season_dates(year)
        print(dates)
        get_season_schedule(year, dates)

def get_games_by_season(year: int) -> None:
    print("Start time: ", time())
    # read season file
    with open(join(project_directory, "..", "seasons", f"{year}-nhl-season.json"), "r") as f:
        season = load(f)
    games_retrieved = 0
    # iterate through dates
    for date in season["dates"]:
        print(date["date"])
    # iterate through games
        for game in date["games"]:
            home_team = game["teams"]["home"]["team"]["name"]
            away_team = game["teams"]["away"]["team"]["name"]
            url = f"https://statsapi.web.nhl.com/api/v1/game/{game['gamePk']}/boxscore"
    # use game pk to get boxscore
            response = get(url)
    # store request in ml/games
            if response.ok:
                game_file = join(project_directory, "..", "games", f"{date['date']}-{away_team}@{home_team}.json")
                with open(game_file, "w") as f:
                    dump(response.json(), f, indent=4)
            else:
                print(url, response.status_code, response.reason, date["date"], game["gamePk"])
            games_retrieved += 1
            if games_retrieved % 100 == 0:
                print(games_retrieved)
            sleep(0.1)

    print("End time: ", time())

def get_games_by_season_for_range(start_year: int, end_year: int) -> None:
    """
    inclusive of end year
    """
    for y in range(start_year, end_year + 1):
        print("-" * 8, y, "-" * 8)
        get_games_by_season(y)
        print("-" * 20)

if __name__ == '__main__':
    #get_seasons_in_range(2008, 2021)
    get_games_by_season_for_range(2008, 2019)
