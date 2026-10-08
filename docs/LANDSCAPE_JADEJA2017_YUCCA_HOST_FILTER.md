# Taxonomically distinct host filtering — Jadeja et al. 2017

Date: 2026-10-02  
System: *Yucca glauca × Tegeticula yuccasella*  
DOI: `10.1002/ece3.3426`  
Status: mechanism-only boundary evidence; not a final plant-fitness effect.

## Mechanism

*Yucca glauca* flowers sequentially from basal to distal positions. The
authors motivate their experiment with the expectation that late-opening
distal flowers are more likely to abort when basal fruits already exist
because those fruits compete for plant resources. **Importantly, the
published 2017 paper attributes this particular fruit-abortion
gradient to Jadeja & Tenhumberg's unpublished observations**; it does
not itself experimentally measure a linked host abortion outcome.

For the pollinating seed predator *Tegeticula yuccasella*, this plant allocation decision is a hard post-oviposition filter:

- females lay eggs in flowers and pollinate them;
- if the flower is aborted, all moth eggs in that flower die;
- moths alter oviposition decisions in response to cues associated with the probability of flower abortion.

The study therefore supplies a taxonomically distinct version of the same causal layer identified in Cardamine and Gentiana:

`raw oviposition exposure -> host-state filter -> effective offspring exposure`.

## Why this matters for IWE

The host filter is not one particular defense pathway.

Across the current examples:

- *Cardamine–Anthocharis*: delay after flowering determines whether eggs remain active enough to reach damaging late instars;
- Portuguese *Gentiana–Phengaris*: bud size, developmental stage and oviposition period alter offspring survival;
- *Yucca–Tegeticula*: host resource allocation determines whether an oviposited flower is retained at all.

These mechanisms differ, but all break the equivalence between **an interaction occurring** and **that interaction surviving the host filter to become an effective future cost**.

## A non-obvious within-study stage break: accept a site or adjust egg number?

The published behavioral experiment manipulated basal-fruit presence
in *Y. glauca* while presenting wild-caught *T. yuccasella* females
with distal flowers. The effects differ among source-defined stages:

| Endpoint | Source comparison | Reported result |
|---|---|---|
| **Flower accepted as an egg-laying site** | Basal fruit present vs absent, **29 trials** | Fewer flowers oviposited when basal fruits are present, **P=0.048** |
| **Egg-laying intensity conditional on oviposition** | Same experiment, 16 positive trials | Difference **not significant**, **P=0.61** |
| **Larvae emerging from top fruits** | Distinct observational dataset spanning three years, **243 fruits** | No association detected with basal fruit number, **P>0.7** |

Thus the demonstrated shift is in **whether a reproductive site receives
any eggs**, not a validated change in the number of eggs laid after
acceptance. Lack of significance for conditional egg number **does not
prove equality**; no larval-success change is established in the
separate observational fruit dataset. The 2017 study also cannot
directly quantify final plant seed fitness under the two host states.

For IWE this is a crucial *gate-versus-intensity* distinction:
`host cue → probability of oviposition` has experimental evidence,
but `host cue → egg number among accepted flowers → successful offspring
→ plant intact seeds` is not one observed causal chain. The proposed
connection to future abortion risk relies partly on unpublished
host-survival observations. Do not promote these three results as
same-unit temporal signal propagation or as a paired predictive null.

Source: Jadeja & Tenhumberg 2017, DOI `10.1002/ece3.3426`, Results
§3.1–3.2 and Methods §2.2; frozen stage summary:
`data/source_reconstructions/jadeja2017_yucca_host_cue_stage_summary.csv`.

## A second, nonmonotone host-filter boundary

The 2013 Canadian COSEWIC Soapweed/Yucca Moth assessments (citing Hurlburt
2004) describe **reverse selective abscission** at the northern Onefour
population: flowers with fewer ovipositions or less pollen are more
likely to be aborted. In contrast, classic yucca sanction examples abort
egg-rich flowers. This does **not** overturn the experimental Jadeja 2017
result, because different populations and measurements are involved.

It shows why "host filtering" should not be coded as a universally
monotone anti-consumer defence. Egg receipt is coupled to adult
pollination, and apparent acceptance of egg-rich flowers may reflect
pollen or reproductive-unit quality rather than a preference for costly
larvae. See `LANDSCAPE_HURLBURT_YUCCA_REVERSE_ABSCISSION.md` for the
secondary-source evidence, competing mechanisms and a falsifiable
within-species comparison. Neither study is promoted to strict H1.

## When is the host filter predictable enough to anticipate?

James et al. 1994, *Oikos* DOI `10.2307/3546140`, tracked **38
Yucca elata inflorescences** across a season with nightly adult
Tegeticula relative abundance, nightly opening flowers and later
mature-fruit fates. The fruit-retention window averaged **five
consecutive nights** (36% of inflorescence anthesis), but appeared
unpredictably at early, middle or late positions. Additional
hand-pollination did not significantly increase fruit maturation,
and adult-moth abundance was not detectably correlated with mature
fruit output.

This is distinct from *Y. glauca* in Jadeja 2017, where the
presence of basal fruits gives moths a directional cue about
late distal flowers' abortion risk and moths alter their oviposition.
Together they motivate a **cross-context discriminator**:

> Does accurate information about future host fruit retention permit
> timing or placement specialization by a seed-eating pollinator,
> whereas poorly predictable retention rewards spreading eggs among
> different reproductive units?

This is an **untested comparative ecological hypothesis**, not a
demonstrated adaptive strategy or an observed within-species
reversal. The James 1994 published abstract contains no recoverable
linked *adult timing → intact seed production* variance-bearing
contrast. See `CANDIDATE_AUDIT_YUCCA_ELATA_JAMES1994.md`;
the candidate remains **P2**, outside strict H1.

## Claim boundary

This study does not supply the final plant reproductive surface required for a primary IWE fitness effect.

It is registered as `mechanism_only` and is used only to test whether host filtering of realized interaction events occurs outside the Lepidoptera systems that motivated the pivot.

The current evidence supports taxonomic breadth of the mechanism, not a quantitative universal law about the direction or magnitude of the filter.
