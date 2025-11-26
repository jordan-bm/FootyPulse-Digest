import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from footypulse.api.football_api import get_league_fixtures, get_player_statistics
from footypulse.analytics.fixtures_processing import fixtures_to_df
from footypulse.analytics.player_extraction import extract_player_ids
from footypulse.analytics.engine import compute_trending_players
import footypulse.api.football_api as api


def main():
    league_id = 39  # Premier League
    season = 2023   # free plan allowed years

    print("Fetching fixtures...")
    raw_fixtures = get_league_fixtures(league_id, season)
    fixtures_df = fixtures_to_df(raw_fixtures)
    print("Fixtures:", len(fixtures_df))

    print("Extracting players...")
    player_ids = extract_player_ids(fixtures_df, api)
    print("Players:", len(player_ids))

    # To stay friendly with rate limits, sample a subset for now
    sampled_ids = list(player_ids)[:50]
    print("Sampling", len(sampled_ids), "players for analytics...")

    trending_df = compute_trending_players(sampled_ids, api, season)
    print(trending_df.head(10))


if __name__ == "__main__":
    main()
