# Hurlburt 2004: exact marked-unit to mature-fruit preflight

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
| \`adult_census.csv\` | \`year, census_date, adult_moth_count\` | one independent adult census date at Onefour |
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
