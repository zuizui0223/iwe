# Ambio 2015 Table 1 × IWE/chocho: measured 2010 host-use audit

This is a **published-aggregate, descriptive** host-use receipt from
Navarro-Cano et al. (2015), "Climate change, phenology, and butterfly
host plant utilization", Ambio DOI 10.1007/s13280-014-0602-z
(https://link.springer.com/article/10.1007/s13280-014-0602-z),
Table 1 on printed page S81 / PDF page 4.

## Measured evidence now accessible

Table 1 reports 2010 Anthocharis cardamines **egg numbers** and
**number of searched host-plant individuals** from South, Central and
North Sweden. It has 7 reported host taxa (the article separately
codes Cardamine paludosa as an octoploid cytotype), across a 3×7
region–host grid. Eighteen cells were sampled; three cells were
marked by the authors as a host not encountered at the field survey,
not as zero eggs on known surveyed plants.

Total of the observed counts:
- 16,453 searched plants;
- 6,187 phenotyped plants (a subsample of those counted);
- 547 eggs; and
- 18 region × taxon rows with both numerator and denominator.

These values reproduce the paper's sampled-plant totals.
The table was transcribed directly from the published open article,
and the explicit non-sampled rows remain missing.

**Quality warning:** for South Sweden C. paludosa, the published
eggs/plant cell states 0.085, but the same row prints 11 eggs / 369
plants, giving 0.02981 eggs/plant. The discrepancy is ~0.0552,
far beyond 3-decimal rounding. The analysis calculates all rates
from integer egg and surveyed-plant counts instead of silently using
the inconsistent ratio. Some other ratios differ slightly from
simple integer divisions, and those deviations are retained.

## Connection to previously frozen chocho geography

The same six-species Oikos name crosswalk from
data/registry/oikos_2018_to_chocho_taxonomy.csv is re-used.
The source additionally distinguishes C. paludosa as a separate
reported octoploid sampling class and **does not pool it into**
C. pratensis or transfer C. pratensis's 0.4 world geographic
credit to it.

Only three full species can be joined to the 11-host frozen
Anthocharis portfolio:
- Capsella bursa-pastoris: 43.0 of 110 fractional region equivalents;
- Cardamine pratensis: 0.4 of 110 equivalents;
- Arabis glabra = Turritis glabra: 2.083333 of 110 equivalents.

Other study host taxa have no corresponding exact source-backed
portfolio entry, and are not assigned zero ecological host use.

### Strict descriptive within-region contrast

From original count numerator / denominator, the egg rate
of C. pratensis relative to C. bursa-pastoris is:

- South 2010: (30/2307)/(6/795) = 1.723;
- Central 2010: (21/67)/(24/556) = 7.261;
- North 2010: (2/180)/(42/719) = 0.190.

The *direction* reverses in the North; the two hosts have very
different world resource-opportunity contributions, so geography
alone is not a proxy for these locally observed egg intensities.
The original Ambio authors already reported region-specific host
preferences, so this is a **transparent cross-source decomposition**,
not an independent discovery or confirmation of a seasonal mechanism.

**Causality and inference boundary**: the source survey is one
year (2010), different visits per region and multiple plants
nested in populations/plots. Published Table 1 lacks plant-level
phenological stages, independent adult flight event data and
cluster-level variances. Egg counts are not a binomial probability
and no regression p-values, CIs or an independent replicate count
are computed. Observed egg use does not prove successful larval
development or plant final fitness. Global WGSRPD3 resource
credit is a species-by-host macrogeographic descriptor, not a
2010 source regional exposure nor a predictor with replication.
It MUST NOT be used for spatial–temporal causal inference here.

The 2010 Ambio fieldwork may overlap the 2010 component of
Toftegaard et al. 2018 Oikos (same study programme, participants
and regions). Treat as **potentially dependent**, never as a
second independent validation programme. The original Dryad
plant-level file is still missing (PR #113 remains draft).

## Reproduction and outputs

Source transcription:
data/registry/ambio_2015_table1_2010_host_use.csv

Build:
    python scripts/audit_ambio_host_use.py --output-dir results/ambio-2010-chocho

Produces:
- ambio_region_host_2010_egg_rates.csv (21 rows; 18 sampled and 3 non-sampled)
- cardamine_vs_capsella_2010_descriptive.csv (3 region contrasts)
- ambio_source_audit.json (hashes, scope, numerical discrepancy)

GitHub Actions workflow and tests assert the exact 16,453 / 6,187 /
547 accounting and prevent fabricated zeros, synonym conflation,
and promotion into IWE strict H1. This is an observational audit
and does not modify chocho's frozen GEB manuscript.
