# Screening batch 003 — backward search from phenology reviews

Date: 2026-09-17
Status: discovery screening; no new quantitative H1 effect admitted yet

## Search anchors

This batch used two prior syntheses as backward-search anchors:

- Elzinga et al. 2007, *Time after time: flowering phenology and biotic interactions* (`10.1016/j.tree.2007.05.006`), which explicitly contrasts pollinator and predispersal-seed-predator selection on flowering phenology;
- Munguía-Rosas et al. 2011, *Meta-analysis of phenotypic selection on flowering phenology suggests that early flowering plants are favoured* (`10.1111/j.1461-0248.2011.01601.x`), whose supplement contains source-level effect sizes and references for flowering time/synchrony selection.

The 2011 meta-analysis is important prior art but does not estimate IWE's primary object. It meta-analyzes phenotypic selection on plant flowering time or among-plant flowering synchrony. IWE instead requires temporal matching between a plant and a biologically identified interaction partner and asks whether the reproductive effect of that matching differs among interaction roles.

## IWE035 — Helianthus annuus × seed-feeding herbivore guild

Source: Pilson 2000, DOI `10.1007/PL00008838`.

Decision: `unresolved_strict`; highest-priority antagonist extraction.

Why it matters:

- flowering date varies genetically;
- seasonal abundance/damage patterns were documented for five seed-feeding herbivores;
- damage by `Haplorhynchites aeneus`, `Homoeosoma electellum`, and `Suleima helianthana` is highest early and declines through the flowering season;
- `Gymnocarena diffusa` shows the opposite seasonal pattern and `Smicronyx` damage is approximately constant;
- damage by `Haplorhynchites`, `Homoeosoma`, and `Suleima` reduces plant fitness;
- selection analysis including `Homoeosoma` and `Suleima` damage removes the apparent directional selection on flowering date, whereas omitting damage yields selection for later flowering.

This is much closer to IWE's strict antagonist target than studies that measure only flowering date and final damage. However, the currently recovered source material does not expose a single overlap/synchrony coefficient and sampling variance on the IWE common scale. It therefore remains unresolved rather than being admitted by inference from mediation.

## IWE036 — Vaccinium hirtum multi-agent counterselection

Source: Mahoro 2002, DOI `10.1139/b01-136`.

Decision: `context_only` / multi-agent evidence.

Four Kyoto subpopulations were followed for two years. Individual flowering rank and among-plant synchrony, fruit set, hand-pollination response, flower predation and predispersal seed predation were measured. Early-flowering plants can be pollen limited, while later plants can experience stronger weevil/fly predation. Importantly, conspecific flowering synchrony itself did not consistently correlate with fruit set or predation.

This is excellent evidence that mutualists and antagonists can impose counteracting seasonal selection, but it does not provide a common plant-partner overlap variable for either interaction role.

## IWE037 — Chamaerops humilis × Derelomus chamaeropsis

Source: Dufay 2010, DOI `10.1111/j.1420-9101.2010.01968.x`.

Decision: `context_only` mixed/nursery-pollination evidence.

The study directly monitored flowering of male and female palms and emergence of the specific nursery pollinator. Female fruit production was pollen/pollinator limited and late female anthesis improved matching to the end of male anthesis. However, nursery costs and benefits are distributed asymmetrically between sexes: larvae develop in male inflorescences whereas female plants receive pollination without supporting larval development.

It therefore cannot yet provide one individual-level net mixed fitness effect, even though it is highly informative about how timing changes the mutualism's cost/benefit structure.

## IWE038 — Ipomopsis aggregata long-term matched benefit/cost programme

Source: Campbell et al. 2022, DOI `10.1111/1365-2745.13875`.

Decision: `context_only` / multi-agent evidence.

Thirteen flowering seasons across 21 years combine pollen-limitation experiments, predispersal seed-predation experiments and demographic data. Full pollination and seed-predator removal both affect seed production, but neither pollen limitation nor seed predation changed detectably with snowmelt date.

This is unusually strong matched benefit/cost evidence and supplies valuable null information. It does not, however, identify a plant-pollinator or plant-predator synchrony exposure; snowmelt/year is the focal external axis.

## IWE039 — sunflower crop-wild phenology and seed predation

Source: Cummings et al. 1999, DOI `10.1007/s004420050936`.

Decision: `context_only` antagonist timing.

Flowering date was the strongest consistent predictor of some seed-damage classes, with peak damage in late August/early September and few wild plants flowering at those peak times. Crop-wild hybrids flowered earlier and experienced much greater predispersal damage.

The study is close to a timing-window design but partner activity is represented mainly through damage timing rather than an independently observed insect activity curve, and final fecundity is treated in linked papers. It is therefore retained for dependence-aware contextual synthesis rather than strict H1.

## IWE040 — sequential Vaccinium congeners

Source: Mahoro 2003, DOI `10.1023/A:1023203325501`.

Decision: `context_only` / multi-agent evidence.

The study compares sequentially flowering congeners under pollinator, flower-predator and seed-predator effects. It is a useful test of the proposed early-flowering pollen-limitation versus late-flowering enemy-exposure tradeoff, but species differences and multiple interacting agents prevent a single partner-synchrony effect.

## Main diagnosis after batch 003

The strict-antagonist literature is not simply absent. Rather, many of its strongest studies identify an enemy-mediated selection pathway by combining:

`flowering date -> seasonal enemy damage -> final fitness`

instead of measuring one explicit plant–enemy overlap metric.

IWE035 is the strongest current candidate for bridging that gap because enemy seasonality and final fitness were measured in the same focal population. It remains unresolved only because a recoverable common-scale quantitative effect has not yet been obtained.

## Next steps

1. Continue source recovery for IWE035, prioritizing original tables/data over secondary summaries.
2. Use the full source lists of Elzinga 2007 and Munguía-Rosas 2011 as finite backward-screening universes rather than open-ended keyword hunting.
3. Freeze a prospective search-completion and holdout rule before interpreting class imbalance as a systematic literature result.
4. Keep multi-agent counterselection systems in a separate evidence map rather than forcing them into mutualist or antagonist H1 rows.
