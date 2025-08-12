from __future__ import annotations

from app.models.metrics import MomentumMetrics, Timeframe


def _multiplier_from_ratio(ratio: float, t: Timeframe) -> float:
    if ratio is None:
        return 0.0
    thresholds = {
        "5m": (2.0, 1.0, 0.5),
        "15m": (1.8, 1.0, 0.5),
        "30m": (1.6, 1.0, 0.5),
        "1h": (1.5, 1.0, 0.5),
    }[t]
    strong, medium, weak = thresholds
    if ratio >= strong:
        return 1.5
    if ratio >= medium:
        return 1.0
    if ratio >= weak:
        return 0.5
    return 0.0


def _multiplier_from_price_change(pct: float, t: Timeframe) -> float:
    if pct is None:
        return 0.0
    thresholds = {"5m": 5, "15m": 8, "30m": 12, "1h": 15}[t]
    if pct >= thresholds:
        return 1.5
    if pct >= thresholds * 0.6:
        return 1.0
    if pct >= thresholds * 0.3:
        return 0.5
    return 0.0


def score_momentum(metrics: MomentumMetrics, timeframe: Timeframe) -> float:
    # Base weights
    weight_volume = 10.0
    weight_price = 10.0
    weight_ath_vol = 12.0
    weight_lp_mcap_inc = 5.0
    weight_holder_growth = 5.0

    score = 0.0

    # Volume Spike
    score += weight_volume * _multiplier_from_ratio(
        metrics.vol_over_avg_ratio or 0.0, timeframe
    )

    # Price Spike
    score += weight_price * _multiplier_from_price_change(
        metrics.price_change_percent or 0.0, timeframe
    )

    # ATH + Volume Spike
    if metrics.ath_hit and (metrics.vol_over_avg_ratio or 0.0) >= {
        "5m": 2.0,
        "15m": 1.8,
        "30m": 1.6,
        "1h": 1.5,
    }[timeframe]:
        score += weight_ath_vol * 1.5

    # LP/MCap increase
    if (metrics.lp_mcap_delta_percent or 0.0) > {"5m": 10, "15m": 15, "30m": 20, "1h": 25}[
        timeframe
    ]:
        score += weight_lp_mcap_inc

    # Holder growth
    if (metrics.holders_growth_percent or 0.0) > {"5m": 100, "15m": 75, "30m": 50, "1h": 25}[
        timeframe
    ]:
        score += weight_holder_growth

    # Cap at 37.5 max
    return min(score, 37.5)


