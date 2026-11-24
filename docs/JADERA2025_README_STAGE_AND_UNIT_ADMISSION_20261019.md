# Jadera 2025: pollination and seed predation are real, but their time and biological units differ

*New, independent mixed ecological programme* for IWE exploration:
Comerford, Carroll & Egan (2025), *A New Twist on an Old Story:
Pollination and Seed Predation in Jadera haematoloma*,
American Naturalist **206**, 179–191,
[DOI 10.1086/736460](https://doi.org/10.1086/736460).
Authors publicly describe this as the **first Hemiptera**
(piercing-sucking bug) identified in the pollinating seed-predator
guild, expanding beyond classical moth-based brood-site pollination.

Original study archive:
[Dryad DOI 10.5061/dryad.2bvq83c2b](https://doi.org/10.5061/dryad.2bvq83c2b),
publicly displayed source README and per-file experimental descriptions,
first issued 2025-05-29. The archive metadata/README describe **five
laboratory and field experiment components**, not five independent
plant-fitness programmes.

## What the original **public source README** actually establishes

| Component | Original biological unit | Benefit or cost endpoint | Why it is not strict flowering synchrony–net fitness |
|---|---|---|---|
| Pollen on bug proboscis | 40 individual bugs | Acquired pollen after nectar feeding on *Cardiospermum* / *Koelreuteria* | Proxy for vector potential, no plant final fitness |
| Greenhouse pollination | **48 plants** nested in **16 mesh tents** (3 plants per tent) | Seedpods / flowers over seven weekly censuses on *Cardiospermum halicacabum* | Treatment stocked with five adult females per bug tent, no independent wild-adult seasonal census; developing pods were deliberately **removed** within first week to keep bugs nectar-feeding, preventing same-unit subsequent seed predation/terminal viability measurement |
| Field pollination | 51 inflorescence branches across 2018–2019 on *Koelreuteria elegans* | Seedpod formation after exclusion versus three adult female bugs experimentally stocked in bags | Adult exposure is imposed rather than independent natural flight; branch-level source outcome is a pollination proxy, not measured final viable seeds or linked offspring damage |
| Nectar and adult longevity | Individual bugs nested in mortality-assay replicates | Adult days to death under nectar versus water | Laboratory adult survival is not contemporaneous adult flight at flowering |
| Offspring seed predation | Seeds nested in assay/arena and pots | Binary germination after **0–4 nymphs per seed**; README reports 30 seeds per dose, 80-day germination observation | Seed viability dose-response is on separate experimental seeds with no matching pollinated plant/flower IDs or natural exposure-date history |

**Critical distinguishing fact from the primary article:** new seedpods
in the controlled greenhouse pollination treatment were *intentionally
removed within their first developmental week*, making the measured
benefit specifically a **pollination-service potential** under
experimental prevention of subsequent seed consumption. The separate
germination assay quantifies **seed-cost potential**. Their observed
benefit/cost effects cannot be algebraically spliced into a single
plant's *net realized intact mature seed output*. In the field, bagged
adult bugs were added around peak host flowering, rather than counted
as a naturally varying independent adult activity curve.

The README's `Greennhouse_time.zip` (original spelling) contains a
`Time` variable defined as a **one-week greenhouse sampling period**.
It is not an independent measurement of Jadera flight overlap and must
not be reinterpreted as a contemporary wild-adult-availability time
series.

The observed effects establish that one herbivore species can
deliver pollination service and later damage seeds, even if
the realized *net* effect across ontogenetic stages is not measured
in a single host-specific, tagged plant trajectory. This is a useful
ecological counterexample to treating all piercing-sucking
seed predators as exclusively antagonistic, **not an eligible
second strict-H1 mixed class effect**.

## Source retrieval integrity and limits, 2026-10-19

A real GitHub Actions runner queried the exact official Dryad
dataset DOI and obtained the public dataset metadata and
original file listing (version `/api/v2/versions/367420`).
The bulk original dataset download returned **HTTP 401**;
all nine version-issued original file downloads returned
HTTP **401** through the file API and **403** through the
official file-stream route. The source retrieval workflow's
success means **the audit executed**; it does **not** mean
any original CSV bytes were obtained.

Therefore actual source row-level counts, model coefficients,
experiment effects, archive checksums of actual CSV bytes and
an original plant ID merge **remain unverified**. Quantities above
were taken from the openly displayed **author-supplied README**,
not a recovered ZIP. We do not describe this as a raw source data
analysis, invent a Hedges g or assign a missing observation date.

Exactly recorded transport status:
`scripts/probe_jadera2025_dryad_source.py` and source-only
[GitHub Actions run 39203486485](https://github.com/zuizui0223/iwe/actions/runs/39203486485).

## Finite, no-contact admission rule and useful next question

Strict H1 needs **independently measured adult partner availability**,
contemporaneous flowering exposure on the correct host and
**same biological unit** direct terminal surviving reproductive
fitness with coherent source n and sampling variance. No available
source description establishes that combination for these
separate Jadera experiments, even if archive access resumes.

A broader, **separate from H1** research question is whether
the *temporal ordering of floral service and offspring cost*,
combined with removal/abscission of ovules or seedpods,
creates a **timing-dependent switch from mutualism to antagonism**.
Jadera provides convincing independent biological motivation,
but direct net-payoff tests require a future experiment retaining
pollinated pods, tracking offspring damage and the final viable
seed crop of those exact tagged flowers, rather than repurposing
the separate lab assays.

Do not contact the authors, submit access requests or
silently promote a source blocked by 401/403.
The machine-readable source/estimator gate is
`data/source_reconstructions/jadera2025_benefit_cost_unit_matrix.csv`.

**Frozen strict-H1 independent clusters remain**
mutualist 2, antagonist 0, mixed 0. This Jadera programme
is a genuine independently described mixed *biological
interaction*, not independently recoverable class-level
synchrony→net-fitness evidence.
