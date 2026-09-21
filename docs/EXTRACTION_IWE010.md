# IWE010 extraction/adjudication receipt — Kudo & Shibata 2021

Source: Kudo G, Shibata A. 2021. *Is increased male flower production a strategy for avoidance of predispersal seed predation in andromonoecious plants?* Ecology and Evolution 11:5646–5656. DOI `10.1002/ece3.7468`.

Archived data: Dryad DOI `10.5061/dryad.b5mkkwhcq`.

Status: direct antagonist phenology evidence; **strict-H1 quantitative extraction remains unresolved pending a final-fitness reconstruction from the archived data**.

## Phenological design

Nine *Peucedanum multivittatum* populations were surveyed across a snowmelt/flowering gradient in the Taisetsu Mountains during 2017–2019.

Early plots flower mainly in July, intermediate plots in late July–August, and late plots after mid-August. The specialist moth *Phaulernis fulviguttella* concentrates oviposition in mid- to late July.

The plot gradient therefore provides a biologically ordered partner-activity window: early flowering overlaps the predator season more strongly, while late flowering escapes it.

## Why the published fruit-number model is not the strict outcome

At the young-fruit stage, fruit number was recorded **before intensive predation damage**. Fruits that were later predated were deliberately included because the authors intended this variable to represent pollination success.

Therefore the published fruit-number / fruit-set response is not final reproductive performance after antagonist damage.

The paper separately records seed-predation damage, but an attack response alone is also not sufficient for the IWE strict plant-fitness estimand.

## Raw-data route

For 2018 and 2019, mature fruits were harvested and intact versus predated fruits were counted. The public Dryad workbook contains reproductive data for 2017–2019 and therefore may permit a direct reconstruction of intact mature fruit production along the flowering/predator timing gradient.

That reconstruction has not been completed here because the workbook contents were not retrievable through the current execution environment.

## Executable adjudication

The pending component is registered as:

- `strict_h1_status = unresolved`;
- `quantitative_status = pending`;
- `timing_metric_type = seasonal_position`;
- `timing_analysis_class = strict_window`;
- `timing_domain = ordered_by_measured_window`;
- anticipated effect family: `standardized_mean_difference`.

No IWE010 effect row is added to `data/extraction/direct_effects.csv`.

Any future row must use `DEP_PEUCEDANUM_KUDO_PROGRAM`.

## Claim boundary

IWE010 establishes a strong antagonist timing mechanism and a public route to final-fitness reconstruction.

It does not justify using the published pre-predation fruit-set model as a final reproductive effect, and it is not counted as an independent programme replicate from IWE011.
