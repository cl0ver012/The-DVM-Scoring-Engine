from __future__ import annotations

from app.models.metrics import SmartMoneyMetrics, Timeframe


def score_smart_money(metrics: SmartMoneyMetrics, timeframe: Timeframe) -> float:
    # Base weights
    weight_whale = 15.0
    weight_dca = 10.0
    weight_net_inflow = 12.5

    score = 0.0

    # Whale Buy (> $15k & >0.25% supply)
    if (metrics.whale_buy_usd or 0.0) >= 15000 and (
        (metrics.whale_buy_supply_percent or 0.0) >= 0.25
    ):
        score += weight_whale * 1.5

    # DCA Accumulation
    dca_thresholds = {"5m": 0.25, "15m": 0.3, "30m": 0.4, "1h": 0.5}
    if (metrics.dca_accumulation_supply_percent or 0.0) >= dca_thresholds[timeframe]:
        score += weight_dca * 1.25

    # Net Inflow (wallets > $10k)
    inflow_thresholds = {"5m": 5000, "15m": 10000, "30m": 10000, "1h": 10000}
    net_inflow = metrics.net_inflow_wallets_gt_10k_usd or 0.0
    if net_inflow >= inflow_thresholds[timeframe]:
        # scale 0.5x to 1.5x from 10k to 50k
        scale = min(max((net_inflow - 10000) / 40000, 0.0), 1.0)  # 0..1
        multiplier = 0.5 + scale * 1.0  # 0.5..1.5
        score += weight_net_inflow * multiplier

    return min(score, 37.5)


