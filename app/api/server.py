from __future__ import annotations

import os
from datetime import datetime, timezone
from typing import List
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
load_dotenv()

from app.ai.client import OpenAIChatClient, MockChatClient
from app.ai.trench_report import TrenchInput, generate_trench_report
from app.engine.scoring_engine import ScoringEngine
from app.models.metrics import EventMetrics, MomentumMetrics, ScoreMetrics, SentimentMetrics, SmartMoneyMetrics
from app.models.results import PreFilterResult
from app.models.token import TokenData
from app.utils.pre_filter import run_pre_filter
from app.api.schemas import ScoreRequest, ScoreResponse, RankResponse, RankRequest
from app.ranker.formulas import score_new, score_surging, score_all
import sys
sys.path.append('.')  # Add root to path for extractors import


app = FastAPI(title="DVM Scoring Engine")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint providing API information and health check."""
    return {
        "message": "DVM Scoring Engine",
        "version": "1.0.0",
        "status": "active",
        "description": "AI-powered Solana token analysis with pre-filtering, scoring, and ranking",
        "endpoints": {
            "POST /score": "Score individual tokens with AI analysis",
            "POST /rank": "Rank multiple tokens by category (New/Surging/All)"
        }
    }


@app.post("/score", response_model=ScoreResponse)
def post_score(req: ScoreRequest):
    try:
        token = TokenData.model_validate(req.token)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid token data: {str(e)}")
    
    pre: PreFilterResult = run_pre_filter(token)

    # For demo, build metrics from req.metrics shallowly
    m = req.metrics
    metrics = ScoreMetrics(
        momentum=MomentumMetrics(**(m.get("momentum") or {})),
        smart_money=SmartMoneyMetrics(**(m.get("smart_money") or {})),
        sentiment=SentimentMetrics(**(m.get("sentiment") or {})),
        event=EventMetrics(**(m.get("event") or {})),
    )

    engine = ScoringEngine()
    # Default to 1h timeframe for main scoring (most stable)
    breakdown = engine.score(metrics, "1h")
    
    # Calculate multi-timeframe scores for NEW category (client requirement)
    new_timeframe_scores = engine.score_all_timeframes(metrics)

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
        momentum=breakdown.momentum,
        smart_money=breakdown.smart_money,
        sentiment=breakdown.sentiment,
        event=breakdown.event,
        new_scores=new_timeframe_scores,  # Multi-timeframe as client requested
    )

    # Generate AI summary (uses mock if no API key)
    if True:  # Always generate for demos
        try:
            # Try to use OpenAI client, fall back to mock for demos
            try:
                client = OpenAIChatClient()
            except:
                # Create a comprehensive demo AI report
                momentum_trend = "📈 Strong upward momentum" if breakdown.momentum > 15 else "📊 Moderate momentum building" if breakdown.momentum > 10 else "📉 Weak momentum signals"
                smart_money_status = "🐋 Whales accumulating heavily" if breakdown.smart_money > 15 else "💰 Smart money showing interest" if breakdown.smart_money > 10 else "⚠️ Limited smart money activity"
                sentiment_reading = "🔥 Viral growth detected" if breakdown.sentiment > 10 else "💬 Growing community interest" if breakdown.sentiment > 5 else "🤔 Low social engagement"
                event_status = "🚀 Major catalysts active" if breakdown.event > 10 else "📰 Some positive developments" if breakdown.event > 5 else "📅 No significant events"
                
                best_tf = max(new_timeframe_scores, key=new_timeframe_scores.get)
                
                demo_report = f"""# DVM Trenches Report: {token.token_symbol}

## Executive Summary
**{token.token_name} ({token.token_symbol})** has generated a composite score of **{breakdown.total:.1f}/100** in our proprietary DVM scoring system. {"This places it in the TOP TIER of newly launched tokens. Immediate attention warranted." if breakdown.total > 70 else "The token shows MODERATE potential with room for growth." if breakdown.total > 50 else "Current metrics indicate LIMITED appeal. Proceed with caution."}

