"""
main script
the goal is to
1. make api calls to get yesterday's results and today's games
2. update database
3. send out email to me with everything I want to know, nicely formatted
"""
import json
import smtplib
from datetime import date
from dotenv import load_dotenv
from email.message import EmailMessage
from os import environ
from os.path import dirname, realpath, join
from smtplib import SMTP_SSL
from sys import argv

project_directory = dirname(realpath(argv[0]))
dotenv_file = join(project_directory, '.env')
json_file = join(project_directory, f"{environ['SEASON']}_hockey.json")

def send_email(body: str):
    server = SMTP_SSL('smtp.gmail.com')
    server.ehlo()
    server.login(environ['SENDER_EMAIL'], environ['SENDER_PASSWORD'])
    mail = EmailMessage()
    mail["subject"] = f"Hockey Digest {date.today()}"
    mail['to'] = environ['RECEIVER_EMAIL']
    mail['from'] = environ['SENDER_EMAIL']
    # TODO: add body and attachment
    mail.set_content = body
    server.send_message(mail)
    server.quit()


def process_game(games: list(dict), history: dict):
    for game in games:
        h = game['home']
        a = game['away']
        h_home = history[h]['home']
        h_overall = history[h]['overall']
        a_away = history[a]['away']
        a_overall = history[a]['overall']
        all_four = [h_overall, h_home, a_overall, a_away]
        round = 1
        for doc in all_four:
            doc['games'] += 1
            doc['overtimes'] += game['overtime']
            score_for = 0
            score_allowed = 0
            if round <= 2:
                score_for = game['home_score']
                score_allowed = game['allowed_score']
            else:
                score_allowed = game['home_score']
                score_for = game['allowed_score']

            doc['goals_for'] += score_for
            doc['goals_allowed'] += score_allowed
            doc['history_for'].append(score_for)
            doc['history_allowed'].append(score_allowed)

            if score_for > doc['max_score']:
                doc['max_score'] = score_for

            if score_for < doc['min_score']:
                doc['min_score'] = score_for

            if score_for == 0:
                doc['goose_eggs'] += 1

            if score_allowed > doc['max_score_allowed']:
                doc['max_score_allowed'] = score_allowed

            if score_allowed < doc['min_score_allowed']:
                doc['min_score_allowed'] = score_allowed

            if score_allowed == 0:
                doc['shutouts'] += 1

            if score_for > score_allowed and game['overtime']:
                doc['overtime_goals'] += 1


            round += 1



if __name__ == '__main__':
    # run the script
    pass