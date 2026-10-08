# Hurlburt 2004: exact marked-unit to mature-fruit preflight

> **Original-source update (2026-10-08):** The university-hosted `NQ95948.pdf` has now been downloaded and inspected. Physical PDF pp. 85–87 (printed pp. 73–75) directly confirm one-to-one flower-marking continuity through fruit retention/abscission and direct adult-moth census. The still-unverified link is **flower-date/ID → post-larval intact viable seeds with variance**, not whether flower IDs ever persisted to retained fruit. See `docs/HURLBURT2004_ORIGINAL_THESIS_SOURCE_AUDIT_20261008.md`. Earlier access failures and preliminary status statements below are historical.

Date: 2026-10-08  
Candidate: \`MIX002_HURLBURT_2004\`  
Study system: *Yucca glauca × Tegeticula yuccasella*, Onefour, Alberta, 1999–2003  
Thesis: Hurlburt (2004), University of Alberta, DOI \`10.7939/r3-fe1d-kj80\`, repository file \`NQ95948.pdf\`.

## Current empirical boundary

The original dissertation's public repository identity has been located, but this
execution environment has **not successfully inspected its 179-page PDF**.
Public Canadian agency material derived from the Hurlburt programme reports:

1. Adult moths were counted several times a week on approximately 100 fresh
   flowers at Onefour during 1999–2003 flowering seasons.
2. Marked clones and inflorescences were followed to fruit set.
3. Mature fruits were dissected, and fruit-level viable-seed variance is
   preserved in government summaries (Onefour pooled 1999–2003:
   146.3 ± 93.9 **SD** viable seeds per sampled mature fruit; n=221).
4. More asynchronous flowers were observed to receive fewer visits and less
   pollen deposition, but source summary statements about their *expected*
   reproductive disadvantage are **not** the observed date-stratified mature
   viable-seed outcome.

The COSEWIC 2013 report also describes unusual northern **reverse selective
abscission**: flowers with fewer eggs or poorer pollination are more likely to
abort than egg-richer flowers in this resource/partner-limited context. This is
an ecological mechanism boundary, **not** an independent marked-unit
synchrony-to-final-fitness comparison.

## Newly explicit adult-detection boundary

The official COSEWIC 2013 assessment (section "Sampling Effort and Methods",
Yucca Moth) states that the 1999–2003 counts were made **inside approximately
100 fresh flowers several times a week**, and that adult Yucca Moth total
abundance **could not be determined** because of short adult lives,
within-year variability, and inability to detect them outside Yucca flowers.

This separates two meanings of "independent" which must not be conflated:

- **Independent of egg receipt / larval injury:** adult moths were directly
  counted rather than inferred from already-laid eggs, so they are a valid
  directly observed *within-flower adult census*.
- **Independent of host-flower sampling opportunity:** **not established**.
  Detection is conditional on fresh host flowers being available and visited
  by observers. A missing census date is not an observed zero-moth day, and
  observed counts alone do not reconstruct an unconditional moth emergence
  distribution outside the sampled flowering period.

### An observed annual discordance, not a timing effect

The COSEWIC 2013 Table 1 yearly summaries illustrate why direct moth
detection **per fresh flower** should not automatically be interpreted
as realized pollination service or timing alignment. At Onefour:

| Year | Moths / flower (source index) | Fruits / clone (source index) |
|---|---:|---:|
| 1999 | 0.456 ± 0.259 | 4.537 ± 0.328 |
| 2000 | 0.563 ± 0.259 | 0.354 ± 0.172 |
| 2001 | 0.388 ± 0.235 | 2.119 ± 0.207 |

The **highest** of these three published annual moths-per-flower
indices (2000) coincides with the **lowest** fruit-per-clone
index. The contrast is observational, combines metrics with different
denominators and potentially different sampling cohorts, and does
**not** establish a negative relationship between synchrony and
fitness or identify a causal mechanism. Floral opportunity,
flower-/clone-level sampling, resource allocation, abortion, and
other annual conditions could change final fruit set independently.

It does demonstrate an empirical risk of treating *per-flower adult
presence* as if it were a sufficient proxy for net plant benefit.
Do not turn the three annual rows into independent seasonal-overlap
effect sizes. Table 1 also repeats identical fruit/inflorescence
and fruit/clone printed values for 2002 and 2003; this may reflect
source aggregation or a transcription issue and is not independently
resolved here.

The preflight therefore preserves `adult_census_detection_context =
moths_counted_within_fresh_host_flowers`,
`independent_unconditional_adult_flight_window_verified=false`,
and `unsampled_adult_activity_imputed_zero=false` regardless of a
successful marked-fruit join. An optional original `flowers_examined`
column can verify dated positive flower-sampling effort. Presence of that
column **does not** itself prove a full, flower-independent adult
flight/activity curve.

This caveat weakens automatic transport to the strict
independent-partner-*availability* estimand. It does not retroactively
prove that the programme is ineligible: after original-source audit, a
defensible, host-availability-conditioned adult activity contrast may
still exist, but must be named correctly and predeclared before seeing
final seeds. Only the original source can establish its interpretability.

Official assessment:
https://www.canada.ca/en/environment-climate-change/services/species-risk-public-registry/cosewic-assessments-status-reports/yucca-moth-various-species-2013.html

The public source summaries do **not** verify a fruit-level key linking
dissected fruits to the marked clone/inflorescence and that marked unit's
opening dates. The repository PDF retrieval failure is a runtime constraint,
not evidence that these keys are absent from the thesis.

Sources:
- https://doi.org/10.7939/r3-fe1d-kj80
- https://www.canada.ca/en/environment-climate-change/services/species-risk-public-registry/cosewic-assessments-status-reports/yucca-moth-various-species-2013.html
- https://www.canada.ca/en/environment-climate-change/services/species-risk-public-registry/cosewic-assessments-status-reports/soapweed-2013/chapter-14.html

## What the new executable gate does

\`src/iwe/hurlburt_join.py\` and
\`scripts/audit_hurlburt_marked_unit_join.py\` test whether a source-reviewed
record collection supports *any* complete, within-season
\`year × clone_id × inflorescence_id\` key connecting flowering and mature fruits,
with repeated, separately measured adult moth observations in that same year.

This is a **necessary linkage gate only**. It does not estimate high/low
synchrony, mortality/abortion, fruit set, net seed production, an SMD, or
paired model prediction.

The four accepted input objects, once located and confirmed in the
*original* thesis or linked field archive, are:

| Input | Required normalized fields | Grain |
|---|---|---|
| \`marked_units.csv\` | \`year, clone_id, inflorescence_id, first_flower_date, last_flower_date\` | one marked inflorescence in a known year |
| \`adult_census.csv\` | \`year, census_date, adult_moth_count\` | one within-flower adult census date at Onefour (optional `flowers_examined` effort) |
| \`mature_fruits.csv\` | \`year, clone_id, inflorescence_id, fruit_id, viable_seeds\` | one dissected mature fruit, nested in the original marked unit |
| \`provenance.json\` | schema below | explicit original-source locators and audit mode |

**These are the desired normalization fields, not a claim that they
were observed in the Hurlburt thesis.** They are never inferred from
COSEWIC annual totals, government population indices, or unmatched
mature fruit dissections. The exact original columns and join must be
documented after direct reading of the thesis.

For *original* source review, provenance must include:

\`\`\`json
{
  "mode": "original_source_review",
  "thesis_doi": "10.7939/r3-fe1d-kj80",
  "site": "Onefour",
  "original_pdf_inspected": true,
  "adult_census_source_locator": "original thesis page and table",
  "flowering_unit_source_locator": "original thesis page and table",
  "mature_fruit_source_locator": "original thesis page and table",
  "fruit_to_marked_unit_link_source_locator": "original thesis evidence for the explicit identifier join"
}
\`\`\`

Generic locators shown above are examples, not verified page
references. Evidence review by a researcher is required and
**cannot be performed by the schema validator alone**. A
\`{"mode": "synthetic_fixture"}\` manifest is permitted only for
testing the algorithm and never sets a positive source-verification
field.

Call once real original records are available:

\`\`\`sh
python scripts/audit_hurlburt_marked_unit_join.py \
  marked_units.csv adult_census.csv mature_fruits.csv \
  provenance.json /tmp/hurlburt-join
\`\`\`

The output \`marked_unit_join_audit.json\` reports annual counts,
matched and unmatched fruit rows, unique linked inflorescences, adult
census dates, status, source-versus-synthetic provenance, and
explicitly \`strict_h1_effect_promoted=false\`.

## Fail-closed boundaries

- A year-total moth count is never a synchrony surface. Adult census
  dates must be independently measured, and at least two census dates
  in a year must coexist with at least two source-linked marked
  inflorescences for that year to pass the minimal structural check.
- A \`year\`-only or \`site × year\` join, or clone ID without original
  inflorescence linkage, is inadmissible. An annual adult-total/annual
  seed-total correlation is not the frozen SMD estimand.
- Repeated fruits within a marked inflorescence share the timing
  exposure. They may provide descriptive fate information, but are
  not independent timing treatments or new dependence clusters.
- Fruit records without the corresponding marked flowering unit
  are flagged as unmatched. A partially matched subset is *not*
  automatically valid, because its selection could depend on
  abscission and successful fruit retention.
- A mature fruit containing zero viable seeds is not equivalent to a
  flower that aborted and consequently never appears in the
  mature-fruit sample. **The absence of a mature fruit row does not
  imply zero plant reproduction or a known abortion fate.**
- This gate cannot distinguish a fully sampled marked-unit history
  from a survivor-only dissection subsample. Net intact viable seeds
  per initially exposed flowering unit require an independently
  documented complete reproductive-fate denominator.
- Even an exactly joined result does not freeze a high/low synchrony
  grouping or supply SMD-ready variance. Timing contrasts must be
  registered using adult and flowering data **before** examining
  mature seeds, with biological units and years kept distinct.
- Male moth count and realized oviposition/egg receipt are different
  windows. A separate, measured developmental/host-filter layer
  would be needed for the later effective-window prediction claim.

## Admission status

**No thesis-level join key has been recovered as of this audit.**
The existing P1 \`blocked_timing_linkage\` and mixed strict-H1 **zero
independent clusters** therefore remain unchanged.

The highest-value next retrieval is the identified original Scholaris
PDF (\`NQ95948.pdf\`), using an authorized institutional or ordinary
browser/library access route. Check thesis tables and appendices for
the exact **1999–2003 marked inflorescence ↔ flower date ↔ dissected
mature fruit** join before spending effort reconstructing means/SD.

If no source-backed key exists, **stop**: do not create one from
annual averages. Continue to another independently measured mixed
programme rather than widening or relaxing the estimand.
