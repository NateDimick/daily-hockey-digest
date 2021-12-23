from csv import writer
from json import load
from os import listdir
from os.path import dirname, realpath, join
from sys import argv
project_directory = dirname(realpath(argv[0]))

"""
relationships to suspect test
shots vs goals scored
shots + blocked shots + goals scored
takeaways vs goals scored

"""


games_folder = join(project_directory, "..", "games")
count = 0
files_checked = 0
for filename in listdir(games_folder):
    files_checked += 1
    with open(join(games_folder, filename), 'r') as f:
        game = load(f)

    away_box = game["teams"]["away"]["teamStats"]["teamSkaterStats"]
    home_box = game["teams"]["home"]["teamStats"]["teamSkaterStats"]
    away_sum = sum([int(float(stat)) for key, stat in away_box.items()])
    home_sum = sum([int(float(stat)) for key, stat in home_box.items()])

    if away_sum == 0 and home_sum == 0:
        continue  # this is a bad data point



