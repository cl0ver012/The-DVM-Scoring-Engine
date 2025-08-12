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
    def score(self, metrics: ScoreMetrics) -> ScoreBreakdown:
        ms = score_momentum(metrics.momentum, metrics.timeframe)
        sm = score_smart_money(metrics.smart_money, metrics.timeframe)
        se = score_sentiment(metrics.sentiment, metrics.timeframe)
        ev = score_event(metrics.event, metrics.timeframe)
        total = ms + sm + se + ev
        return ScoreBreakdown(momentum=ms, smart_money=sm, sentiment=se, event=ev, total=total)


