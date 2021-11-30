"""
This script makes API calls to get information daily
"""
from components.project_directory import project_directory
from datetime import datetime, date
from dotenv import load_dotenv
from json import dump, load
from os import environ
from os.path import join
from requests import get
from zoneinfo import ZoneInfo


url = "https://v1.hockey.api-sports.io/games"
tz_string = 'America/New_York'
timezone = ZoneInfo(tz_string)



def parse_games(game_list_json: dict) -> dict:
    results = []

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

            results.append(game_result)

    return results

def get_scores_from_date(date: date, raw: bool=False, record=True) -> dict:
    """
    get the results from the specified date
    """
    header = {
        'x-apisports-key': environ['API_SPORTS_KEY']
    }
    params = {
        'league': 57,
        'season': environ['SEASON'],
        'date': str(date),
        'timezone': tz_string.lower()
    }
    req = get(url, headers=header, params=params)     

    if record:
        raw_request_file = f"{environ['SEASON']}-raw-requests.json"
        with open(join(project_directory, raw_request_file), 'r') as f:
            raw_file = load(f)
        raw_file = raw_file + req.json()['response']
        with open(join(project_directory, raw_request_file), 'w') as f:
            dump(raw_file, f, indent=4)
        
    if raw:
        return req.json()
    else:
        return parse_games(req.json())

def just_todays_games(game_list_json: dict):
    matchups = []
    for game in game_list_json['response']:
        matchups.append((game['teams']['home']['name'], game['teams']['away']['name'], datetime.fromisoformat(game['date']).time()))

    return matchups