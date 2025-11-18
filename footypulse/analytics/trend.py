def trend_score(form, delta, consistency):
    """
    Combine metrics into a single trend score.
    Tunable weights (initial guess):
      - form: 50%
      - delta (goals - xG): 30%
      - consistency (lower is better): 20% (negative weight)
    """
    form = form or 0
    delta = delta or 0
    consistency = consistency or 0

    return 0.5 * form + 0.3 * delta - 0.2 * consistency
