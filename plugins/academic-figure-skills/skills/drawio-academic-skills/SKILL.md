---
name: drawio-academic-skills
description: "Publication-figure overlay for draw.io. Use instead of drawio whenever the diagram is for a paper, thesis, dissertation, journal, conference, IEEE/ACM submission, manuscript, camera-ready, Word/LaTeX figure, or other publication. Compares complex layout plans, retrieves license-tracked local examples, records figure manifests, and applies venue, figure-type, color, caption/legend, formula, and paper-readability gates for architecture, workflow, roadmap, network-topology, and replicated paper figures."
license: MIT
metadata:
  category: visual-design
  tags:
    - drawio
    - academic
    - paper-figure
    - ieee
    - thesis
    - manuscript
    - workflow
    - math
    - svg
allowed-tools: Read, Write, Bash, AskUserQuestion
---

# Draw.io Academic Overlay

Create, edit, replicate, validate, and export publication-ready draw.io figures by applying academic policy on top of the sibling Draw.io Base Skill. This overlay is intentionally thin: it owns academic policy/gates, academic docs, and paper examples; the sibling base at `../drawio` owns all shared execution (CLI, schema, renderer, themes including `academic`/`academic-color`, references, examples, style presets, Desktop export).

## Required Sibling Base

Resolve shared resources relative to this overlay directory:

- CLI `../drawio/scripts/cli.js`; URL fallback `../drawio/scripts/runtime/diagrams-net-url.js`
- Schema `../drawio/assets/schemas/spec.schema.json`; themes `../drawio/assets/themes/`; palettes `../drawio/assets/palettes/`
- References `../drawio/references/docs/`, `../drawio/references/official/`, `../drawio/references/workflows/`, `../drawio/references/examples/`; shared rework contract `../drawio/references/workflows/visual-review.md`
- Built-in style presets `../drawio/styles/built-in/`

Overlay-local assets: `references/docs/publication-overlay.md`, `academic-figure-playbook.md`, `closed-loop-scientific-figure-checklist.md`, `academic-export-checklist.md`, `layout-candidates-and-manifest.md`, `references/reference-index.json`, `references/examples/`, `references/templates/`, `assets/schemas/figure-manifest.schema.json`, and `scripts/` planning/evidence helpers.

If `../drawio/scripts/cli.js` is missing, stop and report that the sibling base skill must be installed next to this overlay; never silently recreate or vendor-copy base resources into the overlay.

## Non-Negotiable Contract

- Keep academic authoring YAML-first and offline-first. Never create, require, or route through `.mcp.json`, MCP, or a live backend.
- Always deliver `.drawio` as the editable source. Select one primary delivery class from `academic-figure-playbook.md § Academic Delivery Matrix`: `raster-publication` for Word/thesis/raster-first use, `vector-submission` for venue vector delivery, or `draft-preview` for review without a fixed publication target. Do not declare PNG or SVG a universal final default.
- Keep `.spec.yaml`, `.arch.json`, raw YAML, and diagnostics in a project-local work directory such as `.drawio-tmp/<name>/`, unless the user explicitly asks for a reproducible sidecar bundle beside the final output.
- Perform visual self-checks on the selected delivery class's exported primary artifact. Do not substitute an ad hoc browser preview for that artifact. Browser rasterization may produce the final PNG under the derivative gate; preserve the editable source and preview SVG, record provenance, and never treat the review screenshot itself as publication evidence.
- Use the sibling base `../drawio/references/workflows/visual-review.md` for preview structure, issue records, YAML-first rework, and stopping rules; this overlay adds only publication checks.
- Treat external image-generation previews as optional concept previews only. They never replace YAML, artifacts, sidecars, or exported-artifact verification.
- Do not create or modify scratch JS scripts under a user's project-local `.agents/skills/drawio`; port durable fixes to the sibling base skill source instead.

## Academic Preflight

