import pandas as pd

def generate_note(form, trend, consistency):
    # Remarks based on stats

    if trend > 7 and form > 7.3:
        return "Breakout form — elite performance level."
    if trend > 6.5 and consistency > 0.6:
        return "Improving & stable — reliable impact."
    if trend > 6:
        return "Trending upward — watch closely."
    if consistency < 0.4:
        return "Volatile output — high risk/reward."
    if form > 7.0:
        return "High form player — strong current impact."
    return "Steady contributor — balanced output."


def prepare_player_objects(df: pd.DataFrame) -> list[dict]:
    players = []
    for _, row in df.iterrows():
        player = {
            "name": row.get("name", "Unknown"),
            "team": row.get("team", "Unknown"),
            "league": row.get("league", ""),
            "form": float(row.get("form", 0)),
            "trend_score": float(row.get("trend_score", 0)),
            "consistency": float(row.get("consistency", 0)),
            "delta": float(row.get("delta", 0)),
            "photo": row.get("photo", ""),  # API value needed next step
            "logo": row.get("logo", ""),    # API value needed next step
            "note": generate_note(row.get("form", 0),
                                 row.get("trend_score", 0),
                                 row.get("consistency", 0))
        }
        players.append(player)
    return players