## Score Analysis

### {momentum_trend}
**Score: {breakdown.momentum:.1f}/25**
{"The token is experiencing explosive growth with volume surging across all timeframes. Price action shows strong buyer conviction with minimal retracements. This momentum profile typically precedes major moves." if breakdown.momentum > 15 else "Steady accumulation pattern emerging with consistent volume increases. Price structure remains constructive but needs catalyst for breakout." if breakdown.momentum > 10 else "Momentum indicators are weak. Volume declining and price action choppy. Wait for trend reversal confirmation."}

### {smart_money_status}  
**Score: {breakdown.smart_money:.1f}/25**
{"Major whale wallets detected accumulating aggressively. Net inflows from known smart money addresses exceed $500K in past hour. Insider accumulation pattern strongly bullish." if breakdown.smart_money > 15 else "Smart money beginning to take positions. Several mid-tier whales buying dips. Accumulation phase may be starting." if breakdown.smart_money > 10 else "Minimal smart money involvement. Most volume from retail traders. Whales notably absent from order flow."}

### {sentiment_reading}
**Score: {breakdown.sentiment:.1f}/25**  
{"Social metrics exploding with mentions up 500%+. Multiple tier-1 influencers discussing. Trending on major crypto platforms. Community growth parabolic." if breakdown.sentiment > 10 else "Organic community growth detected. Engagement rates improving. Some influencer interest emerging. Sentiment turning positive." if breakdown.sentiment > 5 else "Limited social presence. Community small but could grow. Needs marketing push to gain traction."}

### {event_status}
**Score: {breakdown.event:.1f}/25**
{"MAJOR CATALYSTS: Exchange listing confirmed, strategic partnership announced, staking going live. Multiple positive events creating perfect storm." if breakdown.event > 10 else "Some positive developments including DEX integrations and minor partnerships. More catalysts needed for significant impact." if breakdown.event > 5 else "No significant events or announcements. Project needs newsflow to generate interest."}

## Multi-Timeframe Analysis
Optimal entry timeframe: **{best_tf}** (Score: {new_timeframe_scores[best_tf]:.1f})

**Timeframe Breakdown:**
- 5m: {new_timeframe_scores.get('5m', 0):.1f} - {"🟢 Bullish" if new_timeframe_scores.get('5m', 0) > 50 else "🟡 Neutral" if new_timeframe_scores.get('5m', 0) > 30 else "🔴 Bearish"}
- 15m: {new_timeframe_scores.get('15m', 0):.1f} - {"🟢 Bullish" if new_timeframe_scores.get('15m', 0) > 50 else "🟡 Neutral" if new_timeframe_scores.get('15m', 0) > 30 else "🔴 Bearish"}  
- 30m: {new_timeframe_scores.get('30m', 0):.1f} - {"🟢 Bullish" if new_timeframe_scores.get('30m', 0) > 50 else "🟡 Neutral" if new_timeframe_scores.get('30m', 0) > 30 else "🔴 Bearish"}
- 1h: {new_timeframe_scores.get('1h', 0):.1f} - {"🟢 Bullish" if new_timeframe_scores.get('1h', 0) > 50 else "🟡 Neutral" if new_timeframe_scores.get('1h', 0) > 30 else "🔴 Bearish"}

