def extract_player_stats(raw_json):
    """
    Extract a minimal, normalized view of a player's season stats
    from the /players endpoint response

    Returns:
      dict with keys:
        player_id, name, team, league, games, minutes,
        goals, xg, rating
      or None if no data
    """
    response = raw_json.get("response", [])
    if not response:
        return None

    entry = response[0]
    player = entry.get("player", {})
    stats_list = entry.get("statistics", [])
    if not stats_list:
        return None

    s = stats_list[0]  # first team/league

    games = s.get("games", {}) or {}
    goals_block = s.get("goals", {}) or {}
    league_block = s.get("league", {}) or {}
    team_block = s.get("team", {}) or {}

    # rating in API-Football is typically a string, like "7.4"
    rating_raw = games.get("rating")
    try:
        rating = float(rating_raw) if rating_raw is not None else 0.0
    except (TypeError, ValueError):
        rating = 0.0

    # xG may or may not exist on free plan; handle this
    xg = goals_block.get("expected")
    try:
        xg = float(xg) if xg is not None else None
    except (TypeError, ValueError):
        xg = None

    return {
        "player_id": player.get("id"),
        "name": player.get("name"),
        "team": team_block.get("name"),
        "league": league_block.get("name"),
        "games": games.get("appearences") or 0,
        "minutes": games.get("minutes") or 0,
        "goals": goals_block.get("total") or 0,
        "xg": xg,
        "rating": rating,
    }
