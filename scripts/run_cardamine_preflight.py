#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from iwe.cardamine_pipeline import run_cardamine_preflight
from iwe.cardamine_onset_audit import audit_cardamine_onset_intervals


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run the frozen Cardamine-Anthocharis preflight pipeline from "
            "normalized timing, adult-event and plant-outcome tables."
        )
    )
    parser.add_argument("plant_timing_csv")
    parser.add_argument("adult_events_csv")
    parser.add_argument("adult_provenance_json")
    parser.add_argument("plant_summaries_csv")
    parser.add_argument("output_dir")
    args = parser.parse_args()

    plant_timing = pd.read_csv(Path(args.plant_timing_csv))
    adult_events = pd.read_csv(Path(args.adult_events_csv))
    adult_provenance = json.loads(
        Path(args.adult_provenance_json).read_text(encoding="utf-8")
    )
    plant_summaries = pd.read_csv(Path(args.plant_summaries_csv))

    exposure, audit, effects = run_cardamine_preflight(
        plant_timing,
        adult_events,
        adult_provenance,
        plant_summaries,
    )

    outdir = Path(args.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    exposure.to_csv(outdir / "timing_exposure.csv", index=False)
    onset_audit = audit_cardamine_onset_intervals(plant_timing, adult_events)
    onset_audit.to_csv(outdir / "onset_interval_audit.csv", index=False)
    audit.to_csv(outdir / "outcome_smd_audit.csv", index=False)
    effects.to_csv(outdir / "smd_effects.csv", index=False)

    eligible = int(audit["eligible_smd"].sum()) if not audit.empty else 0
    status = {
        "schema": "iwe_cardamine_preflight_v2",
        "candidate_id": "ANT002_CARDAMINE_ANTHOCHARIS_2024",
        "adult_timing_source_id": adult_provenance["source_id"],
        "adult_timing_source_backed": bool(adult_provenance["source_backed"]),
        "synthetic_fixture": bool(adult_provenance["synthetic_fixture"]),
        "timing_exposure_rows": int(len(exposure)),
        "onset_interval_audit_rows": int(len(onset_audit)),
        "source_identified_onset_groups": int(onset_audit["source_identified_group"].isin(
            ["early_refugium", "core_flight", "late_refugium"]
        ).sum()),
        "scenario_7day_boundary_sensitive_or_unresolved": int((
            ~onset_audit["observed_group_scenario_stable"]
        ).sum()),
        "assumed_survey_lag_is_source_verified": False,
        "onset_interval_audit_is_nonpromoting": True,
        "directional_contrasts_audited": int(len(audit)),
        "eligible_smd_contrasts": eligible,
        "smd_effect_rows": int(len(effects)),
        "promoted_to_primary_extraction": False,
    }
    (outdir / "preflight_status.json").write_text(
        json.dumps(status, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"Wrote Cardamine preflight outputs to {outdir}; "
        f"eligible directional contrasts={eligible}, SMD rows={len(effects)}. "
        "First observed flowering may be left-censored; onset_interval_audit.csv "
        "is a non-promoting observation-lag sensitivity. "
        "No row is promoted to the primary extraction table automatically."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
