import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from footypulse.api.football_api import get_league_fixtures
from footypulse.analytics.fixtures_processing import fixtures_to_df
from footypulse.analytics.player_extraction import extract_player_ids

def main():
    print("Fetching recent fixtures...")
    raw = get_league_fixtures(39, 2023)   # Premier League 2023/2024 (Free API doesn't allow just passed/current season)
    # print("RAW RESPONSE SAMPLE:") # Debug
    # print(raw) # Debug


    fixtures_df = fixtures_to_df(raw)
    print("Fixtures downloaded:", len(fixtures_df))
    print(fixtures_df.head())

    print("\nExtracting players...")
    import footypulse.api.football_api as api

    players = extract_player_ids(fixtures_df, api)
    print("Players extracted:", len(players))
    print(list(players)[:10])  # show sample

if __name__ == "__main__":
    main()
