"""
run this script to get backfill data up to this point of the season
"""
from datetime import date, datetime, timedelta
from dotenv import load_dotenv
from json import dump, load
from os import environ
from requests import get
from time import sleep
from zoneinfo import ZoneInfo

load_dotenv('.env')
header = {
            'x-apisports-key': environ['API_SPORTS_KEY']
        }
url = "https://v1.hockey.api-sports.io/games"
tz_string = 'America/New_York'
timezone = ZoneInfo(tz_string)

raw_requests = []

def parse_games(game_list_json: dict) -> dict:
        results = {
            'games': []
        }

        for game in game_list_json['response']:
            game_result = {
                'home': game['teams']['home']['name'],
                'away': game['teams']['away']['name'],
                'completed': game['status']['short'] in ['FT', 'AOT', 'AP'],
                'date': game['date']
            }
            if game_result['completed']:
                game_result['home_score'] = game['scores']['home']
                game_result['away_score'] = game['scores']['away']
                game_result['overtime'] = game['periods']['overtime'] != None
                game_result['spread'] = game_result['home_score'] - game_result['away_score']
                game_result['total'] = game_result['home_score'] + game_result['away_score']
                home_periods, away_periods = [], []
                for k in game['periods']:
                    period_score = game['periods'][k]
                    if period_score:
                        period_score = period_score.split("-")
                        home_periods.append(int(period_score[0]))
                        away_periods.append(int(period_score[1]))

                game_result['periods'] = {
                    'home': home_periods,
                    'away': away_periods
                }

                results['games'].append(game_result)

        return results

def get_scores_from_date(date: date, raw: bool=False) -> dict:
        """
        get the results from the specified date
        """
        params = {
            'league': 57,
            'season': environ['SEASON'],
            'date': str(date),
            'timezone': tz_string.lower()
        }
        req = get(url, headers=header, params=params)     

        raw_requests.append(req.json())
        if raw:
            return req.json()
        else:
            return parse_games(req.json())

def get_backfill_scores(start_date_iso: str):
        """
        back fill results if application starts mid-season
        """
        iterating_date = date.fromisoformat(start_date_iso)
        yesterday = (datetime.now(timezone) + timedelta(days=-1)).date()
        # iterate from season start date to day before today
        all_games = []
        while iterating_date <= yesterday:
            # get the games for each day
            all_games += get_scores_from_date(iterating_date)['games']
            print(iterating_date)
            print(len(all_games))
            iterating_date = iterating_date + timedelta(days=1)
            sleep(6.2)  # abide by rate limit of 10/minute


        # output results to file
        return all_games

def process_cached_backfill(filename):
    with open(filename, 'r') as f:
        backfill = load(f)

    all_games = []
    for date in backfill:
        all_games += parse_games(date)['games']

    return all_games


if __name__ =='__main__':
    # try:
    #     scores = get_backfill_scores('2021-11-18')
    #     with open('backlog.json', 'w') as f:
    #         dump(scores, f)
    #     with open('raw.json', 'w') as f:
    #         dump(raw_requests, f)
    # except:
    #     with open('raw.json', 'w') as f:
    #             dump(raw_requests, f)
    scores = process_cached_backfill('raw-thru-nov-21.json')
    with open('backlog.json', 'w') as f:
            dump(scores, f)
