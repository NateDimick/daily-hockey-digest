# Daily Hockey Digest

The TL;DR here is that I have a betting strategy around NHL hockey and I want to have all the stats I want easily accessible to me without having to Google "nhl today" every day. This tool is built to run as a scheduled cron job, every morning, update the data, and then create a forecast for today;s games and mail them straight to my inbox.

## How to use

if you want to set this up yourself, you will need

1. and email address to receive emails.
1. a spare gmail account *or* an email account on a server that allows for SMTP (this requires some code changes)
    1. for gmail, you'll have to go into google account setting and allow access from less secure apps.
1. an API key to API-Sports

rename `.example-env` to `.env` and populate the values accordingly

set `daily-digest.py` to run on a crontab job.

there you go.

## useful links I used

[crontab guru](https://crontab.guru)
[this article](https://towardsdatascience.com/how-to-schedule-python-scripts-with-cron-the-only-guide-youll-ever-need-deea2df63b4e)
