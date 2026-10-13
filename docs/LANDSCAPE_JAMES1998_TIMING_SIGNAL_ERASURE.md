# James 1998 — a flowering-time signal is erased before realized larval load

Date: 2026-10-03  
Study: James 1998 MSc thesis, *Yucca kanabensis* × non-pollinating yucca moth lineage  
Archive: Library and Archives Canada, MQ28950  
Landscape role: independent antagonist mechanism showing **temporal signal erasure** along the interaction chain.

## Why this matters

The thesis follows several causal stages in the same Yucca–moth programme:

1. plant flowering timing and fruit age;
2. adult cheater-moth access and oviposition;
3. realized cheater larvae after development;
4. final fruit dissection, including intact and damaged seeds.

Under the original strict-SMD contract the programme remains blocked because the thesis does not publish timing-stratified final-seed means and variance.

The landscape pivot can nevertheless ask a different, source-native question:

> Does a temporal signal visible at oviposition survive into the later consumer stage?

## Strong timing signal at oviposition

The source reports several timing effects before larval realization.

In the fruit-age/isolation experiment:

- fruit age affects new oviposition droplets: **F = 34.65, p < 0.001**;
- spatial isolation affects droplets: **F = 18.37, p < 0.001**;
- fruit age × isolation: **F = 8.20, p = 0.004**.

In the observational plant dataset, flowering date predicts:

- number of nights with new oviposition droplets: **beta = 0.21, t = 3.49, p = 0.001**;
- accumulated ovipositions per fruit: **B = 1.05, t = 3.52, p < 0.001**.

Thus plant timing clearly propagates into adult oviposition exposure.

## The signal disappears at realized larval load

The later plant-level analysis asks whether flowering date, isolation and fruit number predict cheater larvae after development.

They do not.

For larval number, the fitted model on **n = 359** fruits has **R² = 0.000**. The thesis likewise reports no relationship between these timing/access predictors and cheater larval presence.

The biological interpretation offered in the thesis is that strong downstream interactions, especially competition with pollinator larvae, can erase the timing pattern created at oviposition.

Chapter 3 independently supports that downstream filter:

- cheater survival at 12 d depends strongly on host fruit age at oviposition (**Wald = 36.19, p < 0.0001**);
- the fruit-age effect remains detectable at 28 d (**Wald = 4.50, p = 0.039**);
- survival at 29 d depends on the age of pollinator larvae already present when cheaters oviposit (**Wald = 7.14, p = 0.008**).

Thus the mapping from oviposition timing to realized consumer pressure is conditional on host stage and interspecific competition.

## Signal-propagation interpretation

The programme provides a clean example of:

`plant timing -> oviposition exposure -> [host stage + competition] -> realized larvae`

where the temporal signal is strong at the second node and effectively absent at the third.

This is **signal erasure**, not evidence that phenology was biologically irrelevant.

It matters because a study measuring only oviposition would infer a strong timing effect, while a study measuring realized larval pressure could infer essentially none.

## Relation to Cardamine and Kula

The three systems now show three different transformations of a timing signal.

- **Cardamine–Anthocharis:** raw egg exposure is filtered into a shifted/narrowed active-egg window and then into final reproductive fate.
- **Silene–Hadena (Kula):** developmental phase relations reverse the sign of synchrony on predation across years.
- **Yucca cheater moth (James):** flowering-time effects on oviposition disappear before realized larval load.

This motivates treating temporal effects as signals propagated through a causal chain rather than as one invariant synchrony coefficient.

## Claim boundary

The published thesis does not report the final intact/damaged seed response as a flowering-timing regression or a variance-bearing early/late contrast.

Therefore this component stops at realized larval load and is registered as:

- `window_reference_class = realized_interaction_window`;
- `timing_geometry = timing_signal_erasure`;
- `fitness_channel = cost_channel`;
- `outcome_finality = not_final`;
- `landscape_status = mechanism_only`.

Do not infer a final-seed timing null from the larval null.

Source-backed statistics are stored in
`data/source_reconstructions/james1998_timing_signal_erasure.csv`.
