"""Independent original-author Li 2026 light-array seed-count source audit.

Original data are fetched transiently; only independently field-blocked,
aggregate reproductive responses are written to artifacts. No insects,
pollen, seed viability, island treatment or direct mechanism were measured.
"""
from __future__ import annotations

import csv
import hashlib
import io
import math
import urllib.request
from collections import Counter

SOURCE_URL = (
    "https://raw.githubusercontent.com/Dongboli/experimental-data/main/"
    "Artificial%20lights%20at%20night/seedset.csv"
)
ORIGINAL_GIT_BLOB_SHA1 = "b616aca5beeba1457549841477d61ca4f796a147"
SOURCE_DOI = "10.64898/2026.07.10.737511"
FIELDS = {"round", "Treatment", "replicate", "species", "pollinated",
          "Seeds", "Fruit", "Label", "id"}
TREATMENTS = ("C", "P", "L")
SPECIES = ("ML", "SN", "ZC")


def fetch_original_author_bytes() -> bytes:
    request = urllib.request.Request(
        SOURCE_URL, headers={"User-Agent": "IWE-source-audited-field-contrast/0.1"},
    )
    with urllib.request.urlopen(request, timeout=50) as response:
        payload = response.read(100_001)
    if not 1000 <= len(payload) <= 100_000:
        raise ValueError("Li author original response size outside audited range")
    return payload


def _rows(raw: bytes) -> list[dict[str, str]]:
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeError as exc:
        raise ValueError("Invalid source encoding") from exc
    reader = csv.DictReader(io.StringIO(text))
    if not FIELDS <= set(reader.fieldnames or []):
        raise ValueError("Li source lacks required original columns")
    rows = list(reader)
    for r in rows:
        if r["Treatment"] not in TREATMENTS or r["species"] not in SPECIES:
            raise ValueError("Unknown treatment or species label in Li source")
        if r["round"] not in ("1", "2", "3") or r["replicate"] not in ("1", "2", "3"):
            raise ValueError("Unknown original field/round")
        if r["pollinated"] not in ("0", "1", "NA"):
            raise ValueError("Original pollinated flag must be binary or NA")
        for f in ("Seeds", "Fruit"):
            if r[f] != "NA":
                if not r[f].isdigit() or int(r[f]) < 0:
                    raise ValueError("Original seed/fruit count invalid")
        if r["pollinated"] != "NA":
            if r["Seeds"] == "NA":
                raise ValueError("Binary seed presence provided without original seed count")
            if int(r["pollinated"]) != int(int(r["Seeds"]) > 0):
                raise ValueError("Original binary pollinated is not actual pollen: Seeds > 0 rule failed")
        elif r["Seeds"] != "NA":
            raise ValueError("Unknown original seed-presence cannot have known seed count")
    return rows


def _arm(rows: list[dict[str, str]]) -> dict:
    good = [r for r in rows if r["pollinated"] != "NA"]
    count = len(good)
    if count == 0:
        raise ValueError("Empty Li arm after original unknown outcomes")
    successes = sum(int(r["pollinated"]) for r in good)
    return {
        "source_record_rows_including_unknown": len(rows),
        "seed_outcome_known_plant_rows": count,
        "seed_present_plant_rows": successes,
        "seed_presence_fraction": successes / count,
        "actual_seed_count_from_known_plants": sum(int(r["Seeds"]) for r in good),
        "actual_fruit_count_from_known_plants": sum(int(r["Fruit"]) for r in good),
    }


