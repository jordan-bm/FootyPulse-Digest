def performance_delta(goals, xg):
    # Over/under-performance vs expected goals
    # If xg is None, treat it as 0
    if goals is None:
        goals = 0
    if xg is None:
        xg = 0
    return goals - xg
