from __future__ import annotations

from typing import Dict, Tuple

from app.models import PreFilterResult, TokenData


# Definitive thresholds per final spec
MAX_TOKEN_AGE_MINUTES = 60  # 1. Token Age
MAX_TAX_PERCENT = 3.0  # 2. Basic Security Audit
REQUIRED_LP_LOCKED_PERCENT = 100.0  # 3. Liquidity Lock
MIN_VOLUME_5M_USD = 5_000.0  # 4. Initial Volume
MIN_HOLDERS = 101  # 5. Initial Holders (>100)
MAX_TOP10_PERCENT = 30.0  # 6. Holder Distribution (<30%)

# 7. Creator Fees Paid rule (age-gated at 180 days)
FEES_MIN_SOL = 5.0
FEES_ENFORCE_AGE_DAYS = 180.0


def check_token_age(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    return token.token_age_minutes < MAX_TOKEN_AGE_MINUTES, {
        "token_age_minutes": token.token_age_minutes,
        "max_age_minutes": MAX_TOKEN_AGE_MINUTES,
    }


def check_degen_audit(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    audit = token.degen_audit
    ok = (
        (not audit.is_honeypot)
        and (not audit.has_blacklist)
        and (audit.buy_tax_percent < MAX_TAX_PERCENT)
        and (audit.sell_tax_percent < MAX_TAX_PERCENT)
    )
    return ok, {
        "is_honeypot": audit.is_honeypot,
        "has_blacklist": audit.has_blacklist,
        "buy_tax_percent": audit.buy_tax_percent,
        "sell_tax_percent": audit.sell_tax_percent,
        "max_tax_percent": MAX_TAX_PERCENT,
    }


def check_liquidity_locked(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    return (
        token.liquidity_locked_percent >= REQUIRED_LP_LOCKED_PERCENT,
        {
            "liquidity_locked_percent": token.liquidity_locked_percent,
            "required_percent": REQUIRED_LP_LOCKED_PERCENT,
        },
    )


def check_volume_5m(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    return token.volume_5m_usd >= MIN_VOLUME_5M_USD, {
        "volume_5m_usd": token.volume_5m_usd,
        "min_volume_5m_usd": MIN_VOLUME_5M_USD,
    }


def check_holders(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    return token.holders_count > MIN_HOLDERS - 1, {
        "holders_count": token.holders_count,
        "min_holders_exclusive": MIN_HOLDERS - 1,
    }


def check_top10(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    return token.top_10_holders_percent < MAX_TOP10_PERCENT, {
        "top_10_holders_percent": token.top_10_holders_percent,
        "max_top10_percent_exclusive": MAX_TOP10_PERCENT,
    }


def check_fees_paid(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    # Prefer explicit days field; else derive from minutes
    age_days = (
        token.token_age_days
        if token.token_age_days is not None
        else token.token_age_minutes / (60.0 * 24.0)
    )
    enforce = age_days < FEES_ENFORCE_AGE_DAYS
    if not enforce:
        return True, {
            "fees_paid_sol": token.fees_paid_sol,
            "min_fees_paid_sol_exclusive": FEES_MIN_SOL,
            "age_days": age_days,
            "enforced": False,
        }
    # Strictly greater than threshold (exclusive)
    return token.fees_paid_sol > FEES_MIN_SOL, {
        "fees_paid_sol": token.fees_paid_sol,
        "min_fees_paid_sol_exclusive": FEES_MIN_SOL,
        "age_days": age_days,
        "enforced": True,
    }


def run_pre_filter(token: TokenData) -> PreFilterResult:
    checks = {
        "age_lt_1h": check_token_age,
        "degen_audit_pass": check_degen_audit,
        "liquidity_locked_100": check_liquidity_locked,
        "volume_5m_usd_gte_5000": check_volume_5m,
        "holders_gt_100": check_holders,
        "top10_pct_lt_30": check_top10,
        "fees_paid_sol_gt_5_age_lt_180d": check_fees_paid,
    }

    failed = []
    details: Dict[str, object] = {}
    for name, fn in checks.items():
        ok, info = fn(token)
        details[name] = info
        if not ok:
            failed.append(name)

    return PreFilterResult(
        token_address=token.token_address,
        passed=len(failed) == 0,
        failed_checks=failed,
        details=details,
    )


