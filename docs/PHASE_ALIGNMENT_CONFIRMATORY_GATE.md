# Stage-specific phase-alignment confirmatory gate

_Generated from data/registry/phase_alignment_candidates.csv; do not edit counts by hand._

## Current gate

- Candidate programmes/components: **14**
- Dependence clusters: **14**
- Confirmatory-ready positive or null comparisons: **0**
- Near-confirmatory blocked routes: **2**
- Biological endpoint nulls (not paired predictive tests): **2**
- Positive paired realized comparisons (non-confirmatory): **1**
- Independent adult × host timing gains over host calendar alone (not effective-stage tests): **1**

A programme is confirmatory_ready only when it has source-backed raw/adult timing, effective consumer timing, a pre-final host filter, variation in phase alignment, a final plant endpoint, and a paired simpler-vs-stage-specific timing comparison.

## Evidence coverage

- Final plant endpoint present: **12 / 14**
- Phase/alignment varies: **13 / 14**
- Paired simpler-vs-stage comparison available: **1 / 14**
- Paired comparison explicitly blocked by one recoverable object: **2 / 14**

## Paired predictive stress test

- Paired simpler-vs-stage comparisons that reach final plant fitness: **1**
- Positive stage-specific gain, non-confirmatory: **1**
- Paired model nulls (different from biological endpoint nulls): **0**

Current paired positive IDs: PHA_PARKINSONIA.
Current paired model null IDs: none.
Separate biological endpoint null IDs: PHA_POSLEDOVICH2015, PHA_LATHYRUS_LONGTERM.

Only Parkinsonia supplies a source-level paired stage/filter model diagnostic, and it is retrospective rather than confirmatory. Posledovich and long-term Lathyrus are independent biological endpoint/pathway boundaries, not failed M5-vs-M2/M4 predictive model comparisons.

## Candidate states

| Candidate | Interaction | Raw/adult timing | Effective consumer timing | Pre-final filter | Phase varies | Final endpoint | Paired comparison | Status | Blocker |
|---|---|---|---|---|---|---|---|---|---|
| PHA_IWE032 | antagonist | blocked | yes | yes | yes | yes | blocked | near_confirmatory | numeric 2012-2014 female flight timing |
| PHA_KULA2012 | mixed_pollinating_seed_predator | partial | yes | yes | yes | no | partial | mechanism_only | final post-cost plant reproduction absent in Chapter 3 |
| PHA_POSLEDOVICH2015 | antagonist | yes | yes | yes | yes | yes | no | boundary_null | no paired simpler-vs-stage prediction comparison; final response is mature-seedpod escape not viable-seed count |
| PHA_LATHYRUS_LONGTERM | antagonist | partial | no | yes | yes | yes | no | boundary_null | no measured delayed consumer-stage timing or paired simpler-vs-stage predictive comparison |
| PHA_PARKINSONIA | antagonist | partial | partial | partial | yes | yes | yes | paired_realized_positive | realized oviposition rather than independent adult timing; pre-final filter is parasitism/hatch rather than a host-specific phase coordinate |
| PHA_DIANTHUS | mixed_pollinating_seed_predator | no | partial | partial | yes | yes | no | final_landscape_no_alignment | independent adult timing and explicit delayed-stage coordinate absent |
| PHA_GLOCHIDION | mixed_pollinating_seed_predator | yes | yes | yes | no | yes | no | stage_structure | phase lag does not vary as a tested predictor |
| PHA_TROLLIUS | mixed_pollinating_seed_predator | partial | yes | partial | yes | partial | no | mechanism_only | no variance-bearing final plant-fitness comparison across stage-timing classes |
| PHA_IWE031 | antagonist | yes | partial | yes | yes | yes | no | host_sensitivity_final | not a delayed phase-lag design and no natural adult-window comparator |
| PHA_HURLBURT2004 | mixed_pollinating_seed_predator | yes | partial | partial | yes | yes | blocked | near_confirmatory | mature-fruit records not yet source-linked to marked flowering date/cohort |
| PHA_AUCUBA_IMAI | antagonist | yes | yes | yes | yes | yes | no | host_sensitivity_final | host tissue calibration and final-fate experiment are not measured on the same units |
| PHA_WU2015_WHEAT_MIDGE | antagonist | yes | yes | yes | yes | yes | no | host_sensitivity_final | source design contains no cultivar-varying stage-free adult-only comparator |
| PHA_WISE2015_WHEAT_MIDGE | antagonist | yes | partial | yes | yes | yes | no | host_sensitivity_final | no paired calendar/adult-only versus stage-specific predictive comparison; public abstract lacks full timing-group table |
| PHA_RIEMER2024 | antagonist | yes | no | no | yes | yes | partial | paired_adult_host_positive | no measured larval stage/filter and no adult-only or held-out-year comparison |

