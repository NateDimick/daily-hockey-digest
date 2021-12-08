"""
main script
the goal is to
1. make api calls to get yesterday's results and today's games
2. update database
3. send out email to me with everything I want to know, nicely formatted
"""
import json
from components.client import get_scores_from_date, just_todays_games
from components.mailer import send_email
from components.project_directory import project_directory
from datetime import date, timedelta
from dotenv import load_dotenv
from os import environ, read
from os.path import join, exists
from shutil import copyfile
from statistics import mean, mode, stdev
from traceback import format_exc

dotenv_file = join(project_directory, '.env')
load_dotenv(dotenv_file)
json_file = join(project_directory, f"{environ['SEASON']}-processed-results.json")
summaries_file = join(project_directory, f"{environ['SEASON']}-team-summaries.json")
raw_file = join(project_directory, f"{environ['SEASON']}-raw-requests.json")
do_not_run_file = join(project_directory, 'do_not_run.flag')
today = date.today()
yesterday = today + timedelta(days=-1)

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
        # 'games_played_home': len(home_points_allowed),
        # 'games_played_away': len(away_points_allowed),
        'scoring_average': mean(points_scored),
        # 'scoring_stddev': stdev(points_scored),
        # 'scoring_average_home': mean(home_points_scored),
        # 'scoring_average_away': mean(away_points_scored),
        'highest_score': max(points_scored),
        # 'highest_score_home': max(home_points_scored),
        # 'highest_score_away': max(away_points_scored),
        'lowest_score': min(points_scored),
        # 'lowest_score_home': min(home_points_scored),
        # 'lowest_score_away': min(away_points_scored),
        'most_common_score': mode(points_scored),
        'nothingburgers': len([p for p in points_scored if p == 0]),
        # 'nothingburgers_home': len([p for p in home_points_scored if p == 0]),
        # 'nothingburgers_away': len([p for p in away_points_scored if p == 0]),
        'defense_average': mean(points_allowed),
        # 'defense_stddev': stdev(points_allowed),
        # 'defense_average_home': mean(home_points_allowed),
        # 'defense_average_away': mean(away_points_allowed),
        'highest_allowed': max(points_allowed),
        # 'highest_allowed_home': max(home_points_allowed),
        # 'highest_allowed_away': max(away_points_allowed),
        'lowest_allowed': min(points_allowed),
        # 'lowest_allowed_home': min(home_points_allowed),
        # 'lowest_allowed_away': min(away_points_allowed),
        'most_common_allowed': mode(points_allowed),
        'shutouts': len([p for p in points_allowed if p == 0]),
        # 'shutouts_home': len([p for p in home_points_allowed if p == 0]),
        # 'shutouts_away': len([p for p in away_points_allowed if p == 0])
    }

    return summary

def advanced_team_summary(team_name:str, game_log:list) -> dict:
    pass

def make_keys_readable(dict: dict):
    readable_keys = []
    for k in dict:
        key = k.replace('_', ' ')
        if key.endswith('home'):
            key = key.replace('home', 'away/home')
        elif key.endswith('away'):  # away stats would have same name as home stats
            continue
        readable_keys.append(key)
    return readable_keys

def list_stats_filter_home_or_away(summary: dict, home: bool):
    anti_suffix = 'away' if home else 'home'
    stats = []
    for k in summary:
        if not k.endswith(anti_suffix):
            stats.append(summary[k])

    return stats


def daily_job():
    yesterdays_results = get_scores_from_date(yesterday)
    with open(json_file, 'r') as f:
        all_results = json.load(f)
    all_results += yesterdays_results
    with open(json_file, 'w') as f:
        json.dump(all_results, f, indent=4)

    todays_matchups = just_todays_games(get_scores_from_date(today, raw=True, record=False))
    print(todays_matchups)
    data = []
    for matchup in todays_matchups:
        game = {
            'home_team': matchup[0],
            'away_team': matchup[1],
            'datetime': matchup[2].strftime("%I:%M %p").lstrip("0"),
        }
        home_stats = team_summary(matchup[0], game_log(matchup[0]))
        just_home_stats = list_stats_filter_home_or_away(home_stats, True)
        away_stats = team_summary(matchup[1], game_log(matchup[1]))
        just_away_stats = list_stats_filter_home_or_away(away_stats, False)
        readable_stats = make_keys_readable(home_stats)
        game['stats'] = zip(just_away_stats, readable_stats, just_home_stats)
        data.append(game)
        


    send_email(data)

def do_not_run() -> bool:
    return exists(do_not_run_file)

def backup_files(files):
    for file in files:
        copyfile(file, file + '.backup')


if __name__ == '__main__':
    if do_not_run():
        print("do not run")
        exit()
    try:
        backup_files([json_file, raw_file])
        daily_job()
    except Exception as e:
        with open(do_not_run_file, 'w') as f:
            f.write('1')
        with open(join(project_directory, f"{today}-error.log"), 'w') as f:
            f.write(str(e) + '\n\n')
            f.write(format_exc())
