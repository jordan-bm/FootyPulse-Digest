import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from footypulse.api.football_api import get_league_fixtures
from footypulse.analytics.fixtures_processing import fixtures_to_df
from footypulse.analytics.player_extraction import extract_player_ids
from footypulse.analytics.engine import compute_trending_players
from footypulse.digest.templates.render import render_digest
import footypulse.api.football_api as api

def main():
    league = 39   # Premier League
    season = 2023

    print("Fetching fixtures...")
    raw = get_league_fixtures(league, season)
    fixtures_df = fixtures_to_df(raw)

    print("Extracting players...")
    player_ids = extract_player_ids(fixtures_df, api)

    sample = list(player_ids)[:50]

    print("Computing analytics...")
    df = compute_trending_players(sample, api, season)

    print("Rendering digest...")
    output_file = render_digest(df.head(10), "digest_test.html")
    print("Digest written to:", output_file)

if __name__ == "__main__":
    main()
