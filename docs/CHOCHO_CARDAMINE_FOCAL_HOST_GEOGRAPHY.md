# IWE × chocho: Cardamine focal-host geography audit

## Question

Of the 110 added butterfly-level WGSRPD3 resource units for Anthocharis
cardamines in the frozen chocho analysis, how many are covered by the
contemporary range of the single focal host Cardamine pratensis, and
how much of this coverage is shared with other accepted larval hosts?

## Data, exact reconstruction and code

This audit uses the same frozen source identities as chocho:

- chocho commit df6f920a37c7e86a878d9f6375bb4454128b5d66;
- HOSTS mirror commit 808e0b869f9ec1adf8efff87cf6a395adda103e0;
- rWCVPdata/WCVP v13 commit 65bed76bae9d644ccb6ad200c05f9f5071d89e05.

The workflow at .github/workflows/chocho-focal-host-audit.yml checks
out these identities, runs chocho's own
scripts/build_wcvp_hosts_null_sidecars.R, and then calls
scripts/analyze_chocho_cardamine_geography.py.

Reconstructed whole-butterfly union areas MUST match exactly
the pinned chocho 239-species metric row (162 native, 272 contemporary,
110 added). The source check fails rather than changing baselines.

## Meaning of outputs

1. focal_host_geography_receipt.json — species-wide resource counts,
   source-specific confirmation status and focal-host attribution counts;
2. host_contributions.csv — all accepted host species, individual native
   and contemporary footprints and their contributions to newly added
   butterfly-level resource units;
3. new_resource_units.csv — WGSRPD3 unit codes added after retaining the
   introduced distribution of known hosts, with focal-host coverage and
   exclusive/shared support.

The four estimates are deliberately distinct:

- Focal host introduced geography: contemporary focal host units minus
  native focal host units.
- Marginal coverage: newly added butterfly-wide units where the focal
  host is present in the contemporary host range.
- Exclusive coverage: subset of the above with NO other eligible host.
- Fractional attribution: each added butterfly unit gives 1/k credit
  to each of its k eligible contemporary hosts. The credits across all
  host species reconcile to the 110 added butterfly units.

If the exact plant pair is absent in the source-specific HOSTS-WCVP
sidecar, focal counts remain null (unverified), not zero (ecological
absence). The published literature does document the plant-butterfly
relationship independently: Davies and Saccheri 2024,
DOI 10.1002/ece3.11330; Cowley et al. 2001,
DOI 10.1046/j.1365-2656.2001.00509.x.

## Scientific limits

A WCVP regional host range is an opportunity envelope, not an
egg observation, adult flight-time estimate, actual occupied
butterfly range or host invasion-caused range expansion.
No temporal overlap or IWE strict-H1 fitness effects are inferred.
The missing source-backed 2012-2014 female flight dates from
the Dibbinsdale Cardamine programme are still a hard blocker
for its original independent-adult-window SMD contrast.

Next stage: map the WGSRPD3 added units to independent
year-specific host phenophase and adult-flight observations,
accounting for sample effort, climatic differences and year/region
dependence before testing temporal filtering.
