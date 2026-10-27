# Oikos × chocho — source-backed sampling-frame bridge (v0.1)

## Status

**Descriptive evidence-reconciliation completed.** The original 2018
Toftegaard et al. individual-plant Dryad text file remains unrecovered
(Dryad API requires authentication for file download). This audit
does **not** claim to have reanalyzed egg observations or measured
within-year phenological matching.

Published source: Toftegaard et al., *Butterfly–host plant synchrony
determines patterns of host use across years and regions*,
Oikos DOI https://doi.org/10.1111/oik.05720.

Data used here: **Appendix 1, Table A1**, published as
https://www.oikosjournal.org/sites/oikosjournal.org/files/appendix/oik-05720.pdf.
The table describes the NUMBER OF PLANTS with development stage and
oviposition incidence recorded in the corresponding region × species × year,
NOT the count of oviposition events. Table values were manually
transcribed into data/registry/oikos_2018_table_a1_sampling.csv
because binary appendix retrieval was inaccessible in this environment.
The tabular PDF text was readable, but the redirected image screenshot
could not be retrieved. The original table should be visually
rechecked before treating transcription as an archival byte-verified source.

### Sample accounting

15 nonempty region × plant-species combinations × four years
(2010–2013) give **60 sampling cells** and a simple sum of **22,933
plant records**. This is *not* an asserted count of independent
individuals across years, butterflies or eggs.

- Cardamine pratensis: 7,842 recorded plants
- Capsella bursa-pastoris: 3,495
- Arabis glabra: 1,032
- Arabis hirsuta: 3,455
- Arabidopsis thaliana: 4,893
- Thlaspi caerulescens: 2,216

### Frozen name identity and host portfolio

The 11 accepted host names/IDs are sourced from
data/frozen/chocho_cardamine_host_geography_v0.1/host_contributions.csv
(the full HOSTS × WCVP rebuild at pinned chocho commit
df6f920a37c7e86a878d9f6375bb4454128b5d66).

Three Oikos species match that portfolio:

| Oikos published name | Accepted name in chocho | Match |
| --- | --- | --- |
| Cardamine pratensis | Cardamine pratensis | exact |
| Capsella bursa-pastoris | Capsella bursa-pastoris | exact |
| Arabis glabra | Turritis glabra | homotypic synonym |

The synonym is independently backed by Kew POWO,
https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:278233-1.
The remaining Oikos species are not in this particular **frozen**
11-host portfolio. This is NOT evidence of ecological nonuse.
Notably *Thlaspi caerulescens* = *Noccaea caerulescens*
(https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:298955-2),
which must NEVER be joined with the portfolio's *Thlaspi arvense*
merely because the original names share a genus.

Those three matched host species account for 12,369 recorded plants
in the Swedish panel and 45.483333/110 (~41.3%) units of the
**fractionally attributed worldwide added host-resource geography**
in chocho (Capsella 43, Cardamine 0.4, Turritis 2.083333).
These disparate measures are not correlates in a statistical test.
Brassica rapa, the largest geographic contributor (49.2 units of
fractional credit), is NOT among the Oikos six species. Hence even
the accessible Swedish dataset cannot test the global full-portfolio
time-gating hypothesis by itself.

### Interpretation firewall

The published paper already studied plant stage versus egg-laying.
This source audit must NOT be reported as a new independent positive
result for plant stage preference, or as a source of butterfly female
flight observations in 2012–2014 Dibbinsdale.

A novel joint macroecological test would require, for the same
butterfly × host × WGSRPD3 region × year, (i) reliable geographic
opportunity, (ii) independently measured plant phenophase and
adult female/larval activity, and (iii) host use with an explicit
sampling denominator. A later introduction/arrival-time causal
claim also needs independent dated range expansion information.
The Swedish original may be a conditional local mechanism/QA
panel only, not a cross-global validation.

## Reproduction

Run:

    python scripts/audit_oikos_sampling_bridge.py --output-dir outputs/oikos_bridge

Exports the 60-row region/species/year sampling denominator table,
six-species taxonomy/geographic join, and a source-input hash receipt.
All values and identity checks are tested by
tests/test_oikos_sampling_bridge.py.

No IWE strict-H1 effects, source eligibility changes or
chocho manuscript conclusions are modified.