def audit_li_original(
    raw: bytes, *, original_source_verified: bool = True,
) -> tuple[list[dict], list[dict], list[dict], dict]:
    header = f"blob {len(raw)}\0".encode()
    sha1 = hashlib.sha1(header + raw).hexdigest()
    if original_source_verified and sha1 != ORIGINAL_GIT_BLOB_SHA1:
        raise ValueError(f"Li published original Git blob source changed: {sha1}")
    rows = _rows(raw)
    if original_source_verified and len(rows) != 79:
        raise ValueError("Expected 79 original Li field plant rows")
    arms = []
    for treatment in TREATMENTS:
        x = _arm([r for r in rows if r["Treatment"] == treatment])
        arms.append({"treatment": treatment, **x})
    arms_by_name = {r["treatment"]: r for r in arms}
    fields = []
    for field in (1, 2, 3):
        x = [r for r in rows if r["replicate"] == str(field)]
        c = _arm([r for r in x if r["Treatment"] == "C"])
        l = _arm([r for r in x if r["Treatment"] == "L"])
        point = _arm([r for r in x if r["Treatment"] == "P"])
        fields.append({
            "original_hayfield": field,
            "control_seed_present": c["seed_present_plant_rows"],
            "control_seed_known": c["seed_outcome_known_plant_rows"],
            "linear_array_seed_present": l["seed_present_plant_rows"],
            "linear_array_seed_known": l["seed_outcome_known_plant_rows"],
            "point_seed_present": point["seed_present_plant_rows"],
            "point_seed_known": point["seed_outcome_known_plant_rows"],
            "array_minus_control_seed_presence_risk_difference": (
                l["seed_presence_fraction"] - c["seed_presence_fraction"]
            ),
            "point_minus_control_seed_presence_risk_difference": (
                point["seed_presence_fraction"] - c["seed_presence_fraction"]
            ),
        })
    groups = []
    for species in SPECIES:
        for treatment in ("C", "L"):
            sub = [r for r in rows if
                   r["species"] == species and r["Treatment"] == treatment]
            x = _arm(sub)
            groups.append({"source_species": species, "treatment": treatment, **x})
    errors = len(rows) - sum(r["seed_outcome_known_plant_rows"] for r in arms)
    original_expected = {
        "C": (26, 8, 672, 32),
        "P": (25, 12, 967, 33),
        "L": (27, 20, 3729, 149),
    }
    if original_source_verified:
        for treatment, expected in original_expected.items():
            r = arms_by_name[treatment]
            actual = (
                r["seed_outcome_known_plant_rows"], r["seed_present_plant_rows"],
                r["actual_seed_count_from_known_plants"],
                r["actual_fruit_count_from_known_plants"],
            )
            if actual != expected:
                raise ValueError(f"Original Li source arm drift: {treatment}")
        if errors != 1:
            raise ValueError("Expected exactly one originally missing point light seed outcome")
        if ([(x["control_seed_present"], x["control_seed_known"],
              x["linear_array_seed_present"], x["linear_array_seed_known"])
             for x in fields]) != [(1, 6, 4, 8), (3, 11, 7, 9), (4, 9, 9, 10)]:
            raise ValueError("Original Li source 3-hayfield counts drift")

    baseline = arms_by_name["C"]["seed_presence_fraction"]
    array = arms_by_name["L"]["seed_presence_fraction"]
    point = arms_by_name["P"]["seed_presence_fraction"]
    field_changes = [r["array_minus_control_seed_presence_risk_difference"]
                     for r in fields]
    positive = sum(x > 0 for x in field_changes)
    negative = sum(x < 0 for x in field_changes)
    n_signed = positive + negative
    # NOT a valid original randomization-based p: midseason lamps moved
    # and the original treatment assignment sequence is not recovered.
    illustrative_sign_fraction = (
        2 * sum(math.comb(n_signed, i)
                for i in range(min(positive, negative) + 1)) / (2 ** n_signed)
        if n_signed else None
    )
    receipt = {
        "schema": "iwe_alan_li2026_genuine_seed_source_v0.1",
        "original_source_git_blob_sha1": sha1,
        "original_source_sha256": hashlib.sha256(raw).hexdigest(),
        "source_doi": SOURCE_DOI,
        "source_verified_original_git_blob": original_source_verified,
        "source_original_rows": len(rows),
        "seed_outcome_known_plant_rows": len(rows) - errors,
        "unknown_seed_outcome_plant_rows": errors,
        "observed_total_seed_count": sum(
            x["actual_seed_count_from_known_plants"] for x in arms
        ),
        "observed_total_fruits_count": sum(
            x["actual_fruit_count_from_known_plants"] for x in arms
        ),
        "original_field_blocks": 3,
        "source_plant_species_count": len(SPECIES),
        "linear_array_minus_control_pooled_plant_risk_difference": array - baseline,
        "point_minus_control_pooled_plant_risk_difference": point - baseline,
        "linear_array_minus_control_equal_field_mean_risk_difference": (
            sum(field_changes) / len(field_changes)
        ),
        "field_signs_positive": positive,
        "field_signs_negative": negative,
        "two_sided_sign_fraction_descriptive_NOT_randomization_p": illustrative_sign_fraction,
        "source_pollinated_column_is_actual_conspecific_pollen": False,
        "observer_visitation_ever_measured_in_author_csv": False,
        "bulb_number_independent_of_array_geometry_manipulated": False,
        "individually_randomized_field_replications": False,
        "source_plant_labels_proven_distinct": False,
        "mature_seed_viability_measured": False,
        "genuine_original_study": True,
        "inference_level": "source_verified_directional_reproductive_contrast_not_moth_mechanism",
        "strict_iwe_h1_effects_created": 0,
    }
    return arms, fields, groups, receipt
