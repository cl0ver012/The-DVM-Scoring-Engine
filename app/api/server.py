"""FastAPI server for DVM Scoring Engine"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import traceback
import os
from dotenv import load_dotenv

from app.api.schemas import (
    ScoreRequest, ScoreResponse, 
    RankRequest, RankResponse
)
from typing import Dict, Any, Optional
from pydantic import BaseModel

# Define missing request/response models
class ExtractRequest(BaseModel):
    token_address: str

class ExtractResponse(BaseModel):
    success: bool
    data: Optional[Dict[str, Any]]
    message: str

class ReportRequest(BaseModel):
    token_data: Dict[str, Any]
    metrics: Dict[str, Any]
    score: float

class ReportResponse(BaseModel):
    report: Dict[str, Any]
from app.utils.pre_filter import run_pre_filter
from app.models.token import TokenData, DegenAudit
from app.models.metrics import ScoreMetrics, MomentumMetrics, SmartMoneyMetrics, SentimentMetrics, EventMetrics
from app.engine.scoring_engine import ScoringEngine
from app.ranker.formulas import score_new, score_surging, score_all
from app.ai.trench_report import generate_trench_report, TrenchInput
from app.ai.client import OpenAIChatClient
from extractors.unified_extractor import extract_token_data

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="DVM Scoring Engine API",
    description="Deep Value Memetics token scoring and ranking system",
    version="1.0.0"
)

# Configure CORS - Allow all origins during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Initialize components
scoring_engine = ScoringEngine()
# Initialize chat client - always use mock for demo
# To use real OpenAI, ensure you have a valid API key in .env
use_mock = True  # Set to False when you have a valid OpenAI API key

if use_mock:
    print("ℹ️ Using demo AI reports (set use_mock=False in server.py to use OpenAI)")
else:
    try:
        # Check if API key is actually set and not empty
        api_key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not api_key or api_key == "sk-proj-REPLACE_ME":
            raise RuntimeError("OPENAI_API_KEY not configured")
        chat_client = OpenAIChatClient()
    except (RuntimeError, Exception) as e:
        print(f"⚠️ Warning: OpenAI not available ({e}) - Using demo AI reports")
        use_mock = True

if use_mock or 'chat_client' not in locals():
    from app.ai.client import MockChatClient
    # We'll create dynamic reports in the generate_trench_report function
    chat_client = MockChatClient("")  # Empty default, will be replaced dynamically

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "DVM Scoring Engine API",
        "version": "1.0.0",
        "endpoints": [
            "/extract - Extract token data from multiple sources",
            "/score - Score a single token",
            "/rank - Rank multiple tokens",
            "/report - Generate AI trench report"
        ]
    }

@app.post("/extract", response_model=ExtractResponse)
async def post_extract(request: ExtractRequest):
    """Extract token data from all sources"""
    try:
        print(f"\n📊 Extracting data for token: {request.token_address}")
        
        # Extract data using unified extractor
        result = extract_token_data(request.token_address)
        
        # Print extracted scoring variables
        if result and 'combined_data' in result:
            data = result['combined_data']
            print("\n" + "="*60)
            print("🎯 EXTRACTED SCORING VARIABLES FROM APIs")
            print("="*60)
            
            scoring_vars = {
                "📊 MOMENTUM": [
                    ("price_change_percent", data.get('price_change_percent')),
                    ("price_change_5m_percent", data.get('price_change_5m_percent')),
                    ("price_change_24h_percent", data.get('price_change_24h_percent')),
                    ("vol_over_avg_ratio", data.get('vol_over_avg_ratio')),
                ],
                "💰 MARKET DATA": [
                    ("price_now", data.get('price_now')),
                    ("mc_now", data.get('mc_now')),
                    ("volume_24h_usd", data.get('volume_24h_usd')),
                    ("liquidity_usd", data.get('liquidity_usd')),
                ],
                "👥 HOLDERS": [
                    ("holders_count", data.get('holders_count')),
                    ("top_10_holders_percent", data.get('top_10_holders_percent')),
                ]
            }
            
            for category, vars in scoring_vars.items():
                print(f"\n{category}:")
                for name, value in vars:
                    if value is not None:
                        print(f"  ✅ {name}: {value}")
                    else:
                        print(f"  ❌ {name}: Not available")
            
            print("="*60 + "\n")
        
        return ExtractResponse(
            success=True,
            data=result,
            message="Data extraction completed"
        )
        
    except Exception as e:
        print(f"❌ Extraction error: {str(e)}")
        traceback.print_exc()
        return ExtractResponse(
            success=False,
            data=None,
            message=f"Extraction failed: {str(e)}"
        )

@app.post("/score", response_model=ScoreResponse)
async def post_score(request: ScoreRequest):
    """Score a single token"""
    try:
        # Extract token data from request
        token_data = request.token
        token_address = token_data.get('token_address', 'Unknown')
        print(f"\n🎯 Scoring token: {token_address}")
        
        # Run pre-filter
        # Convert dict to TokenData model
        # Ensure degen_audit is properly formatted
        if 'degen_audit' not in token_data or token_data['degen_audit'] is None:
            token_data['degen_audit'] = DegenAudit(
                is_honeypot=False,
                has_blacklist=False,
                buy_tax_percent=0.0,
                sell_tax_percent=0.0
            )
        elif isinstance(token_data['degen_audit'], dict):
            token_data['degen_audit'] = DegenAudit(**token_data['degen_audit'])
        
        token_model = TokenData(**token_data)
        pre_filter_result = run_pre_filter(token_model)
        
        if not pre_filter_result.passed:
            return ScoreResponse(
                passed_prefilter=False,
                failed_checks=pre_filter_result.failed_checks,
                breakdown={},
                total=0.0,
                momentum=0.0,
                smart_money=0.0,
                sentiment=0.0,
                event=0.0
            )
        
        # Create metrics from token data
        # Extract metrics from token_data or request.metrics
        metrics_data = request.metrics if request.metrics else {}
        
        # Create metrics object
        metrics = ScoreMetrics(
            momentum=MomentumMetrics(
                vol_over_avg_ratio=metrics_data.get('vol_over_avg_ratio', 1.0),
                price_change_percent=metrics_data.get('price_change_percent', 0.0),
                ath_hit=metrics_data.get('ath_hit', False),
                holders_growth_percent=metrics_data.get('holders_growth_percent', 0.0)
            ),
            smart_money=SmartMoneyMetrics(
                whale_buy_usd=metrics_data.get('whale_buy_usd', 0.0),
                whale_buy_supply_percent=metrics_data.get('whale_buy_supply_percent', 0.0),
                dca_accumulation_supply_percent=metrics_data.get('dca_accumulation_supply_percent', 0.0),
                net_inflow_wallets_gt_10k_usd=metrics_data.get('net_inflow_wallets_gt_10k_usd', 0.0)
            ),
            sentiment=SentimentMetrics(
                mentions_velocity_ratio=metrics_data.get('mentions_velocity_ratio', 1.0),
                tier1_kol_buy_supply_percent=metrics_data.get('tier1_kol_buy_supply_percent', 0.0),
                influencer_reach=metrics_data.get('influencer_reach', 0),
                polarity_positive_percent=metrics_data.get('polarity_positive_percent', 50.0)
            ),
            event=EventMetrics(
                inflow_over_mcap_percent=metrics_data.get('inflow_over_mcap_percent', 0.0),
                upgrade_or_staking_live=metrics_data.get('upgrade_or_staking_live', False)
            )
        )
        
        # Calculate scores using the scoring engine
        score_result = scoring_engine.score(metrics, "1h")
        total_score = score_result.total
        
        # Print extracted scoring variables
        print("\n" + "="*60)
        print("🔍 EXTRACTED SCORING VARIABLES")
        print("="*60)
        
        print("\n📊 MOMENTUM METRICS:")
        print(f"  vol_over_avg_ratio: {metrics.momentum.vol_over_avg_ratio}")
        print(f"  price_change_percent: {metrics.momentum.price_change_percent}")
        print(f"  ath_hit: {metrics.momentum.ath_hit}")
        print(f"  holders_growth_percent: {metrics.momentum.holders_growth_percent}")
        
        print("\n💰 SMART MONEY METRICS:")
        print(f"  whale_buy_usd: {metrics.smart_money.whale_buy_usd}")
        print(f"  whale_buy_supply_percent: {metrics.smart_money.whale_buy_supply_percent}")
        print(f"  dca_accumulation_supply_percent: {metrics.smart_money.dca_accumulation_supply_percent}")
        print(f"  net_inflow_wallets_gt_10k_usd: {metrics.smart_money.net_inflow_wallets_gt_10k_usd}")
        
        print("\n💬 SENTIMENT METRICS:")
        print(f"  mentions_velocity_ratio: {metrics.sentiment.mentions_velocity_ratio}")
        print(f"  tier1_kol_buy_supply_percent: {metrics.sentiment.tier1_kol_buy_supply_percent}")
        print(f"  influencer_reach: {metrics.sentiment.influencer_reach}")
        print(f"  polarity_positive_percent: {metrics.sentiment.polarity_positive_percent}")
        
        print("\n🎯 EVENT METRICS:")
        print(f"  inflow_over_mcap_percent: {metrics.event.inflow_over_mcap_percent}")
        print(f"  upgrade_or_staking_live: {metrics.event.upgrade_or_staking_live}")
        
        print("="*60 + "\n")
        
        # Build response matching schema
        breakdown = {
            "momentum": score_result.momentum,
            "smart_money": score_result.smart_money,
            "sentiment": score_result.sentiment,
            "event": score_result.event
        }
        
        # Generate AI report if requested
        trench_report = None
        if True:  # Always generate for demo
            print("\n🤖 Generating AI trench report...")
            trench_input = TrenchInput(
                token={
                    'name': token_model.token_name,
                    'symbol': token_model.token_symbol,
                    'address': token_model.token_address
                },
                prefilter={
                    'passed': True,
                    'token_age_minutes': token_model.token_age_minutes,
                    'liquidity_usd': getattr(token_model, 'liquidity_usd', 0),
                    'volume_24h_usd': getattr(token_model, 'volume_24h_usd', 0),
                    'holders_count': token_model.holders_count
                },
                scores={
                    'total': total_score,
                    'momentum': score_result.momentum,
                    'smart_money': score_result.smart_money,
                    'sentiment': score_result.sentiment,
                    'event': score_result.event
                },
                signals=[],  # Could be populated based on score thresholds
                metrics={
                    'momentum': metrics.momentum.model_dump(),
                    'smart_money': metrics.smart_money.model_dump(),
                    'sentiment': metrics.sentiment.model_dump(),
                    'event': metrics.event.model_dump()
                },
                timeframe='multi',
                as_of_utc=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
            )
            trench_report_text = generate_trench_report(trench_input, chat_client)
            # Convert to dict format for response
            trench_report = {
                "markdown": trench_report_text,
                "sections": [
                    {
                        "title": "Analysis",
                        "content": trench_report_text
                    }
                ]
            }
        
        return ScoreResponse(
            passed_prefilter=True,
            failed_checks=[],
            breakdown=breakdown,
            total=total_score,
            momentum=score_result.momentum,
            smart_money=score_result.smart_money,
            sentiment=score_result.sentiment,
            event=score_result.event,
            trench_report_markdown=trench_report_text if trench_report else None,
            trench_report_json=trench_report
        )
        
    except Exception as e:
        print(f"❌ Scoring error: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/rank", response_model=RankResponse)
async def post_rank(request: RankRequest):
    """Rank multiple tokens"""
    try:
        print(f"\n🏆 Ranking {len(request.rows)} tokens in category: {request.tab}")
        
        # Convert RankRow objects to dicts for processing
        tokens = [row.model_dump() for row in request.rows]
        
        # Filter and score tokens
        scored_tokens = []
        for token in tokens:
            # Add required fields for pre-filter
            token_data = {
                'token_address': token.get('id'),
                'token_symbol': token.get('symbol'),
                'token_name': token.get('name'),
                'token_age_minutes': token.get('token_age_minutes', 30),
                'liquidity_locked_percent': token.get('liquidity_locked_percent', 100),
                'volume_5m_usd': token.get('volume_5m_usd', 10000),
                'holders_count': token.get('holders_now', 150),
                'lp_count': token.get('lp_count', 2),
                'lp_mcap_ratio': token.get('lp_now', 100000) / token.get('mc_now', 1) if token.get('mc_now', 1) > 0 else 0.05,
                'top_10_holders_percent': token.get('top_10_holders_percent', 20),
                'bundle_percent': token.get('bundle_percent', 30)
            }
            
            # Convert to TokenData model
            # Ensure degen_audit is properly formatted
            if 'degen_audit' not in token_data or token_data['degen_audit'] is None:
                token_data['degen_audit'] = DegenAudit(
                    is_honeypot=False,
                    has_blacklist=False,
                    buy_tax_percent=0.0,
                    sell_tax_percent=0.0
                )
            elif isinstance(token_data['degen_audit'], dict):
                token_data['degen_audit'] = DegenAudit(**token_data['degen_audit'])
            
            token_model = TokenData(**token_data)
            pre_filter_result = run_pre_filter(token_model)
            if pre_filter_result.passed:
                # Create default metrics for ranking
                metrics = ScoreMetrics()
                score_result = scoring_engine.score(metrics, "1h")
                scored_tokens.append({
                    'token': token_data,
                    'score': score_result.total
                })
        
        # Apply ranking formula based on tab
        sol_usd = 225.0  # Current SOL price, could be fetched dynamically
        
        ranked_rows = []
        for scored_data in scored_tokens:
            # Get the original row data from request
            original_row = next((r for r in tokens if r.get('id') == scored_data['token']['token_address']), {})
            
            # Merge with defaults for ranking formulas
            row = {
                **original_row,
                'mc_change_pct': original_row.get('mc_change_pct', 0),
                'vol_now': original_row.get('vol_now', 0),
                'vol_to_mc': original_row.get('vol_to_mc', 0),
                'kolusd_now': original_row.get('kolusd_now', 0),
                'whale_buy_count': original_row.get('whale_buy_count', 0),
                'netflow_now': original_row.get('netflow_now', 0),
                'kol_velocity': original_row.get('kol_velocity', 0),
                'fee_sol_now': original_row.get('fee_sol_now', 0),
                'mc_now': original_row.get('mc_now', 1),
                'top10_pct': original_row.get('top_10_holders_percent', 20) / 100,  # Convert to decimal
                'bundle_pct': original_row.get('bundle_percent', 30) / 100,  # Convert to decimal
                'minutes_since_peak': 30,  # Default
                'dca_flag': 0,
                'ath_flag': 0,
                'score': scored_data['score']
            }
            
            # Calculate ranking score based on tab
            if request.tab == "New":
                rank_score = score_new(row, sol_usd)
            elif request.tab == "Surging":
                rank_score = score_surging(row, sol_usd)
            else:  # All
                rank_score = score_all(row, sol_usd)
            
            # Add score to row
            row['rank_score'] = rank_score
            ranked_rows.append(row)
        
        # Sort by rank score descending
        ranked_rows.sort(key=lambda x: x['rank_score'], reverse=True)
        
        return RankResponse(tab=request.tab, rows=ranked_rows)
        
    except Exception as e:
        print(f"❌ Ranking error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/report", response_model=ReportResponse)
async def post_report(request: ReportRequest):
    """Generate AI-powered trench report"""
    try:
        token_address = request.token_data.get('token_address', 'Unknown')
        print(f"\n📝 Generating trench report for: {token_address}")
        
        # Create TrenchInput
        trench_input = TrenchInput(
            token=request.token_data,
            prefilter={},
            scores={'total': request.score},
            signals=[],
            metrics=request.metrics,
            timeframe='multi',
            as_of_utc=datetime.utcnow().isoformat()
        )
        
        # Generate report
        report_text = generate_trench_report(trench_input, chat_client)
        
        return ReportResponse(report={'text': report_text})
        
    except Exception as e:
        print(f"❌ Report generation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)