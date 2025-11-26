def compute_form(ratings, max_games=5):
    # Compute a weighted form rating over last `max_games` matches
    # ratings: list of floats, oldest -> newest.
    if not ratings:
        return 0.0

    recent = ratings[-max_games:]
    # Heavier weights on more recent games (reverse them)
    base_weights = [1.5, 1.25, 1.1, 0.9, 0.8]
    weights = base_weights[:len(recent)]
    recent_reversed = recent[::-1]  # newest first

    weighted = [r * w for r, w in zip(recent_reversed, weights)]
    return sum(weighted) / sum(weights)
