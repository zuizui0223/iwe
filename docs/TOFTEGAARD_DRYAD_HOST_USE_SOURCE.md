# Independent Anthocharis host phenology observation data — source gate

The previous IWE × chocho spatial audit (PR #112) decomposes potential
WCVP/HOSTS resource geography of Anthocharis cardamines. It does NOT measure
actual use of these host plants or temporal matching. This new workflow
tests retrieval of a distinct observational dataset (Toftegaard et al. 2018,
Dryad DOI 10.5061/dryad.jp328r6).

The Dryad landing page identifies 'Plant phenology in the field.txt'
(~2.76 MB), covering host plant phenophases and butterfly egg/larval
observations from Sweden 2010–2013, plus sampling site areas. First
acquire raw source and freeze sha256, bytes, line count, and encoding.
Raw data are uploaded as an ephemeral Actions artifact and deliberately
NOT committed before schema/permissions/sampling units are audited.

Expected next methodological gates after a successful download:

- Inspect delimiter, headers, field units, missingness, repeated plant/
  transect/site/year records, and observation effort.
- Define direct observed oviposition/larval use against independent
  host stage, with covariates host identity, region, season and effort.
- Ensure eggs and larvae remain *outcomes*, never independent adult
  butterfly activity used to construct a strict IWE timing exposure.
- Do not treat zero eggs per plant as known absence of adults; do not
  claim geographic expansion from these Swedish local observations.
- IWE strict H1 still lacks independently measured focal Dibbinsdale
  2012–2014 female capture/recapture event DOYs and same-unit final
  plant reproduction. Swedish 2010–2013 observations do not rescue that gate.

The acquisition workflow makes NO biological findings; if the public
file download is blocked, the receipt records that explicit blocker.
