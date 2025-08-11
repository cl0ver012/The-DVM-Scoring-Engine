from app.models import TokenData
from app.utils.pre_filter import run_pre_filter


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
            "top_10_holders_percent": 24.7,
            "fees_paid_sol": 34.87,
        }
    )


def make_failing_token() -> TokenData:
    return TokenData.model_validate(
        {
            "token_address": "Bad1111111111111111111111111111111111111111",
            "token_symbol": "BAD",
            "token_name": "Bad Example Token",
            "token_age_minutes": 70,
            "degen_audit": {
                "is_honeypot": False,
                "has_blacklist": False,
                "buy_tax_percent": 1.0,
                "sell_tax_percent": 1.0,
            },
            "liquidity_locked_percent": 100.0,
            "volume_5m_usd": 7000.0,
            "holders_count": 200,
            "top_10_holders_percent": 20.0,
            "fees_paid_sol": 8.0,
            "token_age_days": 200,
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
    # Should fail due to age < 1h (age_lt_1h)
    assert "age_lt_1h" in result.failed_checks


def base_token(overrides: dict) -> TokenData:
    base = {
        "token_address": "Base111111111111111111111111111111111111111",
        "token_symbol": "BASE",
        "token_name": "Base",
        "token_age_minutes": 30,  # pass age
        "degen_audit": {
            "is_honeypot": False,
            "has_blacklist": False,
            "buy_tax_percent": 1.0,
            "sell_tax_percent": 1.0,
        },
        "liquidity_locked_percent": 100.0,
        "volume_5m_usd": 6000.0,
        "holders_count": 150,
        "top_10_holders_percent": 20.0,
        "fees_paid_sol": 10.0,
        "token_age_days": 1,
    }
    base.update(overrides)
    return TokenData.model_validate(base)


def test_fail_age_check():
    token = base_token({"token_age_minutes": 61})
    result = run_pre_filter(token)
    assert result.passed is False
    assert "age_lt_1h" in result.failed_checks


def test_fail_degen_audit_honeypot():
    token = base_token({"degen_audit": {"is_honeypot": True, "has_blacklist": False, "buy_tax_percent": 1.0, "sell_tax_percent": 1.0}})
    result = run_pre_filter(token)
    assert result.passed is False
    assert "degen_audit_pass" in result.failed_checks


def test_fail_degen_audit_tax():
    token = base_token({"degen_audit": {"is_honeypot": False, "has_blacklist": False, "buy_tax_percent": 3.0, "sell_tax_percent": 2.0}})
    result = run_pre_filter(token)
    assert result.passed is False
    assert "degen_audit_pass" in result.failed_checks


def test_fail_liquidity_lock():
    token = base_token({"liquidity_locked_percent": 99.9})
    result = run_pre_filter(token)
    assert result.passed is False
    assert "liquidity_locked_100" in result.failed_checks


def test_fail_volume_5m():
    token = base_token({"volume_5m_usd": 4999.99})
    result = run_pre_filter(token)
    assert result.passed is False
    assert "volume_5m_usd_gte_5000" in result.failed_checks


def test_fail_holders_gt_100():
    token = base_token({"holders_count": 100})
    result = run_pre_filter(token)
    assert result.passed is False
    assert "holders_gt_100" in result.failed_checks


def test_fail_top10_pct_lt_30():
    token = base_token({"top_10_holders_percent": 30.0})
    result = run_pre_filter(token)
    assert result.passed is False
    assert "top10_pct_lt_30" in result.failed_checks


def test_fail_fees_paid_when_age_lt_180d():
    token = base_token({"fees_paid_sol": 5.0, "token_age_days": 10})
    result = run_pre_filter(token)
    assert result.passed is False
    assert "fees_paid_sol_gt_5_age_lt_180d" in result.failed_checks


def test_skip_fees_when_age_ge_180d():
    token = base_token({"fees_paid_sol": 0.0, "token_age_days": 181})
    result = run_pre_filter(token)
    assert result.passed is True

