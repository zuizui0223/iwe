"""Bounded source-only original-data inventory for an independent limiting-stage test.

Höfer et al. 2022: reduced seed set under water deficit is driven mainly by
reduced flower numbers rather than altered flower visitation/pollination.
Open original Zenodo dataset record 7335086.

Question to gate, NOT already an estimated IWE effect:
Can early plant water/resource state, date-dependent flowering, actual visitor
observations and terminal seed output be linked on the *same plants and years*?
If no, stop this route; never approximate plant time from means or a figure.

This script inspects original CSV and README schemas, reports source checksum,
column names, numeric/nonmissing support, and source ID candidate values.
It NEVER infers biological effects from first rows and never promotes H1.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from collections import Counter
from io import StringIO
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

RECORD = "7335086"
DOI = "10.5281/zenodo.7335086"
PINNED = {
    "Int_data.csv": "d67c32cc5aa357fe6e6d952a801ea38f",
    "Plantlist.csv": "630eb7d3d7c871f65c2bd62890e1597c",
    "Floral_traits.csv": "24f1f01435fa22faa832c415bbd0b77e",
    "README.md": "68bf11faaa9786fbb39f9e32006b336d",
    "Soil_humi_temp.csv": "a44fe8f90b318af4569fac7c0d18440c",
}
MAX_BYTES = 300_000
VARIABLE_KEYS = (
    "plant", "id", "plot", "rep", "treat", "water", "date", "day",
    "flower", "visit", "pollin", "seed", "fruit", "stem",
    "buds", "time", "year", "rain", "soil", "moist", "humi",
)


def exact_url(name: str) -> str:
    if name not in PINNED:
        raise ValueError("off-record source file")
    return ("https://zenodo.org/records/" + RECORD + "/files/"
            + quote(name, safe="") + "?download=1")


def get_original(name: str) -> bytes:
    raw_url = exact_url(name)
    with urlopen(Request(
        raw_url,
        headers={
            "User-Agent": "IWE-source-only-herbivore-limiting-stage-audit/1.0",
            "Accept": "text/csv,text/plain,*/*;q=0.1",
        },
    ), timeout=40) as response:
        raw = response.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise ValueError("unreasonably large source file")
    actual = hashlib.md5(raw).hexdigest()
    if actual != PINNED[name]:
        raise ValueError("frozen Zenodo original MD5 mismatch: " + name)
    return raw


def _reader(raw: bytes):
    # Never infer empty cells as measured zero. Preserve source delimiter
    # and file-native column labels as the author supplied them.
    text = raw.decode("utf-8-sig")
    first_line = text.splitlines()[0]
    delimiter = max((",", ";", "\t"), key=first_line.count)
    if not first_line.count(delimiter):
        raise ValueError("unresolved source CSV delimiter")
    reader = csv.DictReader(StringIO(text), delimiter=delimiter)
    if not reader.fieldnames:
        raise ValueError("no source header")
    fields = reader.fieldnames
    if len(fields) != len(set(fields)):
        raise ValueError("repeated field name in source")
    rows = list(reader)
    if any(None in row for row in rows):
        raise ValueError("extra source CSV cells")
    return fields, rows, delimiter


def inspect_original(name: str, raw: bytes):
    if name == "README.md":
        text = raw.decode("utf-8-sig")
        # Read only public source-defined variable descriptions, no model
        # results fabricated, and never claim a data join from README alone.
        lines = text.splitlines()
        leads = [
            {"line": i + 1, "short_text": line.strip()[:200]}
            for i, line in enumerate(lines)
            if any(k in line.lower() for k in VARIABLE_KEYS)
        ]
        return {
            "source_file": name, "bytes": len(raw), "md5": PINNED[name],
            "readme_lines": len(lines),
            "likely_unit_or_endpoint_definitions": leads[:50],
            "outcome_join_verified": False,
        }
    fields, rows, delimiter = _reader(raw)
    hints = [
        f for f in fields if
        any(k in f.lower() for k in VARIABLE_KEYS)
    ]
    # Inspection here is schema-only: 3 source examples reveal data formats
    # but are NOT reported as independent biological effect estimates.
    preview = [{field: (str(row.get(field, ""))[:40])
                for field in fields[:18]}
               for row in rows[:2]]
    missing = {
        field: sum(
            row.get(field) is None or
            str(row.get(field, "")).strip().lower() in ("", "na", "nan")
            for row in rows
        )
        for field in fields
    }
    literal_var_counts = {}
    for field in hints[:30]:
        values = [str(row.get(field, "")).strip()
                  for row in rows]
        literal_var_counts[field] = {
            "n_values": len(set(values)),
            "first_literal_values": list(dict.fromkeys(values))[:9],
        }
    return {
        "source_file": name,
        "bytes": len(raw),
        "md5": PINNED[name],
        "n_original_rows": len(rows),
        "headers": fields,
        "delimiter": repr(delimiter),
        "timing_id_endpoint_header_candidates": hints,
        "missing_by_header": missing,
        "source_value_shapes": literal_var_counts,
        "first_two_rows_format_only": preview,
        "one_plant_multi_stage_join_verified": False,
        "interaction_time_predictive_effect_estimated": False,
    }


def audit():
    result = {
        "schema": "iwe_hofer2022_original_data_gate_v1",
        "source_doi": DOI,
        "biological_goal":
            "preoutcome water/flower/visitor timing vs terminal seed set",
        "strict_h1_admitted": False,
        "source_data_verified": False,
        "source_file_inventory": [],
        "stage_fitness_effect_estimated": False,
    }
    try:
        original = []
        for name in PINNED:
            raw = get_original(name)
            original.append(inspect_original(name, raw))
        result["source_file_inventory"] = original
        result["source_data_verified"] = True
        result["status"] = "source_schemas_recovered_not_yet_joined"
    except (OSError, TimeoutError, ValueError, UnicodeError, TypeError) as e:
        result["status"] = "original_source_unavailable_or_changed"
        result["source_error"] = type(e).__name__ + ": " + str(e)[:180]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    report = audit()
    (args.outdir / "verified_source_inventory.json").write_text(
        json.dumps(report, indent=2) + "\n", encoding="utf-8"
    )
    print("HOFER_GATE", report["status"], report.get("source_error", ""))
    for row in report["source_file_inventory"]:
        print("HOFER_FILE", row["source_file"],
              "ROWS", row.get("n_original_rows"),
              "COLS", row.get("headers"),
              "SOURCE_VARIABLES", row.get("source_value_shapes"),
              "PREVIEW", row.get("first_two_rows_format_only"))
        if "likely_unit_or_endpoint_definitions" in row:
            print("HOFER_README", json.dumps(
                row["likely_unit_or_endpoint_definitions"][:28]
            ))
    print("Not a source-linked flowering/visit/seed effect until exact IDs pass")
    return 0 if report["source_data_verified"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
