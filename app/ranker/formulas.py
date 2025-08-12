from __future__ import annotations

import math
from typing import Dict


def clamp(x: float, a: float, b: float) -> float:
    return max(a, min(b, x))


def tanh(x: float) -> float:
    return math.tanh(x)


def score_new(r: Dict[str, float], sol_usd: float) -> float:
    price = tanh(r["mc_change_pct"] / 50)
    volmc = 0.5 * tanh(math.log10(max(1, r["vol_now"])) - 5) + 0.5 * tanh(r["vol_to_mc"] / 1.5)
    whales = 0.6 * tanh(r["kolusd_now"] / 250_000) + 0.4 * tanh(math.sqrt(r["whale_buy_count"]) / 3)
    netflow = tanh((r["netflow_now"] / max(1, r["vol_now"])) * 3)
    fresh = math.exp(-clamp(r["minutes_since_peak"], 0, 60) / 75)
    kol = tanh(r["kol_velocity"] / 20)
    fees = tanh(((r["fee_sol_now"] * sol_usd) / max(1, r["mc_now"])) * 8)
    top10 = 1 - clamp(r["top10_pct"], 0, 1)
    bundle = 1 - clamp(r["bundle_pct"], 0, 1)
    dca = 1 if r.get("dca_flag", 0) else 0
    return (
        0.25 * price
        + 0.20 * volmc
        + 0.15 * whales
        + 0.10 * netflow
        + 0.10 * fresh
        + 0.05 * kol
        + 0.05 * fees
        + 0.045 * top10
        + 0.035 * bundle
        + 0.02 * dca
    )


def score_surging(r: Dict[str, float], sol_usd: float) -> float:
    price = tanh(r["mc_change_pct"] / 50)
    whales = 0.6 * tanh(r["kolusd_now"] / 250_000) + 0.4 * tanh(math.sqrt(r["whale_buy_count"]) / 3)
    volmc = 0.5 * tanh(math.log10(max(1, r["vol_now"])) - 5) + 0.5 * tanh(r["vol_to_mc"] / 1.5)
    netflow = tanh((r["netflow_now"] / max(1, r["vol_now"])) * 3)
    kol = tanh(r["kol_velocity"] / 20)
    ath = 1 if r.get("ath_flag", 0) else 0
    dca = 1 if r.get("dca_flag", 0) else 0
    return 0.25 * price + 0.15 * ath + 0.20 * whales + 0.10 * dca + 0.15 * volmc + 0.10 * netflow + 0.05 * kol


def score_all(r: Dict[str, float], sol_usd: float) -> float:
    price = tanh(r["mc_change_pct"] / 50)
    volmc = 0.5 * tanh(math.log10(max(1, r["vol_now"])) - 5) + 0.5 * tanh(r["vol_to_mc"] / 1.5)
    whales = 0.6 * tanh(r["kolusd_now"] / 250_000) + 0.4 * tanh(math.sqrt(r["whale_buy_count"]) / 3)
    netflow = tanh((r["netflow_now"] / max(1, r["vol_now"])) * 3)
    fresh = math.exp(-clamp(r["minutes_since_peak"], 0, 60) / 110)
    kol = tanh(r["kol_velocity"] / 20)
    return 0.28 * price + 0.24 * volmc + 0.18 * whales + 0.14 * netflow + 0.10 * fresh + 0.06 * kol


