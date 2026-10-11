# IWE015 public Dryad source recovery (non-promoting)

Date: 2026-10-08. The primary publisher's Table 1 confirms the four
2012–2013 female cohorts, but the public Dryad source files have yielded HTTP
403 in the local web execution environment, while this container cannot
resolve the datadryad.org domain. This is **not** a data-access restriction
inferred for all environments and does not license imputation.

The public Dryad landing page:
https://datadryad.org/dataset/doi:10.5061/dryad.6q573n5w1

## Network access results and authenticated recovery

Two independently executed GitHub-hosted anonymous probes failed on all six
pinned files (2026-10-08; workflow runs `37736221261` and `37737502478`).
The direct file-stream endpoint returned HTTP **403**; the official
`/api/v2/files/{id}/download` endpoint returned HTTP **401**.
**Zero source files were recovered**. Although GitHub displayed a successful
workflow status, that was because an earlier workflow permitted the download
step to fail. It was never a successful source-download result.

Dryad's official API-account documentation explicitly notes that downloading
some files requires an **OAuth bearer token** even if their metadata are
public. It documents an ORCID-based account/API credential setup
(https://github.com/datadryad/dryad-app/blob/main/documentation/apis/api_accounts.md).
That is a plausible explanation of 401, not proof the particular dataset
requires authentication for every legitimate client.

The retrieval implementation now provides **two distinct public retrieval
methods**, without changing the published source identity:

1. The six pinned individual files under `/api/v2/files/{file_id}/download`
   and `/downloads/file_stream/{file_id}`, which yielded 0/6 anonymously.
2. A **new independent one-time archive route**, the officially documented
   whole-dataset ZIP API:
   `https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.6q573n5w1/download`.
   Run `python -m scripts.probe_iwe015_dataset_zip --output-dir /tmp/iwe015-archive --strict`.
   Only the six exactly pinned source basenames are accepted from the ZIP;
   unknown entries are never written, duplicate paths or an invalid ZIP
   fail closed, and neither final-fitness lineage nor variance is inferred
   from successful retrieval. On opening the archive-fallback PR, CI tries
   this public endpoint once without credentials and writes an access
   manifest; *workflow success* is never evidence that download succeeded.

For repeatable **manual** authenticated access, Dryad documents that its
OAuth **access tokens expire after about ten hours**. Do not store an
unrenewed access token as a durable secret and assume it will continue to
work. Instead, a user with API-account permission may create two GitHub
Actions repository secrets, `DRYAD_CLIENT_ID` and `DRYAD_CLIENT_SECRET`
(Settings → Secrets and variables → Actions). Both manual workflows perform
the documented client-credentials exchange at
`https://datadryad.org/oauth/token` to obtain a fresh short-lived bearer.
A manually supplied `DRYAD_ACCESS_TOKEN` remains an opt-in fallback if
client credentials are not configured.

**Never paste any token or OAuth client secret into this chat, a PR, issue,
commit, or log.** The scripts do not log the secret, and their redirect
handler strips Authorization when a Dryad URL redirects to an external
storage domain. Credentials are only made available to the *manual*
`workflow_dispatch` download steps, not PR-triggered public probes.
A failed OAuth exchange is recorded as `blocked` with no effects promoted.

The individual-file script is:
`python scripts/recover_iwe015_dryad.py --output-dir /tmp/iwe015-dryad --strict`.
The whole-dataset ZIP script is:
`python -m scripts.probe_iwe015_dataset_zip --output-dir /tmp/iwe015-archive --strict`.

Both programs use a size-bounded, source-checked `manifest.json`
(or `archive_manifest.json`) and retain any obtained files only under
`source_files/`. Files recovered in a manual run remain **unreviewed**,
with seven-day GitHub Actions artifact retention.

The strict-H1 extraction, effect sizes, and all IWE015 eligibility gates
remain unchanged.

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
relabels `SE` as `SD`, or promotes IWE015 into strict H1. A 401/403 or
partial download is recorded as `blocked` rather than a false success.
Even a complete download requires manual confirmation of source analysis
and linked biological unit definitions.

Primary source: Zhou et al. (2020), *Evolution* 74:1321–1334,
DOI 10.1111/evo.13965; Dryad DOI 10.5061/dryad.6q573n5w1.
