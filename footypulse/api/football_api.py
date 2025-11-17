import requests
from footypulse.utils.config import API_FOOTBALL_KEY

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_FOOTBALL_KEY
}

def get_leagues():
    # Fetch list of leagues
    url = f"{BASE_URL}/leagues"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()
