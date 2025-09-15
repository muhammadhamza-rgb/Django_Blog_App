# project/settings_prod.py
import os

import dj_database_url
from dotenv import load_dotenv

from .settings_base import *

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = False
ALLOWED_HOSTS = ["*"]

DATABASES = {"default": dj_database_url.config(default=os.getenv("DATABASE_URL"))}
