from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from app.engine.event import score_event
from app.engine.momentum import score_momentum
from app.engine.sentiment import score_sentiment
from app.engine.smart_money import score_smart_money
from app.models.metrics import ScoreMetrics


@dataclass
class ScoreBreakdown:
    momentum: float
    smart_money: float
    sentiment: float
    event: float
    total: float


class ScoringEngine:
    def score(self, metrics: ScoreMetrics, timeframe: str = "1h") -> ScoreBreakdown:
        """Score for a specific timeframe - used internally"""
        ms = score_momentum(metrics.momentum, timeframe)
        sm = score_smart_money(metrics.smart_money, timeframe)
        se = score_sentiment(metrics.sentiment, timeframe)
        ev = score_event(metrics.event, timeframe)
        total = ms + sm + se + ev
        return ScoreBreakdown(momentum=ms, smart_money=sm, sentiment=se, event=ev, total=total)
    
    def score_all_timeframes(self, metrics: ScoreMetrics) -> dict:
        """Calculate scores for all timeframes as client requested for NEW category"""
        timeframes = ["5m", "15m", "30m", "1h"]
        scores = {}
        for tf in timeframes:
            breakdown = self.score(metrics, tf)
            scores[tf] = breakdown.total
        return scores


