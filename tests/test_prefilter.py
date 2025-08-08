from dvm_scoring.models import TokenData
from dvm_scoring.prefilter import run_pre_filter


def make_passing_token() -> TokenData:
    return TokenData.model_validate(
        {
            "token_address": "So11111111111111111111111111111111111111112",
            "token_symbol": "DVM",
            "token_name": "DVM Example Token",
            "token_age_minutes": 35,
            "degen_audit": {
                "is_honeypot": False,
                "has_blacklist": False,
                "buy_tax_percent": 1.5,
                "sell_tax_percent": 2.0,
            },
            "liquidity_locked_percent": 100.0,
            "volume_5m_usd": 7250.0,
            "holders_count": 358,
            "lp_pool_count": 2,
            "liquidity_usd": 12000.0,
            "market_cap_usd": 350000.0,
            "top_10_holders_percent": 24.7,
            "bundle_buys_percent": 18.0,
        }
    )


def make_failing_token() -> TokenData:
    return TokenData.model_validate(
        {
            "token_address": "Bad1111111111111111111111111111111111111111",
            "token_symbol": "BAD",
            "token_name": "Bad Example Token",
            "token_age_minutes": 125,
            "degen_audit": {
                "is_honeypot": True,
                "has_blacklist": True,
                "buy_tax_percent": 5.0,
                "sell_tax_percent": 6.0,
            },
            "liquidity_locked_percent": 50.0,
            "volume_5m_usd": 1200.0,
            "holders_count": 50,
            "lp_pool_count": 1,
            "liquidity_usd": 1000.0,
            "market_cap_usd": 250000.0,
            "top_10_holders_percent": 65.0,
            "bundle_buys_percent": 55.0,
        }
    )


def test_prefilter_passes_for_valid_token():
    token = make_passing_token()
    result = run_pre_filter(token)
    assert result.passed is True
    assert result.failed_checks == []


def test_prefilter_fails_for_invalid_token():
    token = make_failing_token()
    result = run_pre_filter(token)
    assert result.passed is False
    # Should fail multiple checks
    assert len(result.failed_checks) >= 5

