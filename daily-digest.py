"""
main script
the goal is to
1. make api calls to get yesterday's results and today's games
2. update database
3. send out email to me with everything I want to know, nicely formatted
"""
import json
from client import get_scores_from_date, just_todays_games
from datetime import date, timedelta
from dotenv import load_dotenv
from mailer import send_email
from os import environ
from os.path import join
from project_directory import project_directory
from statistics import mean, mode, stdev

dotenv_file = join(project_directory, '.env')
load_dotenv(dotenv_file)
json_file = join(project_directory, f"{environ['SEASON']}-processed-results.json")

def game_log(team_name: str) -> list:
    with open(json_file, 'r') as f:
        all_games = json.load(f)

    return [game for game in all_games if game['home'] == team_name or game['away'] == team_name]

def team_summary(team_name: str, game_log: list) -> dict:
    points_scored = []
    home_points_scored = []
    away_points_scored = []
    points_allowed = []
    home_points_allowed = []
    away_points_allowed = []
    
    for game in game_log:
        ot_home_modifier = -1 if game['overtime'] and game['spread'] > 0 else 0
        ot_away_modifier = -1 if game['overtime'] and game['spread'] < 0 else 0
        if team_name == game['home']:
            points_scored.append(game['home_score'] + ot_home_modifier)
            home_points_scored.append(game['home_score'] + ot_home_modifier)
            points_allowed.append(game['away_score'] + ot_away_modifier)
            home_points_allowed.append(game['away_score'] + ot_away_modifier)
        else:
            points_scored.append(game['away_score'] + ot_away_modifier)
            away_points_scored.append(game['away_score'] + ot_away_modifier)
            points_allowed.append(game['home_score'] + ot_home_modifier)
            away_points_allowed.append(game['home_score'] + ot_home_modifier)

    summary = {
        'games_played': len(game_log),
        'games_played_home': len(home_points_allowed),
        'games_played_away': len(away_points_allowed),
        'scoring_average': mean(points_scored),
        'scoring_stddev': stdev(points_scored),
        'scoring_average_home': mean(home_points_scored),
        'scoring_average_away': mean(away_points_scored),
        'highest_score': max(points_scored),
        'highest_score_home': max(home_points_scored),
        'highest_score_away': max(away_points_scored),
        'lowest_score': min(points_scored),
        'lowest_score_home': min(home_points_scored),
        'lowest_score_away': min(away_points_scored),
        'most_common_score': mode(points_scored),
        'nothingburgers': len([p for p in points_scored if p == 0]),
        'nothingburgers_home': len([p for p in home_points_scored if p == 0]),
        'nothingburgers_away': len([p for p in away_points_scored if p == 0]),
        'defense_average': mean(points_allowed),
        'defense_stddev': stdev(points_allowed),
        'defense_average_home': mean(home_points_allowed),
        'defense_average_away': mean(away_points_allowed),
        'defense_average_home': mean(home_points_allowed),
        'defense_average_away': mean(away_points_allowed),
        'highest_allowed': max(points_allowed),
        'highest_allowed_home': max(home_points_allowed),
        'highest_allowed_away': max(away_points_allowed),
        'lowest_allowed': min(points_allowed),
        'lowest_allowed_home': min(home_points_allowed),
        'lowest_allowed_away': min(away_points_allowed),
        'most_common_allowed': mode(points_allowed),
        'shutouts': len([p for p in points_allowed if p == 0]),
        'shutouts_home': len([p for p in home_points_allowed if p == 0]),
        'shutouts_away': len([p for p in away_points_allowed if p == 0])
    }

    return summary

def daily_job():
    today = date.today()
    yesterday = today + timedelta(days=-1)
    yesterdays_results = get_scores_from_date(yesterday)
    with open(json_file, 'r') as f:
        all_results = json.load(f)
    all_results += yesterdays_results
    with open(json_file, 'w') as f:
        json.dump(all_results, f)

    todays_matchups = just_todays_games(get_scores_from_date(today))
    data = []
    for matchup in todays_matchups:
        game = {
            'home_team': matchup[0],
            'away_team': matchup[1],
            'date': matchup[2],
        }
        game['home_stats'] = team_summary(matchup[0], game_log(matchup[0]))
        game['away_stats'] = team_summary(matchup[1], game_log(matchup[1]))
        data.append(game)


    send_email(data)

if __name__ == '__main__':
    try:
        daily_job()
    except Exception as e:
        with open(join(project_directory, f"{date.today()}-error.log"), 'w') as f:
            f.write(e)
