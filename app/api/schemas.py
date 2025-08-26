from __future__ import annotations

from typing import List, Optional, Literal

from pydantic import BaseModel, Field


class ScoreRequest(BaseModel):
    token: dict  # TokenData fields
    metrics: dict = {}  # Optional ScoreMetrics fields, defaults to empty


class ScoreResponse(BaseModel):
    passed_prefilter: bool
    failed_checks: List[str]
    breakdown: dict
    total: float
    momentum: float
    smart_money: float
    sentiment: float
    event: float
    # Multi-timeframe scores for NEW category (as client requested)
    new_scores: Optional[dict] = None  # {"5m": 0.85, "15m": 0.72, "30m": 0.68, "1h": 0.63}
    trench_report_markdown: Optional[str] = None
    trench_report_json: Optional[dict] = None


class RankRow(BaseModel):
    # Essential fields for ranking (simplified from 25+ fields to core metrics)
    id: str
    symbol: str
    name: str
    price_now: float
    price_change_pct: float = 0.0
    mc_now: float = 0.0
    mc_change_pct: float = 0.0
    vol_now: float = 0.0
    vol_change_pct: float = 0.0
    vol_to_mc: float = 0.0
    lp_now: float = 0.0
    lp_change_pct: float = 0.0
    lp_count: int = 1
    holders_now: int = 0
    holders_change_pct: float = 0.0
    holders_per_mc: float = 0.0
    netflow_now: float = 0.0
    netflow_change_pct: float = 0.0
    whale_buy_count: int = 0
    kolusd_now: float = 0.0
    kolusd_change_pct: float = 0.0
    kol_velocity: float = 0.0
    tx_now: int = 0
    tx_change_pct: float = 0.0
    netbuy_usd_now: float = 0.0
    fee_sol_now: float = 0.0
    fee_to_mc_pct: float = 0.0
    minutes_since_peak: float = 0.0
    top10_pct: float = 0.0
    bundle_pct: float = 0.0
    dca_flag: int = 0
    ath_flag: int = 0


class RankResponse(BaseModel):
    tab: Literal["New", "Surging", "All"]
    rows: List[dict]


class RankRequest(BaseModel):
    tab: Literal["New", "Surging", "All"]
    rows: List[RankRow]


