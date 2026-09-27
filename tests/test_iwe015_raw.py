import math

import pandas as pd
import pytest

from iwe.iwe015_raw import (
    PUBLISHED_IWE015,
    audit_iwe015_group,
    bounded_dispersion_check,
    printed_dispersion_match,
)


def test_bounded_table_values_rule_out_literal_se_interpretation():
    check = bounded_dispersion_check(mean=0.91, printed_dispersion=0.19, n=59)
    assert check["printed_as_sd_possible"] is True
    assert check["printed_as_se_possible"] is False
    assert check["implied_sd_if_printed_is_se"] > 1


def test_printed_dispersion_classifier_distinguishes_sd_and_se():
    assert printed_dispersion_match(2.95, 2.95 / math.sqrt(59), 2.95) == "sd"
    assert printed_dispersion_match(2.95, 0.384, 0.384, tolerance=0.001) == "se"
    assert printed_dispersion_match(2.95, 0.384, 1.5, tolerance=0.001) == "neither"


def test_group_audit_promotes_raw_summary_not_source_label():
    pub = PUBLISHED_IWE015["2012_early"]
    # Construct values with exactly the published successful-fruit mean and
    # approximately the published SD. The test only needs the raw summary to be
    # internally valid; the source's printed label is not trusted.
    # 59 non-negative integer counts with sum=157 (mean=2.661 -> 2.66)
    # and sum of squares=923 (sample SD=2.951 -> 2.95).
    values = [6] * 22 + [5] * 5 + [0] * 32
    for left, right in ((0, 1), (2, 3), (4, 5)):
        values[left] -= 1
        values[right] += 1
    df = pd.DataFrame({"successful": values})

    row, components = audit_iwe015_group(
        df,
        "2012_early",
        successful_fruits_col="successful",
    )
    assert row["n_matches"] is True
    assert row["mean_matches"] is True
    assert row["raw_group_ready"] is True
    assert row["printed_dispersion_matches"] == "sd"
    assert components == []


def test_group_audit_can_crosscheck_bounded_components():
    n = 59
    # Alternating values create legal bounded distributions; the important
    # assertion is the distribution-free impossibility test for the printed SE.
    df = pd.DataFrame(
        {
            "successful": [2.66] * n,
            "initiation": [1.0] * 54 + [0.0] * 5,
            "predation": [1.0] * 35 + [0.0] * 24,
        }
    )
    # successful is constant here, so raw_group_ready is false; component audit
    # still independently establishes that the printed proportion dispersion
    # cannot be a literal SE.
    row, components = audit_iwe015_group(
        df,
        "2012_early",
        successful_fruits_col="successful",
        fruit_initiation_col="initiation",
        predation_rate_col="predation",
    )
    assert row["raw_group_ready"] is False
    by_component = {item["component"]: item for item in components}
    assert by_component["fruit_initiation"]["printed_as_se_possible"] is False
    assert by_component["predation_rate"]["printed_as_se_possible"] is False


def test_unknown_group_fails_closed():
    with pytest.raises(ValueError, match="unknown IWE015 group"):
        audit_iwe015_group(
            pd.DataFrame({"successful": [1.0, 2.0]}),
            "2014_early",
            successful_fruits_col="successful",
        )


def test_invalid_raw_bounds_fail_closed():
    with pytest.raises(ValueError, match="non-negative"):
        audit_iwe015_group(
            pd.DataFrame({"successful": [1.0, -1.0] + [0.0] * 57}),
            "2012_early",
            successful_fruits_col="successful",
        )

    with pytest.raises(ValueError, match="must lie in"):
        audit_iwe015_group(
            pd.DataFrame(
                {
                    "successful": [2.66] * 59,
                    "initiation": [1.2] + [0.9] * 58,
                }
            ),
            "2012_early",
            successful_fruits_col="successful",
            fruit_initiation_col="initiation",
        )
