"""
This Script will be responsible for mailing me my daily dose of hockey info
"""
from components.project_directory import project_directory
from datetime import date
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from os import environ
from os.path import join
from smtplib import SMTP_SSL


def send_email(data: list):
    server = SMTP_SSL('smtp.gmail.com')
    server.ehlo()
    server.login(environ['SENDER_EMAIL'], environ['SENDER_PASSWORD'])
    mail = MIMEMultipart('alternative')
    mail["Subject"] = f"Hockey Digest {date.today()}"
    mail['To'] = environ['RECEIVER_EMAIL']
    mail['From'] = environ['SENDER_EMAIL']
    with open(join(project_directory,'template.html'), 'r') as f:
        body_template = Template(f.read())
    # TODO figure out template rendering
    body = body_template.render(data=data, date=date.today())
    body_part = MIMEText(body, 'html')
    mail.attach(body_part)

    server.sendmail(environ['SENDER_EMAIL'], environ['RECEIVER_EMAIL'], mail.as_string())

    # mail.set_content = body
    # server.send_message(mail)
    server.quit()
