# Observation-conditioned host-portfolio geography sensitivity

## Question and state

The frozen chocho HOSTS portfolio for Anthocharis cardamines contains
11 accepted species and reconstructed potential native/contemporary
resource geography of 162/272 WGSRPD3 regions, leaving 110 regions
added by accepting introduced ranges of recorded hosts.

Navarro-Cano et al. 2015, Ambio DOI 10.1007/s13280-014-0602-z,
Table 1, separately reports eggs on three species not contained
in that fixed 11-host list: Arabis hirsuta, Arabidopsis thaliana,
and Thlaspi caerulescens, accepted as Noccaea caerulescens.
This is evidence of oviposition, NOT larval survival/suitability.

The same source also reports Cardamine paludosa, accepted as a
subspecies of C. pratensis. It is NOT a new species-level host in
this analysis. An infraspecific sensitivity would require consistent
resolution of ALL baseline plant distributions first.

## Source-fixed procedure

- Source WCVP v13: matildabrown/rWCVPdata commit
  65bed76bae9d644ccb6ad200c05f9f5071d89e05.
- Source chocho analysis: commit
  df6f920a37c7e86a878d9f6375bb4454128b5d66.
- Frozen IWE host contributions: data/frozen/
  chocho_cardamine_host_geography_v0.1/host_contributions.csv.
- Published observed egg taxa from Ambio 2015, not Dryad.

Source code: scripts/build_ambio_host_portfolio_wcvp.R

It resolves the three additional taxa to unambiguous accepted WCVP
v13 plant IDs (species rank), checks all original 11 host IDs
and names, and rebuilds each species' native and contemporary
level-3 distributions. Native excludes extinct, doubtful, and
introduced records; contemporary excludes extinct and doubtful
records. It fails closed unless each original host's region counts
AND the frozen 162/272/110 whole portfolio are reproduced.

Source code: src/iwe/host_portfolio_sensitivity.py

It analyzes 2^3 = 8 host-set scenarios: baseline, each of three
single additions, the three pairwise additions, and all three
additions. The principal quantity is set difference between
contemporary and native host-region unions. Additional hosts
can INCREASE or DECREASE this difference: a new host may
add contemporary regions or may make former contemporary-only
regions already available in the native baseline.

Reported columns include original introduced-added regions retained,
original added regions no longer novel because of native resources,
and new introduced-added regions due to candidate-host ranges.
This explicitly avoids assuming that bigger host portfolios
necessarily produce larger introduced-host effects.

## Scientific limits

These three additional plants were observed receiving eggs.
They are NOT confirmed from these data to support successful
larval development. This is a counterfactual host-set *source
sensitivity*, not a corrected global map, an independent
experiment, or a claim about range expansion caused by
naturalized hosts.

In particular, a Swedish 2010 egg record does not establish
butterfly presence in all WCVP regions where the same plant
is native/introduced. Nor does this analysis measure
phenological synchrony, adult butterfly availability, fitness,
or the global prevalence of incomplete HOSTS lists across
all 239 butterflies. The main chocho GEB claim is untouched,
as are IWE strict-H1 effect records.

Kew taxonomic anchors:
- Arabis hirsuta: https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:278269-1
- Thlaspi caerulescens -> Noccaea caerulescens:
  https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:298955-2
- Cardamine pratensis subsp. paludosa:
  https://powo.science.kew.org/taxon/77250211-1

## Reproduction

A source-pinned GitHub Actions workflow can run:
1. Rscript scripts/build_ambio_host_portfolio_wcvp.R
   _external/WCVP
   data/frozen/chocho_cardamine_host_geography_v0.1/host_contributions.csv
   results/portfolio-wcvp
2. python scripts/analyze_ambio_host_portfolio_geography.py
   --wcvp-presence results/portfolio-wcvp/host_region_presence.csv
   --out-dir results/portfolio-sensitivity

Outputs:
- source_taxon_resolution.csv (accepted IDs and scientific names)
- host_region_presence.csv (exact unit sets)
- candidate_portfolio_scenarios.csv (all 8 source-defined scenarios)
- added_region_transitions.csv (per scenario, per affected region)
- portfolio_sensitivity_receipt.json (input hashes and epistemic limits)

Do not use the interrupted Dryad PR #113 to fabricate unobserved
2010 time windows. The original field file is still required
for a properly independent phenophase test.
