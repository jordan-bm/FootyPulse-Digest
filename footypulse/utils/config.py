import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("FOOTBALL_API_KEY")
EMAIL_API_KEY = os.getenv("EMAIL_API_KEY")
