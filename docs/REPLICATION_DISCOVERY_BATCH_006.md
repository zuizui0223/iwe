# Mixed replication discovery batch 006 — public same-programme near-misses

Date: 2026-09-26  
Target: second independent `mixed_pollinating_seed_predator` SMD cluster  
Decision: no new strict-H1 cluster; three high-plausibility public routes adjudicated and closed

## Purpose

The two active mixed P1 routes, Hurlburt 2004 and Rentería/Cantú, now depend on archival linkage data. This batch therefore asked a narrower question:

> Can a fully public, independent nursery-pollination programme provide an independently measured partner window, a prospectively orderable plant timing contrast, final post-cost plant reproduction, and SMD-compatible variance without inventing a join?

Three systems looked unusually promising because each had at least two of those components in public sources.

## 1. Lithophragma bolanderi × Greya politella — Gross et al. 2023

Source: Gross et al. 2023, *Ecology*, DOI `10.1002/ecy.4043`.  
Data: Dryad DOI `10.5061/dryad.jm63xsjg6`.

### What passes

The 2017 programme directly censused adult *Greya* floral visitors repeatedly through the flowering season at two sites. It also collected natural capsules and counted developing seeds, undeveloped ovules, eggs, larvae and partly eaten seeds. Thus adult partner activity and post-cost seed outcomes are both genuinely measured.

### Why it fails strict timing

The capsule outcome sample is organized as site/month collections. The published design does not assign each capsule-producing plant to a flowering date or flowering cohort on the measured *Greya* activity curve.

Therefore an apparent contrast such as "site/month with more Greya versus site/month with fewer Greya" would be a partner-abundance/context contrast, not a prospectively defined plant–partner synchrony contrast.

Decision: `rejected_timing`, DROP.

## 2. Breynia oblongifolia × Epicephala spp. — Finch Richmond programme

Core sources:

- Finch et al. 2018, DOI `10.1186/s12862-018-1314-y`;
- Finch et al. 2019, DOI `10.1111/een.12754`;
- Finch et al. 2021, DOI `10.1186/s12862-021-01889-4`;
- public Figshare adult-observation and herbivory datasets cited by those papers.

### What passes

The Richmond programme directly observed adult *Epicephala* through time. The 2019 study independently measured a biologically appropriate final plant endpoint: net seed production per mature fruit after subtracting seeds consumed by pollinators and other seed herbivores, with crop-level means/SE and fruit-level public data.

This initially looked like an unusually strong same-programme rescue.

### Why it still fails strict timing

The mature fruits in the final-seed study were haphazardly collected from plants during broad crop periods. They were not tagged at flowering or pollination and then followed to mature seed output.

That missing longitudinal link is especially consequential in this system. The same Richmond programme later showed that female flowers can persist for months, remain previously pollinated, contain diapausing *Epicephala*, and subsequently begin fruit development when current adult moths and male flowers are absent.

Therefore:

`mature-fruit collection date != flowering/pollination synchrony date`.

Aligning a fruit crop collected in March/April to adult moth abundance observed in March/April would reuse calendar coincidence as a timing join that the biological system explicitly breaks.

Decision: `rejected_timing`, DROP.

## 3. Ficus pumila × Wiebesia spp. — Liu et al. 2014

Source: DOI `10.1371/journal.pone.0097783`.

### What passes

This is strong direct phenological evidence. The study measured receptive fig crops, adult pollinator emergence/flight, and showed that a partial autumn crop had few available pollinators and mostly aborted. It therefore resolves the former screening uncertainty about whether synchrony matters biologically.

### Why it does not supply the frozen mixed net-fitness surface

*Ficus pumila* is dioecious. Female trees provide the seed-reproduction surface. Pollinator larvae develop in male figs, where the host pays the nursery-pollination seed/ovule cost and produces pollinator offspring.

The plant benefit and nursery cost are therefore sex-separated rather than jointly observed on one final reproductive surface comparable to the admitted mixed systems.

A female-fig abortion contrast is a pollination-availability effect, not the net benefit-minus-seed-predation outcome required for the current `mixed_pollinating_seed_predator` primary estimand.

Decision: `rejected_other`, DROP. IWE019 moves from `unresolved` to `context_only`.

## Consequence

No public-source shortcut closed mixed #2 in this batch.

The active mixed queue remains:

1. Hurlburt 2004 — recover date-stamped flowering/adult-moth observations linked to marked final reproduction;
2. Rentería/Cantú — recover mature-fruit provenance linking final viable/damaged seeds to flowering date/cohort;
3. Bopp 2003/2004 — P2 conditional; long-form source must add both independent adult activity and final plant reproduction;
4. USGS 2022–2023 Joshua tree — P2 source-release watch.

The value of batch 006 is negative but operationally important: adult activity and final reproduction existing somewhere in the same programme is not enough. The plant timing unit that generated the final reproductive observation must itself be orderable against the independently measured partner window.
