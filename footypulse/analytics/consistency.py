import statistics

def consistency_index(ratings):
    # Consistency = stdev / mean.
    # Lower = more consistent. 0 if not enough data.
    if not ratings or len(ratings) < 2:
        return 0.0

    mean_val = statistics.mean(ratings)
    if mean_val == 0:
        return 0.0

    return statistics.stdev(ratings) / mean_val
