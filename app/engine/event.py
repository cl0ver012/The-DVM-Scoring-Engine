from __future__ import annotations

from app.models.metrics import EventMetrics, Timeframe


def score_event(metrics: EventMetrics, timeframe: Timeframe) -> float:
    # Base weights (max 12.5)
    weight_inflow_mcap = 6.0
    weight_liq_drain = 4.0
    weight_upgrade = 2.5

    score = 0.0

    # Inflow/MCap Spike
    if (metrics.inflow_over_mcap_percent or 0.0) >= {"5m": 5, "15m": 8, "30m": 10, "1h": 12}[
        timeframe
    ]:
        score += weight_inflow_mcap

    # Liquidity Drain (Exit)
    if (metrics.liquidity_outflow_percent or 0.0) >= {"5m": 5, "15m": 8, "30m": 10, "1h": 12}[
        timeframe
    ]:
        score += weight_liq_drain

    # Upgrade / Staking Live
    if metrics.upgrade_or_staking_live:
        score += weight_upgrade

    return min(score, 12.5)


