import pandas as pd

def fixtures_to_df(raw_json): # Converts fixture JSON response into a clean DataFrame
    # Raw JSON shape: {'response': [ {fixture}, {fixture}, ... ]}
    fixtures = raw_json.get("response", [])
    rows = []

    for f in fixtures:
        league = f["league"]["name"]
        league_id = f["league"]["id"]
        date = f["fixture"]["date"]
        fixture_id = f["fixture"]["id"]

        home_team = f["teams"]["home"]["name"]
        away_team = f["teams"]["away"]["name"]
        home_team_id = f["teams"]["home"]["id"]
        away_team_id = f["teams"]["away"]["id"]

        home_goals = f["goals"]["home"]
        away_goals = f["goals"]["away"]

        rows.append({
            "fixture_id": fixture_id,
            "league_id": league_id,
            "league": league,
            "date": date,

            "home_team": home_team,
            "away_team": away_team,
            "home_team_id": home_team_id,
            "away_team_id": away_team_id,

            "home_goals": home_goals,
            "away_goals": away_goals
        })

    return pd.DataFrame(rows)