Before generating or editing, determine and state: venue/audience; figure type (`architecture`, `roadmap`, or `workflow`); primary delivery class; color policy; caption/legend/title, formula, terminology/abbreviation, and text-fidelity needs; export expectations. If the publication target is unknown, use `draft-preview` and report that publication delivery is unresolved. Estimate the **node budget** (authoritative targets, thresholds, and split strategies: `references/docs/academic-figure-playbook.md § Node Budget Management`); over target, confirm a split/simplify strategy with the user and start from the compact patterns in `references/templates/`. For complex, ambiguous, multi-loop, paper-derived, or reference-redraw tasks, query the local reference index and compare 2–3 structured layout plans before authoring final YAML. Full decision detail: `references/docs/publication-overlay.md § Required Academic Decisions` and `references/docs/layout-candidates-and-manifest.md`.

### Palette Preflight

After the venue is known, if the user did not specify a palette, use `AskUserQuestion` as a single-select: venue recommendation first with `(Recommended)`, 3-4 choices, each palette's `displayName` as the label, and colorblind/grayscale safety plus venue rationale in each description. Venue map: `references/docs/academic-figure-playbook.md § Venue Palette Mapping`.

If the user already specified a palette or an unambiguous style, map it directly and do not ask. For academic replication, preserve the source palette and skip selection unless the user explicitly requests normalization. Record the chosen name in `meta.palette`. The completion report must name the palette and its colorblind/grayscale safety flags, including any print-gate downgrade.

## Source Understanding

Extract only what the figure needs from papers, reference images, or text-only prompts; keep uncertainties explicit. See `references/docs/publication-overlay.md § Source Understanding` and `references/docs/academic-figure-playbook.md § Scientific Figure Patterns`.

## Diagram Plan Gate

For complex paper-derived figures or academic image-replication work, present 2–3 concise, structurally distinct layout plans and wait for one selection before detailed YAML/rendering; simple academic diagrams may skip the gate. Candidates must preserve the same scientific inventory and expose their reading axis, use-when condition, and main risk. For every non-primary or ambiguous arrow, include `source --relation--> target` so direction and loop closure are reviewable before layout. Workflow: `references/docs/layout-candidates-and-manifest.md`; source template: `references/docs/publication-overlay.md § Diagram Plan Gate`.

## Optional Image Preview

Only after the diagram plan is confirmed, and only with privacy approval before sending unpublished or sensitive content; treat generated text as approximate and correct final labels/formulas/geometry in YAML. Full rules: `references/docs/publication-overlay.md § Optional Image Preview`.

## Task Routing

Choose one route, then load only its files. `overlay` = this directory; `base` = the sibling, resolved from this directory.

- `academic-create` — paper, thesis, IEEE, manuscript, journal, publication-ready figure → overlay `references/docs/publication-overlay.md`, `academic-figure-playbook.md`, `academic-export-checklist.md`; for feedback, fallback, retry, or multi-loop figures also load `closed-loop-scientific-figure-checklist.md`; base `../drawio/references/workflows/create.md`
- `math-formula` — formula, equation, LaTeX, AsciiMath, MathJax, 公式 → base `../drawio/references/docs/math-typesetting.md`, `design-system/formulas.md`
- `edit` — modify an academic bundle or imported `.drawio` → base `../drawio/references/workflows/edit.md`, `../drawio/references/docs/migration-readiness.md`
- `replicate` — redraw screenshot, image, SVG, or reference paper figure → overlay `references/docs/publication-overlay.md`; base `../drawio/references/workflows/replicate.md`, `../drawio/references/docs/design-system/specification.md`, `color-guide.md`
- `base-capabilities` — code/config/live imports, raster extraction, multi-page bundles, AI/SysML/BPMN stencils, or offline postprocess before publication checks → base `../drawio/references/docs/upstream-capability-compatibility.md`; overlay `references/docs/publication-overlay.md`
- `stencil-heavy` — academic cloud, network, AWS, Azure, GCP, Cisco, Kubernetes figure → base `../drawio/references/docs/stencil-library-guide.md`, `ieee-network-diagrams.md`, `../drawio/references/official/xml-reference.md`
- `style-preset` — learn/use/list/delete/rename visual style presets → base `../drawio/references/docs/style-extraction.md`, `style-presets.md`, `../drawio/styles/built-in/`
- `planning-evidence` — compare layout candidates, query bundled references, or initialize/build/validate a figure manifest → overlay `references/docs/layout-candidates-and-manifest.md`, `references/reference-index.json`, `scripts/`
- `direct-xml-exception` — tiny handoff-only XML or exact mxGraph control → base `../drawio/references/upstream/pure-drawio-skill.md`, `../drawio/references/official/xml-reference.md`

