from __future__ import annotations

from typing import Optional, Literal

from pydantic import BaseModel, Field


Timeframe = Literal["5m", "15m", "30m", "1h"]


class MomentumMetrics(BaseModel):
    # Ratios and deltas for the selected timeframe
    vol_over_avg_ratio: Optional[float] = Field(default=None, ge=0)
    price_change_percent: Optional[float] = Field(default=None)
    ath_hit: Optional[bool] = Field(default=None)
    lp_mcap_delta_percent: Optional[float] = Field(default=None)
    holders_growth_percent: Optional[float] = Field(default=None)


class SmartMoneyMetrics(BaseModel):
    whale_buy_usd: Optional[float] = Field(default=None, ge=0)
    whale_buy_supply_percent: Optional[float] = Field(default=None, ge=0)
    dca_accumulation_supply_percent: Optional[float] = Field(default=None, ge=0)
    net_inflow_wallets_gt_10k_usd: Optional[float] = Field(default=None)


class SentimentMetrics(BaseModel):
    mentions_velocity_ratio: Optional[float] = Field(default=None, ge=0)
    tier1_kol_buy_supply_percent: Optional[float] = Field(default=None, ge=0)
    influencer_reach: Optional[int] = Field(default=None, ge=0)
    polarity_positive_percent: Optional[float] = Field(default=None, ge=0, le=100)


class EventMetrics(BaseModel):
    inflow_over_mcap_percent: Optional[float] = Field(default=None)
    liquidity_outflow_percent: Optional[float] = Field(default=None)
    upgrade_or_staking_live: Optional[bool] = Field(default=None)


class ScoreMetrics(BaseModel):
    # Remove timeframe as input - will be calculated internally for all timeframes
    momentum: MomentumMetrics = Field(default_factory=MomentumMetrics)
    smart_money: SmartMoneyMetrics = Field(default_factory=SmartMoneyMetrics)
    sentiment: SentimentMetrics = Field(default_factory=SentimentMetrics)
    event: EventMetrics = Field(default_factory=EventMetrics)


