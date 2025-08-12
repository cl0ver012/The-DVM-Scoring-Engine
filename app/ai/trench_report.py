from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict

from app.ai.client import ChatClient


SYSTEM_PROMPT = (
    "You are a quantitative analyst generating a trench report for a new Solana token. "
    "Be concise, numeric, and objective. No hype. No financial advice. Use UTC times. Only use provided data."
)


@dataclass
class TrenchInput:
    token: Dict[str, str]
    prefilter: Dict[str, object]
    scores: Dict[str, float]
    signals: List[str]
    metrics: Dict[str, object]
    timeframe: str
    as_of_utc: str


def _build_user_prompt(data: TrenchInput) -> str:
    return (
        f"Context:\n"
        f"- Token: {data.token.get('symbol')} ({data.token.get('name')}) — {data.token.get('address')}\n"
        f"- As of (UTC): {data.as_of_utc}\n"
        f"- Prefilter: {data.prefilter.get('passed')}; Failed: {data.prefilter.get('failed_checks')}\n"
        f"- Scores (0–100 total): Momentum {data.scores.get('momentum', 0)}, Smart Money {data.scores.get('smart_money', 0)}, "
        f"Sentiment {data.scores.get('sentiment', 0)}, Event {data.scores.get('event', 0)}, Total {data.scores.get('total', 0)}\n"
        f"- Key signals (timeframe -> value): {data.signals}\n"
        f"- Metrics: {data.metrics}\n\n"
        "Instructions:\n"
        "1) If prefilter failed: output a one-paragraph ‘FILTERED OUT’ note with the exact failed checks, then stop.\n"
        "2) Else write:\n"
        "   - Executive verdict in one line: Bullish / Neutral / Cautious (bands: ≥85, 60–84, <60), with one numeric reason.\n"
        "   - Score breakdown bullets: one per category with top numeric driver(s).\n"
        "   - Positives (max 4 bullets).\n"
        "   - Risks (max 4 bullets).\n"
        "   - What to watch next (max 3 bullets).\n"
        "3) Keep total under ~200–250 words. Use USD abbreviations (K/M) and percentages with 1–2 decimals.\n"
        "Return both: Markdown section first, then a JSON block reflecting the same content."
    )


def generate_trench_report(client: ChatClient, data: TrenchInput, model: str = "gpt-4o", temperature: float = 0.2, max_tokens: int = 1000) -> str:
    prompt = _build_user_prompt(data)
    return client.complete(SYSTEM_PROMPT, prompt, model=model, temperature=temperature, max_tokens=max_tokens)