## Academic Defaults

For academic-paper requests, set these before rendering:

```yaml
meta:
  profile: academic-paper
  figureType: architecture # architecture | roadmap | workflow
  theme: academic # or academic-color when color is acceptable
  palette: okabe-ito # from venue preflight; ieee-bw for IEEE print
  title: Caption-ready title
  description: One sentence explaining the figure intent
  legend: Required when symbols, colors, line styles, or icons need explanation
  print: { target: cn-thesis } # optional gate: cn-thesis | ieee-single | ieee-double
```

Primary deliverables:

- every class: `<name>.drawio`
- `raster-publication`: 300ppi-effective `<name>.png`; prefer Desktop, otherwise use the source-preserving browser derivative gate
- `vector-submission`: `<name>.pdf` or an SVG whose text is converted to paths; for IEEE use an accepted PS/EPS/PDF path
- `draft-preview`: live-text `<name>.svg`, explicitly labeled preview/intermediate rather than publication-final

Intermediate work directory:

- `<name>.spec.yaml`, `<name>.arch.json`, raw or normalized YAML, diagnostics

Record the selected class in `manifest.contract.delivery_class`. Honor extra formats requested by the user, but keep one primary class and do not upgrade a preview into publication evidence.

## Create Flow

1. Classify the figure as `architecture`, `roadmap`, or `workflow`; for complex tasks, query `scripts/reference_index.py`, generate 2–3 plans with `scripts/layout_candidates.py`, and select one before detailed rendering.
2. Initialize `.drawio-tmp/<name>/<name>.manifest.json` with `scripts/figure_manifest.py`; record the contract, reference IDs, candidates, and selection reason.
3. Freeze the approved semantic contract before layout work: stable node/edge IDs, exact labels, `source --relation--> target`, line-style meaning, branch conditions, formulas, and abbreviations. Treat later spacing/routing repairs as geometry-only unless the user separately approves a content change.
4. Draft or normalize the YAML spec as the canonical source; shorten labels before shrinking fonts.
5. Validate and render through the sibling base CLI, then self-check the exported artifact and build the final manifest before reporting:

```bash
node ../drawio/scripts/cli.js input.yaml figure.drawio --validate --write-sidecars --sidecar-dir .drawio-tmp/figure --strict-warnings
# draft-preview
node ../drawio/scripts/cli.js input.yaml figure.svg --validate
# raster-publication when Desktop is available
node ../drawio/scripts/cli.js input.yaml figure.png --validate --use-desktop
# vector-submission when Desktop is available
node ../drawio/scripts/cli.js input.yaml figure.pdf --validate --use-desktop
```

Figure-type patterns: `references/docs/academic-figure-playbook.md`.

## Edit and Replicate Flow

- Edit the `.spec.yaml` sidecar first; if only `.drawio` exists, import via the base CLI (`--input-format drawio --export-spec`).
- For image/SVG replication, preserve text boxes, captions, legends, formulas, edge labels, baseline/offset, font family/size/italic state, alignment, and spacing when visible; use explicit `bounds` for standalone text/formula blocks and `labelOffset` for connector labels off the line.
- Keep regenerated files on the same basename for round-trippable artifacts and sidecars.

## Export Policy

Use the playbook delivery matrix as the single selection authority. For `raster-publication`, verify effective resolution and the final embedded document; for `vector-submission`, export PDF or path-only SVG explicitly and apply venue restrictions; for `draft-preview`, deliver SVG without claiming publication completion. Without the required exporter, generate a diagrams.net URL and report the blocked publication artifact honestly:

```bash
node ../drawio/scripts/cli.js input.yaml figure.pdf --validate --use-desktop
node ../drawio/scripts/runtime/diagrams-net-url.js figure.drawio
```

## Style Presets

