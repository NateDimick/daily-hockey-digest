from json import load
from os import listdir
from os.path import dirname, realpath, join
from sys import argv
project_directory = dirname(realpath(argv[0]))


games_folder = join(project_directory, "..", "games")
count = 0
files_checked = 0
team_names = set()
for filename in listdir(games_folder):
    files_checked += 1
    with open(join(games_folder, filename), 'r') as f:
        game = load(f)

    away_box = game["teams"]["away"]["teamStats"]["teamSkaterStats"]
    home_box = game["teams"]["home"]["teamStats"]["teamSkaterStats"]

    away_sum = sum([int(float(stat)) for key, stat in away_box.items()])
    home_sum = sum([int(float(stat)) for key, stat in home_box.items()])
    team_names.add(game["teams"]["away"]["team"]["name"])
    team_names.add(game["teams"]["home"]["team"]["name"])

    if away_sum == 0 and home_sum == 0:
        count += 1
        print(filename)

    if "all-star" in filename.lower():
        print(filename)

print(count, "/", files_checked)
print(team_names)

"""
This is the output of my script
2008-10-05-Edmonton Oilers@Dallas Stars.json
2008-10-04-Detroit Red Wings@Toronto Maple Leafs.json
2008-10-04-Minnesota Wild@Montréal Canadiens.json
2008-10-05-Anaheim Ducks@Vancouver Canucks.json
2008-10-05-San Jose Sharks@Los Angeles Kings.json
2009-01-25-All-Stars West@All-Stars East.json
2008-10-05-Columbus Blue Jackets@Toronto Maple Leafs.json
2008-10-05-Buffalo Sabres@Detroit Red Wings.json
2008-10-05-Boston Bruins@Washington Capitals.json
2008-10-05-Colorado Avalanche@Chicago Blackhawks.json
2008-10-04-Philadelphia Flyers@New Jersey Devils.json
2008-10-04-Los Angeles Kings@Phoenix Coyotes.json
2008-10-06-New York Islanders@Florida Panthers.json
2008-10-04-New York Islanders@Boston Bruins.json
2008-10-04-St. Louis Blues@Atlanta Thrashers.json
2008-10-05-Nashville Predators@Carolina Hurricanes.json
2008-10-07-Philadelphia Flyers@Philadelphia Phantoms.json
17 / 15107

it appears some of these games are preseason games
not sur eif I should keep them"""