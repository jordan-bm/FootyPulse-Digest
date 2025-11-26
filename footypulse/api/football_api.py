import requests
import pandas as pd
from footypulse.utils.config import API_FOOTBALL_KEY

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_FOOTBALL_KEY
}



def get_players_from_fixtures(league_id, season, limit_games=30):
    fixtures = get_league_fixtures(league_id, season)

    rows = []
    count = 0

    for fixture in fixtures["response"]:
        if count > limit_games:   # prevent free API burn
            break
        
        fixture_id = fixture["fixture"]["id"]
        lineups = get_lineups(fixture_id)

        for team in lineups.get("response", []):
            team_name = team["team"]["name"]
            team_logo = team["team"]["logo"]

            for p in team["startXI"]:
                player = p["player"]
                
                # pull stats for each player
                stats = get_player_statistics(player["id"], season)
                if not stats["response"]: 
                    continue

                stat_block = stats["response"][0]["statistics"][0]  # API response shape

                rows.append({
                    "player_id": player["id"],
                    "name": player["name"],
                    "photo": stats["response"][0]["player"]["photo"],       
                    "team": team_name,
                    "logo": team_logo,                                      
                    "league": stat_block["league"]["name"],
                    "form": float(stat_block["games"]["rating"] or 0),
                    "consistency": float(stat_block["games"]["appearences"] or 0),
                    "delta": float(stat_block["goals"]["total"] or 0),        # replace later w XG delta
                    "trend_score": float(stat_block["goals"]["total"] or 0)  # temp - replaced later
                })

        count += 1
    
    return pd.DataFrame(rows)



def get_leagues(): # Get list of leagues
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

