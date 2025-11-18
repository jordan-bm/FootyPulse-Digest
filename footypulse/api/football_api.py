import requests
from footypulse.utils.config import API_FOOTBALL_KEY

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_FOOTBALL_KEY
}



def get_leagues(): # Fetch list of leagues
    url = f"{BASE_URL}/leagues"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()



def get_league_fixtures(league_id, season): # Get fixtures for a given league and season
    url = f"{BASE_URL}/fixtures"
    params = {
        "league": league_id,
        "season": season
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()


    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()



def get_player_statistics(player_id, season):
    url = f"{BASE_URL}/players"
    params = {"id": player_id, "season": season}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()



def get_lineups(fixture_id): # Gets lineups for a given fixture
    url = f"{BASE_URL}/fixtures/lineups"
    params = {"fixture": fixture_id}

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

