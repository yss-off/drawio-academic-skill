# Figure contract

Use this contract before choosing a chart. It is a compact reasoning record, not a form the user must fill in.

## Minimum contract

Record, or infer and label:

1. **Scientific question** — the question the figure must answer.
2. **Communication goal** — comparison, distribution, relationship, trend, composition, uncertainty, or another explicit goal.
3. **Intended claim** — the conclusion the figure is expected to support; mark it as a hypothesis when the data have not established it.
4. **Evidence** — source paths or identifiers, variable meanings and units, and the unit of independent replication.
5. **Data handling** — filtering, transformation, aggregation, normalization, exclusions, missing/censored values, and uncertainty definition.
6. **Destination** — manuscript, supplement, web, slide, poster, or exploratory review. Record the exact journal and final width when known.
7. **Panel plan** — optional; for each panel, state its unique question and evidence contribution.

Do not invent unknown fields. Separate facts, user-provided choices, inferences, and unresolved items.

## Trigger behavior

- If the question or chart is clear, infer the contract, state material assumptions, and continue.
- If the user only supplies data and asks to “plot it,” ask one question: what scientific question should the figure answer?
- When reviewing an existing figure, infer the contract from the figure, data, caption, and manuscript context. Ask only when ambiguity could change the interpretation.
- For a cosmetic-only edit, preserve the existing contract unless the edit changes scientific meaning.

## Blocking conditions

Stop and ask only when:

- the scientific question cannot be inferred;
- variable meaning, unit, or replication ambiguity could change interpretation;
- a required data source is missing or unreadable; or
- filtering, transformation, exclusion, missing-data, or uncertainty ambiguity could change the conclusion.

Missing journal, final width, or palette is non-blocking. Use a clearly labeled provisional general profile and keep the live-verification item open.

## Multi-panel evidence check

For each proposed panel, record:

```text
panel_id: question -> evidence -> contribution to intended claim
```

Remove redundant panels only after confirming that they do not carry distinct evidence. Do not suppress inconvenient results to simplify the narrative.

## Compact output template

```yaml
scientific_question: ...
communication_goal: ...
intended_claim:
  text: ...
  status: hypothesis | supported_by_supplied_analysis | descriptive_only
data_sources: [...]
variables:
  - name: ...
    meaning: ...
    unit: ...
replication_unit: ...
data_handling:
  transformations: [...]
  missing_and_exclusions: ...
  uncertainty: ...
destination:
  medium: ...
  journal: known value | pending
  final_width: known value | pending
panel_plan: []
assumptions: []
blocking_questions: []
```

This structure guides reasoning and provenance. It does not certify the scientific claim.
