import requests
import pandas as pd
import json
from pathlib import Path
from footypulse.utils.config import API_FOOTBALL_KEY

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_FOOTBALL_KEY
}

# Cache directory: <repo_root>/data/cache
BASE_DIR = Path(__file__).resolve().parents[2]
CACHE_DIR = BASE_DIR / "data" / "cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

def _load_cache(name: str):
    path = CACHE_DIR / name
    if path.exists():
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    return None

def _save_cache(name: str, data):
    path = CACHE_DIR / name
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f)



def get_players_from_fixtures(league_id, season, limit_games=30):
    fixtures = get_league_fixtures(league_id, season)

    rows = []
    count = 0

    for fixture in fixtures["response"]:
        if count >= limit_games:   # prevent API overload
            break
        
        fixture_id = fixture["fixture"]["id"]
        lineups = get_lineups(fixture_id)

        for team in lineups.get("response", []):
            # team info from lineups (for fallback)
            lineup_team_name = team["team"]["name"]
            lineup_team_logo = team["team"]["logo"]

            for p in team.get("startXI", []):
                player = p["player"]
                player_id = player["id"]

                # fetch player season stats
                stats = get_player_statistics(player_id, season)
                if not stats["response"]:
                    continue

                stat = stats["response"][0]
                player_info = stat["player"]
                stat_block = stat["statistics"][0]

                # primary sources from player stats
                team_name = stat_block["team"]["name"] or lineup_team_name
                team_logo = stat_block["team"]["logo"] or lineup_team_logo

                rows.append({
                    "player_id": player_info["id"],
                    "name": player_info["name"],
                    "photo": player_info.get("photo", ""),
                    "team": team_name,
                    "logo": team_logo,
                    "league": stat_block["league"]["name"],

                    # analytics inputs
                    "form": float(stat_block["games"]["rating"] or 0),
                    "consistency": float(stat_block["games"]["appearences"] or 0),
                    "delta": float(stat_block["goals"]["total"] or 0),

                    # sorting
                    "trend_score": float(stat_block["goals"]["total"] or 0)
                })

        count += 1
    
    fixtures = get_league_fixtures(league_id, season) # Debug
    print("Fixtures returned:", len(fixtures.get("response", []))) # Debug


    return pd.DataFrame(rows)



def get_leagues(): # Get list of leagues
    url = f"{BASE_URL}/leagues"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.json()



def get_league_fixtures(league_id, season, use_cache: bool = True):
    # Get fixtures for a given league and season, with caching
    cache_name = f"fixtures_{league_id}_{season}.json"

    if use_cache:
        cached = _load_cache(cache_name)
        if cached is not None:
            return cached

    url = f"{BASE_URL}/fixtures"
    params = {
        "league": league_id,
        "season": season,
        "status": "FT",  # completed only; stats available
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    if use_cache:
        _save_cache(cache_name, data)

    return data



def get_player_statistics(player_id, season, use_cache: bool = True):
    # Get per-season player statistics, cached per (player, season)
    cache_name = f"player_{player_id}_{season}.json"

    if use_cache:
        cached = _load_cache(cache_name)
        if cached is not None:
            return cached

    url = f"{BASE_URL}/players"
    params = {"id": player_id, "season": season}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    if use_cache:
        _save_cache(cache_name, data)

    return data



def get_lineups(fixture_id, use_cache: bool = True):
    # Gets lineups for a given fixture, cached by fixture ID
    cache_name = f"lineups_{fixture_id}.json"

    if use_cache:
        cached = _load_cache(cache_name)
        if cached is not None:
            return cached

    url = f"{BASE_URL}/fixtures/lineups"
    params = {"fixture": fixture_id}

    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    data = response.json()

    if use_cache:
        _save_cache(cache_name, data)

    return data


