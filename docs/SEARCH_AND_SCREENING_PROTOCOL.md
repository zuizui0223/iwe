# Search and screening protocol

## Scope

Search for empirical plant–animal studies linking phenological synchrony, overlap, mismatch, timing difference, or timing manipulation to a quantitative plant reproductive outcome.

## Initial search strata

The initial candidate universe explicitly includes:

1. Hadena–Caryophyllaceae nursery pollination;
2. Epicephala–Phyllanthaceae nursery pollination;
3. Tegeticula/Parategeticula–Yucca nursery pollination;
4. Agaonidae–Ficus pollination;
5. Chiastocheta–Trollius pollination/seed predation;
6. Greya–Lithophragma pollination/seed use;
7. specialist/generalized pollination mismatch systems;
8. florivore and predispersal seed-predator systems with matched timing and reproduction.

Searches may admit systems outside these strata if they meet the same criteria.

## Primary inclusion criteria

A Tier-A record requires all of:

- quantitative plant reproductive or lifetime-fitness outcome;
- direct phenological timing exposure or experimental timing manipulation;
- timing exposure and outcome matched to the same biological context;
- focal animal role classifiable as `mutualist`, `antagonist`, or `mixed_pollinating_seed_predator`;
- information sufficient to recover an effect estimate and sampling variance;
- recoverable exposure direction so the effect can be oriented as greater synchrony.

## Exclusions from primary analysis

Exclude from Tier A, while retaining separately when useful:

- visitation only;
- pollinia removal/pollen deposition without final reproductive outcome;
- oviposition or attack without final reproductive outcome;
- species-level flowering month paired with regional animal occurrence without matched interaction evidence;
- GBIF/iNaturalist/herbarium/museum occurrence-derived overlap;
- narrative claims lacking recoverable effect or variance;
- timing and outcome measured in incompatible populations or years.

## Screening workflow

Each publication receives a stable `study_id`. Each independently extractable dataset/experiment receives `dataset_id`. Screening records must preserve DOI or another source identifier, candidate interaction system, decision (`include`, `context_only`, `exclude`, `unresolved`), reason, and reviewer/status metadata.

No paper is excluded because its result is null, adverse, or biologically inconvenient.

## Dependence rule

The preferred evidence unit is `plant × partner × population/site × year/season × outcome`. Multiple rows from one publication, species pair, site, year, or experiment remain dependent unless the source supports independence. Every admitted effect therefore carries both `study_id` and `dependence_id`.