# Screening batch 002 — strict synchrony versus seasonal timing

Date: 2026-09-16
Status: adjudication and first quantitative sensitivity extraction

## Main result of this batch

The literature is asymmetric in what it measures.

Mutualist studies relatively often measure both plant and pollinator timing and connect their mismatch to seed or fruit production. Antagonist and mixed pollinating-seed-predator studies much more often measure plant flowering date or an early/late seasonal contrast, then quantify attack/predation and plant fitness, without an independently measured partner-activity curve.

IWE therefore keeps two non-interchangeable evidence lanes:

1. **strict synchrony H1** — explicit overlap, absolute mismatch, a verified one-sided mismatch domain, or a timing manipulation prospectively ordered by measured partner availability;
2. **direct seasonal timing sensitivity** — flowering date/seasonal position predicts reproductive outcome in a biologically identified interaction regime, but partner synchrony itself is not quantitatively identified.

The second lane is scientifically useful but cannot be relabelled as the first.

## Strict-H1 progress

### IWE001 — Corydalis ambigua × Bombus spp.

The first extraction was re-audited after freezing `TIMING_METRIC_CONTRACT.md`. Kudo & Ida (2013) reports `mismatch_day = bee first detection - flowering onset`; negative values therefore represent years in which bees preceded flowering and cannot be combined with positive values as a single linear synchrony slope.

Strict H1 now uses only the one-sided domain `mismatch_day >= 0`, where larger values consistently mean that plants flower farther ahead of bee availability.

Recovered site-level Fisher-z effects for mismatch versus natural seed set are:

| Site | n | r | native Fisher z | variance | oriented synchrony z |
|---|---:|---:|---:|---:|---:|
| NFP | 12 | -0.6371 | -0.7533 | 0.1111 | +0.7533 |
| TOEF | 8 | -0.8330 | -1.1978 | 0.2000 | +1.1978 |
| JOZ | 4 | -0.9518 | -1.8511 | 1.0000 | +1.8511 |

All three share one publication/programme dependence structure; they are not three independent studies. JOZ is intentionally very imprecise after the estimand-safe restriction.

### IWE002 — Kudo & Cooper 2019

This remains a high-priority strict-H1 extraction. The source provides 19 years of monitoring, a snow-removal experiment, seed production, and a public Dryad workbook (`10.5061/dryad.q4fm37m`). The paper explicitly reports that seed production declined when flowering preceded bee emergence.

However, IWE002 cannot simply reuse IWE001's sign convention: the 2019 paper describes its mismatch with the opposite algebraic orientation. Population/year overlap with IWE001 must also be mapped before any pooled analysis.

### IWE008 — Qilian alpine-community study 2024

This is a particularly valuable future extraction because flowering and key-pollinator abundance peaks were both monitored and seed setting was measured at the individual level. It also reports asymmetric fitness effects for the two mismatch directions. This motivates the frozen directional-mismatch sub-analysis rather than an absolute-value assumption.

## Mixed interaction adjudication

### IWE015 — Silene stellata × Hadena ectypa

Zhou et al. (2020) compares early and late experimental flowering windows in 2012 and 2013. The early period is `Hadena ectypa`-dominant; the late period is co-pollinator-dominant. Fruit initiation is high in all four experiments, whereas predation differs strongly among periods. Final female reproductive success is measured as successful fruits after predation.

This is excellent evidence for **interaction-regime-dependent seasonal timing**, but early versus late is not itself a quantitative synchrony metric. IWE015 is therefore removed from strict H1 and retained in the timing-sensitivity lane.

From the paper's Table 1, year-specific early-versus-late log response ratios for successful fruits are:

| Year | early mean | late mean | ln(early/late) | delta-method variance |
|---|---:|---:|---:|---:|
| 2012 | 2.66 | 3.91 | -0.3852 | 2.3456 |
| 2013 | 9.77 | 8.60 | +0.1276 | 1.1646 |

The source labels the dispersion values as SE; those source-reported values are used transparently. These effects are deliberately not put in `direct_effects.csv`.

