"""Dynamic AI report generation based on actual token data"""

def generate_dynamic_report(trench_input) -> str:
    """Generate a contextual AI report based on the actual token data and scores"""
    
    token = trench_input.token
    scores = trench_input.scores
    metrics = trench_input.metrics
    prefilter = trench_input.prefilter
    
    # Extract key data
    token_symbol = token.get('symbol', 'Unknown')
    token_name = token.get('name', 'Unknown Token')
    total_score = scores.get('total', 0)
    momentum_score = scores.get('momentum', 0)
    smart_money_score = scores.get('smart_money', 0)
    sentiment_score = scores.get('sentiment', 0)
    event_score = scores.get('event', 0)
    
    # Determine overall rating
    if total_score >= 80:
        rating = "🔥 Exceptional"
        rating_desc = "showing strong bullish signals across multiple categories"
    elif total_score >= 60:
        rating = "🚀 Strong"
        rating_desc = "displaying significant positive momentum and activity"
    elif total_score >= 40:
        rating = "📈 Moderate"
        rating_desc = "with some positive indicators worth monitoring"
    elif total_score >= 20:
        rating = "📊 Neutral"
        rating_desc = "showing mixed signals that require careful observation"
    else:
        rating = "⚠️ Weak"
        rating_desc = "with limited activity and minimal positive indicators"
    
    # Build the report
    report = f"""## 🚀 Token Analysis Report

### 📊 Market Overview
**{token_name} ({token_symbol})** scores **{total_score:.1f}/100** - {rating}

This token is {rating_desc}. """
    
    # Add category-specific insights
    if momentum_score > 30:
        report += f"Strong momentum ({momentum_score:.1f}/37.5) indicates significant price and volume activity. "
    elif momentum_score > 15:
        report += f"Moderate momentum ({momentum_score:.1f}/37.5) suggests steady market interest. "
    else:
        report += f"Low momentum ({momentum_score:.1f}/37.5) reflects minimal price movement and trading volume. "
    
    report += "\n\n### 💡 Key Insights\n"
    
    # Momentum insights
    momentum_metrics = metrics.get('momentum', {})
    if momentum_metrics.get('vol_over_avg_ratio', 0) > 2:
        report += f"- **Volume Surge**: {momentum_metrics['vol_over_avg_ratio']:.1f}x average volume detected 📈\n"
    else:
        report += f"- **Volume Activity**: Normal trading volume ({momentum_metrics.get('vol_over_avg_ratio', 1):.1f}x average)\n"
    
    if momentum_metrics.get('price_change_percent', 0) > 10:
        report += f"- **Price Action**: Strong upward movement (+{momentum_metrics['price_change_percent']:.1f}%) 🚀\n"
    elif momentum_metrics.get('price_change_percent', 0) < -10:
        report += f"- **Price Action**: Significant decline ({momentum_metrics['price_change_percent']:.1f}%) 📉\n"
    else:
        report += f"- **Price Action**: Stable price movement ({momentum_metrics.get('price_change_percent', 0):+.1f}%)\n"
    
    # Smart money insights
    smart_money_metrics = metrics.get('smart_money', {})
    if smart_money_score > 20:
        report += f"- **Smart Money**: High whale activity detected (Score: {smart_money_score:.1f}/37.5) 🐋\n"
    elif smart_money_score > 10:
        report += f"- **Smart Money**: Moderate institutional interest (Score: {smart_money_score:.1f}/37.5)\n"
    else:
        report += f"- **Smart Money**: Limited whale activity observed\n"
    
    if smart_money_metrics.get('whale_buy_usd', 0) > 50000:
        report += f"  - Whale purchases: ${smart_money_metrics['whale_buy_usd']:,.0f} detected\n"
    
    # Sentiment insights
    if sentiment_score > 5:
        report += f"- **Community Sentiment**: Positive social momentum (Score: {sentiment_score:.1f}/12.5) 💬\n"
    else:
        report += f"- **Community Sentiment**: Neutral market sentiment\n"
    
    # Risk Assessment
    report += "\n### ⚠️ Risk Assessment\n"
    
    # Pre-filter status
    if prefilter.get('passed', False):
        report += "- **Pre-filter checks**: ✅ Passed all safety requirements\n"
    else:
        report += "- **Pre-filter checks**: ❌ Failed - High risk detected\n"
    
    # Security audit
    # Get degen_audit from token data if not in prefilter
    degen_audit = token.get('degen_audit', prefilter.get('degen_audit', {}))
    if not degen_audit.get('is_honeypot', False) and not degen_audit.get('has_blacklist', False):
        report += "- **Security audit**: ✅ Clean - No honeypot or blacklist detected\n"
    else:
        report += "- **Security audit**: ❌ Warning - Potential security issues\n"
    
    # Liquidity
    liquidity = prefilter.get('liquidity_locked_percent', 0)
    if liquidity >= 100:
        report += f"- **Liquidity**: ✅ Fully locked ({liquidity:.0f}%)\n"
    elif liquidity > 50:
        report += f"- **Liquidity**: ⚠️ Partially locked ({liquidity:.0f}%)\n"
    else:
        report += f"- **Liquidity**: ❌ Not locked - High rug risk\n"
    
    # Holder concentration
    top_10_percent = prefilter.get('top_10_holders_percent', 0)
    if top_10_percent < 30:
        report += f"- **Holder Distribution**: ✅ Well distributed (Top 10: {top_10_percent:.0f}%)\n"
    elif top_10_percent < 50:
        report += f"- **Holder Distribution**: ⚠️ Moderate concentration (Top 10: {top_10_percent:.0f}%)\n"
    else:
        report += f"- **Holder Distribution**: ❌ High concentration risk (Top 10: {top_10_percent:.0f}%)\n"
    
    # Recommendation
    report += "\n### 🎯 Recommendation\n"
    
    if total_score >= 60:
        report += f"**Strong Buy Signal** - {token_symbol} shows excellent momentum and smart money activity. "
        report += "Consider entering a position while monitoring for sustained volume and whale activity. "
        report += "Set stop-loss at -15% and take profits incrementally above +50%."
    elif total_score >= 40:
        report += f"**Moderate Buy** - {token_symbol} displays positive indicators worth exploring. "
        report += "Wait for confirmation of trend continuation before taking a full position. "
        report += "Consider dollar-cost averaging with tight risk management."
    elif total_score >= 20:
        report += f"**Hold/Watch** - {token_symbol} shows mixed signals. "
        report += "Monitor for increased whale activity or volume spikes before entering. "
        report += "This token may be accumulating before a larger move."
    else:
        report += f"**Avoid/High Risk** - {token_symbol} lacks positive momentum indicators. "
        report += "The low scores suggest minimal market interest and potential downside risk. "
        report += "Wait for significant improvements in metrics before considering entry."
    
    return report
