from app.engine.scoring_engine import ScoringEngine
from app.models.metrics import ScoreMetrics, MomentumMetrics, SmartMoneyMetrics, SentimentMetrics, EventMetrics


def test_scoring_engine_full_score_caps():
    engine = ScoringEngine()
    metrics = ScoreMetrics(
        timeframe="5m",
        momentum=MomentumMetrics(
            vol_over_avg_ratio=3.0,
            price_change_percent=20,
            ath_hit=True,
            lp_mcap_delta_percent=20,
            holders_growth_percent=150,
        ),
        smart_money=SmartMoneyMetrics(
            whale_buy_usd=50000,
            whale_buy_supply_percent=0.5,
            dca_accumulation_supply_percent=0.5,
            net_inflow_wallets_gt_10k_usd=50000,
        ),
        sentiment=SentimentMetrics(
            mentions_velocity_ratio=4.0,
            tier1_kol_buy_supply_percent=0.3,
            polarity_positive_percent=80,
        ),
        event=EventMetrics(
            inflow_over_mcap_percent=10,
            liquidity_outflow_percent=10,
            upgrade_or_staking_live=True,
        ),
    )

    result = engine.score(metrics)
    assert result.momentum <= 37.5
    assert result.smart_money <= 37.5
    assert result.sentiment <= 12.5
    assert result.event <= 12.5
    assert result.total <= 100.0


def test_scoring_engine_partial_example():
    engine = ScoringEngine()
    metrics = ScoreMetrics(
        timeframe="15m",
        momentum=MomentumMetrics(vol_over_avg_ratio=2.0, price_change_percent=10),
        smart_money=SmartMoneyMetrics(net_inflow_wallets_gt_10k_usd=15000),
        sentiment=SentimentMetrics(mentions_velocity_ratio=3.0, polarity_positive_percent=60),
        event=EventMetrics(inflow_over_mcap_percent=9, upgrade_or_staking_live=False),
    )
    result = engine.score(metrics)
    assert 0 <= result.total <= 100
    # sanity: some points should be awarded
    assert result.total > 0


