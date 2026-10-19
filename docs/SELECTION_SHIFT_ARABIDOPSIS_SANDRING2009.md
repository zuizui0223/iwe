# Arabidopsis lyrata pollinator-mediated phenology shifts

Date: 2026-10-02  
Source: Sandring & Ågren 2009, *Pollinator-mediated selection on floral display and flowering time in the perennial herb Arabidopsis lyrata*  
DOI: `10.1111/j.1558-5646.2009.00624.x`  
Status: signed-selection evidence from a randomized pollen-supplementation experiment; not a partner-window study.

## Design

The study quantified selection through female seed production in 2003 and 2005, comparing open-pollinated controls with plants receiving supplemental hand pollination throughout flowering.

Selection gradients were estimated for standardized traits separately by treatment and year. ANCOVA trait × pollination-treatment interaction coefficients were bootstrapped with 3000 samples and reported with BCa 95% confidence intervals.

The source table uses flowering start and flowering end as separate Julian-date traits. Higher native values therefore mean later timing.

IWE defines the pollinator-mediated effect as:

`beta(open pollination) - beta(supplemented pollination)`.

For the canonical signed-selection registry, positive means the interaction shifts selection toward an earlier date on the focal phenology coordinate. Therefore open-minus-supplemented effects on Julian date are multiplied by -1.

Flowering start and flowering end remain distinct coordinates and are not pooled merely because they share this sign orientation.

## Source-reported contrasts

### 2003

Flowering start:
- open beta = +0.09;
- supplemented beta = -0.06;
- source hand-minus-open interaction = -0.16, BCa 95% CI (-0.39, +0.06);
- canonical pollinator-mediated shift = **-0.16**, i.e. toward later flowering start.

Flowering end:
- open beta = -0.23;
- supplemented beta = +0.21;
- source hand-minus-open interaction = +0.46, BCa 95% CI (+0.15, +0.84);
- canonical pollinator-mediated shift = **+0.46**, i.e. toward earlier flowering end.

This is a source-supported reversal: under natural pollination, selection favors earlier flowering end, whereas under pollen supplementation the gradient becomes positive.

### 2005

Flowering start:
- open beta = +0.19;
- supplemented beta = +0.04;
- source hand-minus-open interaction = -0.11, BCa 95% CI (-0.29, +0.04);
- canonical shift = **-0.11**.

Flowering end:
- open beta = -0.09;
- supplemented beta = +0.07;
- source hand-minus-open interaction = +0.13, BCa 95% CI (-0.05, +0.35);
- canonical shift = **+0.13**.

The 2005 treatment differences are not source-significant.

## Uncertainty rule

The source reports BCa bootstrap confidence intervals rather than standard errors for the interaction coefficients. IWE therefore does **not** back-calculate an SE from these asymmetric intervals.

All four rows are retained as `source_interaction_test_no_delta_se`, with the full source interval recorded in `formal_test`. They may support signed evidence mapping and source-level inference but do not enter an inverse-variance pool until compatible uncertainty is recovered.

## Biological interpretation

The experiment adds an independent mutualist programme showing that pollination can alter the direction as well as the strength of phenological selection. The strongest result concerns flowering end in 2003: natural pollination shifts selection toward earlier cessation of flowering.

That does not identify a pollinator activity window. It therefore informs the signed selection-surface module, not the strict synchrony or window-relative geometry module.

All four contrasts share `DEP_ARABIDOPSIS_SANDRING_AGREN_2009`.
