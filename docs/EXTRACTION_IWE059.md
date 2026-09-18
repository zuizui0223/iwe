# IWE059 extraction receipt — Ficus pertusa × pollinating fig wasps

Source: Anstett MC, Kjellberg F, Bronstein JL. 1996. *Waiting for wasps: consequences for the pollination dynamics of Ficus pertusa L.* Journal of Biogeography 23:459–466. DOI `10.1111/j.1365-2699.1996.tb00007.x`.

Status: **unresolved strict-H1 candidate**.

## Why this differs from most mixed studies

The source combines in one biological programme:

- timing/stage of fig crop receptivity and attractiveness;
- temporal variation in pollinator abundance;
- pollinator visitation to crops;
- mature seed production per fig;
- pollinator offspring production per fig.

The abstract reports that crops attracting wasps earlier in development are the most heavily visited but mature the fewest pollinator offspring and seeds per fig. Field observations are combined with simulation models explaining preferential early visitation by temporal variation in pollinator abundance.

This makes IWE059 unusually close to the strict IWE chain:

```text
partner temporal availability × crop receptivity
-> visitation
-> seeds per fig
```

## Why no effect is entered yet

The accessible source does not expose a single registered overlap/mismatch coefficient with sampling variance. It is not valid to convert statements about `earlier attractiveness`, `heavier visitation`, or `fewer seeds` into a standardized timing effect without recovering the underlying crop-level data or source model coefficients.

The original analysis also includes fig size and extended receptivity; any reconstructed timing effect must preserve those design features rather than attributing all seed variation to synchrony.

## Required recovery

Admit IWE059 to strict H1 only if source tables/data permit one of:

1. a crop-level continuous measure of temporal position relative to pollinator abundance with seeds per fig and recoverable uncertainty;
2. a defensible more-matched versus less-matched crop contrast with means, SD/SE and sample sizes;
3. a source regression coefficient/correlation linking the registered timing exposure to seed production.

If only stage-of-attraction or visitation effects can be recovered, move the record to timing/context rather than inventing a strict effect.


## Public-source recovery audit — 2026-09-19

The quantitative blocker is now explicitly an **access/source-data blocker**, not a missing search lead.

Verified public records include:

- the peer-reviewed Journal of Biogeography article and DOI;
- University of Arizona publication metadata;
- a ResearchGate author-uploaded full-text record;
- Marie Charlotte Anstett's CNRS Academia profile, which exposes a current `Download free PDF` action.

Multiple source-authorized/public attachment routes were tested from the execution environment:

1. an older Academia attachment route;
2. the current Academia attachment `attachments/86305960/download_file?s=profile`;
3. a profile-session + cookie + referrer request to that current attachment;
4. the indexed ResearchGate author-upload route;
5. the Wiley publisher PDF route.

The current Academia route and the older author-upload routes return managed anti-bot/Cloudflare HTML rather than the PDF; the publisher route does not expose a machine-retrievable open full text. The responses are validated by content type/body and are not misclassified as source data.

No crop-level raw dataset, supplementary table, institutional full-text mirror, or source regression coefficient has yet been recovered from an accessible repository.

### Locked next action

Do **not** continue trying alternate query parameters against the same Academia/ResearchGate attachment endpoints. IWE059 can advance only through a genuinely different source route, such as:

- an institutional/author repository mirror containing the article or tables;
- archived source data;
- supplementary material with crop-level timing and seed output;
- a source-reported timing coefficient plus uncertainty.

Until one of those appears, IWE059 remains `unresolved_strict` with blocker type `fulltext_or_source_data_access`.

## Dependence

Any crop-level estimates from the study share the same six-year `Ficus pertusa` research programme and must be clustered under one publication/programme dependence identifier.

## Claim ceiling

At present the study supports:

> seasonal pollinator abundance and fig crop receptivity jointly structure visitation, seed production and pollinator reproduction in an obligate nursery-pollination mutualism.

It does not yet contribute a quantitative strict-H1 meta-analysis row.
