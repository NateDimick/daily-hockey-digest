"""
This script makes API calls to get information daily
"""
from datetime import datetime
from dotenv import load_dotenv
from os import environ
from requests import get
from zoneinfo import ZoneInfo
