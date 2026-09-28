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

## Systematic coverage gate

The initial system-family searches above remain a targeted discovery phase. They are not, by themselves, an exhaustive systematic-review denominator.

All paper-level claims about the prevalence or scarcity of qualifying evidence require the machine-readable search-run registry:

`data/registry/search_runs.csv`.

The minimum required coverage plan contains:

- Web of Science Core Collection: mutualist, antagonist, and mixed query families;
- Scopus: mutualist, antagonist, and mixed query families;
- ProQuest Dissertations & Theses (or an explicitly documented equivalent grey-literature index): one broad all-interaction query;
- backward and forward citation chaining from every `include`/`unresolved` publication plus every P1/P2 completion-route anchor, repeated until one full iteration yields no newly eligible source.

OpenAlex is registered as supplementary triangulation. It does not replace the required broad bibliographic indexes or dissertation search.

### Search limits

The required searches use:

- no lower publication-year cutoff;
- no exclusion based on effect direction, significance, or result size;
- no a priori taxonomic restriction beyond the plant–animal interaction scope of IWE;
- no language restriction at discovery. Non-English records may be retained as unresolved until enough information can be translated/adjudicated.

Any source-specific filters required by a database interface must be recorded in the exact `source_query` or run notes.

### Search-run immutability

Each executed search receives a stable `run_id`.

A completed run must record:

1. exact database/source;
2. exact source query;
3. run date;
4. raw result count;
5. exported record file;
6. completed deduplication status.

If a query is materially changed after execution, the old run remains in the registry and a new `run_id` is created. Historical search runs are not overwritten to make the search appear prospectively cleaner.

### Deduplication

Deduplication is performed after export.

Preferred identity order:

1. normalized DOI;
2. another stable source identifier;
3. normalized title + publication year + first author when no stable identifier exists.

A publication found by multiple search runs remains one screening record but retains provenance to every contributing run in the eventual search export/provenance table.

### Coverage claim ceiling

`docs/SEARCH_COVERAGE_STATUS.md` is generated from the run registry.

Until every row marked `coverage_requirement = required` has:

- `status = completed`; and
- `dedup_status = complete`;

the project search status is `targeted_only`.

While status is `targeted_only`, IWE may report the structure of its current targeted corpus and exact completion blockers, but it must not:

- call the search exhaustive/systematic-complete;
- report registry fractions as prevalence estimates for the entire literature;
- claim that no additional eligible studies exist outside the current corpus.

When all required runs are complete, the status becomes `systematic_ready`; this changes the permissible search-coverage claim, not the biological H1 result.
