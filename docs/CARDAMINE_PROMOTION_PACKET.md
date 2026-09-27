# Cardamine transactional promotion packet

Date: 2026-09-27  
Candidate: `ANT002_CARDAMINE_ANTHOCHARIS_2024` / study `IWE032`  
Status: executable draft builder; never mutates the evidence registry

## Purpose

Cardamine is intentionally split into two stages:

1. **preflight** — source-backed adult timing + frozen plant timing/outcome rules produce candidate SMD rows;
2. **promotion** — only after preflight succeeds, construct the coordinated repository changes needed for strict-H1 admission.

Promotion cannot be a one-file append. A valid transition must update four linked objects together:

- `data/extraction/direct_effects.csv`;
- `data/registry/strict_h1_adjudications.csv`;
- `data/registry/replication_candidates.csv`;
- `data/registry/replication_completion_routes.csv`.

## Transaction simulated by the builder

For every estimable year × ecotype × direction Cardamine contrast, the builder drafts a strict Tier-A SMD effect with:

- study: `IWE032`;
- dependence: `DEP_CARDAMINE_DIBBINSDALE_2012_2014`;
- timing: `seasonal_position / strict_window / ordered_by_measured_window`;
- direction: synchrony, represented separately as `core_flight - early_refugium` or `core_flight - late_refugium`;
- outcome: `realized_reproductive_fraction`;
- effect family: `standardized_mean_difference`.

It then simulates:

- replacing `ADJ_IWE032_PENDING` with one exact `eligible + strict_extracted` adjudication per effect row;
- changing `ANT002_CARDAMINE_ANTHOCHARIS_2024` from blocked to `ready`, with `smd_summary_stats=yes`;
- removing that candidate from the completion queue;
- renumbering remaining completion routes within each interaction class.

## Transactional validation

Before emitting the packet, the virtual post-promotion state is checked with the existing validators:

- full combined effect table;
- effect ↔ adjudication consistency;
- full replication-candidate ledger;
- completion routes against the updated candidate ledger;
- study registry, including `IWE032 = include`.

An existing effect-ID collision or stale pending/route structure fails closed.

## Provenance firewall

A promotion packet cannot be built from a synthetic adult-timing manifest.

The adult timing manifest must be real/source-backed and pass the Cardamine provenance contract. The builder therefore cannot turn the CI synthetic fixture into biological evidence.

## Outputs

`scripts/build_cardamine_promotion_packet.py` writes:

- `timing_exposure.csv`;
- `outcome_smd_audit.csv`;
- `draft_direct_effects_append.csv`;
- `draft_strict_adjudications_append.csv`;
- `draft_strict_adjudications_after.csv`;
- `draft_candidate_ready_row.csv`;
- `draft_replication_candidates_after.csv`;
- `draft_completion_routes_after.csv`;
- `promotion_manifest.json`.

The manifest explicitly states `direct_repo_mutation_performed = false`.

## What the packet does not authorize

The packet is not itself evidence admission. It does not:

- edit any repository registry;
- change claim status;
- merge Cardamine into the primary corpus;
- override source verification;
- create an SMD when no predeclared year × ecotype × direction contrast is estimable;
- pool early and late phenological refugia into one comparator.

A human/source audit of the recovered adult timing object and normalized plant outcomes is still required before applying the draft transaction.
