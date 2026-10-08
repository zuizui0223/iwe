#!/usr/bin/env python3
"""Descriptive, source-conditional contrasts of published Berberis fruit states.

NOT a timing effect, an enemy-caused abortion estimate, or plant fitness.
Fruit state F2/f1 is source 'nonaborted', which includes eaten seed coats.
Fruits were sampled in situ after survival; missing whole fruits have no data.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

SOURCE = Path("data/source_reconstructions/meyer2014_berberis_published_fruit_states.csv")
OUTPUT = Path("data/derived/meyer2014_conditional_abortion_contrasts.csv")
HABITATS = ("pine", "dry_scrub")
LABELS = {
    1: "single_seed_aborted",
    2: "exactly_one_of_two_seeds_aborted",
}
HEADER = (
    "habitat", "seeds_per_retained_fruit", "abortion_state",
    "n_without_puncture", "n_with_puncture",
    "p_without_puncture", "p_with_puncture",
    "descriptive_risk_difference_with_minus_without",
    "nonaborted_seeds_per_retained_fruit_upper_bound_without",
    "nonaborted_seeds_per_retained_fruit_upper_bound_with",
    "nonaborted_upper_bound_difference_with_minus_without",
    "source_inference_limit",
)


def generate(source: Path = SOURCE) -> str:
    with source.open(newline="", encoding="utf-8") as file:
        original = list(csv.DictReader(file))
    keyed = {(r["habitat"], int(r["seeds_per_fruit"]),
              r["oviposition_puncture"]): r for r in original}
    expected = {(habitat, seeds, state)
                for habitat in HABITATS
                for seeds in (1, 2)
                for state in ("absent", "present")}
    if len(original) != 8 or set(keyed) != expected:
        raise ValueError("not the four source strata crossed with fruit structure")
    if any(r["study_id"] != "MEYER2014_BERBERIS" for r in original):
        raise ValueError("unexpected source provenance")

    def count(r: dict[str, str], field: str) -> int:
        value = r[field]
        if not value or not value.isdigit():
            raise ValueError(f"missing/invalid count in original source: {field}")
        return int(value)

    def metrics(r: dict[str, str], seeds: int) -> tuple[int, float, float]:
        n = count(r, "fruits_n")
        if n <= 0:
            raise ValueError("no sampled fruit units")
        if seeds == 1:
            a = count(r, "f0_single_aborted")
            retained = count(r, "f1_single_not_aborted")
            if a + retained != n:
                raise ValueError("one-seeded state frequencies do not sum to N")
            return n, a/n, retained/n
        f0 = count(r, "F0_two_aborted")
        f1 = count(r, "F1_one_aborted")
        f2 = count(r, "F2_zero_aborted")
        if f0 + f1 + f2 != n:
            raise ValueError("two-seeded state frequencies do not sum to N")
        return n, f1/n, (f1+2*f2)/n

    out_rows: list[list[str]] = []
    for habitat in HABITATS:
        for seeds in (1, 2):
            without = keyed[(habitat, seeds, "absent")]
            with_ = keyed[(habitat, seeds, "present")]
            n0, p0, upper0 = metrics(without, seeds)
            n1, p1, upper1 = metrics(with_, seeds)
            out_rows.append([
                habitat, str(seeds), LABELS[seeds], str(n0), str(n1),
                f"{p0:.6f}", f"{p1:.6f}", f"{(p1-p0):.6f}",
                f"{upper0:.6f}", f"{upper1:.6f}", f"{(upper1-upper0):.6f}",
                "observed_fruit_state_only_not_intact_seed_or_plant_fitness",
            ])
    import io
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(HEADER)
    writer.writerows(out_rows)
    return buffer.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = generate()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != result:
            print(f"ERROR: conditional source fruit-state derivation is stale: {OUTPUT}")
            return 1
        print("OK: published Berberis fruit-state descriptive contrasts are source-exact.")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(result, encoding="utf-8")
    print(f"Wrote {OUTPUT}; observational state contrasts only, not fitness.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