## Interpretation

There is currently **no positive confirmatory-ready programme** showing that a stage-specific coordinate predicts final plant fitness better than a simpler calendar or adult-only coordinate.

IWE032 Cardamine already contains a positive stage-specific phase-to-final-fate contrast; its remaining blocker is the numeric 2012–2014 female-flight coordinate needed for the paired adult-vs-stage comparison. Hurlburt 2004 Yucca remains the second near-confirmatory route, blocked by the mature-fruit join key. Aucuba-Asphondylia independently provides direct adult monitoring, experimental oviposition timing, a mechanistically defined host-tissue window, and final seed-producing versus gall fate, but lacks the paired simpler-vs-tissue-stage predictive comparison.

Parkinsonia-Penthobruchus now provides an independent positive paired realized diagnostic: among seven matched region-season rows, annual ground-pod egg density correlates only moderately with final seed predation (r=0.476), stage-matched egg density after the vulnerable pod pulse improves the association (r=0.596), and filtering that stage-matched exposure by observed parasitism and hatch raises it to r=0.938; leave-one-region-out RMSE falls from 20.58 to 19.93 to 4.92 percentage points. Relative to the annual-exposure comparator, stage matching alone reduces held-out RMSE by only **3.2%**, whereas the full filtered effective-exposure coordinate reduces it by **76.1%**; the additional gain from stage-matched to filtered exposure is **75.3%**. Thus the current positive is driven mainly by estimating which ovipositions become viable future consumers, not by temporal stage matching alone. Region blocking is required because three regions contribute repeated seasons. Because the exposure is realized oviposition rather than independent adult timing, and the filter is consumer/parasitoid survival rather than a host-specific phase coordinate, this remains non-confirmatory.

Aucuba-Asphondylia adds a strong experimental host-window-to-final-fate test: adult emergence is monitored directly, attack timing is manipulated within the adult season, and complete gall induction that eliminates seed production drops from 80.9% before the host tissue window closes to 8.8% after it closes. Wheat-midge evidence adds two independent positives: Wu 2015 combines independently monitored adult occurrence with an experimentally identified susceptible ear-emergence stage and final yield loss across >400 cultivars; its 2012 synchronization-yield-loss panel gives r=0.935,p=0.005. However, the paper's second predictor—adult catch accumulated during each cultivar's ear-emergence interval—is also stage-conditioned, so Wu lacks a true stage-free adult-only comparator by design. Wise 2015 directly shifts adult exposure across spike development and finds lower final seed damage/yield loss with later exposure. None yet supplies the paired simpler-vs-stage predictive comparison required for confirmatory_ready.

Riemer 2024 adds a distinct field-scale adult-host positive: 88 pea fields with independently measured first male moth arrival and host flowering show a lower final damaged-seed LOOCV RMSE for a moth-by-flowering model (7.36 percentage points) than for a flowering-only model (9.20). This is field-wise leave-one-out across four years, not leave-one-year-out; no adult-only or consumer-stage/filter comparator is fitted. Accordingly it does not increment the confirmatory-ready or paired effective-stage counts.

The registry separately retains two biological boundaries. Posledovich 2015 reports host-species-only effects on mature-seedpod escape among analyzed transferred hosts despite host-stage effects on larval performance; it did not compare predictive timing models or measure all-plant viable seed number. In the 21-year Lathyrus study, variation in flowering-date–seed-predation covariance did not significantly explain variation in flowering-time selection; non-significance does not establish an exactly zero pathway. Neither study is a paired-model predictive null.

Accordingly, stage-specific timing now has a positive paired realized comparison as well as final-seed-loss examples, but **predictive superiority over simpler adult/calendar timing under the full confirmatory contract remains open**.
