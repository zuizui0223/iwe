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

## Consequence — revised 2026-09-28

The antagonist strict corpus is now **empty** after applying the same independent-partner-window and exposure-unit rules retrospectively to IWE011.

The current P1 completion queue is:

1. Cardamine–Anthocharis — plant trajectories and final intact reproduction are public; exact 2012–2014 female capture+recapture timing remains the only biological object missing, with identified public binary assets checked before contact.
2. Parnassia–florivorous beetles — source-defined beetle-abundance cohorts and final seeds exist, but fate of beetle-destroyed marked flowers is missing from the public surface.
3. James 1998 Yucca cheater — same plants carry flowering timing and final intact/damaged seeds; the unpublished plant-level timing-stratified final-seed summary remains missing.

Tomares–Astragalus is demoted to P2. Its published focal synchrony series is newly laid eggs on host shoots, not independent adult availability, and the synchrony comparison is one patch versus one patch. Plant/shoot SD alone cannot repair that design.

IWE011 is likewise no longer a strict effect: its mid- to late-July partner window is based on oviposition/egg observations, and the former HA-versus-HD SMD treated within-plot plants as timing-exposure replicates.

These revisions reduce apparent evidence coverage but remove two internally inconsistent shortcuts. The antagonist target is again to recover a **first** strict SMD cluster before a second replication is sought.
