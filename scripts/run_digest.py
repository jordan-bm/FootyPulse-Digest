import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from footypulse.api.football_api import get_league_fixtures
from footypulse.analytics.fixtures_processing import fixtures_to_df
from footypulse.analytics.player_extraction import extract_player_ids
from footypulse.analytics.engine import compute_trending_players
from footypulse.digest.render import render_digest
from footypulse.email.sender import send_digest_email
import footypulse.api.football_api as api


def main():
    league_id = 39
    season = 2023

    print("Fetching fixtures...")
    raw = get_league_fixtures(league_id, season)
    fixtures_df = fixtures_to_df(raw)

    print("Extracting players...")
    player_ids = extract_player_ids(fixtures_df, api)

    sample = list(player_ids)[:50]

    print("Computing analytics...")
    df = compute_trending_players(sample, api, season)

    print("Rendering HTML digest...")
    digest_path = render_digest(df.head(10), "digest_email.html")

    with open(digest_path, "r", encoding="utf-8") as f:
        html = f.read()

    print("Sending email...")
    status = send_digest_email(
        to_email="rockypuddlez@gmail.com",
        subject="FootyPulse Daily Digest",
        html_content=html
    )

    print("Email status:", status)


if __name__ == "__main__":
    main()
