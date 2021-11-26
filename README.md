# Daily Hockey Digest

## About this Project

I have a gambling strategy based on NHL hockey. This package is built around the `daily_digest.py` script, which is built to be run as a daily cron job. The idea is to get information from API-Sports, which was the best free sports info api I could find, record game results, and then send stats going into a given day's games to my email inbox. Emails are formatted using Jinja, a great html templating tool that is familiar to anyone who has used Flask. Emails are sent over SMTP, which make Google complain about security but I like it because it's easy and fast to set up and use compared to using the gmail sdk. Data is stored in json files because they are easy to load and fast to set up compared to a document store database like Mongo.

## How to use

if you want to set this up yourself, you will need

1. and email address to receive emails.
1. a spare gmail account *or* an email account on a server that allows for SMTP (this requires some code changes)
    1. for gmail, you'll have to go into google account setting and allow access from less secure apps.
1. an API key to API-Sports

rename `.example-env` to `.env` and populate the values accordingly

set `daily_digest.py` to run on a crontab job.

I run this on a raspberry pi that is always on, but I suppose with modifications this could run in the cloud.

there you go.

## Feature Roadmap

If I continue development on this project, then the following will be added in this order of priority:

1. additional stats derived from scoring data/changing the set of produced stats depending on what I want
1. styling to the html template
1. switching from json files to a local or cloud instance of mongo db
1. if I get really adventurous, implementing some ML to give betting suggestions for each game based on collected data

I have bigger ambitions for a local flask app to do similar operations as this, but with the info provided through a web page rather than a daily email. The daily email was a much faster project to get to MVP stage. This project may be deprecated from my use by next season.

## useful links I used

Never used crontab before this project

[crontab guru](https://crontab.guru)
[this article](https://towardsdatascience.com/how-to-schedule-python-scripts-with-cron-the-only-guide-youll-ever-need-deea2df63b4e)

my crontab is:

`0 9 * * * /bin/python3 /home/ubuntu/Projects/daily-hockey-digest/daily_digest.py`
