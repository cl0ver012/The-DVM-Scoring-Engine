from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from app.ai.client import MockChatClient, OpenAIChatClient
from app.ai.trench_report import TrenchInput, generate_trench_report
from app.engine.scoring_engine import ScoringEngine
from app.models.metrics import EventMetrics, MomentumMetrics, ScoreMetrics, SentimentMetrics, SmartMoneyMetrics
from app.models.results import PreFilterResult
from app.models.token import TokenData
from app.utils.pre_filter import run_pre_filter


def load_first_token(path: Path) -> TokenData:
    payload = json.loads(path.read_text(encoding="utf-8"))
    obj = payload[0] if isinstance(payload, list) else payload
    return TokenData.model_validate(obj)


def main() -> int:
    token = load_first_token(Path("data/mock_data.json"))
    pre: PreFilterResult = run_pre_filter(token)

    timeframe = "5m"
    metrics = ScoreMetrics(
        timeframe=timeframe,
        momentum=MomentumMetrics(vol_over_avg_ratio=2.1, price_change_percent=9.2, ath_hit=False, lp_mcap_delta_percent=12.0, holders_growth_percent=40.0),
        smart_money=SmartMoneyMetrics(whale_buy_usd=20000, whale_buy_supply_percent=0.3, dca_accumulation_supply_percent=0.3, net_inflow_wallets_gt_10k_usd=15000),
        sentiment=SentimentMetrics(mentions_velocity_ratio=3.0, tier1_kol_buy_supply_percent=0.3, influencer_reach=30000, polarity_positive_percent=72),
        event=EventMetrics(inflow_over_mcap_percent=6, liquidity_outflow_percent=2, upgrade_or_staking_live=False),
    )
    engine = ScoringEngine()
    breakdown = engine.score(metrics)

    signals = [
        "5m: vol/avg 2.1x",
        "5m: price +9.2%",
        "5m: whale buy $20k, 0.3%",
        "5m: net inflow $15k",
        "5m: mentions 3.0x; polarity 72%",
    ]
    as_of = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    data = TrenchInput(
        token={"symbol": token.token_symbol, "name": token.token_name, "address": token.token_address},
        prefilter={"passed": pre.passed, "failed_checks": pre.failed_checks},
        scores={
            "momentum": breakdown.momentum,
            "smart_money": breakdown.smart_money,
            "sentiment": breakdown.sentiment,
            "event": breakdown.event,
            "total": breakdown.total,
        },
        signals=signals,
        metrics={
            "holders": token.holders_count,
            "top10_pct": token.top_10_holders_percent,
            "lp_usd": None,
            "mcap_usd": token.market_cap_usd if hasattr(token, "market_cap_usd") else None,
            "vol_5m_usd": token.volume_5m_usd,
            "fees_paid_sol": token.fees_paid_sol,
        },
        timeframe=timeframe,
        as_of_utc=as_of,
    )

    # Load .env if present
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except Exception:
        pass

    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        client = OpenAIChatClient(api_key=api_key)
    else:
        client = MockChatClient("# Report\nDemo mode (no OPENAI_API_KEY set).\n```json\n{\n  \"summary_label\": \"Neutral\"\n}\n```\n")

    out = generate_trench_report(client, data)
    print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


