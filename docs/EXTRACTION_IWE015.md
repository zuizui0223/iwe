# IWE015 extraction receipt — Zhou et al. 2020

Source: Zhou J, Reynolds RJ, Zimmer EA, Dudash MR, Fenster CB. 2020. *Variable and sexually conflicting selection on Silene stellata floral traits by a putative moth pollinator selective agent*. Evolution 74:1321–1334. DOI `10.1111/evo.13965`.

Data archive: Dryad `10.5061/dryad.6q573n5w1`.

Status: **timing-sensitivity candidate; quantitative variance unresolved; not strict H1**.

## Biological contrast

The study established replicated early and late flowering-season experimental populations in 2012 and 2013.

- Early window: `Hadena ectypa` dominant.
- Late window: co-pollinating moths dominant.

`H. ectypa` is a pollinating seed predator: adults pollinate while larvae destroy flowers/fruits after oviposition. The seasonal contrast therefore changes the importance of the mixed partner rather than providing a continuous quantitative synchrony score.

## Final female-fitness outcome

The published table reports successful fruits after predation:

| year | early n | early mean ± published uncertainty | late n | late mean ± published uncertainty |
|---|---:|---:|---:|---:|
| 2012 | 59 | 2.66 ± 2.95 | 58 | 3.91 ± 4.13 |
| 2013 | 55 | 9.77 ± 6.91 | 55 | 8.60 ± 7.01 |

The same table also reports fruit-initiation proportions and predation proportions.

## Why the earlier quantitative extraction was withdrawn

The table heading labels the uncertainty as `SE`. However, the same table reports bounded proportions such as `0.59 ± 0.36` with approximately 59 plants. If `0.36` were literally an SE, the implied SD would exceed the mathematical range possible for a variable bounded in [0,1]. Therefore the dispersion label cannot safely be interpreted as a conventional SE for meta-analytic variance calculation without checking the archived raw data or an author clarification.

The previously computed delta-method variances have therefore been removed from `timing_sensitivity_effects.csv`.

The source summary values are retained in `data/extraction/provisional_effects.csv` with `status=variance_unresolved` so that the record remains auditable without entering any quantitative synthesis.

## H1 boundary

This experiment is not a strict H1 effect because `early` versus `late` is not itself a numeric plant–Hadena overlap metric. Early timing coincides with the Hadena activity peak, but the late period also changes the composition of alternative pollinators. The contrast therefore changes multiple components of the pollination environment.

Use is restricted to:

- mixed-system timing sensitivity;
- benefit/cost decomposition context;
- later quantitative analysis only after raw-data reconstruction and a frozen exposure definition.

## Next extraction action

Use the Dryad files `2012_early_female.csv`, `2012_late_female.csv`, `2013_early_female.csv`, and `2013_late_female.csv` to reconstruct the distribution of successful fruits and verify the table dispersion convention. Until then, no effect from IWE015 enters a meta-analytic model.
