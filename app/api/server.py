from __future__ import annotations

import os
from typing import List

from fastapi import FastAPI

from app.ai.client import OpenAIChatClient
from app.ai.trench_report import TrenchInput, generate_trench_report
from app.engine.scoring_engine import ScoringEngine
from app.models.metrics import EventMetrics, MomentumMetrics, ScoreMetrics, SentimentMetrics, SmartMoneyMetrics
from app.models.results import PreFilterResult
from app.models.token import TokenData
from app.utils.pre_filter import run_pre_filter
from app.api.schemas import ScoreRequest, ScoreResponse, RankResponse, RankRequest
from app.ranker.formulas import score_new, score_surging, score_all


app = FastAPI(title="DVM Scoring Engine")


@app.post("/score", response_model=ScoreResponse)
def post_score(req: ScoreRequest):
    token = TokenData.model_validate(req.token)
    pre: PreFilterResult = run_pre_filter(token)

    # For demo, build metrics from req.metrics shallowly
    m = req.metrics
    metrics = ScoreMetrics(
        timeframe=req.timeframe,
        momentum=MomentumMetrics(**(m.get("momentum") or {})),
        smart_money=SmartMoneyMetrics(**(m.get("smart_money") or {})),
        sentiment=SentimentMetrics(**(m.get("sentiment") or {})),
        event=EventMetrics(**(m.get("event") or {})),
    )

    engine = ScoringEngine()
    breakdown = engine.score(metrics)

    resp = ScoreResponse(
        passed_prefilter=pre.passed,
        failed_checks=pre.failed_checks,
        breakdown={
            "momentum": breakdown.momentum,
            "smart_money": breakdown.smart_money,
            "sentiment": breakdown.sentiment,
            "event": breakdown.event,
        },
        total=breakdown.total,
    )

    # Optional AI summary if OPENAI_API_KEY is set
    if os.getenv("OPENAI_API_KEY"):
        client = OpenAIChatClient()
        ti = TrenchInput(
            token={"symbol": token.token_symbol, "name": token.token_name, "address": token.token_address},
            prefilter={"passed": pre.passed, "failed_checks": pre.failed_checks},
            scores={
                "momentum": breakdown.momentum,
                "smart_money": breakdown.smart_money,
                "sentiment": breakdown.sentiment,
                "event": breakdown.event,
                "total": breakdown.total,
            },
            signals=[],
            metrics={"holders": token.holders_count, "top10_pct": token.top_10_holders_percent, "vol_5m_usd": token.volume_5m_usd, "fees_paid_sol": token.fees_paid_sol},
            timeframe=req.timeframe,
            as_of_utc="",
        )
        content = generate_trench_report(client, ti)
        resp.trench_report_markdown = content
        # JSON extraction left to client or future parsing

    return resp


@app.post("/rank", response_model=RankResponse)
def post_rank(req: RankRequest):
    sol_usd = float(os.getenv("SOL_USD", "150"))
    scored = []
    for r in req.rows:
        d = r.model_dump()
        if req.tab == "New":
            s = score_new(d, sol_usd)
        elif req.tab == "Surging":
            s = score_surging(d, sol_usd)
        else:
            s = score_all(d, sol_usd)
        d["score"] = s
        scored.append(d)
    scored.sort(key=lambda x: x["score"], reverse=True)
    return RankResponse(tab=req.tab, rows=scored)


