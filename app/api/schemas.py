from __future__ import annotations

from typing import List, Optional, Literal

from pydantic import BaseModel, Field


class ScoreRequest(BaseModel):
    timeframe: Literal["5m", "15m", "30m", "1h"] = "5m"
    token: dict
    metrics: dict


class ScoreResponse(BaseModel):
    passed_prefilter: bool
    failed_checks: List[str]
    breakdown: dict
    total: float
    trench_report_markdown: Optional[str] = None
    trench_report_json: Optional[dict] = None


class RankRow(BaseModel):
    # Subset needed for ranking and UI
    id: str
    symbol: str
    name: str
    price_now: float
    price_change_pct: float
    mc_now: float
    mc_change_pct: float
    vol_now: float
    vol_change_pct: float
    vol_to_mc: float
    lp_now: float
    lp_change_pct: float
    lp_count: int
    holders_now: int
    holders_change_pct: float
    holders_per_mc: float
    netflow_now: float
    netflow_change_pct: float
    whale_buy_count: int
    kolusd_now: float
    kolusd_change_pct: float
    kol_velocity: float
    tx_now: int
    tx_change_pct: float
    netbuy_usd_now: float
    fee_sol_now: float
    fee_to_mc_pct: float
    minutes_since_peak: float
    top10_pct: float
    bundle_pct: float
    dca_flag: int
    ath_flag: int


class RankResponse(BaseModel):
    tab: Literal["New", "Surging", "All"]
    rows: List[dict]


class RankRequest(BaseModel):
    tab: Literal["New", "Surging", "All"]
    rows: List[RankRow]


