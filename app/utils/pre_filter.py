from __future__ import annotations

from typing import Dict, Tuple

from app.models import PreFilterResult, TokenData


# Pre-filter thresholds per document requirements
MIN_TOKEN_AGE_MINUTES = 60  # 1. Token Age (>1h for safety - avoid rugs)
MAX_TAX_PERCENT = 3.0  # 2. Basic Security Audit (<3%)
REQUIRED_LP_LOCKED_PERCENT = 100.0  # 3. Liquidity Lock (100%)
MIN_VOLUME_5M_USD = 5_000.0  # 4. Initial Volume (>$5k)
MIN_HOLDERS = 100  # 5. Initial Holders (>100)
MIN_LP_COUNT = 1  # 6. LP Count (>1)
MIN_LP_MCAP_RATIO = 0.02  # 7. LP/MCap Ratio (>0.02)
MAX_TOP10_PERCENT = 30.0  # 8. Holder Distribution (<30%)
MAX_BUNDLE_PERCENT = 40.0  # 9. Bundle Percentage (<40%)


def check_token_age(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    return token.token_age_minutes > MIN_TOKEN_AGE_MINUTES, {
        "token_age_minutes": token.token_age_minutes,
        "min_age_minutes": MIN_TOKEN_AGE_MINUTES,
    }


def check_degen_audit(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    """
    Degen audit check with partial data support.
    Prioritizes critical security checks (honeypot, blacklist) over tax data.
    Only enforces tax limits when real tax data is available (not defaults).
    """
    audit = token.degen_audit
    
    # CRITICAL CHECKS (we have reliable data for these from GMGN)
    honeypot_ok = not audit.is_honeypot
    blacklist_ok = not audit.has_blacklist
    
    # TAX CHECKS (only enforce if we have real data, not defaults)
    buy_tax_ok = True
    sell_tax_ok = True
    tax_data_available = False
    
    # Check if tax data looks real (not default zeros from failed scraping)
    if audit.buy_tax_percent > 0.0 or audit.sell_tax_percent > 0.0:
        tax_data_available = True
        buy_tax_ok = audit.buy_tax_percent < MAX_TAX_PERCENT
        sell_tax_ok = audit.sell_tax_percent < MAX_TAX_PERCENT
    
    # PASS if critical checks pass (tax checks only applied when data available)
    ok = honeypot_ok and blacklist_ok and buy_tax_ok and sell_tax_ok
    
    return ok, {
        "is_honeypot": audit.is_honeypot,
        "has_blacklist": audit.has_blacklist,
        "buy_tax_percent": audit.buy_tax_percent,
        "sell_tax_percent": audit.sell_tax_percent,
        "tax_data_available": tax_data_available,
        "critical_checks_passed": honeypot_ok and blacklist_ok,
        "tax_checks_passed": buy_tax_ok and sell_tax_ok,
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
    return token.holders_count > MIN_HOLDERS, {
        "holders_count": token.holders_count,
        "min_holders_exclusive": MIN_HOLDERS,
    }


def check_top10(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    return token.top_10_holders_percent < MAX_TOP10_PERCENT, {
        "top_10_holders_percent": token.top_10_holders_percent,
        "max_top10_percent_exclusive": MAX_TOP10_PERCENT,
    }


def check_lp_count(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    return token.lp_count > MIN_LP_COUNT, {
        "lp_count": token.lp_count,
        "min_lp_count_exclusive": MIN_LP_COUNT,
    }


def check_lp_mcap_ratio(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    return token.lp_mcap_ratio > MIN_LP_MCAP_RATIO, {
        "lp_mcap_ratio": token.lp_mcap_ratio,
        "min_lp_mcap_ratio_exclusive": MIN_LP_MCAP_RATIO,
    }


def check_bundle_percent(token: TokenData) -> Tuple[bool, Dict[str, float]]:
    # Skip check if bundle_percent is not available (None)
    if token.bundle_percent is None:
        return True, {
            "bundle_percent": None,
            "max_bundle_percent_exclusive": MAX_BUNDLE_PERCENT,
            "skipped": True,
        }
    
    return token.bundle_percent < MAX_BUNDLE_PERCENT, {
        "bundle_percent": token.bundle_percent,
        "max_bundle_percent_exclusive": MAX_BUNDLE_PERCENT,
        "skipped": False,
    }


def run_pre_filter(token: TokenData) -> PreFilterResult:
    # Print debug information about the token
    print("\n" + "="*60)
    print("PRE-FILTER DEBUG - Token Values:")
    print("="*60)
    print(f"Token Address: {token.token_address}")
    print(f"Token Symbol: {token.token_symbol}")
    print(f"Token Age: {token.token_age_minutes} minutes")
    print(f"Liquidity Locked: {token.liquidity_locked_percent}%")
    print(f"Volume (5m): ${token.volume_5m_usd:,.2f}")
    print(f"Holders Count: {token.holders_count}")
    print(f"LP Count: {token.lp_count}")
    print(f"LP/MCap Ratio: {token.lp_mcap_ratio:.4f}")
    print(f"Top 10 Holders: {token.top_10_holders_percent}%")
    print(f"Bundle Percent: {token.bundle_percent}%")
    print(f"DegenAudit: Honeypot={token.degen_audit.is_honeypot}, Blacklist={token.degen_audit.has_blacklist}")
    print(f"           Buy Tax={token.degen_audit.buy_tax_percent}%, Sell Tax={token.degen_audit.sell_tax_percent}%")
    print("="*60)
    
    checks = {
        "age_gt_1h": check_token_age,
        "degen_audit_pass": check_degen_audit,
        "liquidity_locked_100": check_liquidity_locked,
        "volume_5m_usd_gte_5000": check_volume_5m,
        "holders_gt_100": check_holders,
        "lp_count_gt_1": check_lp_count,
        "lp_mcap_ratio_gt_002": check_lp_mcap_ratio,
        "top10_pct_lt_30": check_top10,
        "bundle_pct_lt_40": check_bundle_percent,
    }

    failed = []
    details: Dict[str, object] = {}
    
    print("\nPre-filter Check Results:")
    print("-" * 60)
    
    for name, fn in checks.items():
        ok, info = fn(token)
        details[name] = info
        if not ok:
            failed.append(name)
        
        # Print check result with actual vs required values
        status = "✓ PASS" if ok else "✗ FAIL"
        print(f"{status} | {name}: {info}")
    
    print("-" * 60)
    print(f"Overall Result: {'PASSED' if len(failed) == 0 else 'FAILED'}")
    if failed:
        print(f"Failed checks: {', '.join(failed)}")
    print("="*60 + "\n")

    return PreFilterResult(
        token_address=token.token_address,
        passed=len(failed) == 0,
        failed_checks=failed,
        details=details,
    )


