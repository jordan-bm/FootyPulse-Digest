import pandas as pd

from footypulse.analytics.player_stats import extract_player_stats
from footypulse.analytics.form_rating import compute_form
from footypulse.analytics.consistency import consistency_index
from footypulse.analytics.performance_delta import performance_delta
from footypulse.analytics.trend import trend_score


def compute_trending_players(player_ids, api_module, season):
    """
    Given a set/list of player IDs and the api module (football_api),
    fetch stats for each player, compute analytics, and return
    a DataFrame sorted by trend_score desc
    """
    results = []

    for pid in player_ids:
        try:
            raw = api_module.get_player_statistics(pid, season)
        except Exception:
            continue

        stats = extract_player_stats(raw)
        if not stats:
            continue

        # For now, use single rating as 'history' placeholder
        ratings_history = [stats["rating"]] if stats["rating"] else []

        form = compute_form(ratings_history) if ratings_history else 0.0
        delta = performance_delta(stats["goals"], stats["xg"])
        consistency = consistency_index(ratings_history) if ratings_history else 0.0
        trend = trend_score(form, delta, consistency)

        stats["form"] = form
        stats["delta"] = delta
        stats["consistency"] = consistency
        stats["trend_score"] = trend

        results.append(stats)

    if not results:
        return pd.DataFrame()

    df = pd.DataFrame(results)
    df = df.sort_values(by="trend_score", ascending=False).reset_index(drop=True)
    return df
