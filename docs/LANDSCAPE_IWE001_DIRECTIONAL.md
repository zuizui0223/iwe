# IWE001 directional landscape extraction

Date: 2026-10-02  
Source: Kudo & Ida 2013, Ecological Archives E094-213-A1.  
Status: directional landscape extraction on the pivot branch; not part of the strict-H1 primary dataset.

## Question

The native IWE001 correlations span both sides of exact plant-pollinator matching and therefore cannot be interpreted as a single synchrony effect. The landscape pivot instead asks whether the response differs by side of the interaction window.

The source metric is:

mismatch_day = first bumble-bee detection date - flowering onset date.

Therefore:

- mismatch_day > 0 means the plant flowers before bee detection;
- mismatch_day = 0 means matched onset;
- mismatch_day < 0 means bee detection precedes flowering.

## Reproducible source reconstruction

The analysis uses data/source_reconstructions/iwe001_appendix_a_complete_rows.csv, reconstructed from the public Appendix A rows with both natural seed set and mismatch day.

Before any directional subset is calculated, scripts/build_iwe001_directional_landscape.py reproduces the already-registered whole-site Pearson correlations to absolute tolerance 1e-10:

- NFP: r = -0.6823367403, n = 13;
- TOEF: r = -0.9041525384, n = 9;
- JOZ: r = -0.8184761715, n = 7.

Failure to reproduce those values aborts the directional extraction.

## Plant-earlier side

Restricting to mismatch_day > 0 gives:

| Site | n | Pearson r, mismatch vs natural seed set | Fisher z | var(z) |
|---|---:|---:|---:|---:|
| NFP | 11 | -0.5779385588 | -0.6593618330 | 0.1250000000 |
| TOEF | 8 | -0.8329788653 | -1.1977886791 | 0.2000000000 |
| JOZ | 4 | -0.9518477411 | -1.8510818557 | 1.0000000000 |

On this side, larger positive mismatch means flowering occurs farther before bee detection. All three site-level correlations are negative: greater plant lead is associated with lower natural seed set.

This is the first quantitative landscape result recovered by the pivot.

## Partner-earlier side

The opposite side is too sparse for the registered Fisher-z variance:

- NFP: n = 1;
- TOEF: n = 1;
- JOZ: n = 3.

No partner-earlier Fisher-z effect is reported.

## Interpretation boundary

The three site rows share DEP_CORYDALIS_KUDO_LONGTERM and therefore do not constitute three independent programme replications.

The result supports a one-sided directional statement within the Corydalis programme:

> when Corydalis flowers before first Bombus detection, larger temporal lead is associated with lower natural seed set.

It does not establish:

- symmetry of the fitness landscape around exact matching;
- the response when pollinators are earlier than flowering;
- causal effects of the full pollinator activity distribution;
- three independent study replications;
- a general mutualist meta-analytic effect.

The central unresolved geometric question is now explicit: the plant-earlier slope is observable, while the opposite side of W(tau) is essentially absent from this programme.