The mixed result itself is heterogeneous across years: the Hadena-dominant window has lower successful-fruit production in 2012 but slightly higher production in 2013. This is exactly why a mixed system should not be forced into a universal synchrony-benefit story.

### IWE014 — Silene vulgaris × Hadena

Pettersson (1991) remains biologically compelling: Hadena adults pollinate while larvae consume reproductive structures, and early versus late flowering changes predation while final seed set is reported. But the current accessible evidence does not yet supply a recoverable quantitative synchrony effect with sampling variance. It therefore remains unresolved for quantitative admission rather than being promoted because it fits the preferred narrative.

## Antagonist adjudication

### IWE010 / IWE011 — Peucedanum multivittatum × Phaulernis fulviguttella

The system strongly supports phenological exposure to seed predation. The 2021 study reports that the predator's major oviposition period is mid- to late July; seed predation exceeded 50% when flowering occurred before about 20 July and was near absent after about 30 July. The 2025 study extends the system to a four-year phenological selection mosaic and final female fitness.

For strict H1, however, the available studies primarily use plant flowering date/population phenology relative to a seasonal predator window rather than a quantitatively observed partner-activity curve for every population-year. These studies therefore currently belong in the **direct seasonal timing sensitivity** lane, not the strict synchrony meta-analysis.

This does not weaken their biological importance. It clarifies the estimand: they show a temporal enemy window and its reproductive consequences, but do not yet provide the same exposure object as a direct plant-pollinator overlap study.

### IWE028 — Tripolium vulgare × Paroxyna plantaginis

Albrectsen (2000) is the best strict-antagonist candidate recovered so far. Transplants were followed through the season; early flower heads had higher potential seed set and lower attack, and the study links the attack pattern to the density/emergence of ovipositing females. Full-text quantitative recovery is still required to establish an effect and variance on a common scale.

### IWE012 — Gentiana pneumonanthe × Phengaris alcon

Valdés & Ehrlén (2017) clearly shows that the seed predator changes selection on flowering phenology: populations without the butterfly favor earlier flowering, whereas caterpillar attack on early plants shifts selection later where the butterfly is present. But the design is based on predator presence/incidence rather than a continuous partner-activity overlap metric. It is therefore a strong timing-sensitivity study, not a strict H1 effect under the current contract.

## Existing-work check

A targeted search did not recover an existing meta-analysis that already estimates IWE's primary moderator — the plant reproductive effect of phenological synchrony compared among mutualists, antagonists and mixed pollinating seed predators. Existing reviews emphasize that population-level consequences of mismatch are rarely demonstrated, while recent macro work often models potential overlap or extinction risk rather than meta-analysing observed plant reproductive effects.

This keeps the IWE question distinct, but it also confirms that primary effect recovery will be the limiting step rather than statistical method development.

## Current evidence diagnosis

The most likely empirical shape is now:

- **mutualist strict H1:** feasible, with multiple direct candidates;
- **antagonist strict H1:** sparse; many high-quality studies are seasonal-timing rather than direct-overlap studies;
- **mixed strict H1:** very sparse; rich mechanism literature but few synchrony-to-net-fitness effects;
- **timing-sensitivity synthesis:** likely much larger for antagonist and mixed classes.

Therefore IWE should not promise a balanced three-class strict meta-analysis before screening is complete. A valid endpoint is an evidence-map result showing that the ecological literature measures timing differently across interaction classes.

## Next extraction order

1. IWE002 — recover 2019 Corydalis Dryad workbook and map overlap with IWE001.
2. IWE008 — recover species-level directional mismatch effects and dependence structure.
3. IWE028 — recover Tripolium attack/seed-set timing data and determine whether a strict antagonist effect is estimable.
4. IWE014 — attempt quantitative recovery from the 1991 Silene vulgaris paper; otherwise lock as context/sensitivity only.
5. IWE010/IWE011 — build a Peucedanum seasonal-timing extraction without pretending it is direct synchrony.

No cross-class pooled ecological conclusion is yet justified.
