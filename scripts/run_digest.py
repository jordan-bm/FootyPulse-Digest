import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from footypulse.api.football_api import get_players_from_fixtures
from footypulse.analytics.player_extraction import prepare_player_objects
from footypulse.analytics.scoring import add_advanced_metrics   
from footypulse.digest.render import render_digest
from footypulse.email.sender import send_digest_email


def main():
    
    league_id = 39          # Premier League 
    season = 2021           # Free tier season

    print("Fetching player statistics...")
    df = get_players_from_fixtures(league_id=league_id, season=season, limit_games=25)

    if df is None or df.empty:
        print("No player data collected – check league/season combo or API limits.")
        return

    # Add advanced analytics before sorting
    df = add_advanced_metrics(df)

    df = df.sort_values("trend_score", ascending=False).head(10)
    print(f"Players collected (top 10 after scoring): {len(df)}")

    print("Preparing player digest objects...")
    players = prepare_player_objects(df)

    print("Rendering email digest HTML...")
    html = render_digest(players)  # file save upon request only

    print("Sending digest email...")
    status = send_digest_email(
        to_email=os.getenv("FOOTYPULSE_RECEIVER_EMAIL", "test@example.com"), # Pulls email from .env
        subject="FootyPulse Weekly Digest",
        html_content=html
    )

    print("Email status:", status)


if __name__ == "__main__":
    main()
