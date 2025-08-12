from __future__ import annotations

from app.models.metrics import SentimentMetrics, Timeframe


def score_sentiment(metrics: SentimentMetrics, timeframe: Timeframe) -> float:
    # Base weights (max 12.5)
    weight_mentions = 5.0
    weight_kol = 5.0
    weight_polarity = 2.5

    score = 0.0

    # Mentions Velocity (> thresholds by timeframe)
    thresholds = {"5m": 3.0, "15m": 2.5, "30m": 2.0, "1h": 1.75}
    if (metrics.mentions_velocity_ratio or 0.0) >= thresholds[timeframe]:
        score += weight_mentions

    # Tier1 KOL Buy (>0.25% supply)
    if (metrics.tier1_kol_buy_supply_percent or 0.0) >= 0.25:
        score += weight_kol

    # Sentiment Polarity
    polarity_thresholds = {"5m": 70, "15m": 65, "30m": 60, "1h": 55}
    if (metrics.polarity_positive_percent or 0.0) >= polarity_thresholds[timeframe]:
        score += weight_polarity

    return min(score, 12.5)