Use overlay-specific user presets first (`~/.drawio-academic-skills/styles/`), then sibling base bundled presets (`../drawio/styles/built-in/`). Never mutate bundled base presets; copy into the user preset directory before editing or defaulting.

## Quality Gate

Do not claim completion until:

- final `.drawio` and the primary artifact required by `manifest.contract.delivery_class` align with work-dir `.spec.yaml`/`.arch.json`; `meta.profile` is `academic-paper` and `meta.figureType` is `architecture`, `roadmap`, or `workflow`
- `raster-publication` includes a 300ppi-effective PNG; `vector-submission` includes PDF or path-only SVG and passes venue restrictions; `draft-preview` includes SVG and is not reported as publication-final
- no Word/LibreOffice/Pandoc/XeLaTeX manuscript references an SVG containing `<text>` or `dominant-baseline`; keep such SVGs preview-only, or convert every text object to paths before vector publication
- node count satisfies the playbook budget (`references/docs/academic-figure-playbook.md § Node Budget Management`); split or simplify when exceeded
- labels readable at paper/A4 scale; formulas use official delimiters (`$$...$$`, `\(...\)`, AsciiMath backticks); font classes follow the ladder with no label-fit overflow warnings
- mixed CJK/Latin labels request the Times New Roman + SimSun stack (theme `cjk` stack or `meta.font`); verify the stack in generated `.drawio`/SVG and disclose the actual installed fallback when SimSun is unavailable instead of claiming exact SimSun rendering
- captions, legends, callouts, formulas, and edge labels are not clipped or placed on connector lines; legends compact (single multi-line text node)
- every condition or branch label has one visually unambiguous owning connector: place it in that edge's local corridor, normally near the branch point, with visible clearance from node borders and unrelated connectors; whitespace proximity alone must not make it read as a node annotation
- every arrow has a confirmed `source --relation--> target` meaning; process, feedback, control/fallback, and progression connectors remain distinguishable in grayscale; cross-axis arrows do not imply unsupported causality
- feedback, fallback, retry, and multi-loop figures pass `references/docs/closed-loop-scientific-figure-checklist.md`, including functional loop naming, role-based endpoint ports, separated endpoint slots/corridors, orthogonal endpoint legs, balanced grid spacing, border clearance, label ownership, and intended-page-scale inspection
- every Latin-letter abbreviation is expanded at its first figure-visible use, or defined earlier in a figure-internal legend/caption when the full form would overcrowd a node
- colors are not the only carrier of meaning; `meta.palette` matches the venue decision; `PALETTE_PRINT_GATE` is clear — offer `ieee-bw`/`tol-high-contrast` when strict print safety fails
- the visual self-check followed sibling base `../drawio/references/workflows/visual-review.md` on the selected class's exported primary artifact; academic checks additionally cover A4 readability, caption/legend, formulas, print meaning, and venue constraints
- for a generated DOCX, verify that the embedded media bytes match the accepted publication PNG; for a generated PDF, verify the embedded image dimensions and at least 300ppi effective resolution, then inspect the actual rendered page
- requested Desktop exports were attempted or reported unavailable; no MCP config, server, or live backend required
- any browser-rasterized SVG-to-PNG derivative preserves the source and passes the derivative dimensions, renderer, text-alignment, and geometry regression checks
- after every rerender, compare the current node/edge label set, source-target pairs, arrow directions, line styles, and previously accepted fixes with the prior accepted round; a layout-only request must not silently rename, shorten, add, or remove scientific content
- complex-task manifest records the frozen semantic inventory, compared/selected layout, reference IDs, exact CLI commands, artifact hashes/evidence labels, deterministic/visual/publication QA, and residual risks; `pending` or `not_checked` is never reported as PASS

## Completion Report

End with a concise report: selected delivery class; editable, preview, and publication assets with paths; intermediate work directory and figure-manifest path when generated; sibling base CLI commands run; selected layout/reference IDs for complex tasks; publication renderer and pixel dimensions; the selected palette, its colorblind/grayscale safety flags, and any print-gate downgrade; the actual CJK font fallback when the requested font was unavailable; DOCX/PDF embedding checks; blocked publication exports; remaining venue-specific manual checks.
