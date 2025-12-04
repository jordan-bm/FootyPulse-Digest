from __future__ import annotations

from typing import Optional
import pandas as pd


def _safe_minmax(s: pd.Series) -> pd.Series:
    # Normalize a series to [0, 1]. If constant, return 0.5 everywhere
    s = s.astype(float)
    if s.empty:
        return s
    s_min = s.min()
    s_max = s.max()
    if s_max == s_min:
        return pd.Series(0.5, index=s.index)
    return (s - s_min) / (s_max - s_min)


def add_advanced_metrics(
    df: pd.DataFrame,
    min_appearances_for_reliability: int = 10,
) -> pd.DataFrame:
    
    """
    Enhance raw player DataFrame with:
      - goals_per_appearance
      - form_norm, usage_norm, scoring_norm
      - trend_score (0–10)
      - consistency_score
      - note (short string for the digest card)
    """

    df = df.copy()

    # Existing fields:
    # form        -> stat_block["games"]["rating"]
    # consistency -> stat_block["games"]["appearences"]
    # delta       -> stat_block["goals"]["total"]

    df["form"] = df["form"].fillna(0).astype(float)
    df["appearances"] = df["consistency"].fillna(0).astype(float)
    df["goals"] = df["delta"].fillna(0).astype(float)

    # Goals per appearance (basic scoring efficiency)
    df["goals_per_appearance"] = df["goals"] / df["appearances"].where(
        df["appearances"] > 0, 1
    )

    # Normalized components
    df["form_norm"] = _safe_minmax(df["form"])
    df["usage_norm"] = _safe_minmax(df["appearances"])
    df["scoring_norm"] = _safe_minmax(df["goals_per_appearance"])

    # Trend score: weighted mix of form, usage, scoring
    # Tweak weights for more attacking/defensive bias
    df["trend_score"] = (
        0.5 * df["form_norm"]
        + 0.3 * df["scoring_norm"]
        + 0.2 * df["usage_norm"]
    ) * 10.0  # scale to 0–10

    # "Consistency" as a separate score: do they play regularly?
    df["consistency_score"] = df["usage_norm"] * 10.0

    # Generate short notes for digest cards
    notes = []
    for _, row in df.iterrows():
        ts = row["trend_score"]
        apps = row["appearances"]
        form = row["form"]

        if apps < max(3, 0.2 * min_appearances_for_reliability):
            note = "Limited minutes so far; small sample size."
        elif ts >= 8 and form >= 7:
            note = "On fire – elite recent form and usage."
        elif ts >= 7:
            note = "Strong contributor with solid form."
        elif ts >= 5.5:
            note = "Steady regular with decent output."
        else:
            note = "Under the radar; numbers are still modest."

        notes.append(note)

    df["note"] = notes

    return df
