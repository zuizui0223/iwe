# Stage-specific phase-alignment confirmatory gate

_Generated from data/registry/phase_alignment_candidates.csv; do not edit counts by hand._

## Current gate

- Candidate programmes/components: **13**
- Dependence clusters: **13**
- Confirmatory-ready positive or null comparisons: **0**
- Near-confirmatory blocked routes: **2**
- Registered direct null/boundary comparisons: **2**
- Positive paired realized comparisons (non-confirmatory): **1**

A programme is confirmatory_ready only when it has source-backed raw/adult timing, effective consumer timing, a pre-final host filter, variation in phase alignment, a final plant endpoint, and a paired simpler-vs-stage-specific timing comparison.

## Evidence coverage

- Final plant endpoint present: **11 / 13**
- Phase/alignment varies: **12 / 13**
- Paired simpler-vs-stage comparison available: **3 / 13**
- Paired comparison explicitly blocked by one recoverable object: **2 / 13**

## Candidate states

| Candidate | Interaction | Raw/adult timing | Effective consumer timing | Pre-final filter | Phase varies | Final endpoint | Paired comparison | Status | Blocker |
|---|---|---|---|---|---|---|---|---|---|
| PHA_IWE032 | antagonist | blocked | yes | yes | yes | yes | blocked | near_confirmatory | numeric 2012-2014 female flight timing |
| PHA_KULA2012 | mixed_pollinating_seed_predator | partial | yes | yes | yes | no | partial | mechanism_only | final post-cost plant reproduction absent in Chapter 3 |
| PHA_POSLEDOVICH2015 | antagonist | yes | yes | yes | yes | yes | yes | boundary_null | none; retained as null |
| PHA_LATHYRUS_LONGTERM | antagonist | partial | no | yes | yes | yes | yes | boundary_null | delayed consumer-stage timing not measured as a phase coordinate |
| PHA_PARKINSONIA | antagonist | partial | partial | partial | yes | yes | yes | paired_realized_positive | realized oviposition rather than independent adult timing; pre-final filter is parasitism/hatch rather than a host-specific phase coordinate |
| PHA_DIANTHUS | mixed_pollinating_seed_predator | no | partial | partial | yes | yes | no | final_landscape_no_alignment | independent adult timing and explicit delayed-stage coordinate absent |
| PHA_GLOCHIDION | mixed_pollinating_seed_predator | yes | yes | yes | no | yes | no | stage_structure | phase lag does not vary as a tested predictor |
| PHA_TROLLIUS | mixed_pollinating_seed_predator | partial | yes | partial | yes | partial | no | mechanism_only | no variance-bearing final plant-fitness comparison across stage-timing classes |
| PHA_IWE031 | antagonist | yes | partial | yes | yes | yes | no | host_sensitivity_final | not a delayed phase-lag design and no natural adult-window comparator |
| PHA_HURLBURT2004 | mixed_pollinating_seed_predator | yes | partial | partial | yes | yes | blocked | near_confirmatory | mature-fruit records not yet source-linked to marked flowering date/cohort |
| PHA_AUCUBA_IMAI | antagonist | yes | yes | yes | yes | yes | no | host_sensitivity_final | host tissue calibration and final-fate experiment are not measured on the same units |
| PHA_WU2015_WHEAT_MIDGE | antagonist | yes | yes | yes | yes | yes | no | host_sensitivity_final | source design contains no cultivar-varying stage-free adult-only comparator |
| PHA_WISE2015_WHEAT_MIDGE | antagonist | yes | partial | yes | yes | yes | no | host_sensitivity_final | no paired calendar/adult-only versus stage-specific predictive comparison; public abstract lacks full timing-group table |

## Interpretation

There is currently **no positive confirmatory-ready programme** showing that a stage-specific coordinate predicts final plant fitness better than a simpler calendar or adult-only coordinate.

IWE032 Cardamine already contains a positive stage-specific phase-to-final-fate contrast; its remaining blocker is the numeric 2012–2014 female-flight coordinate needed for the paired adult-vs-stage comparison. Hurlburt 2004 Yucca remains the second near-confirmatory route, blocked by the mature-fruit join key. Aucuba-Asphondylia independently provides direct adult monitoring, experimental oviposition timing, a mechanistically defined host-tissue window, and final seed-producing versus gall fate, but lacks the paired simpler-vs-tissue-stage predictive comparison.

Parkinsonia-Penthobruchus now provides an independent positive paired realized diagnostic: among seven matched region-season rows, annual ground-pod egg density correlates only moderately with final seed predation (r=0.476), stage-matched egg density after the vulnerable pod pulse improves the association (r=0.596), and filtering that stage-matched exposure by observed parasitism and hatch raises it to r=0.938; leave-one-region-out RMSE falls from 20.6 to 19.9 to 4.9 percentage points. Region blocking is required because three regions contribute repeated seasons. Because the exposure is realized oviposition rather than independent adult timing, and the filter is consumer/parasitoid survival rather than a host-specific phase coordinate, this remains non-confirmatory.

Aucuba-Asphondylia adds a strong experimental host-window-to-final-fate test: adult emergence is monitored directly, attack timing is manipulated within the adult season, and complete gall induction that eliminates seed production drops from 80.9% before the host tissue window closes to 8.8% after it closes. Wheat-midge evidence adds two independent positives: Wu 2015 combines independently monitored adult occurrence with an experimentally identified susceptible ear-emergence stage and final yield loss across >400 cultivars; its 2012 synchronization-yield-loss panel gives r=0.935,p=0.005. However, the paper's second predictor—adult catch accumulated during each cultivar's ear-emergence interval—is also stage-conditioned, so Wu lacks a true stage-free adult-only comparator by design. Wise 2015 directly shifts adult exposure across spike development and finds lower final seed damage/yield loss with later exposure. None yet supplies the paired simpler-vs-stage predictive comparison required for confirmatory_ready.

The registry also retains complete nulls. Posledovich 2015 shows that manipulated stage matching and temperature alter herbivore performance without altering the mature-seedpod escape endpoint beyond host-species effects. The long-term Lathyrus programme shows that climate-driven changes in phenology–seed-predation covariance do not explain flowering-time selection on intact-seed fitness.

Accordingly, stage-specific timing now has a positive paired realized comparison as well as final-seed-loss examples, but **predictive superiority over simpler adult/calendar timing under the full confirmatory contract remains open**.
