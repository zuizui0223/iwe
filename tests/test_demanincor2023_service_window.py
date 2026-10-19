"""Deterministic software fixtures; source SHA/MD5 and real ecological results are verified by live workflow."""
import math
import pytest
from scripts.analyze_demanincor2023_service_window import (
    PINNED_MD5, SOURCE_ROWS, ARENAS, source_rows, read_original,
    build_plants, evaluate, design, fit_ols, predict_row,
    phase_shift_sensitivity, MODELS,
)


def fixture():
    d = {name: [] for name in PINNED_MD5}
    for c in ARENAS:
        trt = c[0]
        num = c[1:]
        label = "ambient" if trt == "C" else "warmed"
        for sp in ("CH", "NM", "PC"):
            raw_id = "17"
            key = c + "_" + sp + "_17"
            # Actual seeds.txt: Cage TRTMT Species ID Date Sampling DOY
            # Fruits Seeds Ovules Seed_set Weight_tot Weight_seed.
            seed_count = 4 if sp == "CH" else 7
            d["seeds.txt"].append([
                c, trt, sp, raw_id, "20-May", "1", "140",
                "1", str(seed_count), "3", "0.5", "NA", "NA",
            ])
            d["seedset_flowervisit.txt"].append([
                key, trt, c, sp, raw_id, "0.3", str(seed_count), "3",
            ])
            d["flower_onset.txt"].append([
                trt, num, sp, raw_id, "106", "1"
            ])
            d["flower_count.txt"].extend([
                [c, label, sp, raw_id, "89", "106", "1", "109", "2"],
                [c, label, sp, raw_id, "89", "106", "1", "110", "1"],
            ])
        d["bee_density.txt"].extend([
            ["4/19/2021", "109", trt, num, "4"],
            ["4/20/2021", "110", trt, num, "2"],
        ])
    return d


def test_source_summary_header_is_not_silently_shifted():
    true_header = (
        "sp_id trtm cage plant sp ID visrates seeds ovules\n"
    )
    source = (true_header + ("C1_CH_13 C C1 CH 13 0.2 17 3\n" * 234))
    rows = source_rows(source.encode(), "seedset_flowervisit.txt")
    assert len(rows) == 234
    assert len(rows[0]) == 8
    with pytest.raises(ValueError, match="header"):
        source_rows(
            source.replace("plant sp", "plant species").encode(),
            "seedset_flowervisit.txt",
        )
    with pytest.raises(ValueError, match="row width"):
        source_rows(
            (true_header + "C1_CH_13 C C1 CH 13 0.2 17\n" * 234).encode(),
            "seedset_flowervisit.txt",
        )


def test_same_plant_original_stage_and_seedset_join():
    d = fixture()
    plants, exclusions = build_plants(d)
    assert len(plants) == 24
    assert exclusions == {}
    one = next(x for x in plants if x["source_id"] == "C1_CH_17")
    assert one["seed_set"] == pytest.approx(4 / 7)
    assert one["onset"] == 106
    assert one["adultMean"] == pytest.approx(3.0)
    assert one["flowerBeeOverlap"] == pytest.approx(10 / 3)
    assert one["beeCoverage"] == 1.0
    assert one["matchedBloomDOY"] == pytest.approx((2*109+110)/3)
    assert one["overallBloomDOY"] == pytest.approx((2*109+110)/3)
    assert {x["arena"] for x in plants} == set(ARENAS)
    assert len(set(x["source_id"] for x in plants)) == len(plants)


def test_source_disagreement_is_excluded_not_imputed_or_reassigned():
    d = fixture()
    d["seedset_flowervisit.txt"][0][6] = "5"  # changed sum, raw says 4
    with pytest.raises(ValueError, match="not all randomized arenas"):
        # This one removed row is not enough to empty arena because fixture
        # has 3 plant species: append source loss for remaining two too.
        for i in (1, 2):
            d["seedset_flowervisit.txt"][i][6] = "5"
        build_plants(d)
    d = fixture()
    d["seeds.txt"][0][9] = "NA"
    plants, exclusions = build_plants(d)
    assert len(plants) == 23
    assert exclusions["raw_vs_summary_disagreement"] == 1