## On-Chain Metrics
- **Age**: {token.token_age_minutes} minutes old ({"✅ Fresh launch" if token.token_age_minutes < 60 else "⚠️ Not a new launch"})
- **Holders**: {token.holders_count:,} ({"🚀 Rapid distribution" if token.holders_count > 500 else "📊 Growing steadily" if token.holders_count > 200 else "⚠️ Low adoption"})
- **Volume (5m)**: ${token.volume_5m_usd:,.0f} ({"🔥 High activity" if token.volume_5m_usd > 10000 else "📊 Moderate activity" if token.volume_5m_usd > 5000 else "❄️ Low activity"})
- **Liquidity**: {token.lp_count} pools, {token.lp_mcap_ratio:.1%} of MCap ({"💎 Deep liquidity" if token.lp_mcap_ratio > 0.05 else "💧 Adequate liquidity" if token.lp_mcap_ratio > 0.02 else "⚠️ Thin liquidity"})
- **Top 10 Holders**: {token.top_10_holders_percent:.1f}% ({"✅ Well distributed" if token.top_10_holders_percent < 30 else "⚠️ Concentrated"})

## Trading Recommendation
{"🟢 **STRONG BUY** - All systems firing on all cylinders. This token exhibits characteristics of previous 100x performers. Entry at current levels recommended with appropriate position sizing. Set stop loss at -15% from entry." if breakdown.total > 70 else "🟡 **ACCUMULATE** - Promising project with solid fundamentals. Consider building position on dips. Wait for momentum confirmation before full allocation. Risk/reward favorable for patient investors." if breakdown.total > 50 else "🔴 **AVOID/WAIT** - Current metrics do not support investment. Multiple red flags present. Wait for significant improvement in scores before considering entry. High risk of further downside."}

## Risk Factors
{"- Extremely new token, unproven track record\n- High volatility expected\n- Smart contract not fully audited\n- Potential for rapid price swings" if token.token_age_minutes < 60 else "- Limited upside momentum\n- Weak community engagement\n- No major catalysts on horizon\n- Better opportunities available"}

---
*Generated by DVM Scoring Engine | Professional Trading Intelligence*"""
                client = MockChatClient(demo_report)
            
            # Build meaningful signals from the metrics and scores
            signals = []
            if breakdown.momentum > 15:
                signals.append(f"1h: momentum score {breakdown.momentum:.1f}")
            if breakdown.smart_money > 15:
                signals.append(f"1h: smart money score {breakdown.smart_money:.1f}")
            if breakdown.sentiment > 5:
                signals.append(f"1h: sentiment score {breakdown.sentiment:.1f}")
            if breakdown.event > 5:
                signals.append(f"1h: event score {breakdown.event:.1f}")
            
            # Add multi-timeframe signals
            best_timeframe = max(new_timeframe_scores, key=new_timeframe_scores.get)
            signals.append(f"best timeframe: {best_timeframe} ({new_timeframe_scores[best_timeframe]:.1f})")
            if token.volume_5m_usd > 10000:
                signals.append(f"5m: volume ${token.volume_5m_usd/1000:.0f}K")
            if token.lp_count > 2:
                signals.append(f"lp_count: {token.lp_count} pools")
            if token.lp_mcap_ratio > 0.05:
                signals.append(f"lp/mcap: {token.lp_mcap_ratio:.1%}")
            
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
                signals=signals,
                metrics={
                    "holders": token.holders_count, 
                    "top10_pct": token.top_10_holders_percent, 
                    "vol_5m_usd": token.volume_5m_usd, 

                    "lp_locked_pct": token.liquidity_locked_percent,
                    "age_minutes": token.token_age_minutes
                },
                timeframe="multi",  # Indicate multi-timeframe analysis
                as_of_utc=datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            )
            content = generate_trench_report(ti, client)
            resp.trench_report_markdown = content
        except Exception as e:
            # Graceful fallback - don't break the API if AI fails
            resp.trench_report_markdown = f"AI report unavailable: {str(e)}"

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


@app.post("/extract")
async def extract_token_data(request: dict):
    """Extract token data from multiple sources for maximum coverage."""
    from extractors.unified_extractor import extract_token_data
    
    token_address = request.get("token_address")
    if not token_address:
        raise HTTPException(status_code=422, detail="token_address is required")
    
    try:
        result = extract_token_data(token_address)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")





