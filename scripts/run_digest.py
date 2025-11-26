import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from footypulse.api.football_api import get_players_from_fixtures
from footypulse.analytics.player_extraction import prepare_player_objects
from footypulse.digest.render import render_digest
from footypulse.email.sender import send_digest_email

def main():
    league_id = 39           # Premier League (free tier supports 2021-2023)
    season = 2023            # *** IMPORTANT - free API only works for these ***
    
    print("Fetching player statistics...")
    df = get_players_from_fixtures(league_id=league_id, season=season, limit_games=25)
    df = df.sort_values("trend_score", ascending=False).head(10)

    print(f"Players collected: {len(df)}")

    print("Preparing player digest objects...")
    players = prepare_player_objects(df)

    print("Rendering email digest HTML...")
    html = render_digest(players)

    print("Sending digest email...")
    status = send_digest_email(
        to_email="rockypuddlez@gmail.com",     # Receiving Email (changeable)
        subject="FootyPulse Weekly Digest",
        html_content=html
    )

    print("Email status:", status)

if __name__ == "__main__":
    main()
