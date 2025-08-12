from app.ranker.formulas import score_new, score_surging, score_all


def test_ranker_scores_monotonic_example():
    sol_usd = 150.0
    a = {
        "mc_change_pct": 18.4,
        "vol_now": 250_000,
        "vol_to_mc": 2.5,
        "kolusd_now": 250_000,
        "whale_buy_count": 3,
        "netflow_now": 500_000,
        "minutes_since_peak": 8,
        "kol_velocity": 20,
        "fee_sol_now": 150,
        "mc_now": 275_000,
        "top10_pct": 0.21,
        "bundle_pct": 0.18,
        "dca_flag": 1,
        "ath_flag": 0,
    }
    b = dict(a)
    b.update({"mc_change_pct": 240.0, "vol_now": 1_800_000, "kolusd_now": 1_200_000, "whale_buy_count": 25, "ath_flag": 1})
    s_new_a = score_new(a, sol_usd)
    s_new_b = score_new(b, sol_usd)
    assert s_new_b > s_new_a
    s_surg_a = score_surging(a, sol_usd)
    s_surg_b = score_surging(b, sol_usd)
    assert s_surg_b > s_surg_a
    s_all_a = score_all(a, sol_usd)
    s_all_b = score_all(b, sol_usd)
    assert s_all_b > s_all_a


