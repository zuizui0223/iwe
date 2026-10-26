# 2026 Physalis experiment: antagonist response × taxon-specific pollinator service

**Date:** 2026-10-26. **Source stage:** separate original-data candidacy audit; NOT a quantitative IWE H1 effect and NOT a new stage-conversion conclusion.

Original published source: Davis, Cintron, Cohen, Tolz & Thaler (2026), *Oikos*, [DOI 10.1002/oik.11650](https://doi.org/10.1002/oik.11650). Public Dryad dataset [10.5061/dryad.xpnvx0kvp](https://doi.org/10.5061/dryad.xpnvx0kvp), published 2026-02-03.

## Why this programme is biologically distinct

On tomatillo (*Physalis philadelphica*), the source manipulates *Lema daturaphila* beetle herbivory and jasmonic-acid elicitation separately from control, then observes multiple bee taxa and actual fruit response. The paper reports taxon-dependent pollinator effectiveness: e.g. responses of specialist *Colletes latitarsis* differ from generalists including *Apis*, *Bombus*, Augochlorini and *Lasioglossum*. This is independent of IWE's greenhouse *Osmia* study and its shared plant/bee taxa.

Its central ecological contribution to IWE might be **interaction-role filtering**: whether an antagonist changes the fruit-forming value of an individual mutualist visitation event, over and above the date, host reproductive state and pollinator identity. It may distinguish **partner choice versus per-visit effectiveness**, an alternative to explaining changed reproduction using flowering synchrony alone.

Crucially, the study is NOT a pollinating seed predator or a within-lineage adult–larva mixed interaction. Induced herbivory and bee service involve distinct animals. An interaction between herbivory and bee taxon would not add a strict IWE antagonist synchrony SMD.

## Original Dryad files and possible biological joins

The original article's source description identifies eight experiment CSVs, but the **authoritative Dryad published-version file inventory contains 10 files**: those eight experiment CSVs, an additional `Oikos_2021_seeds_fruit_sugar.csv`, and `README.md`. The extra seed/fruit/sugar file is a potential reproductive-quality endpoint, but its raw columns and biological join keys have **not** been inspected.

- 2021: `Oikos_2021_fruit_set_poll_obs.csv` — **single visit** fruit set outcome (0/1), treatment, bee morphospecies, date (`julian_date`), sampled `plant_id`, spatial `block`, visit duration and floral anther state.
- 2021: `Oikos_2021_fruit_weight_poll_obs.csv` — harvested fruit weight (g), treatment, pollinator, `plant_id` and spatial `block`, `days_to_harvest`, foraging covariates.
- 2021: `Oikos_2021_nectar_pollen_foraging.csv` and `Oikos_2021_poll_importance.csv` — foraging and author-derived ecological importance, which must not be relabelled independently observed fruit endpoints.
- 2020: `Oikos_2020_bee_behavior_observations.csv`, `Oikos_2020_cross_season_abundance.csv`, `Oikos_2020_focal_taxa_abundance.csv`, and `Oikos_2020_total_plant_yield.csv`. **Do not join 2020 sources to 2021 flower fruit by `plant_id` alone**; IDs, treatments, experimental replicates and years may differ.

The official public README says rows can lack floral foraging behavior, visit duration, or dehisced-anther states due to observation gaps. Missing values must remain missing, not be filled with zero.

Even with complete source bytes, **`plant_id` by itself is not necessarily a unique flower visit or mature fruit**. Before building a fruit-weight-to-fruit-set or date-to-fruit-outcome model, inspect the original exact visit/flower/fruit identifiers. A many-to-many join by plant and treatment would duplicate fruit responses and fabricate downstream transmission. More than one flower might occur on the same plant on the same day.

## Prospective ecological test if original source is admissible

Pre-define the response as original source **fruit set per documented single visit**, with original experiment blocks held out, original plant ID nested correctly, and date measured at the actual flower visit (not whole-plant first bloom). Compare a null context, visit date, bee morphospecies, herbivory-versus-JA-versus-control, and date × bee identity × herbivory effects, with an outcome-blind training/validation design. Repeated visit observations on one plant, block or flower must be clustered, not counted as independently treated plants.

Then compare the original fruit-weight endpoint only where a source-validated unique visit→fruit key exists, and use 2020 plant yield data only as a **different programme-year stage**, not a 2021 descendant. Published contrasts alone cannot establish a time-dependent conditional filtering effect.

The true physical treatment randomization unit (field plant versus block) and actual date-specific adult bee abundance must be source-verified. The 2021 per-visit observations are realized interactions, **not unconditional bee availability on absent-visit days**, so this programme can test service-context response but might remain below the strict timing H1 and phase-alignment claims.

## Verified Dryad source-access receipt (2026-10-26)

**Machine-executed source gate succeeded, but original data retrieval did not.** The official Dryad REST dataset metadata and **version-issued manifest of 10 author-deposited files** were retrieved and verified structurally. Exact official file routes were attempted for *each* of the 10 filenames without author contact or guessed third-party access:
- **10/10 REST file downloads returned HTTP 401**.
- **10/10 public file-stream downloads returned HTTP 403**.
- **0/10 original CSV/README file bodies recovered**. Consequently **zero source rows, IDs, observed visits, final fruit weights or seed-quality outcomes were inspected or estimated**.
- The extra `Oikos_2021_seeds_fruit_sugar.csv` is visible by its filename in the official manifest only. Its actual contents cannot establish a novel seed-quality result, a tagged fruit-to-seed identity join or a later developmental stage.
- This is a source-access **environment/authorization blocker**, *not* evidence that source observations are missing, that plant seed output is zero, or that the ecology has no signal.

GitHub reproducibility receipts: [original-source run 40280511313](https://github.com/zuizui0223/iwe/actions/runs/40280511313) (six software tests passed; manifest verified; 10 blocked downloads recorded) and [full repo CI 40280511322](https://github.com/zuizui0223/iwe/actions/runs/40280511322) (passed). The source probe's success means **receipt produced**, not an admitted biological effect. Source binary routes had already been tested twice per file; do not invent alternate endpoints, try arbitrary retries, or infer a fit from filename/title.

**Admission decision: `blocked_original_raw_bytes`.** Retain this independently described antagonist-induced service-filtering programme as a candidate, but it contributes **zero additional independent source-quantified reproductive effects, zero stage-complete forecasts and zero strict H1 clusters**. Reopen only if an independently lawful original-data copy becomes available with uniquely keyed flower/date/fruit endpoints and credible experimental replication.

## Current finite original-source retrieval

The executable `scripts/probe_davis2026_physalis_dryad.py` first reads published Dryad REST metadata and only the exact version-issued original file IDs. It tries both permitted official download routes for each file, verifies source SHA-256 when metadata supplies it and inventories original headers and candidate primary keys only if source bytes are actually obtained. This is an auditable, **one-time, no-author-contact** read-only access check.

If original files return HTTP 401/403, treat the source as a *publicly described biological candidate*, not recovered row-level evidence. Mark source access blocked; **do not** fabricate observation dates, source effects or taxon × herbivory coefficients from the README. It is acceptable for the workflow to succeed when the source-access audit executed and accurately recorded such a block; this does not mean scientific estimation succeeded.

No changes to frozen strict H1 (mutualist two independent clusters, antagonist zero, mixed zero). No new numerical fitness effect is currently admitted.
