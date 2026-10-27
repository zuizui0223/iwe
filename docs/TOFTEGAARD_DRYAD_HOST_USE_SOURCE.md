# Independent Anthocharis host phenology observation data — source gate

The previous IWE × chocho spatial audit (PR #112) decomposes potential
WCVP/HOSTS resource geography of Anthocharis cardamines. It does NOT measure
actual use of these host plants or temporal matching. This new workflow
tests retrieval of a distinct observational dataset (Toftegaard et al. 2018,
Dryad DOI 10.5061/dryad.jp328r6).

The Dryad landing page identifies 'Plant phenology in the field.txt'
(~2.76 MB), covering host plant phenophases and butterfly egg/larval
observations from Sweden 2010–2013, plus sampling site areas. First
acquire raw source and freeze sha256, bytes, line count, and encoding.
Raw data are uploaded as an ephemeral Actions artifact and deliberately
NOT committed before schema/permissions/sampling units are audited.

Expected next methodological gates after a successful download:

- Inspect delimiter, headers, field units, missingness, repeated plant/
  transect/site/year records, and observation effort.
- Define direct observed oviposition/larval use against independent
  host stage, with covariates host identity, region, season and effort.
- Ensure eggs and larvae remain *outcomes*, never independent adult
  butterfly activity used to construct a strict IWE timing exposure.
- Do not treat zero eggs per plant as known absence of adults; do not
  claim geographic expansion from these Swedish local observations.
- IWE strict H1 still lacks independently measured focal Dibbinsdale
  2012–2014 female capture/recapture event DOYs and same-unit final
  plant reproduction. Swedish 2010–2013 observations do not rescue that gate.

The acquisition workflow makes NO biological findings; if the public
file download is blocked, the receipt records that explicit blocker.


## Public source access status, 2026-10-27

The *published dataset* is discoverable at Dryad DOI
10.5061/dryad.jp328r6 and contains the listed 2010–2013 data files.
However, GitHub Actions run
https://github.com/zuizui0223/iwe/actions/runs/40466275403
failed to retrieve the actual raw file with all three distinct
documented/public routes:

1. GET /api/v2/files/79537/download: HTTP 401 Unauthorized;
2. GET /downloads/file_stream/79537: HTTP 403 Forbidden;
3. GET /api/v2/datasets/doi%3A10.5061%2Fdryad.jp328r6/download:
   HTTP 401 Unauthorized.

The network-level download authorization failure is not evidence
that the data itself is private, inaccessible in a normal browser,
biologically unavailable, or missing from Dryad. No observations or
measured phenology have been read; the study remains a documented
**not-yet-ingested data source**, not a completed replication.

Repeated attempts with these endpoints are frozen at this
point. The relevant next action is to obtain actual published
files using a normal browser/institutional library route or an
authorized Dryad export and then audit original headers,
time grain, egg/larval detection, sampling denominators,
and taxonomic identity. This preserves the IWE direct-evidence
firewall and avoids replacing observed butterfly adult activity
with egg or larval records. Until the file is present, the
separate acquisition workflow intentionally fails its source
readiness gate, while still archiving the explicit error receipt.


## Updated access diagnosis and local-input gate (2026-10-28)

Dryad's official API-account documentation specifies that file and
dataset downloads require a bearer token:
https://github.com/datadryad/dryad-app/blob/main/documentation/apis/api_accounts.md
The 401 responses recorded above are therefore an authorization
limitation, not a new biological finding or proof of an unpublished
file. Automatic anonymous retries are disabled by default; the old
routes are usable only with --try-anonymous-legacy-downloads for
explicit diagnostics.

Once the original Dryad TXT or dataset ZIP has been downloaded via
an authorized browser/service, run:

    python scripts/acquire_toftegaard_dryad.py \
      --source-file "/path/to/Plant phenology in the field.txt" \
      --output-dir outputs/toftegaard-original

The audit records original SHA-256, bytes, line count, and format,
but source origin, column semantics and observation units remain
unverified until checked separately. It never creates IWE strict-H1
fitness effects or independent female adult flight dates.

Merged PR #114 separately recovers the published Oikos Appendix 1
Table A1 denominators (60 region×species×year cells; 22,933
plant records) and a Kew-backed synonym crosswalk. These are NOT
individual egg/plant-stage records. No API secrets, token-bearing
URLs or uninspected raw observations may be committed.