def test_model_training_standardization_does_not_include_heldout_plant():
    d = fixture()
    plants, _ = build_plants(d)
    train = [x for x in plants if x["arena"] != "C1"]
    test = [x for x in plants if x["arena"] == "C1"]
    model = ("treatment", "species", "logFlowers", "onset", "flowerBeeOverlap")
    X, T = design(train, test, model)
    assert len(X) == 21
    assert len(T) == 3
    beta = fit_ols(X, [x["seed_set"] for x in train])
    assert len(beta) == len(X[0]) == len(T[0])
    assert 0 <= predict_row(T[0], beta) <= 1
    scores = evaluate(plants)
    assert "M6_matched_day_calendar" in scores
    assert "M9_calendar_coverage" in scores
    assert "M10_calendar_coverage_overlap" in scores
    for value in scores.values():
        assert value["n_plants"] == 24
        assert value["n_arenas"] == 8
        assert set(value["per_arena_mse"]) == set(ARENAS)
        assert math.isfinite(value["equal_arena_rmse"])
        assert math.isfinite(value["plant_rmse"])


def test_off_source_bytes_fail_md5_before_decoding(monkeypatch):
    import scripts.analyze_demanincor2023_service_window as script
    class FakeConnection:
        def __enter__(self): return self
        def __exit__(self, *_): return None
        def read(self, *_): return b"not the original biological source"
    monkeypatch.setattr(script, "urlopen", lambda *a, **k: FakeConnection())
    with pytest.raises(ValueError, match="source checksum mismatch"):
        read_original("seeds.txt")
    with pytest.raises(ValueError, match="not in frozen"):
        read_original("unregistered_raw_binary_file")


def test_original_tsv_empty_ovule_is_missing_not_shifted_or_zero():
    header = (
        "Cage\tTRTMT\tSpecies\tID\tDate\tSampling\tDOY\tFruits\t"
        "Seeds\tOvules\tSeed_set\tWeight_tot\tWeight_seed\n"
    )
    regular = (
        "C1\tC\tCH\t13\t14-June\t3\t165\t1\t17\t3\t0.85\t"
        "0.0016\t0.000114286\n"
    )
    # Missing ovules, but Seed_set and both weights are present:
    broken = (
        "C2\tC\tPC\t114\t3-June\t2\t154\t4\t197\t\t1\t"
        "0.1053\t0.000534518\n"
    )
    raw = (header + regular + broken * 599).encode()
    rows = source_rows(raw, "seeds.txt")
    assert len(rows) == 600
    assert len(rows[1]) == 13
    assert rows[1][8] == "197"
    assert rows[1][9] == "NA"  # missing exact fruit ovule count
    assert rows[1][10] == "1"  # author's recorded seed-set field
    assert rows[1][11] == "0.1053"  # author seed mass; not ovules
    assert rows[1][12] == "0.000534518"
    assert rows[0][9] == "3"
    assert rows[0][10] == "0.85"


def test_cyclic_shift_falsifier_preserves_source_calendar_and_zero_reference():
    d = fixture()
    plants, _ = build_plants(d)
    report = phase_shift_sensitivity(d, plants)
    assert report["n_original_census_days_per_arena"] == 2
    assert report["same_shift_used_for_all_arenas"] is True
    assert len(report["per_shift_diagnostics"]) == 2
    assert report["per_shift_diagnostics"][0]["calendar_cyclic_shift"] == 0
    direct = evaluate(plants, specs={
        "M3_flower_bee_overlap": MODELS["M3_flower_bee_overlap"]
    })["M3_flower_bee_overlap"]["equal_arena_rmse"]
    assert report["original_zero_shift_equal_arena_rmse_M3"] == pytest.approx(
        direct
    )
    assert 1 <= report["n_phase_shifts_better_or_equal_M3"] <= 2
    assert math.isfinite(report["median_shifted_M10"])


def test_shifting_bee_phase_requires_common_observation_day_support():
    d = fixture()
    plants, _ = build_plants(d)
    # Break all bee exposure dates for one arena.
    d["bee_density.txt"][0][1] = "999"
    d["bee_density.txt"][1][1] = "998"
    with pytest.raises(ValueError, match="missing original flower/bloom link"):
        phase_shift_sensitivity(d, plants)
