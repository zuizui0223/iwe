# IWE015 public Dryad source recovery (non-promoting)

Date: 2026-10-08. The primary publisher's Table 1 confirms the four
2012–2013 female cohorts, but the public Dryad source files have yielded HTTP
403 in the local web execution environment, while this container cannot
resolve the datadryad.org domain. This is **not** a data-access restriction
inferred for all environments and does not license imputation.

The public Dryad landing page:
https://datadryad.org/dataset/doi:10.5061/dryad.6q573n5w1

## Independent network probe

The repository now includes a narrowly bounded network probe intended to run
on a *separate GitHub-hosted runner*:

`python scripts/recover_iwe015_dryad.py --output-dir /tmp/iwe015-dryad --strict`

It attempts only six pinned, named files from Dryad: four female cohort CSVs,
`data_analysis.R`, and `README.txt`. It tries the published direct download
and API file download URLs, then verifies that the payload is plausible text
rather than an HTML denial or empty/error response.

Outputs are an explicit `manifest.json` with status
`complete`/`blocked`, file SHA256s, source URLs, CSV column names and row
counts; successful raw bytes are placed under `source_files/`. The result is
a *source-access diagnostic*, not a biological result. The workflow
`.github/workflows/iwe015-dryad-probe.yml` runs on changes to the probe and
can be manually dispatched. It uploads any obtained files in a temporary
seven-day GitHub Actions artifact and leaves the code/data registry alone.

## Conditions for real source reanalysis

A complete download is only **step one**.

1. Inspect the provided `README.txt` and `data_analysis.R` to discover
   actual columns and source-defined exclusions rather than mapping
   successful fruits by a guessed label.
2. Reproduce the Table 1 plant counts (59,58,55,55), means
   (2.66,3.91,9.77,8.60), and the correct column-wise dispersion using
   `scripts/audit_iwe015_raw_variance.py`; separately reconcile the
   reported ANOVA degrees of freedom with the 227 Table 1 adult plants.
3. **Resolve the source-unit discrepancy:** the *Oviposition and flower
   fate* methods describe 280/239/294/281 one-week tagged/measured flowers;
   the *Female fitness components* methods refer to all labelled RUs.
   But 2013 Table 1 mean successful fruits per plant (9.77 early, 8.60 late)
   exceed the respective measured flowers per plant (294/55=5.35 and
   281/55=5.11). Do not assume without evidence that the source flower
   totals are a trait-only subset. Audit exact plant/flower identifiers,
   timing coverage, total reproductive-unit denominator and any joins.
4. At the **plant level**, separate observed initiated and intact fruits,
   larval fruit predation, flowers/pistils missing completely after attack,
   and flower-display opportunity. An entirely eaten pistil has
   unknown initial fruit status.
5. Preserve the 2012 and 2013 contrasts as two correlated outcomes of
   **one** Silene–Hadena programme. Test a year-by-period difference only
   with appropriate model/resampling and its assumptions exposed.
6. Preserve separate reproductive channels: successful fruit counts are
   female reproductive fitness **proxy**, while male fitness requires the
   source paternity-assignment component; egg–female correlations do
   not identify net pollination service.

## Stop rule

The download probe never computes Hedges g, changes any registry,
relabels `SE` as `SD`, or promotes IWE015 into strict H1. A 403 or
partial download is recorded as `blocked` rather than a false success.
Even a complete download requires manual confirmation of source analysis
and linked biological unit definitions.

Primary source: Zhou et al. (2020), *Evolution* 74:1321–1334,
DOI 10.1111/evo.13965; Dryad DOI 10.5061/dryad.6q573n5w1.
