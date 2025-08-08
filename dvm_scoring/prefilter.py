from __future__ import annotations

from typing import Dict, Tuple

from .models import PreFilterResult, TokenData


# Constants derived from the requirements document
MAX_TOKEN_AGE_MINUTES = 60  # "New tokens <1h"
MAX_TAX_PERCENT = 3.0
REQUIRED_LP_LOCKED_PERCENT = 100.0
MIN_VOLUME_5M_USD = 5_000.0
MIN_HOLDERS = 101  # ">100" strictly greater
MIN_LP_POOL_COUNT = 2  # ">1" strictly greater
MIN_LP_TO_MCAP_RATIO = 0.02
MAX_TOP10_PERCENT = 30.0
MAX_BUNDLE_BUYS_PERCENT = 40.0


def _calc_lp_to_mcap_ratio(token: TokenData) -> float:
    if token.market_cap_usd <= 0:
        return 0.0
    return token.liquidity_usd / token.market_cap_usd


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


def check_lp_pool_count(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    return token.lp_pool_count > MIN_LP_POOL_COUNT - 1, {
        "lp_pool_count": token.lp_pool_count,
        "min_lp_pool_count_exclusive": MIN_LP_POOL_COUNT - 1,
    }


def check_lp_to_mcap_ratio(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    ratio = _calc_lp_to_mcap_ratio(token)
    return ratio > MIN_LP_TO_MCAP_RATIO - 1e-12, {
        "lp_to_mcap_ratio": ratio,
        "min_ratio_exclusive": MIN_LP_TO_MCAP_RATIO,
        "liquidity_usd": token.liquidity_usd,
        "market_cap_usd": token.market_cap_usd,
    }


def check_top10(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    return token.top_10_holders_percent < MAX_TOP10_PERCENT, {
        "top_10_holders_percent": token.top_10_holders_percent,
        "max_top10_percent_exclusive": MAX_TOP10_PERCENT,
    }


def check_bundles(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    return token.bundle_buys_percent < MAX_BUNDLE_BUYS_PERCENT, {
        "bundle_buys_percent": token.bundle_buys_percent,
        "max_bundle_buys_percent_exclusive": MAX_BUNDLE_BUYS_PERCENT,
    }


def run_pre_filter(token: TokenData) -> PreFilterResult:
    """Run all required pre-filter checks.

    All checks must pass for the token to be eligible for scoring.
    """

    checks = {
        "age_lt_1h": check_token_age,
        "degen_audit_pass": check_degen_audit,
        "liquidity_locked_100": check_liquidity_locked,
        "volume_5m_usd_gte_5000": check_volume_5m,
        "holders_gt_100": check_holders,
        "lp_count_gt_1": check_lp_pool_count,
        "lp_mcap_ratio_gt_0_02": check_lp_to_mcap_ratio,
        "top10_pct_lt_30": check_top10,
        "bundle_buys_pct_lt_40": check_bundles,
    }

    failed = []
    details: Dict[str, object] = {}
    for name, fn in checks.items():
        ok, info = fn(token)
        details[name] = info
        if not ok:
            failed.append(name)

    passed = len(failed) == 0
    return PreFilterResult(
        token_address=token.token_address,
        passed=passed,
        failed_checks=failed,
        details=details,
    )

