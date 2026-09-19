# Database-query syntax correction — 2026-09-19

## Scope

This note records an implementation correction to the frozen IWE database-search protocol before any screening decisions are made from the corrected result inventory.

The biological concepts, interaction classes, search cutoff (`2026-09-17`), inclusion rules and stopping rules are unchanged.

## OpenAlex correction

The original OpenAlex registry serialized each concept family as a whitespace-separated list, for example:

`phenology synchrony mismatch overlap ... seed predation ... fitness reproduction`

OpenAlex Boolean search treats words not separated by Boolean operators as `AND`. Therefore the serialized query required essentially every synonym to occur in the same work and produced diagnostic counts of zero for the antagonist and mixed families.

The intended frozen protocol in `docs/SEARCH_COMPLETION_RULE_V1.md` was instead:

`(timing synonym 1 OR timing synonym 2 ...) AND (interaction synonym 1 OR ...) AND (fitness synonym 1 OR ...)`.

On 2026-09-19 the OpenAlex rows in `data/registry/frozen_database_queries.csv` were corrected to encode those already-frozen concept groups explicitly with uppercase `OR` and `AND`.

No synonym was added because of a returned result and no synonym was removed because it produced an inconvenient result.

## PubMed diagnosis

A live syntax audit showed that the original mutualist PubMed query is translated correctly by PubMed and returned hundreds of records. The earlier stored diagnostic count of zero was therefore not a biological result.

The audit also encountered HTTP 429 after several rapid requests. The count utility is corrected to:

- omit the unnecessary `rettype=count` mode and request `retmax=0` JSON search metadata;
- preserve the original PubMed query strings;
- retry HTTP 429 using `Retry-After`/backoff;
- fail closed on unrecovered HTTP/API errors rather than writing zero;
- pause between requests to respect the unauthenticated E-utilities request limit.


## OpenAlex field-scope correction

After the Boolean/CSV correction, a diagnostic count using OpenAlex's default `search=` endpoint returned tens of thousands of records per broad interaction family. This exposed a second API-equivalence issue before corrected records were screened.

The frozen PubMed strategies explicitly search `Title/Abstract`. Current OpenAlex default work search covers title, abstract **and full text**, whereas OpenAlex provides `title_and_abstract.search` for the equivalent restricted field.

The operational OpenAlex count/inventory therefore uses:

`title_and_abstract.search:<frozen Boolean concept expression>`

together with the original publication-date cutoff.

This changes only the database field implementation so that the two engines search comparable bibliographic text. It does not add/remove biological concepts based on study outcomes.

## Status of earlier counts

The first count artifact containing PubMed `0/0/0` and OpenAlex `34/0/0` is retained only as an implementation diagnostic. It is not a systematic-review result and must not be used to declare any search component complete.

Only counts and inventories produced after this correction may satisfy component B of `data/registry/search_completion_status.csv`.

## Independence from study outcomes

This correction was triggered by impossible/implausible search diagnostics and documented API semantics, not by the direction or significance of any IWE effect.

Corrected database results remain subject to the same prospective deduplication and screening rules as all other search records.
