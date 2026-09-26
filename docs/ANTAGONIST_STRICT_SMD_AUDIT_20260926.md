# Antagonist strict-SMD audit — raw-data and classic near-misses

Date: 2026-09-26  
Status: antagonist #2 remains open; no frozen-contract relaxation

## Sercu et al. 2020 — raw data do not solve the timing gate

*Geum urbanum × Byturus ochraceus*  
DOI: `10.1111/1365-2745.13325`  
Dryad: `10.5061/dryad.x3ffbg7dz`

This source was re-opened because its Dryad archive is unusually complete. It contains individual flower-emergence timing, flower/plant predation status, predated and unpredated seed measurements, and total seed mass.

The public data therefore solve the final-fitness and variance side of the problem.

They do **not** solve the strict timing exposure. The paper's adult beetle emergence and oviposition season are sourced to earlier natural-history studies (Pellmyr 1985; Springer & Goodrich 1986). The focal field programme monitors plant phenology and later seed predation but does not independently census adult *B. ochraceus* abundance/activity through the same season.

The study's “off-peak flowering” metric is explicitly defined relative to the predator period, but that period is not a contemporaneous partner-activity measurement from the focal programme. Observed infection cannot be substituted as the missing activity curve.

Decision: retain `rejected_timing`.

## Gross & Werner 1983 — almost ideal groups, but mixed selective forces

*Solidago graminifolia × Epicauta pennsylvanica*  
DOI: `10.2307/1942589`

This study has several features IWE has been searching for:

- source-defined early/intermediate/late flowering groups;
- independent seasonal counts of the blister-beetle flower predator;
- final filled-seed outcomes with sample sizes and confidence intervals;
- significantly higher predator density on early than late *S. graminifolia* clones.

However, the same seasonal contrast simultaneously changes pollinator availability. The authors explicitly partition the early-group shortfall from maximum potential seed set and attribute most of it to pollinator limitation, with flower predation accounting for only a minority.

Therefore the natural early-versus-late seed-set contrast is not a clean focal-antagonist synchrony effect.

*S. juncea* does not rescue the source: blister-beetle pressure rises later, but the authors interpret the late natural seed-set decline as primarily pollen limitation and do not establish a source-defined predator-only final-fitness contrast.

Decision: `rejected_other`.

## Augspurger 1981 — wrong synchrony reference

*Hybanthus prunifolius*  
DOI: `10.2307/1937745`

The experiment induces plants to flower before the naturally synchronous population and measures pollination, seed-predator infestation, and final mature seed output.

This is a classic demonstration that conspecific reproductive synchrony can influence seed-predator satiation. But the exposure is **plant-to-population synchrony**, not overlap with an independently measured predator activity curve.

Decision: `rejected_timing` for strict IWE H1.

## Pilson 2000 — biologically strong, wrong frozen effect form

Wild sunflower, *Helianthus annuus*, with five seed-feeding herbivores.

The study independently documents seasonal herbivore-abundance patterns and relates flowering date, herbivore damage and plant fitness. It therefore remains valuable direct timing evidence.

The published inferential form is continuous flowering-date/selection analysis, not a prospectively defined high-versus-low partner-window group contrast with SMD-ready variance.

Decision: P2 `blocked_effect_form`. Do not create bins after seeing the response and do not convert a selection slope to SMD.

## Consequence

The antagonist P1 queue is still:

1. *Astragalus lusitanicus × Tomares ballus* — correct biological chain; needs correct-unit final-reproduction variance.
2. James 1998 *Yucca kanabensis ×* non-pollinating yucca moth — same plants have timing + final intact/damaged seeds; needs the unpublished plant-level grouped final-seed table.
3. *Parnassia wightiana × Nonarthra variabilis* — source-defined beetle-abundance cohorts; raw fate archive cited by the paper is currently not retrievable and published seeds/fruit exclude beetle-destroyed peduncles.

The new audits do not reduce the cluster gap, but they close several tempting false shortcuts.
