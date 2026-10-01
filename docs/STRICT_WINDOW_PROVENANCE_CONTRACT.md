# Strict partner-window provenance contract

Date: 2026-09-28  
Status: executable

## Purpose

A row cannot enter strict H1 merely because a paper reports plant timing, interaction intensity and final reproduction.

The plant timing contrast must be ordered by a partner-activity window whose provenance is compatible with the IWE synchrony estimand. This contract turns the partner-window rule into a machine-checked registry.

## Registry

Every current real `strict_window` effect must have exactly one row in:

`data/registry/strict_window_provenance.csv`.

Required fields include:

- `effect_id`;
- `study_id`;
- `window_basis`;
- `same_season`;
- `source_id`;
- `source_measurement`.

## Admissible bases

Current executable admissible values are:

- `direct_adult_census`;
- `trapping`;
- `direct_visitation`;
- `source_defined_visit_evidence`;
- `explicit_overlap_metric`;
- `experimental_partner_availability`.

A strict window must also be same-season.

These labels describe evidence provenance, not effect families.

## Forbidden realized-interaction substitutes

The validator explicitly rejects the following as strict partner-window bases:

- `egg_receipt`;
- `oviposition_success`;
- `attack`;
- `infestation`;
- `larval_occupancy`;
- `damage`;
- `seed_predation`.

Those quantities may be biologically informative mechanisms or responses, but they combine partner presence with host availability, partner choice and/or interaction success. They cannot be recycled as independent partner availability.

## Current strict provenance

After the 2026-09-28 antagonist re-audit, the current real strict corpus contains four effects:

- IWE029 — source-defined same-season oil-bee visit evidence;
- IWE027 HIS — direct same-season bumble-bee visitation/activity;
- IWE027 GOS — direct same-season bumble-bee visitation/activity;
- IWE023 — direct visitation during experimentally shifted flowering weeks.

IWE011 is not registered because its former strict effect was withdrawn: the published seasonal partner window is based on oviposition/egg observations.

IWE015 is not registered while its quantitative effect rows remain on raw-variance hold. Its future provenance is nevertheless fixed: Zhou et al. Figure 1 reports same-season 2012/2013 adult *H. ectypa* and co-pollinator moth density (moths per flower ×100), so any returning IWE015 row must use `window_basis = direct_adult_census`. The separate egg-density series is not an admissible basis. `build_iwe015_promotion_packet.py` transactionally enforces this when raw effects become ready.

## CI behavior

`scripts/validate_window_provenance.py` fails when:

- a current real strict-window effect lacks a provenance row;
- a provenance row points to a non-strict/non-current effect;
- the study ID does not match;
- the basis is forbidden or unknown;
- the partner window is not same-season.

The CI workflow runs this validator immediately after strict-H1 adjudication validation.

## Boundary

This registry does not by itself prove causal identification, adequate spatial replication or correct effect-size variance. It only closes one specific loophole: a strict synchrony effect cannot silently use egg receipt, attack or damage as though those were independent partner activity.

Within-effect sampling grain is handled separately by `STRICT_EFFECT_UNIT_PROVENANCE_CONTRACT.md` and `data/registry/strict_effect_unit_provenance.csv`. A valid partner window therefore does not automatically authorize a causal timing claim.
