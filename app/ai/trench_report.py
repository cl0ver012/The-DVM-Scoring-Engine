from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict

from app.ai.client import ChatClient


SYSTEM_PROMPT = (
    "You are a top-tier DVM Trenches analyst with exclusive access to whale activity and smart money flows. "
    "Write high-value alpha reports using natural American English - conversational but precise. "
    "Focus on specific on-chain evidence, whale wallet patterns, and market dynamics. "
    "Sound like a seasoned trader sharing premium intel. Be clear, confident, and actionable."
)


@dataclass
class TrenchInput:
    token: Dict[str, str]
    prefilter: Dict[str, object]
    scores: Dict[str, float]
    signals: List[str]
    metrics: Dict[str, object]
    timeframe: str  # Now represents analysis type: "multi" for multi-timeframe
    as_of_utc: str


def _build_user_prompt(data: TrenchInput) -> str:
    # Determine primary narrative theme based on strongest score
    momentum_score = data.scores.get('momentum', 0)
    smart_money_score = data.scores.get('smart_money', 0)
    sentiment_score = data.scores.get('sentiment', 0)
    event_score = data.scores.get('event', 0)
    total_score = data.scores.get('total', 0)
    
    # Find dominant theme
    max_score = max(momentum_score, smart_money_score, sentiment_score, event_score)
    if max_score == momentum_score and momentum_score > 15:
        theme = "Momentum"
    elif max_score == smart_money_score and smart_money_score > 15:
        theme = "Smart Money"
    elif max_score == sentiment_score and sentiment_score > 5:
        theme = "Sentiment Driven"
    elif max_score == event_score and event_score > 5:
        theme = "Event Catalyst"
    else:
        theme = "Stability"
    
    # Calculate power indicators for enhanced reporting
    market_cap_tier = "micro" if data.metrics.get('market_cap_usd', 0) < 10000000 else "mid" if data.metrics.get('market_cap_usd', 0) < 100000000 else "large"
    volume_strength = "high" if data.metrics.get('volume_24h_usd', 0) > 1000000 else "moderate" if data.metrics.get('volume_24h_usd', 0) > 100000 else "low"
    
    # Enhanced signal analysis
    top_signals = data.signals[:6]  # More signals for power
    
    return (
        f"🎯 ALPHA REPORT: ${data.token.get('symbol')} ({data.token.get('name')})\n"
        f"📊 DVM Score: {total_score:.0f}/100 | Theme: {theme}\n"
        f"💰 Market Cap: {market_cap_tier.title()}-cap | Volume: {volume_strength}\n"
        f"🔍 Key Signals: {', '.join(top_signals)}\n"
        f"📈 Score Breakdown: Momentum {momentum_score:.0f} | Smart Money {smart_money_score:.0f} | Sentiment {sentiment_score:.0f} | Event {event_score:.0f}\n\n"
        
        "Write a POWERFUL DVM Trenches alpha report using natural American English in this EXACT format:\n\n"
        
        "**🎯 ${SYMBOL} – {Primary Theme} Play**\n"
        '📍 **The Intel:** "Write 2-3 clear sentences sharing what\'s really happening. Start with specific whale moves, '
        "smart money activity, or market dynamics. Use exact numbers and percentages. "
        'End with what traders should watch for next. Sound like a pro sharing premium insights."\n\n'
        
        "**⚡ Bottom Line:** BULLISH/NEUTRAL/CAUTIOUS - clear reason with supporting data\n\n"
        
        "**📊 Score Breakdown:**\n"
        "• Momentum: [score]/37.5 - what's driving price action\n"
        "• Smart Money: [score]/37.5 - what whales are doing\n"
        "• Sentiment: [score]/12.5 - social media and community buzz\n"
        "• Event: [score]/12.5 - upcoming catalysts or news\n\n"
        
        "**👀 What to Watch:** 3 specific things to monitor with clear thresholds\n\n"
        
        "NATURAL AMERICAN ENGLISH EXAMPLES:\n"
        '• "Here\'s what\'s happening: Three major whale wallets just bought $2.1M worth of [TOKEN] in a coordinated 15-minute buying spree. The on-chain data shows they\'re using the same DCA strategy that worked for [previous winner]. This could be the start of something big."\n'
        '• "Word from the trenches: The [TOKEN] team just burned half their supply while top influencers are quietly loading up. Social mentions jumped 340% but the price hasn\'t caught up yet — classic setup before a major move."\n'
        '• "Smart money is rotating: Major wallets sold their [competing token] positions and moved $4.2M into [TOKEN] over the past two days. Volume is building, holder count is growing, and liquidity is locked. All the pieces are falling into place."\n\n'
        
        "WRITING REQUIREMENTS:\n"
        "- Use natural, conversational American English\n"
        "- Include specific wallet activity and transaction details\n"
        "- Reference successful comparable tokens when relevant\n"
        "- Sound like a seasoned trader sharing exclusive insights\n"
        "- Keep under 280 words but deliver maximum value\n"
        "- Use precise numbers, percentages, and timeframes\n"
        "- Make it clear and easy to understand\n"
        "- Use strategic emojis for visual appeal"
    )


def generate_trench_report(data: TrenchInput, client: ChatClient, model: str = "gpt-4o", temperature: float = 0.2, max_tokens: int = 1000) -> str:
    prompt = _build_user_prompt(data)
    return client.complete(SYSTEM_PROMPT, prompt, model=model, temperature=temperature, max_tokens=max_tokens)


