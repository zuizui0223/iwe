# IWE strict-evidence blockers — current execution queue

Date: 2026-09-19  
Status: **execution queue; not an ecological evidence ranking**

The primary H1 gate is still `coverage_only` on the current Fisher-z common scale:

- mutualist: 1 independent programme;
- antagonist: 1 independent programme;
- mixed pollinating seed predator: 1 independent programme.

The broader source-native strict corpus now has **three** closed mutualist programmes (IWE001, IWE029, IWE084), one antagonist programme, and one mixed programme. IWE084 closes a published source-native SMD but does not increase the Fisher-z common-scale count. The most valuable next work is therefore an **independent published antagonist or mixed programme**, not another mutualist source-native effect merely because it is easier to recover.

Machine-readable source:

- `data/registry/strict_blockers.csv`

Executable ranking:

```bash
python scripts/build_strict_blocker_queue.py
```

## Newly closed since the previous queue

### IWE084 — mutualist — Solidago graminifolia × Apis mellifera

The published 1980 seasonal Apis record prospectively orders source-defined early and late clone groups. Source Table-5/Table-10 natural filled-seed means, 95% confidence intervals and clone sample sizes were reconstructed on the source angular scale and registered as:

- Hedges `g = +1.1401607637`;
- sampling variance `= 0.1497495743`;
- `n = 37` clones;
- effect family `standardized_mean_difference`.

The reconstruction is executable and CI-locked. It closes a third independent source-native mutualist programme but is deliberately **not** converted to Fisher-z to change the common-scale gate.

## Priority 1 — can directly change the present replication gate

### IWE067 — antagonist — Ipomopsis × Hylemya

**Gate value:** closes a second published antagonist programme if recovered.

The biological estimand, subset, outcome, dependence structure and Fisher-z calculation are already frozen and implemented in:

- `docs/EXTRACTION_IWE067.md`
- `src/iwe/iwe067.py`
- `scripts/reconstruct_iwe067.py`

The only remaining blocker is raw-data materialization. The required Dryad files are publicly indexed, but all tested anonymous download routes currently return authorization/anti-bot responses rather than the raw files.

**Do not spend effort redesigning the analysis.** The next valid action is only to obtain the two source files through a legitimate public/source-authorized route and execute the frozen reconstruction unchanged.

### IWE059 — mixed — Ficus pertusa × pollinating fig wasps

**Gate value:** closes a second independent mixed programme if a strict effect can be recovered.

The published study combines crop receptivity/attractiveness timing, temporal pollinator abundance, visitation and final seeds/fig, making it unusually close to the strict mixed estimand.

The current blocker is source-level quantitative recovery: a crop-level timing-to-final-seed effect with uncertainty or raw data is not yet in hand. Wiley and older author-upload routes are inaccessible from the execution environment; a current author-profile attachment route is being probed separately.

If only visitation or early-attraction narrative effects can be recovered, IWE059 must move to `context_only` rather than being used to fill the mixed class.

### IWE035 — antagonist — Helianthus × seed-feeding herbivores

**Gate value:** can close an independent published antagonist programme if a direct timing/enemy-exposure to final-fitness coefficient plus sampling uncertainty is recovered.

The paper clearly establishes seasonal enemy structure and a herbivory-mediated flowering-time selection pattern, but current public material exposes the mediation logic rather than a registered synchrony effect with variance.

Do not substitute:

- a flowering-date coefficient from a model omitting herbivory;
- a P-value category;
- damage alone for final plant fitness.

If the original tables/raw data do not yield the required effect, close the record as timing context.

### IWE086 — mutualist — Polemonium × bee pollinators

This remains technically priority 1 in the machine queue because it could close another independent published mutualist programme, but it is **not** the current biological bottleneck after IWE084. JSTOR returns challenge HTML and the ESA/Wiley route is Cloudflare-blocked. Keep the frozen timing contract, but do not spend disproportionate effort on it while antagonist and mixed classes remain at one programme each.

## Priority 2 — useful independent replication, but farther from numerical closure

Published candidates currently requiring original tables, temporal group uncertainty or data joins include:

- `IWE071` — Carduus thoermeri × Rhinocyllus; weekly weevil incidence and developed seeds/head, original week-level uncertainty missing;
- `IWE072` — Carduus pycnocephalus × Rhinocyllus; seed production extends beyond oviposition window, before/after group uncertainty missing;
- `IWE074` — salt-marsh perennial community × consumer guild; seasonal consumer curve + seed set, source tables inaccessible;
- `IWE075` — Scheelea/Attalea × Caryobruchus; crop-level oviposition and surviving-seed data not recovered;
- `IWE008`, `IWE022`, `IWE027` — independent mutualist programmes that can improve common-scale replication once quantitative effects are recovered.

These are worth pursuing after the highest-value routes above or when a source becomes newly accessible.

## Priority 3 — do not mistake technical availability for primary-gate value

### IWE078

The Zenodo dataset-only Oenothera × Mompha programme has already been reconstructed:

- Experiment 1: `n=20`, `r=+0.3154846465`, `z=+0.3266246773`;
- Experiment 2: `n=59`, `r=-0.0536505789`, `z=-0.0537021436`.

It remains provisional because no corresponding formally published research article has been verified under `docs/SOURCE_ELIGIBILITY.md`. Its numerical sign cannot be used to decide source admission.

### IWE002

Recovering more Corydalis data may improve precision but does **not** create an independent programme because it overlaps the IWE001 research programme. It therefore cannot by itself move the cross-class replication gate.

### IWE066

This is an H2 curvature problem, not H1 replication. Its interior peak is biologically important, but recovering day-specific means/uncertainty does not change the current H1 programme count.

## Closed false leads

The following recently looked promising but have now been adjudicated rather than left indefinitely unresolved:

- `IWE011` — raw HUSCAP files contain flowering totals, oviposition totals and final fruit fitness, but no time-resolved partner activity curve; closed as timing context.
- `IWE028` — direct temporal escape/attack evidence, but no observed final-fitness effect at the strict matched grain; closed as timing context.
- `IWE079` — unusually direct Tomares–Astragalus synchrony mechanism and final RSI, but detailed synchrony is available for only two patch-level units; no defensible study-level effect variance; closed as context.
- `IWE087` — four Rhododendron plots have matched peak-flowering Bombus visitation and natural fruit set, but the prospectively frozen deterministic PDF-vector extraction could not recover exact plot means; manual/raster digitization was not substituted.

These records strengthen the evidence-architecture diagnosis and should not be repeatedly reopened simply because primary replication is sparse.

## Execution rule

The queue ranks **recoverability × independent-programme gate value** only. It does not rank ecological importance, effect strength, publication quality or whether a study supports the preferred H1 direction.

A null, opposite-sign or heterogeneous recovered effect is just as valid for closing a programme as a supportive effect.
