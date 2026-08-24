# Chart selection

Choose an encoding from both the figure contract and the observed data structure. A data shape alone does not determine the scientific argument.

## Required recommendation record

Before rendering, provide:

```yaml
recommended_chart: ...
evidence:
  - contract fact or profiler fact
assumptions:
  - unresolved but non-blocking assumption
alternatives:
  - chart: ...
    use_when: ...
risks:
  - possible interpretation or rendering risk
rejected_options:
  - chart: ...
    reason: ...
```

Do not use an unexplained chart name as the decision. Do not describe a heuristic as proof that a chart is scientifically correct.

## Goal and data-shape routes

| Goal | Typical data structure | Strong starting point | Important checks |
|---|---|---|---|
| Show a distribution | one quantitative variable | ECDF, histogram, dot/strip, box or violin plus observations | sample coverage, bin/bandwidth sensitivity, censored values |
| Compare groups | categorical condition plus quantitative response | raw observations plus interval or distribution summary | independent replicate, paired/repeated structure, uncertainty definition |
| Show a relationship | two quantitative variables | scatter or density/hexbin for dense data | nonlinear structure, grouping, measurement error, overplotting |
| Show change over an ordered axis | time/dose/order plus response | points/line with interval when continuity is justified | missing visits, repeated measures, interpolation implied by lines |
| Show composition | parts with a meaningful whole | aligned or 100% stacked bars | denominator, ordering, negative values, too many categories |
| Show a matrix or field | two dimensions plus values | heatmap/image with explicit normalization | center, limits, missing/out-of-range colors, cell geometry |
| Show estimates and uncertainty | named estimates plus intervals | dot-and-whisker or forest plot | interval type, multiplicity, reference line, ordering |
| Show many variables | multivariate observations | selected pair views, correlation matrix, dimensionality-reduction result | selection rationale, scaling, method provenance, information loss |

These are starting points, not mandatory templates.

## Scientific-meaning checks

- Treat identifiers as identifiers even when they are numeric.
- Do not infer that repeated rows are independent replicates.
- Distinguish paired, nested, repeated, and independent observations before aggregating or connecting points.
- Name the estimator and uncertainty. Do not choose a statistical test silently.
- Show raw observations when feasible, especially when summaries may hide distribution shape.
- Distinguish missing, zero, censored, excluded, and out-of-range values.
- State transformations and the treatment of zero or negative values on log-like scales.
- Preserve continuous variables unless the scientific question requires bins; record bin edges and sensitivity.

## Encoding risks

- **Bars and areas:** normally require a meaningful zero because length or area encodes magnitude.
- **Lines:** imply order or continuity; do not connect unrelated categories or missing observations silently.
- **Box/violin/KDE:** can imply distribution structure unsupported by sparse data; expose observations and label limitations.
- **Error bars:** are uninterpretable without SD, SE, CI, percentile, posterior interval, or another named definition.
- **Dual axes:** can manufacture apparent agreement; prefer aligned panels and justify any exception.
- **Area/size:** map data to area, not radius or diameter.
- **Color:** match qualitative, sequential, diverging, or cyclic semantics; add a redundant cue when color distinguishes categories.
- **3D:** avoid decorative perspective and occlusion for ordinary quantitative comparisons.

## Responding to a requested chart

If the requested chart is defensible, use it and document the mapping. If it presents a material interpretation risk:

1. state the risk using the supplied data/contract;
2. recommend a safer primary encoding;
3. offer the requested chart as an explicitly caveated alternative when it remains possible; and
4. stop only when producing it would misrepresent the data or require an unresolved scientific decision.

Do not block a chart solely because a sample count crosses a universal numeric threshold. Present observed group sizes and explain the relevant estimation risk.

## Multi-panel routing

Use panels when one figure supports several linked questions. Give every panel one primary job, keep shared mappings stable, and identify a narrative reading order. Split the figure when different claims, incompatible scales, or dense legends prevent a reliable comparison.

The decision record is provisional until the rendered figure passes numeric, textual, and visual review.
