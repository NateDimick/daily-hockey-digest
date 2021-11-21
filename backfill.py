"""
run this script to get backfill data up to this point of the season
"""
from datetime import date, datetime, timedelta
from json import dump
from os import environ
from requests import get
from time import sleep

header = {
            'x-apisports-key': environ['API_SPORTS_KEY']
        }
url = "https://v1.hockey.api-sports.io/games"
timezone = 'America/New_York'

def parse_games(game_list_json: dict) -> dict:
        results = {
            'games': []
        }

        for game in game_list_json['response']:
            game_result = {
                'home': game['teams']['home']['name'],
                'away': game['teams']['away']['name'],
                'completed': game['status']['short'] in ['FT', 'AOT'],
                'date': game['date']
            }
            game_result['home_score'] = game['scores']['home']
            game_result['away_score'] = game['scores']['away']
            game_result['overtime'] = game['periods']['overtime'] != None
            game_result['spread'] = game_result['home_score'] - game_result['away_score']
            game_result['total'] = game_result['home_score'] + game_result['away_score']
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
            'timezone': timezone.lower()
        }
        req = get(url, headers=header, params=params)     

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

if __name__ =='__main__':
    scores = get_backfill_scores('11-3-2021')