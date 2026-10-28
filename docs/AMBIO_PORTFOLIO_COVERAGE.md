# The frozen 11-host chocho source misses part of locally observed egg use

Source: Navarro-Cano et al. 2015, Ambio Table 1, open DOI
https://doi.org/10.1007/s13280-014-0602-z

This is a **taxonomic/source coverage audit** extending the separate
Ambio observational bridge in PR #115. It is NOT a reanalysis of new
field records, an additional independent programme, a general bias
estimate for all 239 chocho butterfly species, or a phenological
mechanism test.

Across the 547 observed Anthocharis eggs on seven reported host taxa
from Sweden's 2010 survey:

- 200 eggs (36.56%) were on three host species exactly present in
  chocho's frozen resolved 11-host species portfolio;
- 245 eggs (44.79%) were recorded on *Cardamine paludosa*, which the
  source explicitly separates as an octoploid C. pratensis ssp.
  paludosa cytotype rather than the tetraploid C. pratensis ssp.
  pratensis sampled in separate source rows; and
- 102 eggs (18.65%) were on three separately identified taxa not in
  the specific frozen chocho host portfolio: *Arabis hirsuta* (66),
  *Arabidopsis thaliana* (16), *Thlaspi caerulescens* (20).

A counterfactual **taxonomic-grain upper accounting sensitivity**
that groups the separately reported octoploid under the broad
C. pratensis species complex would make 445/547 (81.35%) source
eggs associated with that expanded name/portfolio class. This
is NOT an asserted correction of chocho's host IDs, a new
WCVP distribution, or an additional sampled host species.

The source's three region-specific strict match fractions are
South 36/110 (32.7%), Central 67/194 (34.5%), and
North 97/243 (39.9%). The regional denominators count eggs, not
independent oviposition events or insect individuals. The same
co-occurring source programmes from 2010 likely overlap Oikos 2018,
so do not treat them as a second independent cluster.

**Scientific implication:** The frozen HOSTS × WCVP network is a
source-defined, incomplete set of accepted larval host identities
relative to these observed Swedish eggs. Because missed documented
hosts can change the reconstructed resource geography, results based
on the 11-host union are **conditional on the source's host portfolio**.
The observation neither quantifies global undercount nor negates the
already reported 162/272/110 source-bound geography.

No phenology stage or independent adult butterfly flight dates
have been recovered. The external Toftegaard field-file gate in
PR #113 remains draft/blocked. No IWE strict-H1 fitness evidence
and no chocho GEB manuscript changes are promoted.

Reproduce:

    python scripts/audit_ambio_portfolio_coverage.py --out-dir outputs/ambio-coverage

The output includes regional strict matching, host-taxon egg
accounting and hashes of the pinned inputs. Tests require total
547 = 200 + 245 + 102 and fail if absent regional plants
are silently assigned zero.
