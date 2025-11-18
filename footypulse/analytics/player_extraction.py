def extract_player_ids(fixtures_df, api): 
    # Given a fixtures DataFrame & API client, get all players who played in those fixtures
    # Returns: set(player_id)
    
    player_ids = set()

    for fixture_id in fixtures_df["fixture_id"]:
        lineups_raw = api.get_lineups(fixture_id)
        teams = lineups_raw.get("response", [])

        for team in teams:
            for player in team.get("startXI", []):
                pid = player["player"]["id"]
                if pid:
                    player_ids.add(pid)

            for player in team.get("substitutes", []):
                pid = player["player"]["id"]
                if pid:
                    player_ids.add(pid)

    return player_ids
